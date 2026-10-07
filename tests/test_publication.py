"""Adversarial regression checks for the public CI gate."""
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check_public_repository as checker


class PublicationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'vault'
        self.root.mkdir()
        for name in checker.REQUIRED:
            self.write(name, '')
        self.write('VERSION', '1.1.0\n')
        self.write('CITATION.cff', 'version: "1.1.0"\n')
        self.write('LICENSE.md', 'All rights reserved.')
        self.write('AUTHORS.md', 'Ciprian Ștefan Pleșca')
        self.write('WHITEPAPER.md', 'research ' * 1500)
        self.write('README.md', '\n'.join(['```mermaid\nflowchart LR\n A[Source] --> B[Decision]\n```'] * 4))
        (self.root / 'assets/market-intelligence-vault-hero.png').write_bytes(b'\x89PNG\r\n\x1a\n')
        for name in ['RELEASE_NOTES_1.1.0.md', 'RELEASE_VERIFICATION_1.1.0.md', 'docs/releases/GITHUB_RELEASE_1.1.0.md']:
            self.write(name, 'Released software')

    def write(self, name, text):
        p = self.root / name; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')

    def errors(self):
        return checker.check(self.root)['errors']

    def test_complete_distribution_passes(self):
        self.assertEqual(self.errors(), [])

    def test_each_required_file_fails_when_missing(self):
        for name in checker.REQUIRED:
            with self.subTest(name=name):
                p = self.root / name; data = p.read_bytes(); p.unlink()
                self.assertTrue(self.errors()); p.write_bytes(data)

    def test_production_credential_urls_rejected(self):
        for scheme in ['https', 'postgresql', 'mongodb', 'redis']:
            self.assertTrue(checker.secret_findings(scheme + '://' + 'person:pass' + '@research.invalid/item'))

    def test_reference_and_html_links_checked(self):
        self.write('docs/topic (1).md', 'A topic')
        valid = '[topic](docs/topic%20(1).md "Title")\n[topic][ref]\n[ref]: <docs/topic (1).md>\n<img src="assets/market-intelligence-vault-hero.png">'
        self.assertEqual(checker.document_errors(self.root, self.root / 'README.md', valid), [])
        for text in ['[missing](docs/missing.md)', '![image](assets/missing.png)', '[missing][unresolved]', '<img src="assets/missing.png">']:
            self.assertTrue(checker.document_errors(self.root, self.root / 'README.md', text))

    def test_escape_and_case_mismatch_rejected(self):
        for target in ['../outside.md', 'docs/%2e%2e/%2e%2e/outside.md', 'readme.md']:
            self.assertTrue(checker.document_errors(self.root, self.root / 'README.md', '[file](' + target + ')'))

    def test_code_examples_and_external_links_ignored(self):
        text = '```text\n[example](missing.md)\n```\n`[code](missing.md)`\n[web](https://research.invalid/a)\n[anchor](#section)'
        self.assertEqual(checker.document_errors(self.root, self.root / 'README.md', text), [])

    def test_top_level_citation_must_match(self):
        self.write('CITATION.cff', 'version: "9.0.0"\npreferred-citation:\n  version: "1.1.0"\n')
        self.assertTrue(any('CITATION' in e for e in self.errors()))

    def test_missing_release_documentation_rejected(self):
        (self.root / 'RELEASE_NOTES_1.1.0.md').unlink()
        self.assertTrue(any('RELEASE_NOTES' in e for e in self.errors()))

    def test_all_private_directories_rejected(self):
        for directory in ['private', 'client_data', 'raw_client_data', 'credentials', 'secrets', 'source_archives_private']:
            self.write(directory + '/data.txt', 'Private research')
        self.assertEqual(sum('private or transient' in e for e in self.errors()), 6)

    def test_env_and_private_key_files_rejected(self):
        self.write('.env.production', 'Local configuration')
        self.write('notes.txt', '-----BEGIN ' + 'OPENSSH PRIVATE KEY-----')
        self.assertTrue(any('.env.production' in e for e in self.errors()))
        self.assertTrue(any('private-key' in e for e in self.errors()))

    def test_production_token_rejected_and_redacted(self):
        token = 'ghp' + '_' + 'a' * 36
        self.write('production.py', token)
        errors = self.errors()
        self.assertTrue(any('github-token' in e for e in errors))
        self.assertNotIn(token, json.dumps(errors))

    def test_exact_negative_fixtures_allowed_only_in_named_files(self):
        name = 'tests/test_hardening.py'
        fixture = next(iter(checker.FIXTURES[name]))
        self.write(name, fixture)
        self.assertEqual(self.errors(), [])
        self.write('production.py', fixture)
        self.assertTrue(self.errors())

    def test_unlisted_fake_token_in_tests_is_not_exempted(self):
        self.write('tests/new.py', 'ghp' + '_' + 'a' * 36)
        self.assertTrue(self.errors())

    def test_stale_hero_placeholder_rejected(self):
        self.write('docs/note.md', 'HERO IMAGE' + ' FILE REQUIRED')
        self.assertTrue(any('stale hero' in e for e in self.errors()))

    def test_bad_mermaid_delimiter_rejected(self):
        self.assertTrue(checker.diagram_errors('flowchart LR\n A[Broken --> B[Target]'))

    def test_git_inventory_failure_fails_closed(self):
        (self.root / '.git').mkdir()
        with patch.object(checker.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, b'', b'')):
            self.assertEqual(checker.check(self.root)['status'], 'FAIL')

    def test_tracked_ignored_private_files_are_still_scanned(self):
        self.write('.env', 'Local configuration')
        (self.root / '.git').mkdir()
        names = [p.relative_to(self.root).as_posix() for p in self.root.rglob('*') if p.is_file()]
        with patch.object(checker.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, ('\0'.join(names) + '\0').encode(), b'')):
            self.assertTrue(any('.env' in e for e in self.errors()))

    def test_cli_nonzero_on_failure(self):
        (self.root / 'VERSION').unlink()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = checker.main(['--root', str(self.root)])
        self.assertEqual(code, 1)
        self.assertIn('Public repository checks: FAIL', output.getvalue())


if __name__ == '__main__':
    unittest.main()

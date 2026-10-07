"""Fail-closed, offline public-distribution checks using only the standard library.

Git inventory includes tracked files (even if now ignored) and non-ignored additions.
Without Git metadata, every distribution file is inspected. Secret values are never
printed. Pattern scanning does not provide complete secret, PII or authenticity assurance.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'README.md', 'VERSION', 'CHANGELOG.md', 'SECURITY.md', 'WHITEPAPER.md',
    'CITATION.cff', 'LICENSE.md', 'AUTHORS.md',
    'docs/releases/PUBLICATION_VERIFICATION.md',
    'assets/market-intelligence-vault-hero.png', '.github/workflows/ci.yml',
)
PRIVATE_DIRS = {
    'private', 'client_data', 'raw_client_data', 'credentials', 'secrets',
    'source_archives_private', 'private_client_data', 'local_research_archives',
    '__pycache__', '.score_transaction',
}
SENSITIVE_QUERY = {
    'token', 'access_token', 'api_key', 'apikey', 'secret', 'password',
    'authorization', 'signature', 'sig', 'credential',
}
PATTERNS = (
    ('private-key', r'-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----'),
    ('aws-key', r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    ('github-token', r'\bgh[pousr]_[A-Za-z0-9]{20,}\b'),
    ('github-pat', r'\bgithub_pat_[A-Za-z0-9_]{30,}\b'),
    ('openai-key', r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}\b'),
    ('google-key', r'\bAIza[A-Za-z0-9_-]{35}\b'),
    ('slack-token', r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),
    ('credential-assignment', r'''(?im)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|secret[_-]?key|client[_-]?secret|password|database[_-]?password)\s*["']?\s*[:=]\s*["']([^"'\r\n]{8,})["']'''),
    ('unquoted-credential', r'(?im)^\s*(?:API_KEY|ACCESS_TOKEN|AUTH_TOKEN|SECRET_KEY|CLIENT_SECRET|PASSWORD|DATABASE_PASSWORD)\s*=\s*[^\s"\x27#]{8,}\s*$'),
)
# Exact, reviewed negative-test values. No blanket test-file or dummy-token exemption.
FIXTURES = {
    'tests/test_hardening.py': {
        'https://' + 'u:p@host.example/path',
        'https://' + 'host.example/?token=SECRET',
    },
    'dashboard/tests/test_export.py': {
        'https://' + 'citations.org/a?token=private',
        'https://' + 'citations.org/path?api_key=private',
    },
}


def secret_findings(text):
    """Return kind/line/value internally; callers must redact values in output."""
    found = []
    for kind, pattern in PATTERNS:
        for match in re.finditer(pattern, text):
            found.append((kind, text.count('\n', 0, match.start()) + 1, match.group()))
    for match in re.finditer(r'''(?:https?|postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|mssql)://[^\s"'<>`]+''', text):
        value = match.group().rstrip('),;]')
        try:
            url = urlsplit(value)
            if url.username is not None or url.password is not None or any(
                key.lower() in SENSITIVE_QUERY for key, _ in parse_qsl(url.query, keep_blank_values=True)
            ):
                found.append(('credential-url', text.count('\n', 0, match.start()) + 1, value))
        except ValueError:
            found.append(('malformed-url', text.count('\n', 0, match.start()) + 1, value))
    return found


def candidate_files(root):
    """Never treat a Git inventory failure as permission to skip committed files."""
    if (root / '.git').exists():
        result = subprocess.run(
            ['git', '-C', str(root), 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
            capture_output=True, timeout=30, check=False,
        )
        if result.returncode:
            raise ValueError('Git inventory failed; refusing an incomplete public scan')
        return sorted(set(name for name in result.stdout.decode('utf-8').split('\0') if name))
    names = []
    def failed(error):
        raise ValueError('Cannot enumerate the public distribution') from error
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=failed):
        # Git internals are never part of a source distribution. Other directories are scanned.
        dirs[:] = [name for name in dirs if name != '.git']
        for name in dirs:
            p = Path(directory) / name
            if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
                raise ValueError('Linked distribution directory refused')
        names.extend((Path(directory) / name).relative_to(root).as_posix() for name in files)
    return sorted(names)


def safe_file(root, name):
    """Require confined, unlinked files with exact casing on every platform."""
    current = root
    parts = Path(name).parts
    if not parts or Path(name).is_absolute() or '..' in parts or '\\' in name:
        return False
    for part in parts:
        if not current.is_dir() or part not in {p.name for p in current.iterdir()}:
            return False
        current = current / part
        if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):
            return False
    return current.is_file() and current.resolve().is_relative_to(root.resolve())


def diagram_errors(diagram):
    errors = []
    if not diagram.strip().startswith('flowchart '):
        errors.append('unsupported Mermaid type for this release')
    for opening, closing in [('(', ')'), ('[', ']'), ('{', '}')]:
        if diagram.count(opening) != diagram.count(closing):
            errors.append('unbalanced Mermaid delimiter')
    if '-->' not in diagram:
        errors.append('empty Mermaid flow')
    return errors


def markdown_targets(text):
    """Collect inline, reference-style and HTML references outside code examples."""
    text = re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1\s*$', '', text)
    text = re.sub(r'`[^`\n]*`', '', text)
    definitions = {}
    for match in re.finditer(r'(?m)^\s{0,3}\[([^\]\n]+)\]:\s*(<[^>]+>|\S+)', text):
        definitions[' '.join(match[1].split()).casefold()] = match[2].strip('<>')
    targets, errors = [], []
    # Nested parentheses in filenames and optional quoted link titles are supported.
    for match in re.finditer(r'!?\[([^\]\n]*)\]\(', text):
        start = match.end(); depth = 1; pos = start
        while pos < len(text) and depth:
            if text[pos] == '\\':
                pos += 2; continue
            depth += (text[pos] == '(') - (text[pos] == ')')
            pos += 1
        if depth:
            errors.append('unclosed Markdown link'); continue
        value = text[start:pos-1].strip()
        if value.startswith('<'):
            end = value.find('>')
            if end < 0: errors.append('unclosed Markdown destination'); continue
            value = value[1:end]
        else:
            value = re.split(r'\s+["\x27]', value, maxsplit=1)[0]
        targets.append(value)
    for match in re.finditer(r'!?\[([^\]\n]+)\](?:\[([^\]\n]*)\])?', text):
        if text[match.end():match.end()+1] in ('(', ':') or match[1].startswith('^'):
            continue
        key = ' '.join((match[2] or match[1]).split()).casefold()
        if key in definitions:
            targets.append(definitions[key])
        elif match[2] is not None:
            errors.append('undefined Markdown reference')
    targets += [m[2] for m in re.finditer(r'''(?is)<(?:img|a)\b[^>]*?\b(?:src|href)\s*=\s*(["'])(.*?)\1''', text)]
    return targets, errors


def document_errors(root, path, text):
    targets, errors = markdown_targets(text)
    if text.count('```') % 2:
        errors.append('unbalanced code fences')
    for target in targets:
        if target.startswith(('#', '//')):
            continue
        try:
            url = urlsplit(target)
            if url.scheme in {'http', 'https', 'mailto', 'tel'}:
                continue
            if url.scheme:
                errors.append('unsupported or unsafe reference scheme'); continue
            value = unquote(url.path)
            if not value or '\\' in value or '\0' in value:
                errors.append('empty or unsafe local reference'); continue
            candidate = (root / value.lstrip('/') if value.startswith('/') else path.parent / value).absolute()
            # Normalize .. but keep links visible for safe_file to refuse them.
            candidate = Path(os.path.normpath(candidate))
            name = candidate.relative_to(root).as_posix()
            if not safe_file(root, name):
                errors.append('broken, linked or case-mismatched local reference: ' + name)
        except (ValueError, OSError):
            errors.append('unsafe or inaccessible local reference')
    for diagram in re.findall(r'```mermaid\s*\n(.*?)```', text, re.S):
        errors += diagram_errors(diagram)
    return errors


def check(root):
    root = root.resolve()
    errors, fixtures = [], []
    try:
        names = candidate_files(root)
    except (OSError, ValueError, subprocess.SubprocessError, UnicodeError):
        return {'status': 'FAIL', 'files_checked': 0, 'errors': ['Public file inventory could not be established']}
    public = set(names)
    def required(name):
        if name not in public or not safe_file(root, name):
            errors.append(name + ': required public file missing, excluded or unsafe')
            return False
        return True
    for name in REQUIRED:
        required(name)
    diagrams = words = 0
    for name in names:
        try:
            if not safe_file(root, name):
                errors.append(name + ': missing, linked or unsafe public file'); continue
            p = root / name; parts = [v.casefold() for v in Path(name).parts]
            if any(v in PRIVATE_DIRS or v.startswith(('engagement_', 'delivery_')) for v in parts[:-1]) or (len(parts) > 2 and parts[:2] == ['08_evidence', 'archives']):
                errors.append(name + ': private or transient public path'); continue
            if p.name.casefold().startswith('.env') or p.name.casefold() == 'credentials.json' or p.suffix.casefold() in {'.pem', '.key', '.p12', '.pfx', '.pyc', '.log'} or p.name in {'id_rsa', 'id_ed25519', 'id_dsa', 'id_ecdsa'}:
                errors.append(name + ': credential or transient public file'); continue
            raw = p.read_bytes()
            try:
                text = raw.decode('utf-8-sig')
            except UnicodeError:
                # Binary assets are scanned for ASCII credential signatures too.
                text = raw.decode('ascii', errors='ignore')
                if p.suffix.casefold() not in {'.png', '.jpg', '.jpeg', '.pdf', '.zip', '.ico', '.woff', '.woff2'}:
                    errors.append(name + ': unsupported binary public file')
            for kind, line, value in secret_findings(text):
                if kind == 'credential-url' and value in FIXTURES.get(name, set()):
                    fixtures.append(name + ':' + str(line)); continue
                errors.append(f'{name}:{line}: possible {kind} (value redacted)')
            if p.suffix.casefold() == '.md':
                errors.extend(name + ': ' + e for e in document_errors(root, p, text))
                diagrams += len(re.findall(r'```mermaid\s*\n', text))
                if 'assets/market-intelligence-vault-hero.png' in public and 'HERO IMAGE FILE REQUIRED' in text:
                    errors.append(name + ': stale hero placeholder despite existing hero image')
            if p.suffix.casefold() == '.mmd':
                errors.extend(name + ': ' + e for e in diagram_errors(text))
        except (OSError, UnicodeError, ValueError):
            errors.append(name + ': public file could not be checked')
    try:
        if safe_file(root, 'VERSION'):
            version = (root / 'VERSION').read_text(encoding='utf-8-sig').strip()
            if not re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?', version):
                errors.append('VERSION: invalid release version')
            else:
                for name in (f'RELEASE_NOTES_{version}.md', f'RELEASE_VERIFICATION_{version}.md', f'docs/releases/GITHUB_RELEASE_{version}.md'):
                    required(name)
            if safe_file(root, 'CITATION.cff'):
                citation = (root / 'CITATION.cff').read_text(encoding='utf-8-sig')
                versions = re.findall(r'^version:\s*([^\r\n]+)', citation, re.M)
                if len(versions) != 1 or versions[0].split(' #')[0].strip().strip('"\x27') != version:
                    errors.append('CITATION.cff: top-level release version does not match VERSION')
        if safe_file(root, 'AUTHORS.md') and 'Ciprian Ștefan Pleșca' not in (root / 'AUTHORS.md').read_text(encoding='utf-8'):
            errors.append('AUTHORS.md: author mismatch')
        if safe_file(root, 'LICENSE.md') and 'All rights reserved.' not in (root / 'LICENSE.md').read_text(encoding='utf-8'):
            errors.append('LICENSE.md: rights reservation missing')
        if safe_file(root, 'WHITEPAPER.md'):
            words = len(re.findall(r'\b[\w]+(?:[’\x27-][\w]+)*\b', (root / 'WHITEPAPER.md').read_text(encoding='utf-8')))
            if words < 1500: errors.append('WHITEPAPER.md: below required minimum')
        if safe_file(root, 'README.md') and len(re.findall(r'```mermaid\s*\n', (root / 'README.md').read_text(encoding='utf-8'))) < 4:
            errors.append('README.md: four Mermaid diagrams required')
        if safe_file(root, 'assets/market-intelligence-vault-hero.png') and not (root / 'assets/market-intelligence-vault-hero.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
            errors.append('Hero image is not a PNG')
    except (OSError, UnicodeError):
        errors.append('Required metadata could not be read')
    return {'status': 'PASS' if not errors else 'FAIL', 'files_checked': len(names),
            'markdown_mermaid_blocks': diagrams, 'whitepaper_words': words,
            'known_synthetic_negative_fixtures': fixtures, 'errors': errors,
            'limitations': 'Offline pattern/reference checks only; not complete secret/PII detection, source authentication, full CFF schema validation or Mermaid rendering.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        result = check(args.root)
    except (OSError, ValueError, subprocess.SubprocessError):
        result = {'status': 'FAIL', 'errors': ['Repository checks could not complete']}
    print(json.dumps(result, indent=2, ensure_ascii=True))
    print(f"Public repository checks: {result['status']} ({len(result['errors'])} error(s))")
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())

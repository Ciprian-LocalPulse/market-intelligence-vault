import sys
import json
import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path
from datetime import date
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from common import DEFAULT_ROOT,load_contract,load_data
from validate_repository import validate
from generate_summary import render
from build_delivery_package import build
from check_sources import check

class IntegrityTests(unittest.TestCase):
    def test_release_integrity(self):
        self.assertEqual(validate(DEFAULT_ROOT,date(2026,10,6),True),[])
    def test_schema_contract_alignment(self):
        contract=load_contract(DEFAULT_ROOT)
        for name,path in [('source','08_evidence/source_library.csv'),('evidence','08_evidence/evidence_register.csv'),('opportunity','05_opportunities/opportunity_database.csv'),('risk','06_risks/risk_register.csv'),('competitor','03_competitors/competitor_database.csv'),('customer_segment','04_customers/customer_segments_template.csv')]:
            schema=json.loads((DEFAULT_ROOT/f'schemas/{name}_schema.json').read_text())
            self.assertEqual(set(schema['properties']),set(contract[path]['fields']))
            self.assertEqual(schema['required'],contract[path]['required'])
    def test_sample_labels(self):
        for path,rows in load_data(DEFAULT_ROOT).items():
            for row in rows:
                if 'sample_status' in row: self.assertEqual(row['sample_status'],'FICTIONAL SAMPLE',path)
    def test_summary_has_required_sections_and_counterevidence(self):
        text=render(DEFAULT_ROOT,date(2026,10,6))
        for section in ['Executive Snapshot','Top 5 Findings','Top 3 Opportunities','Top 3 Risks','Market Attractiveness','Competitive Pressure','Customer Signals','Strategic Recommendation','Confidence Level','Immediate Next Actions','Decision Required']:
            self.assertIn('## '+section,text)
        self.assertIn('FICTIONAL DEMONSTRATION ONLY',text); self.assertIn('EV-006',text); self.assertIn('contradicts',text)
    def test_source_checker_exposes_synthetic_and_conflict(self):
        issues='\n'.join(check(DEFAULT_ROOT,date(2026,10,6)))
        self.assertIn('synthetic artifact',issues); self.assertIn('unresolved conflicting evidence',issues)

    def test_source_checker_stale_duplicate_missing_and_low(self):
        from common import read_csv,write_csv
        with tempfile.TemporaryDirectory(dir=DEFAULT_ROOT.parent) as tmp:
            root=Path(tmp)/'vault'
            shutil.copytree(DEFAULT_ROOT,root,ignore=lambda src,names: {n for n in names if n=='__pycache__' or n.endswith('.pyc') or ((Path(src)/n).is_dir() and n.startswith('delivery_'))})
            fields,rows=read_csv(root/'08_evidence/source_library.csv')
            rows[0].update(publication_date='2020-01-01',reliability_score='5')
            rows[1]['source_url']=rows[0]['source_url']
            rows[2]['source_url']=''
            write_csv(root/'08_evidence/source_library.csv',fields,rows)
            issues='\n'.join(check(root,date(2026,10,6)))
            for expected in ['freshness Stale','duplicate source URL','missing URL','low-reliability source']:
                self.assertIn(expected,issues)
    def test_package_hashes_no_clutter_no_overwrite_and_live_gate(self):
        with tempfile.TemporaryDirectory(dir=DEFAULT_ROOT.parent) as tmp:
            root=Path(tmp)/'vault'
            shutil.copytree(DEFAULT_ROOT,root,ignore=lambda src,names: {n for n in names if n=='__pycache__' or n.endswith('.pyc') or ((Path(src)/n).is_dir() and n.startswith('delivery_'))})
            dest=build(root,date(2026,10,6))
            self.assertTrue((dest/'EXECUTIVE_SUMMARY.md').is_file())
            self.assertFalse((dest/'tools').exists()); self.assertFalse((dest/'tests').exists())
            for line in (dest/'CHECKSUMS.sha256').read_text().splitlines():
                digest,path=line.split('  ',1)
                self.assertEqual(digest,hashlib.sha256((dest/path).read_bytes()).hexdigest())
            with self.assertRaises(ValueError): build(root,date(2026,10,6))
            with self.assertRaisesRegex(ValueError,'non-LIVE'): build(root,date(2026,10,6),'live','delivery_live')

if __name__=='__main__': unittest.main()

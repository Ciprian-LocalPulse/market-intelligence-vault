import sys
import shutil
import tempfile
import unittest
from pathlib import Path
from datetime import date
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from common import DEFAULT_ROOT,read_csv,write_csv,safe_output
from validate_repository import validate

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=DEFAULT_ROOT.parent); self.root=Path(self.temp.name)/'vault'
        shutil.copytree(DEFAULT_ROOT,self.root,ignore=lambda src,names: {n for n in names if n=='__pycache__' or n.endswith('.pyc') or ((Path(src)/n).is_dir() and n.startswith('delivery_'))})
    def tearDown(self): self.temp.cleanup()
    def errors(self): return '\n'.join(validate(self.root,date(2026,10,6)))
    def mutate(self,path,fn):
        fields,rows=read_csv(self.root/path); fn(rows); write_csv(self.root/path,fields,rows)
    def test_missing_required_file(self):
        (self.root/'README.md').unlink(); self.assertIn('Missing required file',self.errors())
    def test_empty_required_field(self):
        self.mutate('06_risks/risk_register.csv',lambda rows:rows[0].update(title=''))
        self.assertIn('empty required field title',self.errors())
    def test_duplicate_ids(self):
        self.mutate('06_risks/risk_register.csv',lambda rows:rows.append(dict(rows[0])))
        self.assertIn('duplicate ID',self.errors())
    def test_bad_evidence_reference(self):
        self.mutate('05_opportunities/opportunity_database.csv',lambda rows:rows[0].update(evidence_ids='EV-MISSING'))
        self.assertIn('missing reference evidence_ids=EV-MISSING',self.errors())
    def test_invalid_confidence_value(self):
        self.mutate('08_evidence/evidence_register.csv',lambda rows:rows[0].update(confidence_level='CERTAIN'))
        self.assertIn('unsupported confidence_level',self.errors())
    def test_invalid_range_and_nonfinite(self):
        for value in ('101','NaN'):
            self.mutate('06_risks/risk_register.csv',lambda rows:rows[0].update(risk_score=value))
            self.assertIn('invalid risk_score',self.errors())
    def test_malformed_csv(self):
        with (self.root/'06_risks/risk_register.csv').open('a',encoding='utf-8') as f: f.write('one,two\n')
        self.assertIn('Malformed CSV',self.errors())
    def test_header_mismatch(self):
        p=self.root/'06_risks/risk_register.csv'
        p.write_text(p.read_text().replace('risk_id,','wrong_id,',1),encoding='utf-8')
        self.assertIn('header/order mismatch',self.errors())
    def test_future_date(self):
        self.mutate('03_competitors/competitor_database.csv',lambda rows:rows[0].update(as_of_date='2099-01-01'))
        self.assertIn('future as_of_date',self.errors())
    def test_source_metadata_drift(self):
        self.mutate('08_evidence/evidence_register.csv',lambda rows:rows[0].update(publisher='Incorrect publisher'))
        self.assertIn('source metadata drift',self.errors())
    def test_invalid_weights(self):
        self.mutate('09_scores/opportunity_scoring_model.csv',lambda rows:rows[0].update(weight='90'))
        self.assertIn('weights must sum to 100',self.errors())
    def test_unsafe_output_and_no_overwrite(self):
        for output in ('../escape','README.md','.'):
            with self.subTest(output=output),self.assertRaises(ValueError): safe_output(self.root,output)
    def test_stale_calculations_detected(self):
        self.mutate('06_risks/risk_register.csv',lambda rows:rows[0].update(risk_score='1'))
        self.assertIn('saved fields differ', '\n'.join(validate(self.root,date(2026,10,6),True)))
    def test_missing_source_url(self):
        self.mutate('08_evidence/source_library.csv',lambda rows:rows[0].update(source_url=''))
        self.assertIn('empty required field source_url',self.errors())

if __name__=='__main__': unittest.main()

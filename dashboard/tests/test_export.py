import hashlib,json,shutil,sys,tempfile,unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'dashboard'))
from common import read_csv,write_csv,load_data,load_contract
from export_dashboard_data import payloads,export,project,approval,sensitivity
from launch_dashboard import verify_snapshot,STATIC,DATA,handler_for
from initialize_engagement import initialize
ASOF=date(2026,10,6)
def ignore(src,names):return {n for n in names if n=='__pycache__' or n.endswith('.pyc') or ((Path(src)/n).is_dir() and n.startswith(('delivery_','engagement_')))}

class ExportTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory(dir=ROOT.parent);self.root=Path(self.temp.name)/'vault';shutil.copytree(ROOT,self.root,ignore=ignore)
    def tearDown(self):self.temp.cleanup()
    def mutate(self,path,fn):fields,rows=read_csv(self.root/path);fn(rows);write_csv(self.root/path,fields,rows)
    def data(self):return payloads(self.root,ASOF)
    def test_demo_type_ids_conflicts_and_scores_preserved(self):
        d=self.data();self.assertEqual(d['executive']['meta']['demo_label'],'FICTIONAL DEMONSTRATION DATA');self.assertEqual(d['executive']['data']['coverage']['with_support'],5)
        claims=d['evidence']['data']['claims'];self.assertEqual(claims[0]['label'],'INFERENCE');self.assertEqual(claims[3]['label'],'HYPOTHESIS');self.assertTrue(claims[0]['contradiction_flag'])
        relation=d['evidence']['data']['relationships'][0];self.assertIsInstance(relation['claim_id'],str);self.assertIsInstance(relation['evidence_id'],str)
        contradiction=d['contradictions']['data']['records'][0];self.assertEqual(contradiction['contradicting_evidence'],['EV-006']);self.assertTrue(contradiction['reason'])
        self.assertEqual(d['opportunities']['data']['records'][0]['opportunity_score'],52.48)
        self.assertEqual(d['executive']['meta']['approval']['status'],'ACTION NOT APPROVED')
    def test_optional_missing_stays_null_and_legitimate_zero_stays_zero(self):
        self.mutate('08_evidence/claims_register.csv',lambda r:r[0].update(confidence_score='',confidence_level=''))
        self.assertIsNone(self.data()['evidence']['data']['claims'][0]['confidence_score'])
        c=load_contract(self.root)['06_risks/risk_register.csv'];self.assertEqual(project({'likelihood':'0'},'likelihood',c)['likelihood'],0)
    def test_missing_required_rejected(self):
        self.mutate('05_opportunities/opportunity_database.csv',lambda r:r[0].update(market_demand=''))
        with self.assertRaises(ValueError):self.data()
    def test_invalid_score_range_rejected(self):
        self.mutate('05_opportunities/opportunity_database.csv',lambda r:r[0].update(opportunity_score='101'))
        with self.assertRaises(ValueError):self.data()
    def test_stale_or_manipulated_stored_score_rejected(self):
        self.mutate('05_opportunities/opportunity_database.csv',lambda r:r[0].update(opportunity_score='99'))
        with self.assertRaisesRegex(ValueError,'does not reconcile'):self.data()
    def test_malformed_csv_rejected(self):
        with (self.root/'06_risks/risk_register.csv').open('a') as f:f.write('"unterminated')
        with self.assertRaises(ValueError):self.data()
    def test_mixed_modes_refused(self):
        self.mutate('06_risks/risk_register.csv',lambda r:r[0].update(sample_status='LIVE'))
        with self.assertRaises(ValueError):self.data()
    def test_sensitive_source_url_refused(self):
        self.mutate('08_evidence/source_library.csv',lambda r:r[0].update(source_url='https://citations.org/a?token=private'))
        with self.assertRaises(ValueError):self.data()
    def test_sensitive_url_in_notes_refused_without_leak(self):
        self.mutate('08_evidence/evidence_register.csv',lambda r:r[0].update(analyst_notes='https://citations.org/path?api_key=private'))
        with self.assertRaises(ValueError) as exc:self.data()
        self.assertNotIn('private',str(exc.exception))
    def test_private_archives_and_unlisted_notes_absent(self):
        (self.root/'08_evidence/private_interview.txt').write_text('PRIVATE SENTINEL',encoding='utf-8')
        d=self.data();text=json.dumps(d);self.assertNotIn('PRIVATE SENTINEL',text);self.assertNotIn('archive_reference',text);self.assertNotIn('archive_sha256',text)
    def test_approval_calls_unchanged_gates_and_historical_review_expires(self):
        with patch('export_dashboard_data.check_live',side_effect=ValueError('Critical risk unresolved')):
            a=approval(self.root,load_data(self.root),ASOF,'LIVE');self.assertEqual(a['status'],'ACTION NOT APPROVED');self.assertTrue(any('Critical risk unresolved' in r for r in a['reasons']))
        with patch('export_dashboard_data.check_live'):
            a=approval(self.root,load_data(self.root),date(2020,1,1),'LIVE');self.assertEqual(a['status'],'ACTION NOT APPROVED')
    def test_snapshot_hash_coverage_and_tamper(self):
        folder=export(self.root,ASOF,'dashboard/data_test');dash=folder.parent/'snapshot_fixture';dash.mkdir();shutil.copytree(folder,dash/'data');self.assertEqual(len(verify_snapshot(dash)['files']),12)
        with (dash/'data/evidence.json').open('a') as f:f.write(' ')
        with self.assertRaises(ValueError):verify_snapshot(dash)
    def test_confined_output_and_unknown_file_overwrite_refused(self):
        with self.assertRaises(ValueError):export(self.root,ASOF,'../escape')
        (self.root/'dashboard/data/private.txt').write_text('private')
        with self.assertRaises(ValueError):export(self.root,ASOF,refresh=True)
    def test_no_canonical_inputs_changed(self):
        paths=load_contract(self.root);before={p:(self.root/p).read_bytes() for p in paths};export(self.root,ASOF,'dashboard/data_test');self.assertTrue(all((self.root/p).read_bytes()==b for p,b in before.items()))
    def test_sensitivity_reconciles_and_bounds_every_tested_rating(self):
        d=self.data();raw=load_data(self.root);row=raw['05_opportunities/opportunity_database.csv'][0];item=d['opportunities']['data']['records'][0]
        self.assertTrue(item['sensitivity']['scenarios']);self.assertTrue(all(0<=s['tested_value']<=5 for s in item['sensitivity']['scenarios']));self.assertEqual(item['sensitivity']['baseline_rank'],1)
        self.assertAlmostEqual(item['confidence_multiplier']*item['merit_score'],item['opportunity_score'],delta=0.01)
        self.assertIn(item['sensitivity']['decision_status'],('SENSITIVE DECISION','STABLE WITHIN TESTED RANGE'))
    def test_empty_engagement_has_no_fake_observations(self):
        dest=initialize(self.root,'engagement_empty');d=payloads(dest,ASOF);self.assertEqual(d['executive']['meta']['mode'],'NOT YET RESEARCHED');self.assertEqual(d['evidence']['data']['records'],[]);self.assertEqual(d['opportunities']['data']['records'],[])
    def test_http_allowlist_excludes_repository_and_archives(self):
        self.assertFalse(any('archive' in p or p.startswith(('tools/','08_evidence/','config/')) for p in STATIC|DATA));self.assertEqual(len(DATA),13)
    def test_sensitivity_flags_category_change_near_threshold(self):
        d=load_data(self.root);row=dict(d['05_opportunities/opportunity_database.csv'][0]);row.update(confidence_score='100',market_demand='0',strategic_fit='1')
        factors=[f for f in d['09_scores/factor_assessments.csv'] if f['entity_id']==row['opportunity_id']]
        result=sensitivity(row,[row],factors,d['09_scores/opportunity_scoring_model.csv'],'opportunity_score')
        self.assertEqual(result['status'],'RANK SENSITIVE');self.assertTrue(any(s['category_changed'] for s in result['scenarios']))

if __name__=='__main__':unittest.main()

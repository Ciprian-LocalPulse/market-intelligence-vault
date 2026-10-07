import copy,csv,hashlib,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from datetime import date
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from common import DEFAULT_ROOT,load_data,load_contract,read_csv,write_csv,confined,safe_url,input_digest,evidence_score,ids
from validate_repository import validate
from calculate_scores import calculate,save
from check_sources import check
from build_delivery_package import build,check_live,delivery_policy,viewer_export
from verify_package import verify
from schema_validation import errors_for,check_schema
from initialize_engagement import initialize

ASOF=date(2026,10,6)
def ignores(src,names):return {n for n in names if n=='__pycache__' or n.endswith('.pyc') or ((Path(src)/n).is_dir() and n.startswith(('delivery_','engagement_')))}

class HardeningTests(unittest.TestCase):
    def test_malformed_delivery_configuration_fails_closed(self):
        (self.root/'config/delivery_policy.json').write_text('null',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Malformed delivery policy'):delivery_policy(self.root)
        (self.root/'config/live_signoff.json').write_text('null',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Malformed live sign-off'):check_live(self.root,self.live_data(),ASOF,{})
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=DEFAULT_ROOT.parent)
        self.root=Path(self.temp.name)/'vault';shutil.copytree(DEFAULT_ROOT,self.root,ignore=ignores)
    def tearDown(self):self.temp.cleanup()
    def mutate(self,path,fn):
        fields,rows=read_csv(self.root/path);fn(rows);write_csv(self.root/path,fields,rows)
    def errors(self):return '\n'.join(validate(self.root,ASOF))
    def live_data(self):
        data=calculate(self.root,ASOF)
        for rows in data.values():
            for row in rows:
                if 'sample_status' in row:row['sample_status']='LIVE'
        for d in data['07_strategy/recommendations.csv']:d['status']='APPROVED'
        return data
    def signoff(self):
        p=self.root/'config/live_signoff.json';s=json.loads(p.read_text())
        s.update(status='APPROVED',scope='Controlled audit fixture',reviewer='Fixture reviewer',decision_authority='Fixture authority',as_of_date=ASOF.isoformat(),input_digest=input_digest(self.root),approved_decision_ids=['DEC-001'])
        s['checks']={k:True for k in s['checks']};p.write_text(json.dumps(s),encoding='utf-8');return s

    def test_unlisted_private_note_not_exported(self):
        (self.root/'08_evidence/private_interview.txt').write_text('AUDIT PRIVATE SENTINEL')
        folder=build(self.root,ASOF)
        self.assertFalse((folder/'08_evidence/private_interview.txt').exists())

    def test_contract_path_escape_rejected(self):
        p=self.root/'config/data_contract.json';c=json.loads(p.read_text());c['../sentinel.csv']=c['06_risks/risk_register.csv'];p.write_text(json.dumps(c),encoding='utf-8')
        self.assertIn('unsafe configuration',self.errors())
        with self.assertRaises(ValueError):load_data(self.root)

    def test_confined_rejects_absolute_traversal_and_windows_paths(self):
        for path in ('../escape','C:/private','/private','a/../b','a\\b'):
            with self.subTest(path=path),self.assertRaises(ValueError):confined(self.root,path)

    def test_source_reliability_ceiling(self):
        self.mutate('08_evidence/source_library.csv',lambda r:r[4].update(reliability_score='0'))
        self.assertIn('reliability exceeds source ceiling',self.errors())

    def test_archive_tamper(self):
        (self.root/'12_examples/synthetic_sources/SRC-001.md').write_text('Modified archive')
        self.assertIn('archive checksum mismatch',self.errors())

    def test_url_credentials_and_reserved_live_hosts(self):
        for url in ['https://u:p@host.example/path','https://host.example/?token=SECRET','https://example.invalid/a','https://127.0.0.1/a']:
            with self.subTest(url=url),self.assertRaises(ValueError):safe_url(url,'LIVE')

    def test_speculation_cannot_support_fact(self):
        self.mutate('08_evidence/claims_register.csv',lambda r:r[3].update(label='FACT'))
        self.mutate('08_evidence/evidence_register.csv',lambda r:r[3].update(verification_status='speculation'))
        self.assertIn('unsupported FACT',self.errors())

    def test_duplicate_semantic_mapping(self):
        self.mutate('08_evidence/claim_evidence_map.csv',lambda r:r.append({**r[0],'map_id':'MAP-999'}))
        self.assertIn('duplicate semantic evidence mapping',self.errors())

    def test_reference_list_syntax(self):
        for bad in ['EV-001||EV-002','EV-001|',' EV-001','EV-001|EV-001']:
            with self.subTest(bad=bad),self.assertRaises(ValueError):ids(bad)

    def test_fractional_tier_rejected(self):
        self.mutate('08_evidence/source_library.csv',lambda r:r[0].update(tier='1.5'))
        self.assertIn('invalid tier',self.errors())

    def test_conflict_cannot_be_hidden_by_context_mapping(self):
        self.mutate('08_evidence/claim_evidence_map.csv',lambda r:r[-1].update(relationship='context'))
        self.mutate('08_evidence/claims_register.csv',lambda r:r[0].update(contradiction_flag='false'))
        self.assertIn('contradiction flag/map mismatch',self.errors())
        self.assertEqual(calculate(self.root,ASOF)['08_evidence/claims_register.csv'][0]['confidence_score'],'59.00')

    def test_grade_a_requires_full_directness(self):
        model=load_data(self.root)['09_scores/confidence_model.csv']
        row={r['factor']:r['input_max'] for r in model};row.update(verification_status='verified',direct_or_indirect='direct',freshness_status='Current',contradiction_flag='false',directness_score='10')
        self.assertEqual(evidence_score(row,model),(59,'D'))

    def test_zero_relevance_or_reliability_cannot_score_high(self):
        model=load_data(self.root)['09_scores/confidence_model.csv']
        row={r['factor']:r['input_max'] for r in model};row.update(verification_status='verified',direct_or_indirect='direct',freshness_status='Current',contradiction_flag='false')
        for field in ('relevance_score','reliability_score'):
            self.assertEqual(evidence_score({**row,field:'0'},model)[0],0)

    def test_stale_checker_recomputes_claim_confidence(self):
        self.mutate('08_evidence/source_library.csv',lambda r:r[1].update(publication_date='2020-01-01'))
        text='\n'.join(check(self.root,ASOF))
        self.assertIn('SRC-002: freshness Stale',text);self.assertIn('CLM-002: low or uncomputed claim confidence',text)

    def test_stale_origin_does_not_inflate_corroboration(self):
        d=load_data(self.root);ev={**d['08_evidence/evidence_register.csv'][1],'evidence_id':'EV-007','claim_id':'CLM-001','publication_date':'2020-01-01'}
        d['08_evidence/evidence_register.csv'].append(ev)
        d['08_evidence/claim_evidence_map.csv'].append({**d['08_evidence/claim_evidence_map.csv'][0],'map_id':'MAP-007','evidence_id':'EV-007'})
        scored=calculate(self.root,ASOF,d)
        self.assertEqual(scored['08_evidence/evidence_register.csv'][0]['corroboration_score'],'0.00')

    def test_schema_runtime_and_schema_corruption(self):
        schema={'type':'integer','minimum':1,'maximum':5}
        self.assertTrue(errors_for(1.5,schema));self.assertTrue(errors_for(True,schema));self.assertTrue(errors_for(6,schema))
        with self.assertRaises(ValueError):check_schema({'type':'string','unknownKeyword':True})
        p=self.root/'schemas/source_schema.json';s=json.loads(p.read_text());s['properties']['tier']['maximum']=10;p.write_text(json.dumps(s),encoding='utf-8')
        self.assertIn('source schema: invalid or incompatible',self.errors())

    def test_factor_drift_and_missing_basis(self):
        self.mutate('09_scores/factor_assessments.csv',lambda r:r[0].update(input_value='1'))
        self.assertIn('factor value drift',self.errors())
        self.mutate('09_scores/factor_assessments.csv',lambda r:r.pop())
        self.assertIn('Missing factor assessment coverage',self.errors())

    def test_formula_text_sanitized_only_in_export(self):
        d=load_data(self.root);path='06_risks/risk_register.csv';d[path][0]['title']=' =1+1'
        rows,count=viewer_export(self.root,d,load_contract(self.root),path)
        self.assertEqual(rows[0]['title'],"' =1+1");self.assertEqual(d[path][0]['title'],' =1+1');self.assertEqual(count,1)

    def test_missing_signoff_rejects_live(self):
        with self.assertRaisesRegex(ValueError,'named approved sign-off'):check_live(self.root,self.live_data(),ASOF,delivery_policy(self.root))

    def test_stale_signoff_digest(self):
        self.signoff();(self.root/'METHODOLOGY.md').write_text('# Changed method',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'stale or does not match'):check_live(self.root,self.live_data(),ASOF,delivery_policy(self.root))

    def test_approved_enter_cannot_use_weak_support(self):
        self.signoff();d=self.live_data();d['07_strategy/recommendations.csv'][0]['decision']='ENTER'
        with self.assertRaisesRegex(ValueError,'confidence >=75'):check_live(self.root,d,ASOF,delivery_policy(self.root))

    def test_open_critical_risk_rejected(self):
        self.signoff();d=self.live_data();d['06_risks/risk_register.csv'][0]['classification']='Critical'
        with self.assertRaisesRegex(ValueError,'Critical risk requires'):check_live(self.root,d,ASOF,delivery_policy(self.root))

    def test_draft_narratives_outside_template_names_rejected(self):
        policy=delivery_policy(self.root);p=self.root/'11_delivery/final_report_structure.md';p.write_text('# Draft\n\n[Complete]',encoding='utf-8');self.signoff()
        # Remove other unfinished narratives so this check targets the explicitly altered file.
        policy['live_files']=['11_delivery/final_report_structure.md'];policy['approved_extra_files']=[]
        with self.assertRaisesRegex(ValueError,'unresolved narrative'):check_live(self.root,self.live_data(),ASOF,policy)

    def test_zero_likelihood_and_zero_impact_risk(self):
        for field in ('likelihood','impact'):
            d=load_data(self.root);d['06_risks/risk_register.csv'][0][field]='0'
            self.assertEqual(calculate(self.root,ASOF,d)['06_risks/risk_register.csv'][0]['risk_score'],'0.00')

    def test_interrupted_refresh_is_blocked(self):
        (self.root/'.score_transaction').mkdir()
        self.assertIn('Incomplete score transaction',self.errors())

    def test_refresh_failure_rolls_back_all_changed_files(self):
        d=load_data(self.root);before={p:(self.root/p).read_bytes() for p in d}
        for path in ('06_risks/risk_register.csv','05_opportunities/opportunity_database.csv'):d[path][0]['confidence_score']='1.00'
        import os
        replace=os.replace;count=[0]
        def fail_second(src,dst):
            if '.score_transaction/new/' in str(src).replace('\\','/'):
                count[0]+=1
                if count[0]==2:raise OSError('Injected disk failure')
            return replace(src,dst)
        with patch('os.replace',side_effect=fail_second),self.assertRaises(OSError):save(self.root,d)
        self.assertFalse((self.root/'.score_transaction').exists())
        self.assertTrue(all((self.root/p).read_bytes()==b for p,b in before.items()))

    def test_manifest_and_checksum_coverage(self):
        folder=build(self.root,ASOF);self.assertEqual(verify(folder),[])
        (folder/'extra.txt').write_text('undeclared');self.assertIn('Manifest inventory mismatch',verify(folder))

    def test_build_reproducible_payload(self):
        first=build(self.root,ASOF,output='delivery_first');second=build(self.root,ASOF,output='delivery_second')
        self.assertEqual((first/'CHECKSUMS.sha256').read_bytes(),(second/'CHECKSUMS.sha256').read_bytes())

    def test_initialization_preserves_foundation_and_blanks_business_data(self):
        before=(self.root/'08_evidence/source_library.csv').read_bytes();dest=initialize(self.root,'engagement_fixture')
        self.assertEqual((self.root/'08_evidence/source_library.csv').read_bytes(),before)
        for path,rows in load_data(dest).items():
            if 'sample_status' in load_contract(dest)[path]['fields']:self.assertEqual(rows,[])

    def test_malformed_csv_cli_is_controlled_failure(self):
        with (self.root/'06_risks/risk_register.csv').open('a') as f:f.write('"unterminated')
        run=subprocess.run([sys.executable,str(self.root/'tools/check_sources.py'),'--root',str(self.root),'--as-of','2026-10-06'],capture_output=True,text=True)
        self.assertEqual(run.returncode,2);self.assertNotIn('Traceback',run.stderr);self.assertNotIn('unterminated',run.stderr)

    def test_reviewed_live_test_builds_and_verifies(self):
        # A local software fixture only. No URL is fetched and no real research/approval is asserted.
        d=load_data(self.root);contract=load_contract(self.root)
        for rows in d.values():
            for r in rows:
                if 'sample_status' in r:r['sample_status']='LIVE'
        archives=self.root/'08_evidence/test_archives';archives.mkdir()
        srcs={r['source_id']:r for r in d['08_evidence/source_library.csv']}
        for sid,r in srcs.items():
            artifact=archives/(sid+'.txt');artifact.write_text('TEST FIXTURE ONLY: controlled local validation artifact. No real-market data.',encoding='utf-8')
            r.update(source_url='https://audit-fixture.org/'+sid,archive_reference=artifact.relative_to(self.root).as_posix(),archive_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest())
        for ev in d['08_evidence/evidence_register.csv']:ev['source_url']=srcs[ev['source_id']]['source_url']
        for r in d['07_strategy/recommendations.csv']:r['status']='APPROVED'
        for path,rows in d.items():write_csv(self.root/path,contract[path]['fields'],rows)
        policy=json.loads((self.root/'config/delivery_policy.json').read_text())
        policy['live_files']=list(contract)+['VERSION']
        (self.root/'config/delivery_policy.json').write_text(json.dumps(policy),encoding='utf-8')
        save(self.root,calculate(self.root,ASOF));self.signoff()
        folder=build(self.root,ASOF,'live','delivery_live_fixture')
        self.assertEqual(verify(folder),[]);self.assertTrue((folder/'APPROVAL_RECORD.json').is_file())
        self.assertFalse((folder/'12_examples').exists());self.assertFalse((folder/'08_evidence/test_archives').exists())
        manifest=json.loads((folder/'PACKAGE_MANIFEST.json').read_text())
        self.assertFalse(manifest['contains_synthetic_data']);self.assertEqual(manifest['mode'],'live')

    def test_grade_and_rounding_do_not_change_factual_money(self):
        from generate_summary import render
        d=load_data(self.root);d['08_evidence/claims_register.csv'][0]['finding']='ESTIMATE: measured fixture price is USD 65.50.'
        text=render(self.root,ASOF,d)
        self.assertIn('USD 65.50',text)

    def test_export_text_cannot_inject_markdown_html(self):
        from common import md
        text=md('<script>bad()</script> [bad](javascript:bad())')
        self.assertNotIn('<script>',text);self.assertIn('\\[bad\\]',text)

    def test_multiplier_preserves_formula_reconciliation(self):
        for row in calculate(self.root,ASOF)['05_opportunities/opportunity_database.csv']:
            self.assertAlmostEqual(float(row['merit_score'])*float(row['confidence_multiplier']),float(row['opportunity_score']),delta=0.01)

if __name__=='__main__':unittest.main()

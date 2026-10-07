"""Build an allowlisted delivery with bound live sign-off and verified checksums."""
import argparse,csv,hashlib,json,re,shutil,sys
from pathlib import Path
from common import root_arg,safe_output,load_contract,write_csv,confined,input_digest,as_date,ids
from validate_repository import validate,markdown_errors
from calculate_scores import calculate
from generate_summary import render
from verify_package import verify

IRREVERSIBLE={'ENTER','EXPAND','ACQUIRE','PARTNER','DIFFERENTIATE','REPOSITION'}

def delivery_policy(root):
    p=json.loads(confined(root,'config/delivery_policy.json',True).read_text(encoding='utf-8'))
    if not isinstance(p,dict):raise ValueError('Malformed delivery policy')
    for key in ('foundation_files','live_files','approved_extra_files'):
        if not isinstance(p.get(key),list) or len(set(p[key]))!=len(p[key]):raise ValueError('Malformed export allowlist')
        for path in p[key]:
            confined(root,path,True)
            if path.startswith(('tools/','tests/')) or Path(path).suffix.lower() in ('.env','.key','.pem','.pfx','.db','.sqlite','.exe'):
                raise ValueError('Prohibited private or executable export path')
    if type(p.get('include_live_source_archives')) is not bool:raise ValueError('Invalid archive export policy')
    return p

def check_live(root,data,as_of,policy):
    for path,rows in data.items():
        for row in rows:
            if 'sample_status' in row and row['sample_status']!='LIVE':raise ValueError('Live delivery refuses non-LIVE row in '+path)
    signoff=json.loads(confined(root,'config/live_signoff.json',True).read_text(encoding='utf-8'))
    if not isinstance(signoff,dict) or not isinstance(signoff.get('checks'),dict) or not isinstance(signoff.get('approved_decision_ids'),list) or not all(isinstance(v,str) for v in signoff['approved_decision_ids']) or not isinstance(signoff.get('critical_risk_acceptances'),list):
        raise ValueError('Malformed live sign-off')
    required={'evidence_review','source_rights_review','privacy_review','contradiction_review','calculation_review','bias_review','narrative_review'}
    if signoff.get('status')!='APPROVED' or any(not isinstance(signoff.get(f),str) or not signoff[f].strip() for f in ('scope','reviewer','decision_authority')):
        raise ValueError('Live delivery requires named approved sign-off')
    if signoff.get('as_of_date')!=as_of.isoformat() or signoff.get('input_digest')!=input_digest(root):raise ValueError('Live sign-off is stale or does not match reviewed inputs')
    if set(signoff.get('checks',{}))!=required or any(signoff['checks'][k] is not True for k in required):raise ValueError('All manual live review gates must be explicitly attested')
    decisions=data['07_strategy/recommendations.csv']
    if not decisions or any(r['status']!='APPROVED' for r in decisions):raise ValueError('Live delivery requires explicitly approved recommendations')
    if set(signoff.get('approved_decision_ids',[]))!={r['decision_id'] for r in decisions}:raise ValueError('Decision approval coverage mismatch')
    risk_acceptances={r.get('risk_id'):r for r in signoff.get('critical_risk_acceptances',[]) if isinstance(r,dict)}
    for risk in data['06_risks/risk_register.csv']:
        if risk['classification']=='Critical':
            acceptance=risk_acceptances.get(risk['risk_id'],{})
            if risk['status']!='ACCEPTED' or not acceptance.get('authority') or not acceptance.get('rationale') or acceptance.get('review_date')!=as_of.isoformat():
                raise ValueError('Critical risk requires current named acceptance')
    claims={r['claim_id']:r for r in data['08_evidence/claims_register.csv']}
    evidence={r['evidence_id']:r for r in data['08_evidence/evidence_register.csv']}
    mapping=data['08_evidence/claim_evidence_map.csv']
    for decision in decisions:
        if not ids(decision['claim_ids']):raise ValueError('Recommendation lacks material claims')
        if decision['decision']=='TEST' and float(decision['budget_cap'])<=0:raise ValueError('TEST requires a positive explicit budget cap')
        if decision['decision'] in IRREVERSIBLE:
            if float(decision['confidence_score'])<75:raise ValueError('Irreversible commitment requires confidence >=75')
            for cid in ids(decision['claim_ids']):
                claim=claims[cid]
                support=[m for m in mapping if m['claim_id']==cid and m['relationship']=='supports']
                if claim['label']=='HYPOTHESIS' or claim['contradiction_flag']=='true' or claim['freshness_status'] in ('Aging','Stale','Unknown') or not support:
                    raise ValueError('Irreversible commitment has an unresolved material claim')
                if any(evidence[m['evidence_id']]['verification_status']!='verified' for m in support):raise ValueError('Irreversible commitment requires verified support')
            for path in ['06_risks/assumptions_register.csv','06_risks/unknowns_register.csv','06_risks/dependency_register.csv','08_evidence/evidence_gap_register.csv','08_evidence/research_debt_register.csv']:
                if any(decision['decision_id'] in ids(r['decision_ids']) and r['critical']=='true' and r['status'] not in ('CLOSED','VALIDATED','RESOLVED','COMPLETE') for r in data[path]):
                    raise ValueError('Irreversible commitment has an unresolved critical uncertainty')
            entity_ids=set(ids(decision['opportunity_ids']))
            if any(r['entity_id'] in entity_ids and r['basis_type']!='OBSERVATION' for r in data['09_scores/factor_assessments.csv']):raise ValueError('Commitment opportunity factors remain assumed or unknown')
    # All exported narratives, not just files named template, receive placeholder/content checks.
    for path in set(policy['live_files'])|set(policy['approved_extra_files']):
        if path.endswith('.md'):
            text=confined(root,path,True).read_text(encoding='utf-8')
            if 'FICTIONAL DEMONSTRATION ONLY' in text or 'FICTIONAL SAMPLE' in text:raise ValueError('Live narrative contains fictional sample marker')
            if re.search(r'\[(?:complete|question|scope|name|YYYY-MM-DD|reviewed|owner|date|status|rating|category|issue|decision|RECOMMENDATION|time-sensitive|three |measured|credible|weakest|best |approved)',text,re.I):
                raise ValueError('Live delivery refuses unresolved narrative placeholders')
    return signoff

def viewer_export(root,data,contract,path):
    """Neutralize formula-leading strings in distributable CSVs; canonical files remain exact."""
    rows=[];count=0
    for row in data[path]:
        copy=dict(row)
        for field,value in copy.items():
            if field not in contract[path]['ranges'] and value.lstrip().startswith(('=','+','-','@')):
                copy[field]="'"+value;count+=1
        rows.append(copy)
    return rows,count

def build(root,as_of,mode='foundation',output='delivery_output'):
    root=Path(root).resolve()
    if mode not in ('foundation','live'):raise ValueError('Unsupported delivery mode')
    dest=safe_output(root,output);errors=validate(root,as_of)
    if errors:raise ValueError('\n'.join(errors))
    policy=delivery_policy(root);data=calculate(root,as_of);contract=load_contract(root)
    if mode=='foundation' and any(r.get('sample_status')=='LIVE' for rows in data.values() for r in rows):raise ValueError('Foundation export refuses LIVE client data')
    signoff=check_live(root,data,as_of,policy) if mode=='live' else None
    paths=set(policy['foundation_files' if mode=='foundation' else 'live_files'])|set(policy['approved_extra_files'])
    if mode=='live' and policy['include_live_source_archives']:
        archives={r['archive_reference'] for r in data['08_evidence/source_library.csv']}
        if not archives<=set(policy['approved_extra_files']):raise ValueError('Source archives require explicit export approval')
    if mode=='live' and not policy['include_live_source_archives']:
        paths-={r['archive_reference'] for r in data['08_evidence/source_library.csv']}
    # No stage until all inputs and manual gates pass. Never traverse an unlisted directory.
    stage=dest.with_name(dest.name+'.building')
    if stage.exists():raise ValueError('Staging path already exists')
    stage.mkdir(parents=True);sanitized=0
    before=input_digest(root)
    try:
        for path in sorted(paths):
            if path=='EXECUTIVE_SUMMARY.md':continue
            source=confined(root,path,True);target=confined(stage,path)
            target.parent.mkdir(parents=True,exist_ok=True)
            if path in contract:
                rows,count=viewer_export(root,data,contract,path);sanitized+=count
                write_csv(target,contract[path]['fields'],rows)
            else:shutil.copyfile(source,target)
        (stage/'EXECUTIVE_SUMMARY.md').write_text(render(root,as_of,data),encoding='utf-8')
        (stage/'README.md').write_text('# Market Intelligence Vault — '+mode+' delivery\n\nVersion '+(root/'VERSION').read_text().strip()+
            '. As-of '+as_of.isoformat()+'.\n\nRead [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md), then the analytical areas and methodology.\n'+
            ('This is a reusable framework with fictional demonstrations and unfilled templates.\n' if mode=='foundation' else 'Named manual review and decision approvals accompany this engagement.\n')+
            '\nPython tools and development tests remain in the full repository. This package is for reading,\n'+
            'not the quick-start software workflow. CSV text is sanitized for spreadsheet viewing;\n'+
            'canonical analytical inputs remain in the controlled repository.\n',encoding='utf-8')
        if mode=='live':(stage/'APPROVAL_RECORD.json').write_text(json.dumps(signoff,indent=2)+'\n',encoding='utf-8')
        link_errors=markdown_errors(stage)
        if link_errors:raise ValueError('\n'.join(link_errors))
        if input_digest(root)!=before:raise ValueError('Inputs changed during packaging; snapshot refused')
        actual={p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file()}
        actual|={'PACKAGE_MANIFEST.json','CHECKSUMS.sha256'}
        manifest={'product':'Market Intelligence Vault','version':(root/'VERSION').read_text().strip(),'model_version':'1.0.1',
         'mode':mode,'as_of':as_of.isoformat(),'contains_synthetic_data':any(r.get('sample_status')=='FICTIONAL SAMPLE' for rows in data.values() for r in rows),
         'input_digest':before,'csv_viewer_cells_sanitized':sanitized,'source_archives_distributed':mode=='foundation' or policy['include_live_source_archives'],
         'approval':'Foundation framework only' if mode=='foundation' else 'Named sign-off bound to input digest',
         'checksum_scope':'Every declared file except CHECKSUMS.sha256; the inventory includes both metadata files.',
         'files':sorted(actual)}
        (stage/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        hashes=[hashlib.sha256((stage/path).read_bytes()).hexdigest()+'  '+path for path in sorted(actual-{'CHECKSUMS.sha256'})]
        (stage/'CHECKSUMS.sha256').write_text('\n'.join(hashes)+'\n',encoding='utf-8')
        errors=verify(stage)
        if errors:raise ValueError('\n'.join(errors))
        stage.rename(dest)
    except Exception:
        resolved=stage.resolve()
        if root in resolved.parents and resolved==dest.with_name(dest.name+'.building').resolve():shutil.rmtree(resolved)
        raise
    return dest

def main():
    parser=argparse.ArgumentParser(description=__doc__);root_arg(parser)
    parser.add_argument('--mode',choices=['foundation','live'],default='foundation');parser.add_argument('--output',default='delivery_output')
    args=parser.parse_args()
    try:print('Created '+str(build(args.root,args.as_of,args.mode,args.output)));return 0
    except (ValueError,OSError,KeyError,csv.Error,TypeError,UnicodeError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())

"""Validate boundaries, CSV records, provenance, schemas, models and saved scores."""
import argparse,csv,json,re,sys,hashlib
from pathlib import Path
from urllib.parse import unquote
from common import root_arg,load_contract,read_csv,number,ids,as_date,confined,safe_url
from schema_validation import validate_schemas

ENTITY_MODELS={'05_opportunities/opportunity_database.csv':'opportunity_scoring_model','02_market/market_assessment.csv':'market_attractiveness_model','03_competitors/competitor_database.csv':'competitor_pressure_model','06_risks/risk_register.csv':'risk_scoring_model','05_opportunities/gap_register.csv':'gap_scoring_model','07_strategy/decision_matrix.csv':None}

def factor_keys(data,contract):
    expected=set()
    for path,model in ENTITY_MODELS.items():
        factors=[r['factor'] for r in data['09_scores/'+model+'.csv'] if r['factor']!='evidence_confidence'] if model else ['potential_upside','cost','time_to_value','execution_difficulty','risk','strategic_fit']
        for row in data[path]:
            for factor in factors:expected.add((path,row[contract[path]['primary']],factor))
    return expected

def markdown_errors(root,paths=None):
    root=Path(root).resolve();errors=[]
    for p in paths if paths is not None else root.rglob('*.md'):
        if p.relative_to(root).parts[0].startswith(('delivery_','engagement_')):continue
        try:text=p.read_text(encoding='utf-8')
        except (OSError,UnicodeError):errors.append('Unreadable Markdown: '+p.relative_to(root).as_posix());continue
        if text.count('```')%2:errors.append(p.name+': unbalanced code fences')
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
            if '://' in target or target.startswith('#'):continue
            target=unquote(target.split('#')[0].strip('<>'))
            try:
                candidate=(p.parent/target).resolve()
                if root not in candidate.parents or not candidate.exists():raise ValueError()
            except (ValueError,OSError):errors.append(p.relative_to(root).as_posix()+': broken or unsafe link')
        if '12_examples' in p.relative_to(root).parts and 'FICTIONAL DEMONSTRATION ONLY' not in text:errors.append(p.name+': missing fictional demonstration label')
    return errors

def validate(root,as_of,audit_scores=False):
    root=Path(root).resolve();errors=[];data={}
    if (root/'.score_transaction').exists():return ['Incomplete score transaction; run calculate_scores.py --recover']
    try:
        inventory=json.loads(confined(root,'config/required_files.json',True).read_text(encoding='utf-8'))
        contract=load_contract(root)
        if not isinstance(inventory,list) or len(set(inventory))!=len(inventory):raise ValueError()
        for path in inventory:confined(root,path)
    except (OSError,ValueError,TypeError,KeyError):return ['Cannot load release contract: malformed or unsafe configuration']
    for path in inventory:
        try:
            p=confined(root,path,True)
            if p.stat().st_size==0:errors.append('Empty required file: '+path)
        except (OSError,ValueError):errors.append('Missing required file or unsafe path: '+path)
    for path,c in contract.items():
        try:fields,rows=read_csv(confined(root,path,True))
        except (OSError,ValueError,csv.Error,UnicodeError):errors.append('Malformed CSV '+path);continue
        if fields!=c['fields']:errors.append(path+': header/order mismatch');continue
        data[path]=rows;seen=set()
        for i,row in enumerate(rows,2):
            prefix=f'{path}:{i}'
            for field in c['required']:
                if not row[field].strip():errors.append(prefix+': empty required field '+field)
            key=row[c['primary']]
            if key in seen:errors.append(prefix+': duplicate ID')
            seen.add(key)
            if not re.fullmatch(r'[A-Z][A-Z0-9-]*' if c['primary'].endswith('_id') else r'[a-z][a-z0-9_]*',key):errors.append(prefix+': invalid primary key syntax')
            for field,bounds in c['ranges'].items():
                if row[field]!='':
                    try:
                        n=number(row[field],*bounds)
                        if field in c.get('integers',[]) and not n.is_integer():raise ValueError()
                    except ValueError:errors.append(prefix+': invalid '+field)
            for field,values in c['enums'].items():
                if row[field] and row[field] not in values:errors.append(prefix+': unsupported '+field)
            for field,value in row.items():
                if field.endswith('_date') and value:
                    try:
                        parsed=as_date(value)
                        if field in ('publication_date','access_date','observed_date','as_of_date','review_date') and parsed>as_of:raise ValueError()
                    except (ValueError,TypeError):errors.append(prefix+': invalid or future '+field)
                if any(ord(ch)<32 and ch not in ('\n','\r','\t') for ch in value):errors.append(prefix+': control character in '+field)
            if row.get('override')=='true' and not row.get('override_reason','').strip():errors.append(prefix+': override requires reason')
            if path=='02_market/market_assessment.csv':
                try:
                    if not float(row['som'])<=float(row['sam'])<=float(row['tam']):errors.append(prefix+': SOM <= SAM <= TAM violated')
                except ValueError:pass
    if errors:return errors
    indexes={path:{r[c['primary']]:r for r in data[path]} for path,c in contract.items()}
    for path,c in contract.items():
        for i,row in enumerate(data[path],2):
            for field,target in c['references'].items():
                target_path,key=target.split(':');target_rows={r[key]:r for r in data[target_path]}
                try:values=ids(row[field])
                except ValueError:errors.append(f'{path}:{i}: malformed reference list {field}');continue
                for value in values:
                    target_row=target_rows.get(value)
                    if target_row is None:errors.append(f'{path}:{i}: missing reference {field}={value}');continue
                    if row.get('sample_status') and target_row.get('sample_status') and row['sample_status']!=target_row['sample_status']:errors.append(path+': mixed status reference')
    if errors:return errors
    sources=indexes['08_evidence/source_library.csv'];evidence=indexes['08_evidence/evidence_register.csv'];claims=indexes['08_evidence/claims_register.csv']
    maps=data['08_evidence/claim_evidence_map.csv'];semantic=set()
    for sid,row in sources.items():
        try:safe_url(row['source_url'],row['sample_status'])
        except ValueError:errors.append(sid+': unsafe or invalid source URL')
        try:
            archive=confined(root,row['archive_reference'],True)
            if not re.fullmatch(r'[a-f0-9]{64}',row['archive_sha256']) or hashlib.sha256(archive.read_bytes()).hexdigest()!=row['archive_sha256']:errors.append(sid+': archive checksum mismatch')
            if row['sample_status']=='LIVE' and archive.suffix.lower() in ('.md','.txt','.csv','.json'):
                text=archive.read_text(encoding='utf-8')
                if 'FICTIONAL DEMONSTRATION ONLY' in text or 'FICTIONAL SAMPLE' in text:errors.append(sid+': synthetic archive cannot be LIVE')
        except (OSError,ValueError,UnicodeError):errors.append(sid+': missing, unsafe or unreadable archive reference')
        if row['publication_date'] and as_date(row['publication_date'])>as_date(row['access_date']):errors.append(sid+': publication after access')
    for eid,row in evidence.items():
        src=sources[row['source_id']]
        for field in ['source_title','source_url','publisher','publication_date','access_date','origin_group','topic']:
            if row[field]!=src[field]:errors.append(eid+': source metadata drift in '+field)
        if float(row['reliability_score'])>float(src['reliability_score']):errors.append(eid+': reliability exceeds source ceiling')
        directness=float(row['directness_score'])
        if (row['direct_or_indirect']=='direct' and directness<15) or (row['direct_or_indirect']=='indirect' and directness>15):errors.append(eid+': directness label/score conflict')
        if not any(m['evidence_id']==eid and m['claim_id']==row['claim_id'] for m in maps):errors.append(eid+': missing evidence map')
    for m in maps:
        pair=(m['claim_id'],m['evidence_id'])
        if pair in semantic:errors.append(m['map_id']+': duplicate semantic evidence mapping')
        semantic.add(pair)
        if evidence[m['evidence_id']]['claim_id']!=m['claim_id']:errors.append(m['map_id']+': claim/evidence mismatch')
    for cid,row in claims.items():
        support={m['evidence_id'] for m in maps if m['claim_id']==cid and m['relationship']=='supports'}
        if set(ids(row['evidence_ids']))!=support:errors.append(cid+': support list/map mismatch')
        if row['label']=='FACT' and (not support or any(evidence[e]['verification_status']!='verified' or evidence[e]['direct_or_indirect']!='direct' for e in support)):errors.append(cid+': unsupported FACT or nonverified/indirect support')
        flags=any(evidence[m['evidence_id']]['contradiction_flag']=='true' for m in maps if m['claim_id']==cid)
        contrad=any(m['claim_id']==cid and m['relationship']=='contradicts' for m in maps)
        if (flags or contrad) and row['contradiction_flag']!='true':errors.append(cid+': contradiction flag/map mismatch')
    for path,rows in data.items():
        if not path.startswith('09_scores/') or path.endswith('factor_assessments.csv'):continue
        try:
            if abs(sum(number(r['weight']) for r in rows)-100)>1e-9:raise ValueError()
            if any(float(r['input_max'])<=float(r['input_min']) for r in rows):raise ValueError()
            if path.endswith('confidence_model.csv') and any(float(r['weight'])!=float(r['input_max']) for r in rows):raise ValueError()
        except (ValueError,KeyError):errors.append(path+': invalid model or weights must sum to 100')
    try:
        cfg=json.loads(confined(root,'config/freshness.json',True).read_text(encoding='utf-8'))
        if 'default' not in cfg:raise ValueError()
        for thresholds in cfg.values():
            a,b,c=[thresholds[k] for k in ('current_days','recent_days','aging_days')]
            if not all(type(x) is int for x in (a,b,c)) or not 0<=a<b<c:raise ValueError()
        policy=json.loads(confined(root,'config/scoring_policy.json',True).read_text(encoding='utf-8'))
        if set(policy['claim_type_caps'])!=set(['FACT','INFERENCE','ESTIMATE','HYPOTHESIS','RECOMMENDATION']):raise ValueError()
        for cap in policy['claim_type_caps'].values():number(cap)
        if policy['model_version']!='1.0.1' or policy['opportunity_confidence_floor']!=0.25 or policy['opportunity_confidence_weight']!=0.75:raise ValueError()
    except (OSError,ValueError,KeyError,TypeError):errors.append('Invalid freshness or scoring policy')
    expected=factor_keys(data,contract);present=set()
    for r in data['09_scores/factor_assessments.csv']:
        key=(r['entity_file'],r['entity_id'],r['factor'])
        if key in present:errors.append(r['assessment_id']+': duplicate factor assessment')
        present.add(key)
        if key not in expected:errors.append(r['assessment_id']+': unknown factor target');continue
        target=indexes[r['entity_file']][r['entity_id']]
        if float(target[r['factor']])!=float(r['input_value']):errors.append(r['assessment_id']+': factor value drift')
        if target['sample_status']!=r['sample_status']:errors.append(r['assessment_id']+': mixed factor status')
        if r['basis_type']=='OBSERVATION' and (not r['evidence_ids'] or not r['claim_ids']):errors.append(r['assessment_id']+': observation requires claim and evidence')
        if r['basis_type']=='ASSUMPTION' and not r['assumption_ids']:errors.append(r['assessment_id']+': assumption reference required')
    if expected-present:errors.append('Missing factor assessment coverage')
    errors+=validate_schemas(root,contract,data)
    errors+=markdown_errors(root)
    if audit_scores and not errors:
        try:
            from calculate_scores import calculate
            recomputed=calculate(root,as_of,data)
            for path,rows in recomputed.items():
                if rows!=data[path]:errors.append(path+': saved fields differ from recomputation; run calculate_scores.py')
        except (ValueError,KeyError,TypeError,OSError):errors.append('Score audit failed on invalid input')
    return errors

def main():
    parser=argparse.ArgumentParser(description=__doc__);root_arg(parser);parser.add_argument('--audit-scores',action='store_true')
    args=parser.parse_args();errors=validate(args.root,args.as_of,args.audit_scores)
    for error in errors:print('ERROR: '+error)
    print(f'Validation {"FAILED" if errors else "PASSED"}: {len(errors)} error(s).')
    return int(bool(errors))
if __name__=='__main__':sys.exit(main())

"""Export a confined, validated, read-only dashboard snapshot. No external requests."""
import argparse,csv,hashlib,json,re,shutil,sys
from datetime import date,datetime,timezone
from pathlib import Path
from common import DEFAULT_ROOT,confined,load_data,load_contract,ids,number,confidence_band,freshness,input_digest,weighted,opportunity_score,opportunity_category,gate,safe_url
from calculate_scores import calculate
from validate_repository import validate
from build_delivery_package import check_live,delivery_policy,IRREVERSIBLE

FILES=('executive','market','opportunities','risks','competitors','customers','evidence','sources','contradictions','assumptions','research-gaps','action-plan')
CLOSED={'CLOSED','VALIDATED','RESOLVED','COMPLETE','RETIRED','CANCELLED'}
DERIVED={'confidence_score','confidence_level','confidence','freshness_status','freshness_score','evidence_grade','corroboration_score','claim_limit','evidence_confidence','raw_score','merit_score','confidence_multiplier','input_basis_status','opportunity_score','action_category','decision_gate','risk_score','classification','structural_zero','review_required','market_attractiveness_score','rating','recommended_posture','competitor_pressure_score','gap_score','score'}
# Explicit field projection. No archive paths, archival bytes, credentials or arbitrary files.
SOURCES='source_id source_title source_url publisher publication_date access_date source_type topic tier reliability_score origin_group locator usage_rights'
EVIDENCE='evidence_id claim_id source_id evidence_type direct_or_indirect finding supporting_quote_or_summary locator reliability_score freshness_score directness_score corroboration_score relevance_score confidence_score confidence_level evidence_grade freshness_status contradiction_flag verification_status analyst_notes'
CLAIMS='claim_id label finding business_impact recommended_action evidence_ids confidence_score confidence_level contradiction_flag owner decision_status priority freshness_status claim_limit'

def snapshot_date(root):
    data=load_data(root)
    dates={r['as_of_date'] for r in data['07_strategy/recommendations.csv'] if r.get('as_of_date')}
    if len(dates)>1:raise ValueError('Recommendations require one reviewed snapshot date')
    return date.fromisoformat(next(iter(dates))) if dates else date.today()

def project(row,fields,contract):
    out={}
    for key in fields.split() if isinstance(fields,str) else fields:
        value=row.get(key,'')
        if not value:out[key]=None
        elif key in contract['ranges']:out[key]=number(value,*contract['ranges'][key])
        elif key in contract['references']:out[key]=ids(value) if key.endswith('_ids') or key=='current_evidence' else value
        elif key in ('critical','contradiction_flag','structural_zero','override'):out[key]=value=='true'
        else:out[key]=value
    if 'confidence_score' in out:out['confidence_category']=confidence_band(out['confidence_score']) if out['confidence_score'] is not None else None
    return out

def sensitivity(row,all_rows,factors,model,score_field):
    uncertain=[f for f in factors if f['basis_type']!='OBSERVATION']
    business=[f for f in model if f['factor']!='evidence_confidence']
    total=sum(float(f['weight']) for f in business)
    normalized=[{**f,'weight':str(float(f['weight'])*100/total)} for f in business]
    score=lambda r:opportunity_score(weighted(r,normalized),float(r['confidence_score']))
    baseline=score(row);identity='opportunity_id';rank=lambda value:1+sum(float(r[score_field])>value for r in all_rows if r[identity]!=row[identity] and r[score_field]!='')
    scenarios=[]
    if row.get('confidence_score','')=='':return {'status':'NOT TESTABLE — MISSING SUPPORT','scenarios':[]}
    for basis in uncertain:
        field=basis['factor']
        if field not in {f['factor'] for f in business}:continue
        for delta in (-1,1):
            altered=dict(row);v=min(5,max(0,float(row[field])+delta))
            if v==float(row[field]):continue
            altered[field]=str(v);value=score(altered)
            scenarios.append({'factor':field,'delta':delta,'tested_value':v,'score':round(value,2),'category':opportunity_category(value),'rank':rank(value),'rank_changed':rank(value)!=rank(baseline),'category_changed':opportunity_category(value)!=opportunity_category(baseline)})
    sensitive=any(s['rank_changed'] or s['category_changed'] for s in scenarios)
    return {'status':'RANK SENSITIVE' if sensitive else 'STABLE WITHIN TESTED RANGE' if scenarios else 'NO UNCERTAIN FACTORS TO TEST','decision_status':'SENSITIVE DECISION' if sensitive else 'STABLE WITHIN TESTED RANGE' if scenarios else 'NOT TESTED','baseline_rank':rank(baseline),'scenarios':scenarios,'method':'One uncertain business factor at a time, ±1, bounded 0–5. Confidence held fixed. Not statistical intervals or joint stress testing. Categories/ranks may require review; strategic actions and approval are never automatically changed.'}

def approval(root,data,as_of,mode):
    reasons=[]
    if mode!='LIVE':reasons.append('Fictional or unresearched records cannot authorize a live action. A reviewed live engagement and named sign-off are required.')
    else:
        try:check_live(root,data,as_of,delivery_policy(root))
        except (ValueError,OSError,KeyError,TypeError,csv.Error):reasons.append('Repository live gates: '+str(sys.exc_info()[1]).splitlines()[0])
    if mode=='LIVE' and as_of!=datetime.now(timezone.utc).date():reasons.append('Historical snapshot: current-date review and refresh required.')
    return {'status':'ACTION NOT APPROVED' if reasons else 'APPROVED','reasons':reasons,'review_date':as_of.isoformat(),'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'All recommendations must satisfy unchanged 1.0.1 live-delivery gates. This is a snapshot, not signer authentication.'}

def payloads(root,as_of):
    root=Path(root).resolve();errors=validate(root,as_of,False)
    if errors:raise ValueError('Repository validation failed; no dashboard export. '+errors[0])
    contract=load_contract(root);data=load_data(root);recomputed=calculate(root,as_of,data)
    for path,rows in data.items():
        for row,expected in zip(rows,recomputed[path]):
            for field in DERIVED & row.keys():
                if row[field] and row[field]!=expected[field]:raise ValueError('Stored score or derived metadata does not reconcile: '+path+'/'+field)
    states={r['sample_status'] for rows in data.values() for r in rows if 'sample_status' in r}
    if len(states)>1:raise ValueError('Mixed synthetic/live/template records refused')
    mode='LIVE' if states=={'LIVE'} else 'FICTIONAL DEMONSTRATION' if states=={'FICTIONAL SAMPLE'} else 'NOT YET RESEARCHED'
    cfg=json.loads(confined(root,'config/dashboard_config.json',True).read_text(encoding='utf-8'))
    if not isinstance(cfg,dict) or not isinstance(cfg.get('engagement_name'),str) or not cfg['engagement_name'].strip():raise ValueError('Engagement name must be explicitly configured')
    if mode=='LIVE' and (cfg.get('sample_status')!='LIVE' or cfg['engagement_name']=='Northstar Analytics'):raise ValueError('Live engagement metadata must replace demo configuration')
    before=input_digest(root)
    read=lambda p,fields=None:[project(r,fields or contract[p]['fields'],contract[p]) for r in data[p]]
    src=read('08_evidence/source_library.csv',SOURCES)
    fresh_cfg=json.loads(confined(root,'config/freshness.json',True).read_text())
    for r in src:
        if r['source_url']:safe_url(r['source_url'], 'LIVE' if mode=='LIVE' else 'FICTIONAL SAMPLE')
        r['freshness_status']=freshness(r['publication_date'] or '',r['topic'],fresh_cfg,as_of)[0]
        r['archive_status']='INTEGRITY CHECK PASSED';r['authentication_status']='Publisher identity not authenticated'
    ev=read('08_evidence/evidence_register.csv',EVIDENCE);claims=read('08_evidence/claims_register.csv',CLAIMS)
    maps=read('08_evidence/claim_evidence_map.csv');factors=read('09_scores/factor_assessments.csv')
    assumptions=read('06_risks/assumptions_register.csv');unknowns=read('06_risks/unknowns_register.csv');dependencies=read('06_risks/dependency_register.csv')
    gaps=read('08_evidence/evidence_gap_register.csv');research=read('08_evidence/research_gap_register.csv');debt=read('08_evidence/research_debt_register.csv')
    decisions=read('07_strategy/recommendations.csv');options=read('07_strategy/decision_matrix.csv')
    status=approval(root,data,as_of,mode)
    for r in decisions:
        r['recorded_status']=r.pop('status');r['approval']=status;r['action_class']='IRREVERSIBLE COMMITMENT' if r['decision'] in IRREVERSIBLE else 'REVERSIBLE VALIDATION / OBSERVATION' if r['decision'] in ('TEST','MONITOR','WAIT') else 'AVOIDANCE POSTURE'
    opp=read('05_opportunities/opportunity_database.csv')
    original=data['05_opportunities/opportunity_database.csv']
    for r,raw in zip(opp,original):
        own=[f for f in data['09_scores/factor_assessments.csv'] if f['entity_id']==r['opportunity_id'] and f['entity_file']=='05_opportunities/opportunity_database.csv']
        r['sensitivity']=sensitivity(raw,original,own,data['09_scores/opportunity_scoring_model.csv'],'opportunity_score') if r['confidence_score'] is not None else {'status':'NOT TESTABLE — MISSING SUPPORT','scenarios':[]}
    risks=read('06_risks/risk_register.csv');competitors=read('03_competitors/competitor_database.csv')
    for r in competitors:r['pressure_category']=None if r['competitor_pressure_score'] is None else 'Very strong' if r['competitor_pressure_score']>=80 else 'Strong' if r['competitor_pressure_score']>=60 else 'Moderate' if r['competitor_pressure_score']>=40 else 'Limited'
    contradiction=[]
    for c in claims:
        linked=[m for m in maps if m['claim_id']==c['claim_id']]
        if c['contradiction_flag'] or any(m['relationship']=='contradicts' for m in linked):
            contradiction.append({'claim_id':c['claim_id'],'claim':c['finding'],'supporting_evidence':[m['evidence_id'] for m in linked if m['relationship']=='supports'],'contradicting_evidence':[m['evidence_id'] for m in linked if m['relationship']=='contradicts'],'reason':'; '.join(m['interpretation'] for m in linked if m['relationship']=='contradicts'),'most_likely_interpretation':None,'confidence_score':c['confidence_score'],'confidence_category':c['confidence_category'],'resolution_status':'UNRESOLVED','required_follow_up':[g['research_method'] for g in gaps if g['claim_id']==c['claim_id']]})
    models={p.split('/')[-1].replace('.csv',''):rows for p,rows in data.items() if p.startswith('09_scores/') and p.endswith('_model.csv')}
    outputs={
      'executive':{'decisions':decisions,'options':options,'unknowns':unknowns,'dependencies':dependencies,'coverage':{'claims':len(claims),'with_support':sum(any(m['claim_id']==c['claim_id'] and m['relationship']=='supports' for m in maps) for c in claims),'open_gaps':sum(g['status'] not in CLOSED for g in gaps+research+debt),'critical_unknowns':sum(r['critical'] and r['status'] not in CLOSED for r in unknowns),'fresh_sources':sum(r['freshness_status'] in ('Current','Recent') for r in src),'source_count':len(src),'stale_or_unknown_sources':sum(r['freshness_status'] in ('Stale','Unknown') for r in src)},'models':models,'factors':factors},
      'market':{'records':read('02_market/market_assessment.csv'),'signals':read('02_market/market_signals.csv')},
      'opportunities':{'records':opp},'risks':{'records':risks},'competitors':{'records':competitors,'pricing':read('03_competitors/pricing_comparison_template.csv'),'changes':read('03_competitors/competitor_change_log.csv')},
      'customers':{'records':read('04_customers/customer_segments_template.csv'),'pains':read('04_customers/pain_points_template.csv'),'triggers':read('04_customers/buying_triggers_template.csv'),'objections':read('04_customers/objections_template.csv'),'insights':read('04_customers/customer_evidence_template.csv')},
      'evidence':{'claims':claims,'records':ev,'relationships':maps},'sources':{'records':src,'quality':{'missing_urls':sum(r['source_url'] is None for r in src),'duplicate_urls':len([r['source_url'] for r in src if r['source_url']])-len({r['source_url'] for r in src if r['source_url']}),'low_reliability':sum(r['reliability_score']<=5 for r in src)}},
      'contradictions':{'records':contradiction},'assumptions':{'records':assumptions},'research-gaps':{'records':gaps,'questions':research,'debt':debt},'action-plan':{'records':read('07_strategy/action_plan.csv')}
    }
    if input_digest(root)!=before:raise ValueError('Inputs changed during dashboard export')
    canonical=json.dumps(outputs,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()
    if mode=='LIVE' and any(marker in canonical.decode().lower() for marker in ('fictional demonstration','fictional sample','synthetic region a','synthetic interview','synthetic audit','synthetic conversation','(invented)','northstar analytics')):
        raise ValueError('Known fictional business content refused in live dashboard')
    def scan(value):
        if isinstance(value,dict):
            for v in value.values():scan(v)
        elif isinstance(value,list):
            for v in value:scan(v)
        elif isinstance(value,str):
            for url in re.findall(r'https?://[^\s<>"\']+',value):
                safe_url(url.rstrip(').,;'),'LIVE' if mode=='LIVE' else 'FICTIONAL SAMPLE')
    scan(outputs)
    meta={'contract_version':'1.1.0','repository_version':confined(root,'VERSION',True).read_text().strip(),'model_version':'1.0.1','engagement_name':cfg['engagement_name'],'mode':mode,'demo_label':'FICTIONAL DEMONSTRATION DATA' if mode=='FICTIONAL DEMONSTRATION' else None,'as_of_date':as_of.isoformat(),'validated_at':datetime.now(timezone.utc).isoformat(),'snapshot_id':hashlib.sha256(canonical).hexdigest(),'input_digest':before,'approval':status,'score_reconciliation':'Populated derived values reconcile; unavailable optional values remain null.'}
    return {name:{'meta':meta,'data':outputs[name]} for name in FILES}

def export(root,as_of,output='dashboard/data',refresh=False):
    root=Path(root).resolve()
    if not output.startswith('dashboard/data') or len(Path(output).parts)!=2:raise ValueError('Dashboard exports must use a confined dashboard/data snapshot directory')
    dest=confined(root,output);stage=confined(root,output+'.building');backup=confined(root,output+'.previous')
    if stage.exists() or backup.exists():raise ValueError('Interrupted dashboard export: preserve and review staging/backup before retry')
    allowed={f+'.json' for f in FILES}|{'snapshot.json'}
    if dest.exists() and (not refresh or any(p.name not in allowed or not p.is_file() or p.is_symlink() for p in dest.iterdir())):raise ValueError('Refusing overwrite or unlisted dashboard data file')
    values=payloads(root,as_of);stage.mkdir(parents=True)
    moved=False
    try:
        for name,value in values.items():(stage/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        manifest={'meta':values['executive']['meta'],'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())}}
        (stage/'snapshot.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        if dest.exists():dest.rename(backup);moved=True
        stage.rename(dest)
        if moved:shutil.rmtree(backup)
    except Exception:
        if moved and not dest.exists():backup.rename(dest)
        if stage.exists():shutil.rmtree(stage)
        raise
    return dest

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=DEFAULT_ROOT);p.add_argument('--as-of',type=date.fromisoformat);p.add_argument('--output',default='dashboard/data');p.add_argument('--refresh',action='store_true');a=p.parse_args()
    try:print('Exported '+str(export(a.root,a.as_of or snapshot_date(a.root),a.output,a.refresh)));return 0
    except (ValueError,OSError,KeyError,TypeError,csv.Error,UnicodeError):print('ERROR: dashboard export refused invalid or unsafe inputs; run validation. No fallback snapshot generated.',file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())

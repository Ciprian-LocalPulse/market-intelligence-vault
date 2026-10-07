"""Recompute scores and derived views from versioned models. No network access."""
import argparse
import copy
import json
import sys
import hashlib
import shutil
from common import (root_arg, load_data, load_contract, weighted, evidence_score, freshness,
                    number, ids, confidence_band, opportunity_score, opportunity_category,
                    gate, risk_class, fmt, write_csv, confined)

def calculate(root, as_of, data=None):
    data = copy.deepcopy(load_data(root) if data is None else data)
    cfg = json.loads((root/'config/freshness.json').read_text(encoding='utf-8'))
    policy=json.loads((root/'config/scoring_policy.json').read_text(encoding='utf-8'))
    model = lambda name: data['09_scores/'+name+'.csv']
    evidence = {r['evidence_id']:r for r in data['08_evidence/evidence_register.csv']}
    maps = data['08_evidence/claim_evidence_map.csv']
    claims = {r['claim_id']:r for r in data['08_evidence/claims_register.csv']}
    for row in evidence.values():
        row['freshness_status'],fresh=freshness(row['publication_date'],row['topic'],cfg,as_of)
        row['freshness_score']=str(fresh)
    for row in evidence.values():
        row['freshness_status'], fresh = freshness(row['publication_date'],row['topic'],cfg,as_of)
        row['freshness_score'] = str(fresh)
        origins = {evidence[m['evidence_id']]['origin_group'] for m in maps
                   if m['claim_id']==row['claim_id'] and m['relationship']=='supports'
                   and evidence[m['evidence_id']]['verification_status']=='verified'
                   and evidence[m['evidence_id']]['direct_or_indirect']=='direct'
                   and evidence[m['evidence_id']]['freshness_status'] in ('Current','Recent')
                   and float(evidence[m['evidence_id']]['reliability_score'])>=15
                   and float(evidence[m['evidence_id']]['relevance_score'])>=10}
        cap = 0 if len(origins)<=1 else 10 if len(origins)==2 else 15 if len(origins)==3 else 20
        row['corroboration_score'] = fmt(cap)
        score, grade = evidence_score(row,model('confidence_model'))
        row['confidence_score'], row['evidence_grade'] = fmt(score), grade
        row['confidence_level'] = confidence_band(score)
    for cid,row in claims.items():
        support = [m for m in maps if m['claim_id']==cid and m['relationship']=='supports']
        critical = [m for m in support if m['materiality']=='critical'] or support
        score = min((float(evidence[m['evidence_id']]['confidence_score']) for m in critical),default=0)
        contradiction = row['contradiction_flag']=='true' or any(m['claim_id']==cid and (m['relationship']=='contradicts' or evidence[m['evidence_id']]['contradiction_flag']=='true') for m in maps)
        cap=policy['claim_type_caps'][row['label']]
        if contradiction:cap=min(cap,59)
        score=min(score,cap)
        row['confidence_score'],row['confidence_level'] = fmt(score),confidence_band(score)
        row['claim_limit']='UNRESOLVED CONFLICT' if contradiction else 'TYPE CAP' if score==cap and cap<100 else 'CRITICAL SUPPORT'
        states=[evidence[m['evidence_id']]['freshness_status'] for m in critical]
        severity={'Current':0,'Recent':1,'Aging':2,'Stale':3,'Unknown':4}
        row['freshness_status']=max(states,key=lambda s:severity[s]) if states else 'Unknown'
    def confidence(row):
        if 'claim_ids' in row:
            return min((float(claims[c]['confidence_score']) for c in ids(row['claim_ids'])),default=0)
        if 'claim_id' in row:
            return float(claims[row['claim_id']]['confidence_score'])
        ref = row.get('evidence_ids',row.get('current_evidence',''))
        return min((float(claims[evidence[e]['claim_id']]['confidence_score']) for e in ids(ref)),default=0)
    for path,rows in data.items():
        if path.startswith(('08_evidence/evidence_register','08_evidence/claims_register','10_dashboards/')):
            continue
        for row in rows:
            if 'confidence_score' in row:
                row['confidence_score']=fmt(confidence(row))
            if 'confidence' in row:
                row['confidence']=fmt(confidence(row))
            if path=='05_opportunities/opportunity_database.csv':
                conf=confidence(row); row['evidence_confidence']=str(conf/20)
                raw=weighted(row,model('opportunity_scoring_model'))
                # Remove the additive confidence term; renormalize the 95 points of business merit.
                business=[f for f in model('opportunity_scoring_model') if f['factor']!='evidence_confidence']
                total=sum(float(f['weight']) for f in business)
                normalized=[{**f,'weight':str(float(f['weight'])*100/total)} for f in business]
                merit=weighted(row,normalized);adjusted=opportunity_score(merit,conf)
                basis=[r['basis_type'] for r in data['09_scores/factor_assessments.csv'] if r['entity_file']==path and r['entity_id']==row['opportunity_id']]
                basis_status='UNKNOWN INPUTS' if 'UNKNOWN' in basis else 'ASSUMED INPUTS' if 'ASSUMPTION' in basis else 'OBSERVED INPUTS'
                row.update(raw_score=fmt(raw),merit_score=fmt(merit),confidence_multiplier=f'{0.25+0.75*conf/100:.6f}',input_basis_status=basis_status,opportunity_score=fmt(adjusted),action_category=opportunity_category(adjusted),decision_gate=gate(conf))
            elif path=='02_market/market_assessment.csv':
                score=weighted(row,model('market_attractiveness_model'))
                row.update(market_attractiveness_score=fmt(score),rating='Attractive' if score>=75 else 'Selective' if score>=55 else 'Challenging' if score>=40 else 'Unattractive',recommended_posture='REVIEW ENTRY' if score>=75 else 'TEST NARROW SCOPE' if score>=55 else 'MONITOR' if score>=40 else 'AVOID UNTIL CONDITIONS CHANGE')
            elif path=='03_competitors/competitor_database.csv':
                row['competitor_pressure_score']=fmt(weighted(row,model('competitor_pressure_model')))
            elif path=='06_risks/risk_register.csv':
                score=weighted(row,model('risk_scoring_model'))
                # An event impossible within the horizon or having no impact has zero exposure.
                structural=float(row['likelihood'])==0 or float(row['impact'])==0
                if structural and row['override']!='true':score=0
                row.update(risk_score=fmt(score),classification=risk_class(score,row))
                row['structural_zero']='true' if structural else 'false'
                row['review_required']='ZERO-EXPOSURE ASSUMPTION: VERIFY' if structural else 'MANUAL CRITICAL ACCEPTANCE' if row['classification']=='Critical' else 'OWNER REVIEW'
            elif path=='05_opportunities/gap_register.csv':
                row['evidence_confidence']=str(confidence(row)/20)
                row['gap_score']=fmt(weighted(row,model('gap_scoring_model')))
            elif path=='07_strategy/decision_matrix.csv':
                row['score']=fmt(opportunity_score(weighted(row,model('decision_scoring_model')),confidence(row)))
                row['decision_gate']=gate(confidence(row))
            if 'as_of_date' in row and path in ('05_opportunities/opportunity_database.csv','02_market/market_assessment.csv','03_competitors/competitor_database.csv','06_risks/risk_register.csv','05_opportunities/gap_register.csv','07_strategy/decision_matrix.csv','07_strategy/recommendations.csv','07_strategy/action_plan.csv'):
                row['as_of_date']=as_of.isoformat()
    contract = load_contract(root)
    views = {
        '05_opportunities/opportunity_scorecard.csv':'05_opportunities/opportunity_database.csv',
        '10_dashboards/executive_dashboard_template.csv':'07_strategy/recommendations.csv',
        '10_dashboards/opportunity_dashboard_template.csv':'05_opportunities/opportunity_database.csv',
        '10_dashboards/competitor_dashboard_template.csv':'03_competitors/competitor_database.csv',
        '10_dashboards/risk_dashboard_template.csv':'06_risks/risk_register.csv',
    }
    for dest,source in views.items():
        data[dest]=[{k:r[k] for k in contract[dest]['fields']} for r in data[source]]
    return data

def save(root,data):
    root=root.resolve();contract=load_contract(root);before=load_data(root)
    changes=[p for p in data if data[p]!=before[p]]
    if not changes:return
    stage=root/'.score_transaction'
    if stage.exists():raise ValueError('Incomplete score transaction: recover before proceeding')
    stage.mkdir()
    journal={'paths':changes,'installed':[]}
    (stage/'journal.json').write_text(json.dumps(journal),encoding='utf-8')
    try:
        for path in changes:
            original=confined(root,path,True);backup=confined(stage,'backup/'+path)
            backup.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,backup)
            write_csv(confined(stage,'new/'+path),contract[path]['fields'],data[path])
        (stage/'journal.json').write_text(json.dumps(journal),encoding='utf-8')
        for path in changes:
            original=confined(root,path,True);backup=confined(stage,'backup/'+path,True)
            if original.read_bytes()!=backup.read_bytes():raise ValueError('Concurrent input change; refresh refused')
            journal['installed'].append(path)
            (stage/'journal.json').write_text(json.dumps(journal),encoding='utf-8')
            import os
            os.replace(confined(stage,'new/'+path,True),original)
    except Exception:
        recover(root)
        raise
    shutil.rmtree(stage)

def recover(root):
    root=root.resolve();stage=root/'.score_transaction'
    if not stage.exists():return
    journal=json.loads(confined(root,'.score_transaction/journal.json',True).read_text(encoding='utf-8'))
    for path in journal['installed']:
        original=confined(root,path);backup=confined(stage,'backup/'+path,True)
        shutil.copyfile(backup,original)
    if stage.resolve().parent==root:shutil.rmtree(stage)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    root_arg(parser)
    parser.add_argument('--recover',action='store_true',help='Roll back an interrupted score transaction')
    args=parser.parse_args(); args.root=args.root.resolve()
    try:
        if args.recover:
            recover(args.root);print('Score recovery completed. Run validation and refresh.');return 0
        from validate_repository import validate
        errors=validate(args.root,args.as_of)
        if errors:
            raise ValueError('\n'.join(errors))
        data=calculate(args.root,args.as_of)
        save(args.root,data)
        print(f'Scores and five derived views refreshed at {args.as_of}. Synthetic status preserved.')
    except (ValueError,OSError,KeyError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr); return 1
    return 0

if __name__=='__main__':
    sys.exit(main())

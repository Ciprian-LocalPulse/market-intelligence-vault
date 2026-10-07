"""Build an executive Markdown summary from freshly recalculated structured inputs."""
import argparse
import sys
from common import root_arg, safe_output, md, ids
from calculate_scores import calculate
from validate_repository import validate

def render(root,as_of,data=None):
    data=calculate(root,as_of,data)
    claims=data['08_evidence/claims_register.csv']
    decisions=data['07_strategy/recommendations.csv']
    opportunities=sorted(data['05_opportunities/opportunity_database.csv'],key=lambda r:(-float(r['opportunity_score']),r['opportunity_id']))
    risks=sorted(data['06_risks/risk_register.csv'],key=lambda r:(-float(r['risk_score']),r['risk_id']))
    sources={r['source_id']:r for r in data['08_evidence/source_library.csv']}
    evidence={r['evidence_id']:r for r in data['08_evidence/evidence_register.csv']}
    maps=data['08_evidence/claim_evidence_map.csv']
    statuses={r.get('sample_status') for path,rows in data.items() for r in rows if 'sample_status' in r}
    synthetic='FICTIONAL SAMPLE' in statuses
    out=['# Executive summary','', '**Market Intelligence Vault · Foundation Release 1.0.0**','',
         f'As-of: {as_of}. Scores recomputed from current inputs and model files.','']
    out[2]='**Market Intelligence Vault · Interactive Intelligence Release '+(root/'VERSION').read_text().strip()+'**'
    if synthetic: out+=['> **FICTIONAL DEMONSTRATION ONLY.** Every business observation and amount is synthetic. No real-market decision is supported.','']
    def heading(title): out.extend(['## '+title,''])
    def table(headers,rows):
        out.append('| '+' | '.join(headers)+' |'); out.append('| '+' | '.join(['---']*len(headers))+' |')
        def executive_value(v):
            # Whole points are presentation only. Labels/gates are derived from unrounded inputs.
            import re
            return re.sub(r'\b(\d{1,3})\.(\d{2})\b',lambda m:f'{float(m.group(0)):.0f}',str(v))
        rounded={i for i,h in enumerate(headers) if any(word in h for word in ('Confidence','Score','Merit','Pressure'))}
        out.extend('| '+' | '.join(md(executive_value(v) if i in rounded else v) for i,v in enumerate(row))+' |' for row in rows); out.append('')
    heading('Executive Snapshot')
    if decisions:
        r=decisions[0]
        out.extend([f"**{md(r['decision'])}** · {md(r['status'])} · Confidence {float(r['confidence_score']):.0f}/100.",
                    f"Commitment cap: {r['currency']} {float(r['budget_cap']):,.0f}. {md(r['rationale'])}",''])
    else: out+=['No recommendation recorded. Decision remains unavailable.','']
    heading('Top 5 Findings')
    table(['Claim / label','Finding','Confidence / freshness','Impact / action'],[(r['claim_id']+' / '+r['label'],r['finding'],r['confidence_score']+' '+r['confidence_level']+' / '+r['freshness_status']+' / '+r['claim_limit'],r['business_impact']+'; '+r['recommended_action']) for r in sorted(claims,key=lambda r:(float(r['priority']),r['claim_id']))[:5]])
    heading('Top 3 Opportunities')
    table(['ID / opportunity','Merit / adjusted','Confidence','Basis / category / gate','Next test'],[(r['opportunity_id']+' '+r['title'],r['merit_score']+' / '+r['opportunity_score'],r['confidence_score'],r['input_basis_status']+' / '+r['action_category']+' / '+r['decision_gate'],r['next_validation_step']) for r in opportunities[:3]])
    heading('Top 3 Risks')
    table(['ID / risk','Score / class','Confidence','Owner','Trigger / mitigation'],[(r['risk_id']+' '+r['title'],r['risk_score']+' '+r['classification'],r['confidence_score'],r['owner'],r['trigger']+'; '+r['mitigation']) for r in risks[:3]])
    heading('Market Attractiveness')
    table(['Market / scope','Score / rating','Confidence','Drivers','Risks / posture'],[(r['market']+'; '+r['scope'],r['market_attractiveness_score']+' '+r['rating'],r['confidence_score'],r['key_drivers'],r['key_risks']+'; '+r['recommended_posture']) for r in data['02_market/market_assessment.csv']])
    heading('Competitive Pressure')
    table(['Competitor','Pressure','Confidence','Strength / weakness'],[(r['company'],r['competitor_pressure_score'],r['confidence_score'],r['strengths']+' / '+r['weaknesses']) for r in sorted(data['03_competitors/competitor_database.csv'],key=lambda r:-float(r['competitor_pressure_score']))])
    heading('Customer Signals')
    table(['Segment','Job','Confidence','Sampling / price limit'],[(r['name'],r['jobs_to_be_done'],r['confidence_score'],r['population_limit']+'; price sensitivity: '+r['price_sensitivity']) for r in data['04_customers/customer_segments_template.csv']])
    heading('Strategic Recommendation')
    for r in decisions:
        out.extend([f"**{r['decision_id']} — {r['decision']} ({r['status']})**. {md(r['rationale'])}",
                    f"Upside: {md(r['expected_upside'])}. Major risk: {md(r['major_risk'])}.",
                    f"Material claims: {md(r['claim_ids'])}. Next test: {md(r['next_validation_step'])}.",''])
    heading('Confidence Level')
    out+=['Confidence is the weakest material claim support, with conflicts retained. It is a prioritization index, not a probability. Synthetic support never establishes real-world confidence. Executive indices display whole points; stored CSV values and unrounded category/gate logic remain authoritative.','']
    heading('Immediate Next Actions')
    table(['Action','Owner','Metric','Dependency','Status'],[(r['action'],r['owner'],r['success_metric'],r['dependency'],r['status']) for r in data['07_strategy/action_plan.csv'] if r['phase']=='Days 1–30'])
    heading('Decision Required')
    out.extend(md(r['decision_required']) for r in decisions)
    if not decisions: out.append('Define the decision, then capture supporting evidence.')
    out+=['','No proposed recommendation is promoted to approved by this generator.','']
    heading('Evidence Trail and Counterevidence')
    table(['Claim','Relation','Evidence / source','Locator','Publication / access','Archive'],[(m['claim_id'],m['relationship'],m['evidence_id']+' / '+evidence[m['evidence_id']]['source_id'],evidence[m['evidence_id']]['locator'],evidence[m['evidence_id']]['publication_date']+' / '+evidence[m['evidence_id']]['access_date'],sources[evidence[m['evidence_id']]['source_id']]['archive_reference']) for m in maps])
    heading('Open Research Gaps')
    table(['Claim','Missing evidence','Owner / due'],[(r['claim_id'],r['missing_evidence'],r['owner']+' / '+r['due_date']) for r in data['08_evidence/evidence_gap_register.csv']])
    out+=['This generated summary reports structured records. Complete the reviewed narrative templates for the final report.','']
    return '\n'.join(out)

def main():
    parser=argparse.ArgumentParser(description=__doc__); root_arg(parser)
    parser.add_argument('--output',default='executive_summary.md')
    args=parser.parse_args(); args.root=args.root.resolve()
    try:
        errors=validate(args.root,args.as_of)
        if errors: raise ValueError('\n'.join(errors))
        text=render(args.root,args.as_of)
        output=safe_output(args.root,args.output); output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(text,encoding='utf-8'); print(f'Created {output}')
        return 0
    except (ValueError,OSError,KeyError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr); return 1

if __name__=='__main__': sys.exit(main())

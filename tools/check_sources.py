"""Offline source audit. Findings flag research work, not website verification."""
import argparse
import json
import sys
import csv
from urllib.parse import urlsplit, urlunsplit
from common import root_arg, load_data, freshness, ids

def canonical_url(url):
    p=urlsplit(url)
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip('/'),p.query,''))

def check(root,as_of):
    data=load_data(root); issues=[]; urls={}
    from validate_repository import validate
    validation=validate(root,as_of)
    issues+=['Data integrity: '+e for e in validation]
    cfg=json.loads((root/'config/freshness.json').read_text(encoding='utf-8'))
    for row in data['08_evidence/source_library.csv']:
        sid=row['source_id']; url=row['source_url']
        if not url:
            issues.append(f'{sid}: missing URL')
        else:
            key=canonical_url(url)
            if key in urls: issues.append(f'{sid}: duplicate source URL with {urls[key]}')
            urls[key]=sid
        status,_=freshness(row['publication_date'],row['topic'],cfg,as_of)
        if status in ('Stale','Unknown'): issues.append(f'{sid}: freshness {status}')
        if float(row['reliability_score'])<15: issues.append(f'{sid}: low-reliability source')
        if url.startswith('synthetic://'): issues.append(f'{sid}: synthetic artifact; not external evidence')
    # Never trust saved confidence. Canonical source metadata is authoritative for this audit.
    from calculate_scores import calculate
    sources={r['source_id']:r for r in data['08_evidence/source_library.csv']}
    for ev in data['08_evidence/evidence_register.csv']:
        src=sources.get(ev['source_id'])
        if src:
            for field in ('publication_date','access_date','source_url','source_title','publisher','origin_group','topic'):
                ev[field]=src[field]
            ev['reliability_score']=str(min(float(ev['reliability_score']),float(src['reliability_score'])))
    data=calculate(root,as_of,data)
    maps=data['08_evidence/claim_evidence_map.csv']
    for row in data['08_evidence/claims_register.csv']:
        cid=row['claim_id']
        if not any(m['claim_id']==cid and m['relationship']=='supports' for m in maps):
            issues.append(f'{cid}: claim without supporting evidence')
        if not row['confidence_score'] or float(row['confidence_score'])<60:
            issues.append(f'{cid}: low or uncomputed claim confidence')
        if row['contradiction_flag']=='true' or any(m['claim_id']==cid and m['relationship']=='contradicts' for m in maps):
            issues.append(f'{cid}: unresolved conflicting evidence')
    for row in data['08_evidence/evidence_register.csv']:
        if not row['confidence_score'] or float(row['confidence_score'])<60:
            issues.append(f"{row['evidence_id']}: low or uncomputed evidence confidence")
    return issues

def main():
    parser=argparse.ArgumentParser(description=__doc__); root_arg(parser)
    parser.add_argument('--strict',action='store_true',help='Exit 1 when findings exist')
    args=parser.parse_args(); args.root=args.root.resolve()
    try:
        issues=check(args.root,args.as_of)
        for issue in issues: print('REVIEW: '+issue)
        print(f'Offline audit completed: {len(issues)} finding(s). Reachability and truth not checked.')
        return 1 if args.strict and issues else 0
    except (ValueError,KeyError,OSError,csv.Error,TypeError,UnicodeError):
        print('ERROR: source audit refused malformed or unreadable input; run repository validation.',file=sys.stderr); return 2

if __name__=='__main__': sys.exit(main())

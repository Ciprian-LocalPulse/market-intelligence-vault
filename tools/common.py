"""Shared CSV contracts and scoring primitives; Python standard library only."""
from pathlib import Path
from datetime import date
import csv
import json
import math
import os
import tempfile
import re
import hashlib
import ipaddress
import html
from urllib.parse import urlsplit, parse_qsl

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
MODEL_VERSION = '1.0.1'

def confined(root, value, exists=False):
    """Resolve a canonical relative POSIX path; reject escape, absolute and linked paths."""
    root=Path(root).resolve()
    if not isinstance(value,str) or not value or '\\' in value or ':' in value:
        raise ValueError('Path must be a nonempty relative POSIX path')
    parts=value.split('/')
    if any(p in ('','..','.') for p in parts) or value.startswith('/'):
        raise ValueError('Unsafe relative path')
    target=(root/value).resolve()
    if root not in target.parents:
        raise ValueError('Path escapes repository')
    current=root
    for part in parts:
        current=current/part
        if current.is_symlink() or (hasattr(current,'is_junction') and current.is_junction()):
            raise ValueError('Linked paths are not accepted')
    if exists and not target.is_file():
        raise ValueError('Referenced file is absent')
    return target

def safe_url(url, sample_status):
    if not isinstance(url,str) or any(c.isspace() or ord(c)<32 for c in url):
        raise ValueError('Invalid source URL')
    parsed=urlsplit(url)
    if parsed.username is not None or parsed.password is not None:
        raise ValueError('Credential-bearing URL is prohibited')
    secrets={'token','access_token','api_key','apikey','secret','password','authorization','signature','sig','credential'}
    if any(key.lower() in secrets for key,value in parse_qsl(parsed.query,keep_blank_values=True)):
        raise ValueError('Sensitive query credentials must not be retained')
    if parsed.scheme=='synthetic' and parsed.netloc and sample_status=='FICTIONAL SAMPLE':
        return
    if parsed.scheme not in ('http','https') or not parsed.hostname:
        raise ValueError('Source requires a valid HTTP(S) URL, or a labeled synthetic identifier')
    host=parsed.hostname.lower()
    if sample_status=='LIVE':
        if host in ('localhost','example.com','example.net','example.org') or host.endswith(('.invalid','.test','.localhost','.example')):
            raise ValueError('Reserved or placeholder host is prohibited in LIVE data')
        try:
            if not ipaddress.ip_address(host).is_global:
                raise ValueError('Nonpublic source IP is prohibited')
        except ValueError as exc:
            if 'prohibited' in str(exc): raise
    try: parsed.port
    except ValueError: raise ValueError('Invalid URL port') from None

def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f, strict=True)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError(f'{path}: missing or duplicate CSV headers')
        rows = []
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'{path}: inconsistent row width at line {reader.line_num}')
            rows.append(row)
        return reader.fieldnames, rows

def write_csv(path, fields, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.csv-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction='raise')
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temporary, path)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()

def number(value, low=0, high=100):
    if isinstance(value, bool):
        raise ValueError('Boolean is not a score')
    try:
        n = float(value)
    except (TypeError, ValueError):
        raise ValueError('Missing or nonnumeric input') from None
    if not math.isfinite(n) or not low <= n <= high:
        raise ValueError(f'Input outside finite range {low}–{high}')
    return n

def ids(value):
    if value=='': return []
    if not isinstance(value,str) or not re.fullmatch(r'[A-Z][A-Z0-9-]*(?:\|[A-Z][A-Z0-9-]*)*',value):
        raise ValueError('Reference list requires canonical IDs separated by single pipes')
    result=value.split('|')
    if len(set(result))!=len(result): raise ValueError('Duplicate reference ID')
    return result

def as_date(value):
    if len(value) != 10:
        raise ValueError('Use ISO YYYY-MM-DD')
    return date.fromisoformat(value)

def root_arg(parser):
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--as-of', type=as_date, default=date.today(), help='Fix for reproducible freshness')

def load_contract(root):
    contract=json.loads(confined(root,'config/data_contract.json',True).read_text(encoding='utf-8'))
    if not isinstance(contract,dict) or not contract: raise ValueError('Invalid data contract')
    for path,c in contract.items():
        confined(root,path)
        if not isinstance(c,dict) or not isinstance(c.get('fields'),list) or not c['fields'] or len(set(c['fields']))!=len(c['fields']):
            raise ValueError('Invalid CSV field contract')
        fields=set(c['fields'])
        if not all(isinstance(f,str) and re.fullmatch(r'[a-z][a-z0-9_]*',f) for f in fields): raise ValueError('Invalid field name')
        if c.get('primary') not in fields or not set(c.get('required',[]))<=fields: raise ValueError('Invalid primary/required contract')
        for family in ('references','ranges','enums'):
            if not isinstance(c.get(family),dict) or not set(c[family])<=fields: raise ValueError('Invalid contract '+family)
        for bounds in c['ranges'].values():
            if not isinstance(bounds,list) or len(bounds)!=2: raise ValueError('Invalid range contract')
            lo,hi=[number(n,-1e20,1e20) for n in bounds]
            if lo>hi: raise ValueError('Reversed range contract')
        if not set(c.get('integers',[]))<=set(c['ranges']): raise ValueError('Invalid integer contract')
    for c in contract.values():
        for target in c['references'].values():
            if not isinstance(target,str) or target.count(':')!=1: raise ValueError('Invalid reference contract')
            path,field=target.split(':')
            if path not in contract or field not in contract[path]['fields']: raise ValueError('Unknown reference target')
    return contract

def load_data(root):
    return {path: read_csv(confined(root,path,True))[1] for path in load_contract(root)}

def confidence_band(score):
    score = number(score)
    for threshold, label in [(90,'Very High'),(75,'High'),(60,'Moderate'),(40,'Low')]:
        if score >= threshold:
            return label
    return 'Very Low'

def freshness(pub_date, topic, config, as_of):
    if not pub_date:
        return 'Unknown', 0
    age = (as_of - as_date(pub_date)).days
    if age < 0:
        raise ValueError('Publication date lies after as-of date')
    thresholds = config.get(topic, config['default'])
    current, recent, aging = [thresholds[k] for k in ('current_days','recent_days','aging_days')]
    if not 0 <= current < recent < aging:
        raise ValueError('Freshness thresholds must strictly increase')
    if age <= current:
        return 'Current', 20
    if age <= recent:
        return 'Recent', 15
    if age <= aging:
        return 'Aging', 8
    return 'Stale', 0

def evidence_score(row, model):
    raw = sum(number(row[f['factor']], float(f['input_min']), float(f['input_max'])) for f in model)
    status = row['verification_status']
    if status not in ('verified','unverified','speculation','unsupported'):
        raise ValueError('Unsupported verification status')
    if status == 'unsupported':
        return 0.0, 'G'
    if status == 'speculation':
        return min(raw,19), 'F'
    if status == 'unverified':
        return min(raw,39), 'E'
    score = raw
    if row['direct_or_indirect']=='direct' and number(row['directness_score'],0,20)<20:
        score=min(score,89 if number(row['directness_score'],0,20)>=15 else 59)
    if number(row['relevance_score'],0,15)==0:
        score=0
    elif number(row['relevance_score'],0,15)<=5:
        score=min(score,39)
    if number(row['reliability_score'],0,25)==0:
        score=0
    if number(row['reliability_score'],0,25)<=5:
        score=min(score,39)
    if row['direct_or_indirect'] == 'indirect':
        score = min(score,74)
    if row['freshness_status'] == 'Unknown':
        score = min(score,59)
    if row['freshness_status'] == 'Stale':
        score = min(score,39)
    if (score >= 90 and row['direct_or_indirect']=='direct' and number(row['directness_score'],0,20)==20 and row['freshness_status']=='Current'
            and number(row['reliability_score'],0,25)>=20 and number(row['corroboration_score'],0,20)>=15
            and number(row['relevance_score'],0,15)>=10):
        grade = 'A'
    elif (score >=75 and row['direct_or_indirect']=='direct' and number(row['directness_score'],0,20)>=15 and row['freshness_status'] in ('Current','Recent')):
        grade = 'B'
    elif score >=60:
        grade = 'C'
    else:
        grade = 'D'
    return score, grade

def weighted(row, model):
    if abs(sum(number(f['weight']) for f in model)-100)>1e-9:
        raise ValueError('Model weights must sum to 100')
    result = 0.0
    for f in model:
        value = number(row[f['factor']],float(f['input_min']),float(f['input_max']))
        lo, hi = float(f['input_min']), float(f['input_max'])
        normalized = (value-lo)/(hi-lo)
        if f['direction']=='inverse':
            normalized = 1-normalized
        elif f['direction']!='positive':
            raise ValueError('Invalid orientation')
        result += number(f['weight'])*normalized
    return result

def opportunity_score(raw, confidence):
    return number(raw)*(0.25+0.75*number(confidence)/100)

def opportunity_category(score):
    for threshold,label in [(85,'PRIORITIZE'),(70,'VALIDATE'),(55,'EXPLORE'),(40,'WATCH')]:
        if score>=threshold:
            return label
    return 'DEPRIORITIZE'

def gate(confidence):
    return 'RESEARCH REQUIRED' if confidence<60 else 'VALIDATION ONLY' if confidence<75 else 'REVIEW FOR COMMITMENT'

def risk_class(score, row):
    if (number(row['impact'],0,5)==5 and number(row['likelihood'],0,5)>=3) or row['override']=='true':
        return 'Critical'
    return 'Critical' if score>=80 else 'High' if score>=60 else 'Moderate' if score>=35 else 'Low'

def safe_output(root, output):
    root = Path(root).resolve()
    p = (root/output).resolve() if not Path(output).is_absolute() else Path(output).resolve()
    if p == root or root not in p.parents:
        raise ValueError('Output must be a new path inside the repository')
    if p.exists():
        raise ValueError(f'Output already exists: {p}; choose a new snapshot path')
    confined(root,p.relative_to(root).as_posix())
    return p

def input_digest(root):
    """Bind sign-off to all declared inputs, models and report files, excluding generated scores."""
    root=Path(root).resolve()
    policy=json.loads(confined(root,'config/delivery_policy.json',True).read_text(encoding='utf-8'))
    paths=set(policy['live_files'])|set(policy['approved_extra_files'])|set(load_contract(root))
    paths|={'VERSION','config/data_contract.json','config/freshness.json','config/scoring_policy.json','config/delivery_policy.json'}
    paths.discard('EXECUTIVE_SUMMARY.md')
    hasher=hashlib.sha256()
    for path in sorted(paths):
        payload=confined(root,path,True).read_bytes()
        hasher.update(path.encode()+b'\0'+hashlib.sha256(payload).digest())
    # Archive hashes in source records bind archival content; the validator independently verifies them.
    return hasher.hexdigest()

def fmt(value):
    return f'{value:.2f}'

def md(value):
    text=html.escape(str(value),quote=False).replace('|','\\|').replace('\n',' ').replace('\r',' ')
    for char in ('[',']','`','*','_'):
        text=text.replace(char,'\\'+char)
    return text

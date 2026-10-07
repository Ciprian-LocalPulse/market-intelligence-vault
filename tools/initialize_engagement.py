"""Create a separate engagement with blank business records; preserve the foundation release."""
import argparse,json,shutil,sys
from common import root_arg,safe_output,confined,load_contract,write_csv

def initialize(root,output):
    dest=safe_output(root,output)
    if '/' in output or '\\' in output:raise ValueError('Use one new engagement directory name')
    if not output.startswith('engagement_'):raise ValueError('Name must start with engagement_')
    files=json.loads(confined(root,'config/required_files.json',True).read_text(encoding='utf-8'))
    dest.mkdir()
    try:
        for path in files:
            source=confined(root,path,True);target=confined(dest,path)
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        contract=load_contract(dest)
        for path,c in contract.items():
            if 'sample_status' in c['fields']:write_csv(dest/path,c['fields'],[])
        (dest/'EXECUTIVE_SUMMARY.md').write_text('# Executive summary\n\nNo engagement research or recommendation exists yet.\n',encoding='utf-8')
        signoff=json.loads((dest/'config/live_signoff.json').read_text(encoding='utf-8'))
        signoff.update(status='DRAFT',input_digest='',approved_decision_ids=[])
        (dest/'config/live_signoff.json').write_text(json.dumps(signoff,indent=2)+'\n',encoding='utf-8')
    except Exception:
        if dest.resolve().parent==root.resolve():shutil.rmtree(dest)
        raise
    return dest

def main():
    p=argparse.ArgumentParser(description=__doc__);root_arg(p);p.add_argument('--output',required=True)
    args=p.parse_args()
    try:print('Created '+str(initialize(args.root.resolve(),args.output)));return 0
    except (ValueError,OSError,KeyError,TypeError):print('ERROR: initialization refused invalid input or existing path',file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())

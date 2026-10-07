"""Verify exact file inventory and SHA-256 coverage, not source authenticity."""
from pathlib import Path
import argparse,hashlib,json,re,sys
from common import confined

def verify(folder):
    folder=Path(folder).resolve();errors=[]
    try:
        manifest=json.loads(confined(folder,'PACKAGE_MANIFEST.json',True).read_text(encoding='utf-8'))
        actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
        declared=manifest['files']
        if not isinstance(declared,list) or len(set(declared))!=len(declared) or actual!=set(declared):errors.append('Manifest inventory mismatch')
        hashes={}
        for line in confined(folder,'CHECKSUMS.sha256',True).read_text(encoding='utf-8').splitlines():
            digest,path=line.split('  ',1);p=confined(folder,path,True)
            if path in hashes or not re.fullmatch(r'[a-f0-9]{64}',digest):errors.append('Invalid or duplicate hash entry')
            hashes[path]=digest
            if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:errors.append('Checksum mismatch: '+path)
        if set(hashes)!=(actual-{'CHECKSUMS.sha256'}):errors.append('Checksum coverage mismatch')
        if any(p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()) for p in folder.rglob('*')):errors.append('Linked path in package')
    except (OSError,ValueError,KeyError,TypeError,UnicodeError):errors.append('Malformed or unsafe package metadata')
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);args=p.parse_args()
    errors=verify(args.folder)
    for error in errors:print('ERROR: '+error)
    print('Package integrity '+('FAILED' if errors else 'PASSED'))
    return int(bool(errors))
if __name__=='__main__':sys.exit(main())

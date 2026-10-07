"""Serve only explicit dashboard assets on 127.0.0.1. No source fetching or telemetry."""
import argparse,hashlib,json,mimetypes,sys,webbrowser
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlsplit,unquote

DASH=Path(__file__).resolve().parent
STATIC={'index.html','assets/css/dashboard.css','assets/icons/vault.svg'}|{'assets/js/'+f+'.js' for f in ('app','data-loader','charts','filters','tables','evidence','utils')}
DATA={'data/'+f+'.json' for f in ('snapshot','executive','market','opportunities','risks','competitors','customers','evidence','sources','contradictions','assumptions','research-gaps','action-plan')}

def verify_snapshot(dash):
    folder=dash/'data'
    if folder.is_symlink() or (hasattr(folder,'is_junction') and folder.is_junction()):raise ValueError('Linked snapshot refused')
    manifest=json.loads((folder/'snapshot.json').read_text(encoding='utf-8'))
    expected={p[5:] for p in DATA}-{'snapshot.json'}
    if set(manifest['files'])!=expected or {p.name for p in folder.iterdir()}!=expected|{'snapshot.json'}:raise ValueError('Snapshot inventory mismatch')
    for name,digest in manifest['files'].items():
        p=folder/name
        if p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise ValueError('Snapshot integrity failure')
        record=json.loads(p.read_text(encoding='utf-8'))
        if record['meta']!=manifest['meta']:raise ValueError('Mixed snapshot metadata')
    return manifest

def handler_for(dash,port,guard=None):
    dash=dash.resolve()
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.headers.get('Host') not in (f'127.0.0.1:{port}',f'localhost:{port}'):self.send_error(403);return
            path=unquote(urlsplit(self.path).path).lstrip('/') or 'index.html'
            if path not in STATIC|DATA:self.send_error(404);return
            if path in DATA and guard is not None and not guard():self.send_error(409,'Repository changed; stop and relaunch after review');return
            target=dash/path
            # Check every ancestor and resolve before reading. No directory listings or repository mounts.
            chain=[target]+list(target.parents)[:len(target.relative_to(dash).parts)-1]
            if any(p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()) for p in chain) or dash not in target.resolve().parents or not target.is_file():self.send_error(404);return
            content=target.read_bytes();self.send_response(200)
            self.send_header('Content-Type',(mimetypes.guess_type(path)[0] or 'application/octet-stream')+'; charset=utf-8')
            self.send_header('Content-Length',str(len(content)));self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer')
            self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
            self.end_headers();self.wfile.write(content)
        def log_message(self,*args):pass
    return Handler

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=8765);p.add_argument('--snapshot-only',action='store_true',help='Serve a previously exported snapshot; never claim current repository approval');p.add_argument('--open',action='store_true');a=p.parse_args()
    if not 1024<=a.port<=65535:p.error('Use port 1024–65535')
    guard=None
    try:
        if not a.snapshot_only:
            root=DASH.parent;sys.path.insert(0,str(root/'tools'))
            from export_dashboard_data import export,snapshot_date
            from common import input_digest,load_data,confined
            export(root,snapshot_date(root),refresh=True)
            baseline=input_digest(root)
            archives={r['archive_reference']:r['archive_sha256'] for r in load_data(root)['08_evidence/source_library.csv']}
            def guard():
                try:return input_digest(root)==baseline and all(hashlib.sha256(confined(root,path,True).read_bytes()).hexdigest()==digest for path,digest in archives.items())
                except (ValueError,OSError,KeyError):return False
        verify_snapshot(DASH)
        server=ThreadingHTTPServer(('127.0.0.1',a.port),handler_for(DASH,a.port,guard))
        url=f'http://127.0.0.1:{a.port}/';print('Dashboard: '+url+'\nLocal snapshot only. Ctrl+C stops the server.',flush=True)
        if a.open:webbrowser.open(url)
        try:server.serve_forever()
        except KeyboardInterrupt:pass
        finally:server.server_close()
        return 0
    except (ValueError,OSError,KeyError,TypeError):print('ERROR: invalid snapshot, failed export, or unavailable local port. No server started.',file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())

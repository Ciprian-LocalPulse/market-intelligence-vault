export const FILES=['executive','market','opportunities','risks','competitors','customers','evidence','sources','contradictions','assumptions','research-gaps','action-plan'];
const digest=async bytes=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(v=>v.toString(16).padStart(2,'0')).join('');
export async function loadData(){
 const response=await fetch('data/snapshot.json',{cache:'no-store'});if(!response.ok)throw Error('Snapshot unavailable. Relaunch after repository validation.');const manifest=await response.json();
 if(manifest.meta?.contract_version!=='1.1.0'||JSON.stringify(Object.keys(manifest.files).sort())!==JSON.stringify(FILES.map(f=>f+'.json').sort()))throw Error('Dashboard data contract or inventory mismatch.');
 const output={meta:manifest.meta};
 await Promise.all(FILES.map(async name=>{const r=await fetch(`data/${name}.json`,{cache:'no-store'});if(!r.ok)throw Error('Snapshot incomplete or repository changed. Relaunch after review.');const bytes=await r.arrayBuffer();if(await digest(bytes)!==manifest.files[name+'.json'])throw Error('Snapshot checksum mismatch.');const obj=JSON.parse(new TextDecoder().decode(bytes));if(JSON.stringify(obj.meta)!==JSON.stringify(manifest.meta))throw Error('Mixed snapshot refused.');output[name]=obj.data;}));
 if(output.meta.mode==='FICTIONAL DEMONSTRATION'&&output.meta.demo_label!=='FICTIONAL DEMONSTRATION DATA')throw Error('Demo labeling absent.');
 if(!['LIVE','FICTIONAL DEMONSTRATION','NOT YET RESEARCHED'].includes(output.meta.mode))throw Error('Invalid data mode.');return output;
}

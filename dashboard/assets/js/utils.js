export const missing=v=>v===null||v===undefined||v==='';
export const whole=v=>missing(v)?'No data available':Number.isFinite(Number(v))?String(Math.round(Number(v))):'No data available';
export const band=v=>missing(v)?'Not yet researched':v>=90?'Very High':v>=75?'High':v>=60?'Moderate':v>=40?'Low':'Very Low';
export const text=v=>missing(v)?'No data available':Array.isArray(v)?(v.length?v.join(' · '):'No data available'):String(v);
export const esc=v=>text(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const human=v=>String(v).replaceAll('_',' ').replace(/\b\w/g,c=>c.toUpperCase());
export const closed=r=>['CLOSED','VALIDATED','RESOLVED','COMPLETE','RETIRED','CANCELLED'].includes(r.status);
export function pill(value){return `<span class="pill">${esc(value)}</span>`;}
export function confidence(value){return missing(value)?'Not yet researched':`${whole(value)} · ${band(value)}`;}
export function model(value,category){return missing(value)?'No data available':`${whole(value)} · ${text(category)}`;}
export function approval(meta){const a=meta.approval;const today=new Date().toISOString().slice(0,10);return a?.status==='APPROVED'&&meta.mode==='LIVE'&&a.review_date===today?a:{status:'ACTION NOT APPROVED',reasons:[...(a?.reasons||[]),...(a?.status==='APPROVED'?['Snapshot approval is historical. Current repository review required.']:[])]};}
export function fields(obj,pairs){return `<dl class="fields">${pairs.map(([label,key])=>`<div><dt>${esc(label)}</dt><dd>${esc(typeof key==='function'?key(obj):obj[key])}</dd></div>`).join('')}</dl>`;}
export const empty=message=>`<div class="empty">${esc(message||'No data available · Not yet researched')}</div>`;
export function scoredetail(obj){return `<details><summary>Exact stored arithmetic · derived scores</summary>${fields(obj,Object.keys(obj).filter(k=>/score|multiplier/.test(k)).map(k=>[human(k),k]))}<p class="note">Stored decimals support reconciliation, not measurement precision.</p></details>`;}

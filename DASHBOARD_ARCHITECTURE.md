# Dashboard architecture — 1.1.0

## Boundary and data flow

Canonical contracted CSVs + model/policy JSON → existing validator → reconciliation → explicit field
projection → 12 normalized JSON files + snapshot manifest → loopback allowlisted server → browser integrity
check → read-only views. Repository inputs are never edited by dashboard export or interaction.

Python standard library owns export, validation, score reconciliation and the server. Native browser
ES modules own presentation, sorting, filtering, accessible detail dialogs and printing. No build process,
third-party runtime library, tracking, external fonts, CDN or external network fetch is required.

`tools/export_dashboard_data.py` owns the export. `dashboard/launch_dashboard.py` refreshes it and
serves a fixed path set; it never serves the repository or lists directories. `data-loader.js` rejects
missing files, bad hashes, unsupported contracts and mixed metadata before rendering any intelligence.
`app.js` owns the 14 routes; `utils.js`, `filters.js`, `tables.js`, `charts.js` and `evidence.js` separate
formatting, pure selection, tables, ordinal charts and evidence drilldown.

## Trust-preserving controls

- Existing 1.0.1 CSV contracts, schemas, factor bases, model arithmetic and live gates remain intact.
- Populated derived values must reconcile. Optional unavailable fields remain null; required missing values fail.
- All records must have one mode; LIVE metadata must be explicitly configured. Known fictional markers fail LIVE export.
- Approval uses `check_live` without changing its rules. Historical review dates and fictional data cannot display live APPROVED.
- Export text is escaped in the browser; citations are text, not automatically navigated URLs. Credential URLs in any exported string are refused.
- Archive reference, archival bytes and archive SHA are not included in dashboard JSON. Integrity status derives from validation.
- Exports stage atomically with checked names and exact inventory; unknown files prevent overwrite.
- Server checks Host, binds 127.0.0.1, uses no-store, nosniff and restrictive CSP. Linked paths and private routes are refused.
- Full-repository serving refuses data requests after digest or archive changes. Already-loaded pages remain explicitly dated snapshots; this is not real-time monitoring.
- Standalone snapshots verify hashes only. Source and signer authentication, concurrent-edit security and access control remain outside the product.

## Presentation and sensitivity

Eight overview cards identify their scope and interpretation. Pressure uses the strongest recorded competitor,
not an invented market average. Confidence uses the selected recommendation's weakest material support.
Registered counts describe the registers, not research completeness. No zero is imputed for missing data.

Opportunity sensitivity varies one ASSUMPTION/UNKNOWN factor at a time by ±1, clamps only at the model's
0–5 boundaries and holds support fixed. It tests rank and category changes; SENSITIVE DECISION means review
is needed. It never changes an action or creates authority. Joint stress tests and statistical intervals are absent.

## Delivery

Full repository and a separate dashboard-only snapshot ZIP are provided. The snapshot ZIP includes an explicit
static/data allowlist, its launcher and README, never source archives or private notes. Existing client-package
allowlists are unchanged. A populated live snapshot requires its own confidentiality and approval review before sharing.

## 1.2.0 roadmap

Prioritize field-level revision/supersession history and propagation to decisions; normalize duplicated source
editing; add reviewed scenario and joint-factor sensitivity; conduct timed executive/analyst usability studies;
expand browser/platform accessibility tests. Source ingestion, authenticated cloud operations, automated monitoring,
publisher authentication and empirical calibration remain separate roadmap capabilities.

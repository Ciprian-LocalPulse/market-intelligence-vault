# Release verification — Market Intelligence Vault 1.1.0

Interactive Intelligence Release. Executed 2026-10-07 on Windows with Python 3.12.14,
bundled Node.js, Codex in-app Chromium browser and installed Google Chrome PDF rendering.
This is implementation verification by the developing assistant, not independent external assurance.
All Northstar Analytics business observations remain **FICTIONAL DEMONSTRATION DATA**.
The demonstration review date remains 2026-10-06; validation timestamps are separately shown.

## Executed results

| Check | Result |
|---|---|
| Original repository suite | 68 passed, 0 failed |
| Dashboard exporter/security/edge-case suite | 18 passed, 0 failed |
| JavaScript UI logic suite | 11 passed, 0 failed |
| Total automated tests | 97 passed |
| Repository validation with score audit | PASSED, 0 errors |
| Canonical score reconciliation | All populated derived values match preserved calculations |
| Snapshot integrity | 12 JSON payloads plus manifest, matching SHA-256 and metadata |
| Canonical preservation | 50 CSV/schema/policy/archive files compared byte for byte with 1.0.1 |
| Browser navigation | All 14 sections rendered successfully |
| Responsive overview | 1440×1000, 1280×800, 1024×768 and 390×844; 8 cards, no page overflow after repair |
| Print views | Overview and Decision Brief rendered to A4 PDF, 3 pages each; every page labeled fictional |
| HTTP allowlist | 23 allowed static/data routes returned 200 |
| Private/traversal routes | 10 probes returned 404 |
| Invalid Host | 403 |
| Changed-repository guard | Controlled false-guard fixture returned 409 |

Commands executed from the release root:

```text
python -m unittest discover -s tests -v
python -m unittest discover -s dashboard/tests -v
node --test dashboard/tests/test_ui.mjs
python tools/validate_repository.py --as-of 2026-10-06 --audit-scores
python tools/export_dashboard_data.py --as-of 2026-10-06 --refresh
```

Normal validated startup was also executed with `python dashboard/launch_dashboard.py --port 8766`.
Index and snapshot requests returned 200 and the embedded browser rendered the final overview.
Port 8765 timed out on this workstation; port 8766 was verified without changing network protections.

The original suite tests scoring caps, critical downside, stale/unknown sources, archive tamper,
provenance, sign-off expiry, input-bound approval, irreversible recommendations and delivery privacy.
Dashboard tests cover malformed/mixed/unsafe input, typed single vs multiple IDs, null vs zero,
derived-score tamper, missing required data, snapshot integrity, private archive omission,
credential URLs, exact allowlists, empty initialized engagements and sensitivity bounds/category changes.
No canonical ratings were edited to make a demonstration scenario appear more robust.

## Browser and print observations

Combined opportunity category/search filters reduced three records to one. Numeric score sort
worked in both directions. Keyboard Enter opened opportunity detail; Escape closed the native
dialog and restored focus. Uncertain-factor selection reduced sensitivity to two scenarios.
Contradicted-only evidence retained both support and counterevidence (2 of 6 mapped observations).
Claim detail showed CLM-001 support index 59 separately from EV-001 observation index 75 and
EV-006 index 73. Weakest material claims CLM-001 and CLM-004 remain visible. Opportunity detail
shows supporting observations, counterevidence, all associated decision risks, factor provenance,
all tied weakest oriented factors and unrounded-category sensitivity. Customer insight shows
observation count, source tier, integrity status, unauthenticated publisher status and sampling limits.
No console errors were observed during route verification.

Mobile navigation and wide tables use contained horizontal scrolling; the document itself does not
overflow. The demonstration banner remains visible while scrolling and is repeated in dialog titles.
Semantic headings, explicit control labels, sortable headings, keyboard focus and native dialog
behavior were checked. A comprehensive screen-reader/WCAG certification was not performed.

Both final PDFs were rasterized and every page inspected. Navigation and route controls are omitted;
weak claim text, contradiction, action-not-approved warning, whole-point indices and fictional labels
remain. Print columns are independent of responsive screen breakpoints. Native print dialog behavior
could not be confirmed in the embedded browser; the actual print CSS was verified using Chrome PDF
output. Pagination can vary with a browser, paper size, user margins or populated engagement.

## Security and preserved authority

Loopback binding, strict Host checks, confinement, symlink/junction checks, no directory listing,
no-store, nosniff, no-referrer and restrictive CSP were verified in implementation and HTTP probes.
Only explicit dashboard assets and JSON are served. Raw archives, tools, config, source-library CSV,
private repository paths and encoded traversal are inaccessible. The standalone package has an
explicit static/data allowlist. Citation URLs are displayed as escaped text and never fetched.
Credential-bearing URLs are rejected during export, including free-text fields. Archive integrity
is checked before export; loaded snapshots are not a monitoring service. No CDN, remote fonts,
telemetry, scraping, ingestion, cloud authentication or score calibration was added.

The 1.0.1 scoring model, evidence floors/caps, contradiction caps, ordinal risk rules and irreversible
action gates are unchanged. The existing delivery-policy allowlists are unchanged; dashboard
delivery is a separately confined snapshot. Historical live approval does not confer current approval.
Fictional and unresearched modes cannot display live authority. A locally edited manifest or attestation
does not authenticate a publisher or signer. Automated credential checks do not replace professional
review for private notes, personal data, rights, omissions or source identity.

## Final self-audit

| Question | Assessment |
|---|---|
| Usability without false confidence? | Whole indices, explicit bands, fictional banner and unapproved action persist. |
| Recommendation and weakest dependency within five minutes? | Overview/brief expose TEST, CLM-001/004, largest downside and validation step. Designed for this task; no timed executive study was performed. |
| Recommendation trace to claims/evidence? | Material claims and source-quality drilldown retain support and counterevidence. |
| Contradictions visible? | Dedicated monitor, evidence filter and claim/opportunity details. |
| Missing distinguishable from zero? | Null exports and explicit missing labels; zero preserved and tested. |
| Synthetic unmistakable? | Global banner, dialog title, record status and every print page. |
| Approval gates preserved? | Unchanged check_live rules, date-aware presentation, read-only UI. |
| Indices rather than probabilities? | No percent confidence or statistical interval claim; model arithmetic disclosed. |

## Scope and limitations

Static read-only local snapshot; refresh/export is required after canonical edits. A standalone
snapshot cannot inspect the originating repository. Hashes support integrity, not authenticity.
Single-factor ordinal ±1 sensitivity holds confidence fixed and is not a joint stress test, statistical
interval or authority to change decisions. Registered counts do not prove research completeness.
The risk matrix is ordinal triage, not a calibrated probability surface. These checks do not establish
real-market validity, empirical calibration, source identity, signer identity or externally audited security.

Recommended 1.2.0 priorities: timed executive/analyst usability studies and screen-reader testing;
human-reviewed source import with rights/provenance controls; authenticated local review/sign-off;
joint scenario stress testing; longitudinal outcome collection to evaluate index calibration.
External ingestion, authentication and monitoring need a separate design and threat review.

## File inventory relative to 1.0.1

The full source ZIP contains 186 release files plus its package manifest (187 entries).
The standalone dashboard ZIP contains 25 explicitly selected files plus its manifest (26 entries),
including no raw archives or repository tools/config. Both ZIPs passed CRC checks, exact-entry
inventory checks and byte-for-byte payload comparison. Per-file SHA-256 values are inside each ZIP;
external checksums also cover both ZIPs, the two verified PDFs and the dashboard preview.

Historical delivery/engagement output folders and Python caches were excluded from the new source
release. Existing audit and 1.0.1 verification documents remain historical records.

Created files (36):

- `DASHBOARD_ARCHITECTURE.md`
- `DASHBOARD_DATA_CONTRACT.md`
- `RELEASE_NOTES_1.1.0.md`
- `RELEASE_VERIFICATION_1.1.0.md`
- `config/dashboard_config.json`
- `dashboard/README.md`
- `dashboard/assets/css/dashboard.css`
- `dashboard/assets/icons/vault.svg`
- `dashboard/assets/js/app.js`
- `dashboard/assets/js/charts.js`
- `dashboard/assets/js/data-loader.js`
- `dashboard/assets/js/evidence.js`
- `dashboard/assets/js/filters.js`
- `dashboard/assets/js/tables.js`
- `dashboard/assets/js/utils.js`
- `dashboard/data/action-plan.json`
- `dashboard/data/assumptions.json`
- `dashboard/data/competitors.json`
- `dashboard/data/contradictions.json`
- `dashboard/data/customers.json`
- `dashboard/data/evidence.json`
- `dashboard/data/executive.json`
- `dashboard/data/market.json`
- `dashboard/data/opportunities.json`
- `dashboard/data/research-gaps.json`
- `dashboard/data/risks.json`
- `dashboard/data/snapshot.json`
- `dashboard/data/sources.json`
- `dashboard/index.html`
- `dashboard/launch_dashboard.py`
- `dashboard/package.json`
- `dashboard/tests/QA_RESULTS_1.1.0.json`
- `dashboard/tests/TEST_RESULTS_1.1.0.txt`
- `dashboard/tests/test_export.py`
- `dashboard/tests/test_ui.mjs`
- `tools/export_dashboard_data.py`

Changed files (6):

- `CHANGELOG.md`
- `EXECUTIVE_SUMMARY.md`
- `README.md`
- `VERSION`
- `config/required_files.json`
- `tools/generate_summary.py`

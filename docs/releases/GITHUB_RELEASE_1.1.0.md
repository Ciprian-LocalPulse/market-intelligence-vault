# Market Intelligence Vault v1.1.0 — Interactive Intelligence Release

First public GitHub release, published from `main` as `v1.1.0` after release verification.

## Overview and major capabilities

Version 1.1.0 adds a read-only local executive interface to the existing evidence and decision framework.
The hardened scoring model remains 1.0.1. Fourteen sections cover executive decisions, market,
competitors, customers, opportunities, risks, evidence, sources, contradictions, assumptions, research
gaps, the 90-day plan and methodology. Eight overview cards show scoped indices and registered gaps.

## Evidence, opportunity, risk and decision support

Claim drilldowns retain support and counterevidence, source quality, freshness, directness and exact
stored arithmetic. Opportunity details show business merit separately from support, factor provenance,
related risks and bounded single-factor ±1 sensitivity. The risk matrix is ordinal; confidence does
not discount exposure. Decision briefs distinguish proposals, reversible validation and irreversible
commitments. Fictional data cannot display live authority. Sorting/filtering never deletes evidence.

## Security hardening and dashboard delivery

Validated exports contain twelve normalized JSON files plus an integrity manifest. Missing optional
values stay null. Loopback serving uses exact allowlists, Host/confinement checks and restrictive CSP.
No raw archives, remote assets, trackers or ingestion are exposed by the dashboard. Existing live
approval gates, archive checks and reading-package privacy controls are preserved. System fonts,
keyboard interactions, responsive views and A4 print styles are included.

## Documentation and rights

Public preparation adds architecture, data-contract navigation, a substantive whitepaper, contributor
and governance guidance, responsible disclosure, citation metadata, issue/PR forms and CI configuration.
The owner approved an All rights reserved notice for this prepared distribution. Earlier local grants
are preserved historically; this release does not purport to revoke earlier-copy permissions.

## Testing

The public release passed 86 repository tests, 18 dashboard export tests and 11 JavaScript tests
(115 total) locally. PUBLICATION_VERIFICATION.md records scope and limitations. Score/schema
validation passed with zero errors; an exported Git checkout passed archive and snapshot hash
verification. Remote execution is recorded in GitHub Actions. Browser and PDF inspection are
local implementation checks, not external accessibility or security certification.

## Known limitations

No automated ingestion, authenticated service, publisher/signer authentication, real-time monitoring
or empirical calibration. Single-factor sensitivity is not a joint statistical stress test. Hashes
prove integrity only. The supplied study is FICTIONAL DEMONSTRATION DATA and ACTION NOT APPROVED.
The owner-supplied hero is a presentation asset, not research evidence or a dashboard capture.
Source and business validity require professional human review.

## Upgrade notes

Use the full repository for Python commands. Launch `python dashboard/launch_dashboard.py`; if the
default port times out locally, use `--port 8766`. Do not open HTML directly as a file. Refresh export
after reviewed canonical changes; categories use unrounded arithmetic despite whole-point display.
Keep existing schema/model contracts and migrate any 1.0.0 consumers according to the preserved
1.0.1 notes. A public preparation commit changes documentation and rights metadata, not model math.

## Author

Ciprian Ștefan Pleșca — Independent Software Researcher & Product Creator.
Copyright © 2026 Ciprian Ștefan Pleșca. All rights reserved.

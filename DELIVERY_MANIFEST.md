# Delivery manifest

**Market Intelligence Vault — Quality Hardening Release 1.0.1**

| Component | Included content | Location |
| --- | --- | --- |
| Executive Decision Brief | One-page decision structure, board summary and priorities | `01_executive/` |
| Market Intelligence Report | Overview, sizing, growth, maturity, drivers and barriers | `02_market/` |
| Competitor Database | Profiles, comparable criteria, pricing, positioning and change log | `03_competitors/` |
| Customer Intelligence | Segments, jobs, pains, buying/switching triggers and objections | `04_customers/` |
| Opportunity Map | Scored hypotheses, formal gap detection and prioritization | `05_opportunities/` |
| Risk Register | Exposure, mitigation, assumptions, unknowns and dependencies | `06_risks/` |
| Strategic Recommendations | Decision options, scenario planning and action plan | `07_strategy/` |
| Source Library | Sources, evidence, claims, maps, contradictions, gaps and debt | `08_evidence/` |
| Evidence Framework | Model definitions, confidence grades and scoring guides | `09_scores/` and root guides |
| Monitoring Views | Derived executive, opportunity, competitor and risk CSV views | `10_dashboards/` |
| Delivery Guidance | Assembly, readout, quality review and archive structure | `11_delivery/` |
| Demonstration | Fully synthetic Northstar Analytics case and archived synthetic sources | `12_examples/` |
| Controls | Python tools, JSON schemas, config and automated tests | `tools/`, `schemas/`, `config/`, `tests/` |

The full repository includes all components. Generated foundation delivery includes the analytical
areas, guides, models, schemas/config, a generated executive summary, package manifest and hashes.
Developer tools/tests remain in the full repository ZIP. Live packages exclude `12_examples/` and
refuse synthetic structured rows. Templates must be completed for a live engagement.

Approval record: [scope] · [as-of date] · [QA score] · [reviewer] · [decision authority] · [open limits].
The shipped foundation has no live recommendation approval and no independent market validation.

## Quality Hardening Release 1.0.1

The full repository includes executable tools, tests and setup guides. The reading package uses
explicit allowlists and a reader README; it excludes software setup guides and development tests.
Its PACKAGE_MANIFEST.json lists all delivered files, including itself and CHECKSUMS.sha256.
Checksums cover every delivered file except the checksum file. A live package adds APPROVAL_RECORD.json
and excludes demonstrations, internal audit notes and source archives unless explicitly approved.
CSV viewing copies may contain leading apostrophes to neutralize formula text. Canonical CSVs remain
in the controlled repository and must not be replaced by viewing exports.

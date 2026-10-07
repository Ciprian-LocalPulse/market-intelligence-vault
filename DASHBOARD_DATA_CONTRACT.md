# Dashboard data contract — 1.1.0

All twelve JSON files contain `{meta, data}`. UTF-8 JSON, finite numeric values, true JSON booleans,
canonical IDs and arrays for pipe-delimited references. Unavailable optional values are null; missing
required canonical inputs reject export. No imputed observations, scores, source authentication or approvals.

## Common metadata

contract_version 1.1.0; repository_version 1.1.0; model_version 1.0.1; engagement_name from explicit
configuration; mode LIVE / FICTIONAL DEMONSTRATION / NOT YET RESEARCHED; demo_label exactly
FICTIONAL DEMONSTRATION DATA for the fictional mode; as_of_date from the reviewed scoring snapshot;
validated_at in UTC; snapshot_id digest of normalized analytical output; input_digest bound to canonical
inputs and reviewed narratives; approval status, reasons, review_date and scope; score_reconciliation explanation.

`snapshot.json` adds exact filename-to-SHA256 coverage of the twelve JSON files and the same meta.
All files must share identical metadata. Hash integrity proves bytes only, not truth or publisher identity.
The snapshot ID identifies normalized output, not an authenticated approval signature.

## File topology

| File | Data fields and provenance |
| --- | --- |
| executive.json | decisions and options from recommendations/decision_matrix; unknowns, dependencies, coverage counts; model definitions and factor bases |
| market.json | market assessment and market signals |
| opportunities.json | canonical opportunity records plus separately derived single-factor sensitivity scenarios |
| risks.json | risk register, hardened structural_zero, classification and review_required |
| competitors.json | competitor records, pricing comparison limits and change log; disclosed pressure bands |
| customers.json | segments, pains, triggers, objections and customer evidence insights |
| evidence.json | claims, observations and all support/contradiction/context mappings |
| sources.json | explicit public citation metadata, computed freshness and validated integrity status; no archive location or bytes |
| contradictions.json | all flagged or mapped unresolved conflicts, both evidence lists, map interpretation and follow-up; most_likely_interpretation remains null if absent |
| assumptions.json | canonical assumptions with critical flags and decision IDs |
| research-gaps.json | evidence gaps, research questions and research debt, preserving absent decision/priority data |
| action-plan.json | canonical 90-day plan, owners, metrics, dependencies, priority, risk and status |

## Fields, joins and categories

Canonical field names and primary IDs are preserved; `DATA_DICTIONARY.md` and `config/data_contract.json`
remain authoritative for their meanings. Numeric fields are converted using declared ranges. Reference fields
become arrays without inventing relationships. `confidence_category` derives only from a present support index.

Source and observation exports use explicit field lists. Archive path/hash fields are omitted. All other exported
entity types project only fields declared in their canonical CSV contracts; no directory discovery or arbitrary
extra files are used. Claim label is retained. Decision status is renamed `recorded_status` and separate `approval`
is calculated through unchanged live gates; a recorded APPROVED label is not sufficient.

Market, opportunity and risk categories remain calculator-owned. Pressure presentation bands are Very strong ≥80,
Strong ≥60, Moderate ≥40, Limited below40; this is a disclosed interface interpretation of the existing pressure
index. Model inputs remain 0–5 ordinal ratings. Source reliability is 0–25, not a fabricated source confidence index.
Confidence bands remain Very High ≥90, High ≥75, Moderate ≥60, Low ≥40, Very Low below40.

## Sensitivity object

status, decision_status, baseline_rank, scenarios and method. Each scenario records factor, delta, tested_value,
score, category, rank and changed flags. Only uncertain nine-factor business inputs are tested, one at a time;
support stays fixed. With missing support, status is NOT TESTABLE — MISSING SUPPORT and scenarios are empty.
No recommendation is automatically recalculated; category/rank changes flag review. Exact scenario arithmetic
remains available; executive indices use whole points. This is not a confidence interval or probability model.

## Failure behavior and confidentiality

Invalid CSVs/contracts, bad scores, invalid ranges, unsafe paths, known demo content in LIVE mode, unsafe
URLs in any exported string, mixed sample status or concurrent input changes reject export. The previous valid
snapshot is not silently shown as fresh. The launcher refuses to start when refresh fails. The browser rejects
unverified/mixed files and shows DATA UNAVAILABLE — NO FALLBACK.
Human review is still needed for secrets that are not credential-bearing URLs, sensitive business prose and PII.
Only share explicitly reviewed snapshots. Dates, approvals and analytical inputs need refresh after changes.

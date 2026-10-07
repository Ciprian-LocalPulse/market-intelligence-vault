# Release notes — 1.0.1

**Market Intelligence Vault · Quality Hardening Release · 2026-10-06**

## Changes that affect trust

- Explicit file allowlisting replaces broad directory copying. Unlisted private notes do not export.
- Live delivery requires named sign-off tied to inputs, decision coverage, manual attestations,
  current Critical-risk acceptance and commitment-specific evidence gates.
- Contracts, archives and outputs are confined; archive hashes detect modifications. LIVE rejects
  reserved source hosts, retained credentials and known fictional archive markers.
- FACT support, directness, semantic mapping duplicates, reference syntax and integer types are enforced.
- Shipped JSON schemas validate converted records and remain aligned with CSV field/range/enum contracts.
- Source audits recompute support and return controlled errors on malformed CSVs.
- Refresh writes use recovery journals and exception rollback. Incomplete refresh blocks delivery.
- Client CSV viewing copies neutralize formula-leading text. Full package inventory/hash coverage is verified.

## Model changes

Model version is 1.0.1. Evidence grades require the stated directness; reliability/relevance failure
cannot be overcome by recent dates. Claim types and unresolved conflicts cap confidence. Corroboration
derives from eligible independent supporting origins. Opportunity merit excludes additive confidence
and adjusts once using 0.25+0.75×support. Zero likelihood or impact yields zero risk exposure absent
an upward override. Decision weights now live in a versioned CSV. All business factors have basis records.

Northstar claim confidence becomes 59/72/66/59/78. Opportunities become 52.48/47.40/33.53.
DEC-001 remains a PROPOSED research TEST, now confidence 59 Low. Do not compare these indices with
archived 1.0.0 rankings without recomputing both under the same model.

## Compatibility and migration

Old files/IDs are preserved where practical; new columns and factor_assessments require revised exact
CSV contracts. raw_score is retained as a deprecated legacy view. Consumers enforcing 1.0.0 headers
must migrate. The original 1.0.0 directory remains the baseline. The initializer creates blank
engagement records rather than silently relabeling examples. No live project data was migrated.

## Remaining limits

No empirical calibration, signer authentication, encryption configuration, full JSON Schema engine,
source fetcher, automatic revision history or graphical dashboard. Release tests use synthetic goldens;
live engagements require their own content and approval reviews. Professional delivery readiness is
limited to the framework/demo; no real-market intelligence or capital decision is approved.

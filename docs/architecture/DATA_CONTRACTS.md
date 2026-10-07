# Data contract guide

[config/data_contract.json](../../config/data_contract.json) owns exact CSV headers, required values,
ranges, enums, primary keys and references. [DATA_DICTIONARY.md](../../DATA_DICTIONARY.md) explains
all fields. Six canonical JSON schemas validate the shipped object subset; this is not a general
JSON Schema implementation. Use stable IDs, ISO dates, numeric points and explicit sample status.
Optional empty CSV scalars project to JSON null; missing required values fail.

| Object | Canonical contract and important relationships |
|---|---|
| Source | [source schema](../../schemas/source_schema.json): source_id, citation, publisher, dates, topic, tier, reliability ceiling, origin group and archived locator/hash |
| Evidence | [evidence schema](../../schemas/evidence_schema.json): evidence_id, source_id, bound claim_id, scoped observation, status/directness and calculator-owned strength/grade/freshness |
| Claim | CSV contract for [claims_register.csv](../../08_evidence/claims_register.csv); type, scope, support references, derived confidence and conflict flag. No separate claim JSON schema is shipped. |
| Relationship | [claim_evidence_map.csv](../../08_evidence/claim_evidence_map.csv): support, contradicts or context; materiality and interpretation |
| Opportunity | [opportunity schema](../../schemas/opportunity_schema.json): claim/evidence and segment joins, nine business factors, merit, adjusted score and review gate |
| Risk | [risk schema](../../schemas/risk_schema.json): ordinal exposure factors, owner, trigger, mitigation, critical override and structural-zero review |
| Competitor | [competitor schema](../../schemas/competitor_schema.json): comparable scope, pressure factors, pricing period and supporting IDs |
| Customer segment | [segment schema](../../schemas/customer_segment_schema.json): jobs, pains, buying barriers, population limits and claim/evidence IDs |

The source and evidence registries repeat citation fields under a consistency check. They are not
independently editable truths. Current evidence binds one claim even though the map records relationship
semantics; many-claim lifecycle support is planned. Unresolved conflict caps claim confidence rather
than deleting either observation.

Dashboard export is specified in [DASHBOARD_DATA_CONTRACT.md](../../DASHBOARD_DATA_CONTRACT.md).
Twelve `{meta,data}` files share metadata and are covered by snapshot.json. Source archive paths,
hashes and bytes are omitted from the dashboard; integrity status is included. Single IDs remain
strings, plural references arrays, booleans true/false, finite numbers numeric and missing scalars null.
The dashboard exposes read-only projections, not a mutation API or an external ingestion endpoint.

# Data dictionary

## Conventions

UTF-8 CSV, comma separator, one header row, quoted cells where needed. IDs are strings.
Dates are ISO `YYYY-MM-DD`. Monetary values are numeric with a separate currency and period.
Percentages in prose are percentages; CSV scores are points, not percentage probabilities.
Blank optional fields mean unavailable; blank required inputs fail validation. Pipe-delimited
references contain unique IDs without spaces. JSON uses null for optional unavailable scalars.
`sample_status` is FICTIONAL SAMPLE, LIVE or TEMPLATE. Never change fictional content to LIVE.

## Entities and joins

| Object | Primary key | Joins | Owner |
| --- | --- | --- | --- |
| Source | source_id | origin_group is an independence group | Research lead |
| Evidence | evidence_id | source_id; claim_id | Research lead |
| Claim | claim_id | claim map; evidence_ids are support references | Analysis lead |
| Map | map_id | claim_id; evidence_id; relationship | Analysis lead |
| Competitor | competitor_id | segment; evidence_ids; claim_ids | Competitive intelligence lead |
| Segment | segment_id | evidence_ids; claim_ids | Customer research lead |
| Opportunity | opportunity_id | segment_id; evidence_ids; claim_ids | Product lead |
| Risk | risk_id | evidence_ids; claim_ids | Risk owner |
| Recommendation | decision_id | claim_ids; opportunity_ids; risk_ids | Strategy lead |
| Action | action_id | decision_id; evidence_ids | Named action owner |

## Field families

`finding` is a scoped conclusion; `supporting_quote_or_summary` is the extracted observation.
`label`/`evidence_type` classify the statement, not its certainty. `confidence_score` is derived
support strength. `contradiction_flag` records an unresolved interpretation conflict, not a
judgment that the underlying source is false. `verification_status` is verified, unverified,
speculation or unsupported. `direct_or_indirect` says whether the observation matches the claim.
`origin_group` identifies the originating publisher or dataset, including reprints.

`confidence_level`, `evidence_grade`, `freshness_score`, `freshness_status`, business scores,
ratings, gates and dashboard views are calculator-owned. Confidence factors other than freshness
are analyst inputs; corroboration is capped by the independent supporting-origin count.
Market attractiveness is entrant appeal. Competitor pressure is stronger competitive force.
Opportunity burden factors and risk mitigation readiness are inverse-oriented.

## Complete machine-readable contract

[config/data_contract.json](config/data_contract.json) specifies every CSV, exact column order,
primary key, required cells, reference targets, numeric ranges and allowed values. Model files
define factors, weights, orientation and anchors. JSON schemas define the six principal objects.
The validator applies CSV contracts, semantic controls and the closed shipped JSON Schema subset using the standard library; it is not a general-purpose JSON Schema implementation. Convert optional blanks to null and typed numbers before validating
CSV-derived JSON with a full schema engine in an external integration.


## Model and delivery additions

archive_sha256 owns snapshot integrity. factor_assessments stores rating bases. Claim freshness and type/conflict limits are derived. merit_score excludes confidence; raw_score is deprecated. structural_zero describes an explicitly rated impossible/immaterial risk, not missing data. decision_ids/critical attach uncertainty to commitment gates. Exported viewing CSVs are not canonical analytical inputs.

## Field inventory

### `09_scores/confidence_model.csv`

Primary key: `factor`.

- `factor`: required.
- `weight`: required; range [0, 100].
- `input_min`: required; range [0, 0].
- `input_max`: required; range [0, 100].
- `direction`: required.
- `definition`: required.
- `anchor_0`: required.
- `anchor_mid`: required.
- `anchor_max`: required.

### `09_scores/opportunity_scoring_model.csv`

Primary key: `factor`.

- `factor`: required.
- `weight`: required; range [0, 100].
- `input_min`: required; range [0, 0].
- `input_max`: required; range [0, 100].
- `direction`: required.
- `definition`: required.
- `anchor_0`: required.
- `anchor_mid`: required.
- `anchor_max`: required.

### `09_scores/risk_scoring_model.csv`

Primary key: `factor`.

- `factor`: required.
- `weight`: required; range [0, 100].
- `input_min`: required; range [0, 0].
- `input_max`: required; range [0, 100].
- `direction`: required.
- `definition`: required.
- `anchor_0`: required.
- `anchor_mid`: required.
- `anchor_max`: required.

### `09_scores/market_attractiveness_model.csv`

Primary key: `factor`.

- `factor`: required.
- `weight`: required; range [0, 100].
- `input_min`: required; range [0, 0].
- `input_max`: required; range [0, 100].
- `direction`: required.
- `definition`: required.
- `anchor_0`: required.
- `anchor_mid`: required.
- `anchor_max`: required.

### `09_scores/competitor_pressure_model.csv`

Primary key: `factor`.

- `factor`: required.
- `weight`: required; range [0, 100].
- `input_min`: required; range [0, 0].
- `input_max`: required; range [0, 100].
- `direction`: required.
- `definition`: required.
- `anchor_0`: required.
- `anchor_mid`: required.
- `anchor_max`: required.

### `09_scores/gap_scoring_model.csv`

Primary key: `factor`.

- `factor`: required.
- `weight`: required; range [0, 100].
- `input_min`: required; range [0, 0].
- `input_max`: required; range [0, 100].
- `direction`: required.
- `definition`: required.
- `anchor_0`: required.
- `anchor_mid`: required.
- `anchor_max`: required.

### `08_evidence/source_library.csv`

Primary key: `source_id`.

- `sample_status`: required.
- `source_id`: required.
- `source_title`: required.
- `source_url`: required.
- `publisher`: required.
- `publication_date`: optional/derived.
- `access_date`: required.
- `source_type`: required.
- `topic`: required.
- `tier`: required; range [1, 5]; integer.
- `reliability_score`: required; range [0, 25].
- `origin_group`: required.
- `locator`: required.
- `archive_reference`: required.
- `usage_rights`: required.
- `analyst_notes`: required.
- `archive_sha256`: required.

### `08_evidence/claims_register.csv`

Primary key: `claim_id`.

- `sample_status`: required.
- `claim_id`: required.
- `label`: required.
- `finding`: required.
- `business_impact`: required.
- `recommended_action`: required.
- `evidence_ids`: optional/derived; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `confidence_level`: optional/derived.
- `contradiction_flag`: required.
- `owner`: required.
- `decision_status`: required.
- `as_of_date`: required.
- `priority`: required; range [1, 5]; integer.
- `freshness_status`: optional/derived.
- `claim_limit`: optional/derived.

### `08_evidence/evidence_register.csv`

Primary key: `evidence_id`.

- `sample_status`: required.
- `evidence_id`: required.
- `claim_id`: required; references `08_evidence/claims_register.csv:claim_id`.
- `source_id`: required; references `08_evidence/source_library.csv:source_id`.
- `source_title`: required.
- `source_url`: required.
- `publisher`: required.
- `publication_date`: optional/derived.
- `access_date`: required.
- `topic`: required.
- `evidence_type`: required.
- `direct_or_indirect`: required.
- `finding`: required.
- `supporting_quote_or_summary`: required.
- `locator`: required.
- `reliability_score`: required; range [0, 25].
- `freshness_score`: optional/derived; range [0, 20].
- `directness_score`: required; range [0, 20].
- `corroboration_score`: required; range [0, 20].
- `relevance_score`: required; range [0, 15].
- `confidence_score`: optional/derived; range [0, 100].
- `confidence_level`: optional/derived.
- `evidence_grade`: optional/derived.
- `freshness_status`: optional/derived.
- `analyst_notes`: required.
- `contradiction_flag`: required.
- `verification_status`: required.
- `origin_group`: required.

### `08_evidence/claim_evidence_map.csv`

Primary key: `map_id`.

- `sample_status`: required.
- `map_id`: required.
- `claim_id`: required; references `08_evidence/claims_register.csv:claim_id`.
- `evidence_id`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `relationship`: required.
- `materiality`: required.
- `interpretation`: required.

### `05_opportunities/opportunity_database.csv`

Primary key: `opportunity_id`.

- `sample_status`: required.
- `opportunity_id`: required.
- `title`: required.
- `segment_id`: required; references `04_customers/customer_segments_template.csv:segment_id`.
- `gap_category`: required.
- `label`: required.
- `market_demand`: required; range [0, 5].
- `growth_potential`: required; range [0, 5].
- `pain_intensity`: required; range [0, 5].
- `competitive_saturation`: required; range [0, 5].
- `differentiation_potential`: required; range [0, 5].
- `monetization_potential`: required; range [0, 5].
- `implementation_difficulty`: required; range [0, 5].
- `time_to_market`: required; range [0, 5].
- `evidence_confidence`: optional/derived; range [0, 5].
- `strategic_fit`: required; range [0, 5].
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `claim_ids`: required; references `08_evidence/claims_register.csv:claim_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `raw_score`: optional/derived; range [0, 100].
- `opportunity_score`: optional/derived; range [0, 100].
- `action_category`: optional/derived.
- `decision_gate`: optional/derived.
- `business_impact`: required.
- `owner`: required.
- `next_validation_step`: required.
- `status`: required.
- `as_of_date`: required.
- `merit_score`: optional/derived; range [0, 100].
- `confidence_multiplier`: optional/derived; range [0, 1].
- `input_basis_status`: optional/derived.

### `05_opportunities/opportunity_scorecard.csv`

Primary key: `opportunity_id`.

- `sample_status`: required.
- `opportunity_id`: required; references `05_opportunities/opportunity_database.csv:opportunity_id`.
- `raw_score`: required; range [0, 100].
- `confidence_score`: required; range [0, 100].
- `opportunity_score`: required; range [0, 100].
- `action_category`: required.
- `decision_gate`: required.
- `as_of_date`: required.
- `merit_score`: optional/derived; range [0, 100].
- `confidence_multiplier`: optional/derived; range [0, 1].
- `input_basis_status`: optional/derived.

### `06_risks/risk_register.csv`

Primary key: `risk_id`.

- `sample_status`: required.
- `risk_id`: required.
- `title`: required.
- `category`: required.
- `label`: required.
- `horizon_days`: required; range [1, 3650]; integer.
- `likelihood`: required; range [0, 5].
- `impact`: required; range [0, 5].
- `detectability`: required; range [0, 5].
- `velocity`: required; range [0, 5].
- `mitigation_readiness`: required; range [0, 5].
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `claim_ids`: required; references `08_evidence/claims_register.csv:claim_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `risk_score`: optional/derived; range [0, 100].
- `classification`: optional/derived.
- `override`: required.
- `override_reason`: optional/derived.
- `mitigation`: required.
- `trigger`: required.
- `owner`: required.
- `residual_risk`: required.
- `status`: required.
- `as_of_date`: required.
- `structural_zero`: optional/derived.
- `review_required`: optional/derived.

### `03_competitors/competitor_database.csv`

Primary key: `competitor_id`.

- `sample_status`: required.
- `competitor_id`: required.
- `company`: required.
- `website`: required.
- `geography`: required.
- `segment`: required; references `04_customers/customer_segments_template.csv:segment_id`.
- `product`: required.
- `pricing`: required; range [0, 100000000].
- `pricing_currency`: required.
- `pricing_period`: required.
- `positioning`: required.
- `target_customer`: required.
- `funding`: required.
- `partnerships`: required.
- `strengths`: required.
- `weaknesses`: required.
- `differentiators`: required.
- `recent_changes`: required.
- `market_signals`: required.
- `brand_strength`: required; range [0, 5].
- `pricing_pressure`: required; range [0, 5].
- `product_maturity`: required; range [0, 5].
- `distribution`: required; range [0, 5].
- `switching_costs`: required; range [0, 5].
- `capital_strength`: required; range [0, 5].
- `innovation_velocity`: required; range [0, 5].
- `customer_loyalty`: required; range [0, 5].
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `claim_ids`: required; references `08_evidence/claims_register.csv:claim_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `competitor_pressure_score`: optional/derived; range [0, 100].
- `owner`: required.
- `as_of_date`: required.

### `03_competitors/competitor_matrix_template.csv`

Primary key: `assessment_id`.

- `sample_status`: required.
- `competitor_id`: required; references `03_competitors/competitor_database.csv:competitor_id`.
- `assessment_id`: required.
- `criterion`: required.
- `rating_0_5`: required; range [0, 5]; integer.
- `basis`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `as_of_date`: required.

### `03_competitors/positioning_map_template.csv`

Primary key: `position_id`.

- `sample_status`: required.
- `competitor_id`: required; references `03_competitors/competitor_database.csv:competitor_id`.
- `position_id`: required.
- `x_axis`: required.
- `x_value_0_5`: required; range [0, 5]; integer.
- `y_axis`: required.
- `y_value_0_5`: required; range [0, 5]; integer.
- `interpretation`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `as_of_date`: required.

### `03_competitors/pricing_comparison_template.csv`

Primary key: `price_id`.

- `sample_status`: required.
- `competitor_id`: required; references `03_competitors/competitor_database.csv:competitor_id`.
- `price_id`: required.
- `plan`: required.
- `price`: required.
- `currency`: required.
- `billing_period`: required.
- `minimum_commitment`: required.
- `included_units`: required.
- `overage`: required.
- `setup_fee`: required.
- `tax_basis`: required.
- `comparison_limit`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `as_of_date`: required.

### `03_competitors/competitor_change_log.csv`

Primary key: `change_id`.

- `sample_status`: required.
- `change_id`: required.
- `competitor_id`: required; references `03_competitors/competitor_database.csv:competitor_id`.
- `signal_type`: required.
- `observed_date`: required.
- `previous_value`: required.
- `new_value`: required.
- `materiality`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `response`: required.
- `owner`: required.
- `status`: required.

### `04_customers/customer_segments_template.csv`

Primary key: `segment_id`.

- `sample_status`: required.
- `segment_id`: required.
- `name`: required.
- `icp_inclusion`: required.
- `icp_exclusion`: required.
- `jobs_to_be_done`: required.
- `pains`: required.
- `desired_outcomes`: required.
- `buying_triggers`: required.
- `switching_triggers`: required.
- `decision_criteria`: required.
- `price_sensitivity`: required.
- `objections`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `claim_ids`: required; references `08_evidence/claims_register.csv:claim_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `label`: required.
- `population_limit`: required.
- `owner`: required.
- `as_of_date`: required.

### `04_customers/pain_points_template.csv`

Primary key: `pain_id`.

- `sample_status`: required.
- `pain_id`: required.
- `segment_id`: required; references `04_customers/customer_segments_template.csv:segment_id`.
- `pain`: required.
- `frequency`: required.
- `severity_0_5`: required; range [0, 5]; integer.
- `cost_basis`: required.
- `label`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `as_of_date`: required.

### `04_customers/buying_triggers_template.csv`

Primary key: `trigger_id`.

- `sample_status`: required.
- `trigger_id`: required.
- `segment_id`: required; references `04_customers/customer_segments_template.csv:segment_id`.
- `trigger`: required.
- `trigger_type`: required.
- `observable_event`: required.
- `validation_question`: required.
- `label`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `as_of_date`: required.

### `04_customers/objections_template.csv`

Primary key: `objection_id`.

- `sample_status`: required.
- `objection_id`: required.
- `segment_id`: required; references `04_customers/customer_segments_template.csv:segment_id`.
- `objection`: required.
- `decision_stage`: required.
- `response_test`: required.
- `rejection_threshold`: required.
- `label`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `as_of_date`: required.

### `04_customers/customer_evidence_template.csv`

Primary key: `customer_evidence_id`.

- `sample_status`: required.
- `customer_evidence_id`: required.
- `segment_id`: required; references `04_customers/customer_segments_template.csv:segment_id`.
- `method`: required.
- `sample_size`: required.
- `sampling_frame`: required.
- `insight`: required.
- `bias_limit`: required.
- `consent_status`: required.
- `label`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `as_of_date`: required.

### `02_market/market_assessment.csv`

Primary key: `market_id`.

- `sample_status`: required.
- `market_id`: required.
- `market`: required.
- `scope`: required.
- `currency`: required.
- `period`: required.
- `tam`: required; range [0, 1000000000000000.0].
- `sam`: required; range [0, 1000000000000000.0].
- `som`: required; range [0, 1000000000000000.0].
- `label`: required.
- `market_size`: required; range [0, 5].
- `growth_rate`: required; range [0, 5].
- `profitability`: required; range [0, 5].
- `customer_concentration`: required; range [0, 5].
- `switching_friction`: required; range [0, 5].
- `regulation`: required; range [0, 5].
- `competitive_intensity`: required; range [0, 5].
- `barriers_to_entry`: required; range [0, 5].
- `technology_disruption`: required; range [0, 5].
- `macro_sensitivity`: required; range [0, 5].
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `claim_ids`: required; references `08_evidence/claims_register.csv:claim_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `market_attractiveness_score`: optional/derived; range [0, 100].
- `rating`: optional/derived.
- `key_drivers`: required.
- `key_risks`: required.
- `recommended_posture`: optional/derived.
- `as_of_date`: required.

### `05_opportunities/gap_register.csv`

Primary key: `gap_id`.

- `sample_status`: required.
- `gap_id`: required.
- `category`: required.
- `question`: required.
- `segment_id`: required; references `04_customers/customer_segments_template.csv:segment_id`.
- `unmet_need`: required; range [0, 5].
- `underserved_reach`: required; range [0, 5].
- `alternative_failure`: required; range [0, 5].
- `solution_feasibility`: required; range [0, 5].
- `evidence_confidence`: optional/derived; range [0, 5].
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `claim_ids`: required; references `08_evidence/claims_register.csv:claim_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `gap_score`: optional/derived; range [0, 100].
- `falsification`: required.
- `owner`: required.
- `as_of_date`: required.

### `06_risks/assumptions_register.csv`

Primary key: `assumption_id`.

- `sample_status`: required.
- `assumption_id`: required.
- `assumption`: required.
- `label`: required.
- `basis`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `failure_impact`: required.
- `validation_method`: required.
- `owner`: required.
- `due_date`: required.
- `status`: required.
- `decision_ids`: required; references `07_strategy/recommendations.csv:decision_id`.
- `critical`: required.

### `06_risks/unknowns_register.csv`

Primary key: `unknown_id`.

- `sample_status`: required.
- `unknown_id`: required.
- `question`: required.
- `decision_affected`: required; references `07_strategy/recommendations.csv:decision_id`.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `resolution_method`: required.
- `owner`: required.
- `due_date`: required.
- `status`: required.
- `decision_ids`: required; references `07_strategy/recommendations.csv:decision_id`.
- `critical`: required.

### `06_risks/dependency_register.csv`

Primary key: `dependency_id`.

- `sample_status`: required.
- `dependency_id`: required.
- `dependency`: required.
- `dependent_action`: required; references `07_strategy/action_plan.csv:action_id`.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `owner`: required.
- `due_date`: required.
- `fallback`: required.
- `status`: required.
- `decision_ids`: required; references `07_strategy/recommendations.csv:decision_id`.
- `critical`: required.

### `08_evidence/evidence_gap_register.csv`

Primary key: `gap_id`.

- `sample_status`: required.
- `gap_id`: required.
- `claim_id`: required; references `08_evidence/claims_register.csv:claim_id`.
- `missing_evidence`: required.
- `decision_impact`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `research_method`: required.
- `owner`: required.
- `due_date`: required.
- `status`: required.
- `decision_ids`: required; references `07_strategy/recommendations.csv:decision_id`.
- `critical`: required.

### `08_evidence/research_gap_register.csv`

Primary key: `gap_id`.

- `sample_status`: required.
- `gap_id`: required.
- `question`: required.
- `importance`: required.
- `current_evidence`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence`: optional/derived; range [0, 100].
- `recommended_research`: required.
- `priority`: required.
- `owner`: required.
- `status`: required.

### `08_evidence/research_debt_register.csv`

Primary key: `debt_id`.

- `sample_status`: required.
- `debt_id`: required.
- `claim_id`: required; references `08_evidence/claims_register.csv:claim_id`.
- `debt_type`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `decision_exposure`: required.
- `resolution`: required.
- `owner`: required.
- `due_date`: required.
- `status`: required.
- `decision_ids`: required; references `07_strategy/recommendations.csv:decision_id`.
- `critical`: required.

### `02_market/market_signals.csv`

Primary key: `signal_id`.

- `sample_status`: required.
- `signal_id`: required.
- `signal_type`: required.
- `signal`: required.
- `label`: required.
- `observed_date`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `promotion_criteria`: required.
- `response`: required.
- `owner`: required.
- `status`: required.

### `07_strategy/recommendations.csv`

Primary key: `decision_id`.

- `sample_status`: required.
- `decision_id`: required.
- `decision`: required.
- `label`: required.
- `rationale`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `claim_ids`: required; references `08_evidence/claims_register.csv:claim_id`.
- `opportunity_ids`: required; references `05_opportunities/opportunity_database.csv:opportunity_id`.
- `risk_ids`: required; references `06_risks/risk_register.csv:risk_id`.
- `confidence_score`: optional/derived; range [0, 100].
- `expected_upside`: required.
- `major_risk`: required.
- `next_validation_step`: required.
- `budget_cap`: required; range [0, 1000000000000.0].
- `currency`: required.
- `decision_required`: required.
- `owner`: required.
- `status`: required.
- `as_of_date`: required.

### `07_strategy/action_plan.csv`

Primary key: `action_id`.

- `sample_status`: required.
- `action_id`: required.
- `decision_id`: required; references `07_strategy/recommendations.csv:decision_id`.
- `phase`: required.
- `action`: required.
- `owner`: required.
- `objective`: required.
- `success_metric`: required.
- `dependency`: required.
- `priority`: required.
- `risk`: required.
- `status`: required.
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `as_of_date`: required.

### `07_strategy/decision_matrix.csv`

Primary key: `option_id`.

- `sample_status`: required.
- `option_id`: required.
- `decision`: required.
- `potential_upside`: required; range [0, 5].
- `cost`: required; range [0, 5].
- `time_to_value`: required; range [0, 5].
- `execution_difficulty`: required; range [0, 5].
- `risk`: required; range [0, 5].
- `confidence`: optional/derived; range [0, 100].
- `strategic_fit`: required; range [0, 5].
- `score`: optional/derived; range [0, 100].
- `evidence_ids`: required; references `08_evidence/evidence_register.csv:evidence_id`.
- `claim_ids`: required; references `08_evidence/claims_register.csv:claim_id`.
- `decision_gate`: optional/derived.
- `as_of_date`: required.

### `10_dashboards/executive_dashboard_template.csv`

Primary key: `decision_id`.

- `sample_status`: required.
- `decision_id`: required.
- `decision`: required.
- `confidence_score`: required; range [0, 100].
- `budget_cap`: required.
- `currency`: required.
- `status`: required.
- `as_of_date`: required.

### `10_dashboards/opportunity_dashboard_template.csv`

Primary key: `opportunity_id`.

- `sample_status`: required.
- `opportunity_id`: required.
- `title`: required.
- `opportunity_score`: required; range [0, 100].
- `confidence_score`: required; range [0, 100].
- `action_category`: required.
- `decision_gate`: required.
- `owner`: required.
- `as_of_date`: required.
- `merit_score`: optional/derived; range [0, 100].
- `input_basis_status`: optional/derived.

### `10_dashboards/competitor_dashboard_template.csv`

Primary key: `competitor_id`.

- `sample_status`: required.
- `competitor_id`: required.
- `company`: required.
- `competitor_pressure_score`: required; range [0, 100].
- `confidence_score`: required; range [0, 100].
- `as_of_date`: required.

### `10_dashboards/risk_dashboard_template.csv`

Primary key: `risk_id`.

- `sample_status`: required.
- `risk_id`: required.
- `title`: required.
- `risk_score`: required; range [0, 100].
- `classification`: required.
- `confidence_score`: required; range [0, 100].
- `trigger`: required.
- `owner`: required.
- `as_of_date`: required.

### `09_scores/factor_assessments.csv`

Primary key: `assessment_id`.

- `sample_status`: required.
- `assessment_id`: required.
- `entity_file`: required.
- `entity_id`: required.
- `factor`: required.
- `input_value`: required; range [0, 5].
- `basis_type`: required.
- `claim_ids`: optional/derived; references `08_evidence/claims_register.csv:claim_id`.
- `evidence_ids`: optional/derived; references `08_evidence/evidence_register.csv:evidence_id`.
- `assumption_ids`: optional/derived; references `06_risks/assumptions_register.csv:assumption_id`.
- `rationale`: required.
- `reviewed_by`: required.
- `review_date`: required.

### `09_scores/decision_scoring_model.csv`

Primary key: `factor`.

- `factor`: required.
- `weight`: required; range [0, 100].
- `input_min`: required; range [0, 0].
- `input_max`: required; range [0, 100].
- `direction`: required.
- `definition`: required.
- `anchor_0`: required.
- `anchor_mid`: required.
- `anchor_max`: required.

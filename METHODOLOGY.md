# Methodology

## Decision before research

Define a single decision question, geography, category boundaries, observation period, decision
horizon, capital at risk and acceptable loss. List feasible alternatives before searching for
evidence. Record inclusion and exclusion criteria so convenient sources cannot silently widen scope.

## Research sequence

| Stage | Required output | Release criterion |
| --- | --- | --- |
| Scope | Decision charter and questions | Boundaries and stop rules agreed |
| Capture | Source record and archived locator | Source origin and rights recorded |
| Extract | One scoped claim per evidence item | Observation separated from interpretation |
| Challenge | Counterevidence and gaps | Alternative explanation and missing variables recorded |
| Synthesize | Market, competitor and customer analysis | Units and periods comparable |
| Prioritize | Scores and sensitivity | Inputs anchored; uncertainty preserved |
| Decide | Option, downside, validation step and owner | Approval recorded; commitment gates passed |
| Monitor | Change log and research debt | New evidence traced to affected decisions |

Triangulate independent origins rather than counting links. A company disclosure is authoritative
about a stated price on its own plan, but does not establish customer outcomes. A review may show
that a complaint exists, but cannot establish prevalence. Count observations and limitations together.

## Market arithmetic

Prefer bottom-up eligible accounts × realized annual spend. TAM covers the defined category;
SAM applies geographic, channel and product eligibility constraints; SOM applies delivery and
acquisition capacity. Reconcile overlapping account definitions and do not multiply unrelated
top-down percentages. Show low, base and high assumptions separately without inventing probabilities.

## Decision logic

Review irreversible downside before weighted appeal. A strong opportunity cannot offset a
prohibited activity, an unowned critical risk or absent financing. Select a reversible **TEST**
when the uncertainty can be resolved affordably. **ENTER**, **EXPAND** and **ACQUIRE** require
reviewed live evidence, sufficient economics, capacity and an explicit approval record.
Model scores advise a discussion; the decision matrix cannot authorize spending.

## Repeatability

Use the model CSVs as the single weight source and archive them with each delivery. Fix an as-of
date for reproducible freshness. Version scope changes and retain superseded evidence. Recalculate
after a source refresh and show how recommendations changed. In a sample run, synthetic sources
are internal demonstration artifacts with synthetic URLs and no claim to external verification.

## Market attractiveness model

Use 0–5 claim-backed inputs and weights from `09_scores/market_attractiveness_model.csv`:
market size 15, growth 12, profitability 15, customer concentration 8, switching friction 8,
regulation 8, competitive intensity 10, entry barriers 8, disruption exposure 8 and macro
sensitivity 8. The first three are positive. All remaining factors measure burden and are
inverted as 5−input. Attractiveness=Σ(weight×oriented input/5).

>=75 Attractive → REVIEW ENTRY; 55–<75 Selective → TEST NARROW SCOPE; 40–<55 Challenging →
MONITOR; <40 Unattractive → AVOID UNTIL CONDITIONS CHANGE. Confidence remains separate.
For an incumbent expansion, entry barriers and switching effects may have different meanings:
create a separately versioned model rather than silently changing orientation.

Synthetic MKT-001 contributions: 9+7.2+9+4.8+3.2+4.8+4+3.2+3.2+4.8=53.20, Challenging.
Scope-specific research can still be proposed; the index does not mandate a universal choice.

## Competitor pressure model

Weights: brand 12, pricing 14, product maturity 14, distribution 16, switching costs 12,
capital 10, innovation 10 and loyalty 12. Every 0–5 factor is positive for incumbent pressure.
Pressure=Σ(weight×input/5). >=75 Intense, 55–<75 Material, 35–<55 Limited, <35 Low.
Report pressure per relevant task/segment with confidence. Do not average unrelated rivals
or discount pressure because evidence is weak. Cedar Metric synthetic contributions:
7.2+8.4+11.2+12.8+7.2+6+6+7.2=66.00, Material.

## Decision matrix

All options use a common horizon and resource envelope. Raw comparison weights: upside 25,
inverse cost 15, inverse time to value 10, inverse execution difficulty 10, inverse risk 15,
strategic fit 25. Normalize every 0–5 input by 5. Score=raw×(0.25+0.75×confidence/100).
Confidence is the weakest material claim, not a free analyst input. The matrix ranks feasible
options only; infeasible or prohibited options remain excluded regardless of score. Approval
and opportunity commitment gates still apply. Record rationale for each option's factor ratings.

## Using factor anchors

Model CSVs provide zero, middle and maximum anchors. In the 0–5 business models, the middle
anchor denotes 3; use 1/2/4 only with a written interpolation rationale. In the confidence model,
the dedicated confidence scoring guide owns exact point anchors and overrides the generic
middle description. Anchors are engagement-specific starting rubrics, not measured sector
benchmarks. Define spend viability and growth benchmarks before assigning market ratings.

## Model 1.0.1 hardening

Opportunity business merit excludes additive confidence and uses the documented 25% floor/75%
support adjustment. The decision comparison now reads decision_scoring_model.csv instead of
hard-coded weights and applies the same support adjustment once. Market attractiveness and competitor
pressure weights/orientations are retained, with explicit per-factor provenance. Gap inputs remain
weighted unmet-need signals; a high gap score with weak or assumed evidence is an UNVERIFIED signal,
not proof of a market gap. Only reviewed high-confidence observations can justify a strong assertion.

Model 1.0.0 remains a historical method in the preserved baseline, not the active scoring procedure.
The earlier decision formula's 50% floor is superseded. All indices are judgment tools and require
sensitivity review. The current weights have no empirical outcome calibration.

# Opportunity scoring — model 1.0.1

## Business merit and evidence support

Use the nine business factors from opportunity_scoring_model.csv. The preserved model file also
contains the legacy 5-point evidence-confidence factor for compatibility; the current merit
calculation excludes that factor and normalizes business weights from 95 to 100.

| Factor | Original business weight | Direction |
| --- | ---: | --- |
| Demand | 15 | Positive |
| Growth | 10 | Positive |
| Pain intensity | 15 | Positive |
| Saturation | 10 | Inverse |
| Differentiation | 10 | Positive |
| Monetization | 10 | Positive |
| Implementation difficulty | 8 | Inverse |
| Time to market | 7 | Inverse |
| Strategic fit | 10 | Positive |

`merit = 100/95 × Σ(business_weight × oriented_input/5)`

`Opportunity Score = merit × (0.25 + 0.75 × material_claim_confidence/100)`

Confidence now enters once. Fully unsupported merit=100 adjusts to 25, not 50. The 25% floor
preserves visibility for an untested idea; it does not indicate a 25% success probability. UNKNOWN
inputs and ASSUMPTION inputs are exposed through factor_assessments and input_basis_status.
Scores based on invented or contingent ratings must remain explicitly hypothetical.

Categories use unrounded results: >=85 PRIORITIZE; >=70 VALIDATE; >=55 EXPLORE; >=40 WATCH;
<40 DEPRIORITIZE. Separate gates: <60 RESEARCH REQUIRED, 60–<75 VALIDATION ONLY, >=75 REVIEW FOR
COMMITMENT. No category grants spending authority. An irreversible live choice also requires
resolved critical uncertainties, reviewed factor observations, risk acceptance and named sign-off.

## Worked fictional example

OPP-001 business contributions sum to 72. Merit=72×100/95=75.7894736842. Confidence=59 from the
disputed critical claim. Multiplier=0.25+0.75×0.59=0.6925. Adjusted=52.4842105263 → stored 52.48,
WATCH, RESEARCH REQUIRED. The sample can request a small research TEST; it cannot justify expansion.

OPP-002: merit 60, confidence 72, adjusted 47.40. OPP-003: merit 46×100/95, confidence 59,
adjusted 33.53. All business ratings are synthetic assumptions.

## Compatibility and sensitivity

`raw_score` preserves the original ten-factor view and is deprecated for ranking. Use merit_score,
opportunity_score, confidence and input_basis_status together. Archived 1.0.0 rankings must not be
silently compared with model 1.0.1. Every input requires a scoped basis record. Test uncertain factors
by ±1 and show whether rank or decision changes. Two decimal storage supports reproducibility,
not accurate measurement. Demand, pain and monetization overlap; no statistical independence is claimed.

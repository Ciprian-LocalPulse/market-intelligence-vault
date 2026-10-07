# Confidence scoring — model 1.0.1

## Observation strength

Reliability 0–25, freshness 0–20, directness 0–20, independent corroboration 0–20 and relevance
0–15 sum to 100. These are judgment points, not calibrated probabilities. Retain the allocation
as an explicit heuristic; no empirical validation or superiority over alternative weights is claimed.

| Factor | Anchors |
| --- | --- |
| Reliability | 0 no credible source; 5 unverifiable; 10 opaque method; 15 documented with limits; 20 auditable primary; 25 independently auditable |
| Freshness | Current 20; Recent 15; Aging 8; Stale or Unknown 0 |
| Directness | 0 speculative; 5 remote proxy; 10 relevant proxy; 15 partial observation; 20 direct scoped observation |
| Corroboration | 0 one eligible origin; 10 two; 15 three; 20 four or more |
| Relevance | 0 outside scope; 5 narrow overlap; 10 partial match; 15 full population/geography/period match |

Evidence reliability cannot exceed the source-library ceiling. Zero relevance or reliability sets
score 0. Reliability <=5 or relevance <=5 caps at 39. Verified indirect support caps at 74. A
direct label requires >=15 directness; less than full directness caps at 89. Unknown date caps at
59; Stale caps at 39. Unverified caps at 39; speculation caps at 19; unsupported status sets 0.

Corroboration is derived, not manually promoted. Only mapped supporting observations that are
verified, direct, Current/Recent, reliability >=15 and relevance >=10 qualify. Repeated origin
groups count once. Origin independence remains a reviewer judgment; the software does not verify
publisher ownership. Contradicting and contextual evidence never count as supporting corroboration.

## Ordered A–G grade rules

| Grade | Rule |
| --- | --- |
| G | Unsupported status |
| F | Speculation status, capped at 19 |
| E | Unverified status, capped at 39 |
| A | >=90, verified, directness=20, Current, reliability>=20, corroboration>=15, relevance>=10 |
| B | >=75, verified, direct label/directness>=15, Current or Recent |
| C | Remaining verified support >=60 |
| D | Remaining verified weak/indirect/stale support |

Apply the rules in order. G can share numeric zero with D when a verified observation is outside
scope; the status explains the difference. Grade measures observation quality, not endorsement of
the attached business interpretation. Two valid observations can contradict without becoming false.

## Claim confidence

Take the weakest critical supporting observation; if no critical support is marked, take the
weakest supporting observation. With no support use 0. Apply claim-type caps: FACT 100, INFERENCE
89, ESTIMATE 74, HYPOTHESIS 59, RECOMMENDATION 0. Recommendations belong in the decision register
and cannot serve as factual support. An unresolved map or evidence/claim contradiction caps the
claim at 59. This policy prevents a hypothesized or disputed conclusion from receiving a high
confidence band solely because its source observations are strong.

Bands: >=90 Very High; >=75 High; >=60 Moderate; >=40 Low; <40 Very Low. Material-object confidence
is the weakest referenced material claim. Claim freshness is the weakest critical support status,
with Unknown worse than Stale. Contradiction flags must agree with the map and evidence flags.

These caps are conservative governance choices, not measured truth probabilities. A precise fact
can rely on one official source; it does not automatically require an A grade to be useful.
Never compare synthetic confidence with live evidence quality.

## Worked synthetic case

EV-001 has 20+20+20+0+15=75 → B. Its source observation remains sound within the invented case.
CLM-001 is disputed and caps at 59 Low. EV-006 counterevidence scores 73 C. CLM-004 is a procurement
hypothesis and caps at 59 despite observation score 63. DEC-001 therefore has confidence 59 Low
and supports only a capped research TEST proposal.

## Freshness

Configurable inclusive windows in config/freshness.json: default 30/90/180 days; pricing 14/45/90;
market 90/180/365; customer 30/90/180; product 30/60/120. After the third window the item is Stale.
Missing publication date is Unknown. Future dates fail. Publication date, not access date, defines
age. A refreshed source requires a new reviewed observation; score refresh never rewrites observed dates.

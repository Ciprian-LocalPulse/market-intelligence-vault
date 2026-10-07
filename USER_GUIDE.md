# Analyst workflow

## 1. Scope the decision

Write geography, category, period, decision horizon, feasible options, capital limit and stop rules
before researching. Read the executive brief structure to understand which questions must be answered.
Create `engagement_<name>` using the initializer. Do not relabel synthetic data LIVE.

## 2. Capture before interpreting

Add a real source with publication/access date, stable citation URL, origin group, exact locator,
rights basis and a confined archive reference. Record its SHA-256 hash. Source reliability is a
ceiling: claim-specific evidence can be weaker, never silently stronger. An official disclosure can
be authoritative for its own terms and still weak for a customer-outcome inference.

Add one scoped observation per evidence row. Create a typed claim and map supports/contradicts/context.
Critical materiality identifies indispensable support. Match source metadata exactly. Direct evidence
needs directness >=15; a full observation is 20. Indirect evidence cannot claim full directness.
Keep flagged counterevidence visible even when it is contextual. FACT requires verified direct support.

## 3. Structure analysis and uncertainty

Populate market, competitors and customer records with scope, units, period and evidence references.
Use genuine observed prices only for matched plans and conditions. Record observed customer behavior,
sampling frame and consent status separately from expressed preference. Unobserved willingness to pay
remains a hypothesis. Add assumptions, unknowns, dependencies, gaps and research debt with affected
decision IDs and a critical flag. Close them only after the documented resolution criterion is met.

## 4. Assign scored factors

Each scored business factor needs one record in `09_scores/factor_assessments.csv`: target file/ID,
factor, actual input value, OBSERVATION/ASSUMPTION/UNKNOWN basis, evidence/claim or assumption IDs,
rationale, reviewer and date. Use model anchors. UNKNOWN is not zero. If an unknown factor cannot be
estimated defensibly, leave the required numeric input blank and do not score that option yet.
ASSUMPTION means a contingent estimate; it does not establish demand or economics.

An OBSERVATION basis does not prove a causal interpretation. Explain interpolation from a measured
task to an ordinal rating. Record why ±1 could or could not change the decision. Source independence
must be reviewed, not invented through origin labels. The calculator derives corroboration only
from eligible current/recent verified direct support; stale or same-origin links do not add points.

## 5. Recompute and challenge

Run calculation, validation with `--audit-scores`, and the source audit at the same as-of date.
Schemas are checked against converted records as part of validation. Read current claim freshness
and limits rather than a saved score alone. Evidence grades describe an observation; claim confidence
also reflects inference, estimates, hypotheses and unresolved conflict. No score is a truth probability.

Opportunity merit excludes additive confidence and is adjusted once. `raw_score` is a deprecated
compatibility view, not the ranking measure. `merit_score`, `opportunity_score` and `input_basis_status`
must be shown together. Model 1.0.1 is not numerically comparable to 1.0.0 without recomputation.

## 6. Complete narratives and approval

Replace authoring prompts, preserve labels, cite counterevidence, and state downside, alternative,
owner, metric and stop rule. Keep proposal status until authority is documented. For live delivery,
review the explicit live file allowlist and remove demonstration-only links. Do not add private
archives unless redistribution is approved. The source library may reference an archive retained
only in the controlled workspace; that is intentional and must be disclosed to the reader.

After all files and calculations are final, compute the review digest:

```text
python -c "from pathlib import Path; import sys; sys.path.insert(0,'tools'); from common import input_digest; print(input_digest(Path('.')))"
```

Have the actual reviewer and decision authority complete `config/live_signoff.json` with APPROVED
status, scope, date, that digest, approved decision IDs, required review attestations and any dated
Critical-risk acceptance. The software cannot authenticate their identities. Never fill this record
on someone else's behalf without authorization. Any changed reviewed input requires a new sign-off.

## 7. Deliver and maintain

Build `--mode live` only after the checks pass. A bounded TEST can be approved to resolve weak
evidence; irreversible choices require confidence >=75, current/recent reviewed support and no
unresolved critical uncertainty. Verify the exact package inventory and hashes before distribution.
CSV viewing exports neutralize formula-leading text and must not replace canonical inputs.

Refresh pricing/product signals at the chosen volatility cadence. Preserve source revisions,
superseded interpretations and decision history manually; automatic supersession is not implemented.
An access date is not a new observation. Score refresh does not update change-log observation dates.
Archive the model version, approval record and package together. Follow SECURITY_AND_PRIVACY.md.

# Risk scoring

## Exposure model

Inputs use 0–5. Likelihood is judged within the recorded horizon: 0 implausible within scope,
1 rare, 2 possible, 3 plausible, 4 likely, 5 already occurring. Impact: 0 immaterial, 1 minor,
2 contained, 3 material rework, 4 threatens objectives, 5 threatens viability or creates an
unacceptable legal/safety consequence. These are ordinal anchors, not numerical probabilities.

Detectability means difficulty of early detection: 0 immediate and reliable, 3 intermittent,
5 likely invisible before harm. Velocity: 0 more than a year, 1 quarters, 2 months, 3 weeks,
4 days, 5 hours. Mitigation readiness: 0 absent, 1 proposed, 2 owned but untested, 3 partly tested,
4 tested with remaining limitations, 5 proven and available.

`Risk Score = 30×L/5 + 35×I/5 + 15×D/5 + 10×V/5 + 10×(5−M)/5`

| Score (unrounded) | Class | Response |
| --- | --- | --- |
| >=80 | Critical | Escalate before commitment; named acceptance authority required |
| >=60 | High | Owner, trigger, tested mitigation and review date required |
| >=35 | Moderate | Mitigate or explicitly accept within scope |
| <35 | Low | Monitor at the stated cadence |

Impact=5 and likelihood>=3 forces Critical even if weighted score is lower. A documented
`override=true` also forces Critical; `override_reason` is required. Overrides cannot lower risk.
Confidence is reported separately and never discounts exposure: weak threat evidence demands
research, not a lower risk score. Re-score residual risk only after mitigation is observed.

## Worked fictional example

RSK-001: L4, I4, D3, V4, M2. Score=24+28+9+8+6=75 → High. Confidence 78, High.
Confidence is reported separately and does not reduce the score. The connector spike and manual-import fallback are the
next tests. RSK-003 has unproven willingness-to-pay mitigation and remains explicitly open.

The model compares threats within one scope and horizon. It does not sum to portfolio expected
loss and cannot price tail risks. Review common causes and correlated dependencies separately.

## Quality hardening rule in 1.0.1

If likelihood=0 or impact=0, exposure is 0 unless a documented upward Critical override exists.
The output marks a structural zero and demands verification of that assumption. Missing data cannot
be entered as zero. The weighted model otherwise remains unchanged; it is an ordinal triage index,
not expected loss. Confirm common causes, interaction effects and catastrophic downside separately.
Critical live risks require ACCEPTED status and a named, dated acceptance in the bound sign-off.
The three synthetic exposures remain 75, 66 and 72. Paid-demand and procurement confidence are now
59 Low because disputed/hypothesized claims are capped. Risk exposure is never discounted by confidence.

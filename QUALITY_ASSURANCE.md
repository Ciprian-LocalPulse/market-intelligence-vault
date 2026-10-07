# Quality assurance

## Release audit

Assign each category 0 absent, 1 material defects, 2 partly complete, 3 adequate with limits,
4 strong with minor defects, 5 fully reviewed. Record evidence and reviewer name for each score.
`Quality Score = sum(weight × category_rating / 5)`, maximum 100. A score is review coverage,
not the truth probability of a market conclusion.

| Review | Weight | Required evidence |
| --- | ---: | --- |
| Evidence audit | 15 | Material claims trace to valid scoped observations |
| Source audit | 10 | Provenance, rights, origin independence and exact locators reviewed |
| Calculation audit | 15 | Formulas, weights, boundaries and saved scores reconcile |
| Contradiction review | 10 | Counterevidence retained and effect on recommendation stated |
| Bias check | 10 | Selection, survivorship, sponsorship and confirmation risks documented |
| Unsupported claim check | 10 | Unknowns exposed; hypotheses never promoted without observation |
| Formatting review | 5 | Links, units, headers, labels and readable Markdown |
| Executive clarity review | 10 | Decision, downside and requested commitment visible |
| Actionability review | 10 | Owner, metric, dependency, stop rule and review date |
| Freshness review | 5 | Topic-specific age and unknown dates reviewed |

## Hard gates

Delivery requires no validator errors, passing tests, reconciled saved scores and a signed review.
Live delivery additionally requires no synthetic/TEMPLATE data, approved recommendations, valid
HTTP(S) source URLs, a fact-check/rights review and no unowned Critical risk. Block delivery if a
critical factual claim lacks support, a score is manipulated, a material contradiction is hidden,
or an estimate is presented as observed revenue. Numerical QA cannot waive these gates.

90–100 can release after gate checks; 80–<90 requires documented remediation and a second review;
below 80 requires rework. Foundation delivery is a reusable product with synthetic examples and
does not pass the real-evidence gate for capital decisions.

## Reviewer record

| Category | Rating /5 | Evidence | Reviewer | Review date | Open issue |
| --- | --- | --- | --- | --- | --- |
| [category] | [rating] | [audit artifact or locator] | [name] | [date] | [issue or none] |

Record final score, gate status, approved scope and signature in the delivery manifest. Automated
release checks are recorded separately in RELEASE_VERIFICATION.md; they do not substitute for
an independent human content review.

## Hardening controls in 1.0.1

Live sign-off is machine-checked for a named reviewer/authority, all required attestations, decision
coverage and exact input digest. Critical risk acceptance and irreversible-commitment evidence gates
are enforced. The record is an attestation, not identity authentication. Numerical completeness QA
cannot establish empirical truth. The old 93/100 author score is superseded by the stricter audit.

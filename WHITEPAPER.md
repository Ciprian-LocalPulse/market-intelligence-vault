# Market Intelligence Vault

## An Evidence-Based Framework for Traceable Market and Decision Intelligence

**Author: Ciprian Ștefan Pleșca**  
Product baseline: 1.1.0 · Scoring model: 1.0.1 · 2026

© 2026 Ciprian Ștefan Pleșca. All rights reserved.

## 1. Abstract

Market Intelligence Vault is a local framework for connecting market research to decisions through
explicit evidence, claims, uncertainty and review gates. Its central unit is a traceable analytical
dependency: a recommendation references material claims, claims have scoped supporting and challenging
observations, and observations retain source identity, dates and archival locators. Heuristic indices
help organize comparison while preserving assumptions and limits. The interactive dashboard presents
the same dependencies to executives and analysts. This paper describes the implemented 1.1.0 product,
the retained 1.0.1 scoring policy and the responsibilities that remain with human reviewers. It makes
no claim of predictive accuracy, empirical calibration or source authentication.

## 2. Introduction

Market research becomes useful when it changes a well-defined choice. A broad collection of sector
reports may inform a discussion without explaining which observation justifies entry, a pilot or a
delay. Market Intelligence Vault starts with the decision question and preserves the reasoning that
connects it to research. The repository combines structured registers, versioned rubrics, semantic
validation, reviewable recommendations and a local executive interface. It is intended to make an
analysis inspectable and reproducible at a stated date. It is not an operated intelligence feed or
a substitute for the person accountable for the resulting action.

## 3. The Market Intelligence Problem

A typical research brief mixes company disclosures, analyst estimates, customer anecdotes and
strategic recommendations in one narrative. Readers may lose the distinction between an observed
statement and the interpretation placed on it. Repeated articles can be mistaken for independent
corroboration. A current access date can conceal an old observation. An attractive revenue scenario
can distract from an unresolved delivery constraint. These problems are not solved by adding more
links. They require explicit scope, relationship semantics, dates, alternative explanations and
ownership. The framework records those elements so a reviewer can challenge a conclusion without
reconstructing the entire research process from prose.

## 4. Information Overload vs Decision Intelligence

Information volume and decision relevance are different quantities. A hundred relevant-looking
citations may contribute little to a choice if they describe another population, pricing period or
delivery model. Decision intelligence asks which uncertainty matters, which observation could reduce
it and what commitment would become defensible afterward. The framework therefore distinguishes
registered research coverage from knowledge completeness. Its dashboard counts claims with mapped
support and open gaps; these are descriptions of the register, not assurances that all important
variables have been found. A concise decision brief should expose the weakest dependency, not merely
the largest source count.

## 5. Design Philosophy

The implemented design favors explicit records over hidden inference. Canonical CSVs keep analytical
inputs inspectable. Stable IDs support joins and references across reports. Model CSVs and policy
configuration own arithmetic and governance limits. Python tools validate before creating an export;
browser modules display validated projections without mutating research. Evidence support, business
appeal and approval remain separate. Failure is visible: invalid or mixed snapshots do not render
invented fallback intelligence. The design assumes a trusted local operator and makes that boundary
explicit. It does not claim to prevent an operator from rewriting code, inventing an attestation or
deliberately falsifying a research record.

## 6. Evidence Before Conclusions

Evidence capture should begin with a scoped observation: what was observed, in which population,
geography and period, and by what method. A customer describing reconciliation burden establishes
that the description occurred within a sample; it does not establish market prevalence or paid demand.
A vendor publishing a price supports a dated pricing statement, not a claim about customer value.
The observation and the business interpretation should therefore remain distinct. Reviewers record
directness, relevance, verification status and source quality before promoting a claim. The software
can enforce required fields and conservative limits, but the semantic decision about what the
observation supports remains a professional judgment.

## 7. Evidence Traceability

The source library retains citation metadata, an origin group, dates, rights context and an archived
locator with a checksum. An evidence record references that source and its currently bound claim.
The claim-evidence map distinguishes supporting, contradicting and contextual relationships. A
recommendation then references material claim IDs along with related opportunities and risks. This
trail allows a reviewer to move from a proposed action to the observation and source that constrain
it. The current data topology binds one claim per evidence record; many-claim observation lifecycle
support is not yet implemented. Stable IDs and mapping tables are useful infrastructure, but do not
by themselves establish complete revision history or automated impact propagation.

## 8. Facts, Inferences, Estimates and Hypotheses

Statement labels describe the kind of assertion, not its truth. A FACT requires scoped observational
support. An INFERENCE interprets observations under stated assumptions. An ESTIMATE depends on a
calculation and input scope. A HYPOTHESIS remains a proposition to test. A RECOMMENDATION proposes
action and must not serve as factual evidence for itself. Model 1.0.1 limits maximum claim confidence
by type: inference 89, estimate 74 and hypothesis 59, while recommendations receive no factual support
score. These conservative caps prevent a strong source observation from silently converting an
uncertain business interpretation into apparent high-certainty knowledge. They are governance choices,
not empirically measured probabilities of truth.

## 9. Source Quality

Source assessment considers method transparency, reliability, relevance, directness, independence,
freshness and usage rights. Source reliability creates a ceiling for the attached evidence record.
Origin groups prevent repeated copies of one source from being counted as independent support.
However, identifying independent origins remains a reviewer task: the tools do not authenticate
publisher ownership or detect every syndicated relationship. A URL does not prove factual truth.
A file hash proves local integrity of the referenced bytes, not publisher authenticity, source
permission or semantic accuracy. Rights review is separate from reliability; a useful observation
may still be inappropriate to archive or distribute without permission.

## 10. Confidence Assessment

Observation strength sums heuristic points for reliability, freshness, directness, independent
corroboration and relevance. The nominal allocations are 25, 20, 20, 20 and 15 points. Additional
rules constrain weak, speculative, unverified, indirect or stale observations. Claim confidence
follows the weakest critical supporting observation; if none is marked critical, it follows the
weakest support. A lack of support produces zero. Material business-object confidence follows the
weakest referenced material claim. Confidence scores are not probabilities. The numerical ordering
supports review discipline and comparison within the rubric; it does not establish an empirically
calibrated chance that the claim is correct or that a business outcome will occur.

## 11. Contradictory Evidence

Contradiction is a relationship between interpretations and observations, not automatic proof that
one publisher is false. Two valid observations may describe different workflows or populations.
The framework retains both sides and records the reason for the conflict and the follow-up needed.
An unresolved contradiction caps claim confidence at 59. Counterevidence does not count as supportive
corroboration. The dashboard provides a dedicated contradiction view and keeps challenging evidence
available in claim and opportunity details. Reviewers should ask whether disagreement reflects scope,
measurement, timing or a substantive competing explanation. The software does not select a convenient
side or resolve the disagreement silently.

## 12. Information Freshness

Freshness uses a reviewed as-of date and the observation's publication date, not merely the time a
URL was accessed. Configurable windows distinguish Current, Recent, Aging and Stale, with topic-specific
thresholds for pricing, market, customer and product information. Missing publication dates remain
Unknown; refreshing scores does not invent a date or rewrite an earlier observation. Future dates
fail validation. A source refresh should create a reviewed observation, with scope and downstream
claims reconsidered. The local dashboard is a dated snapshot. It does not fetch sources in the
background or continuously determine whether external facts have changed since that date.

## 13. Research Gaps

Evidence gaps, research questions, research debt, assumptions and critical unknowns serve different
purposes. A gap identifies missing support for a claim. A question specifies an observation to seek.
Research debt records deferred work and its decision consequences. A critical unknown can block an
irreversible commitment even when the weighted opportunity index looks appealing. The registers
preserve those entries with relevant dependencies and ownership where supplied. The dashboard does
not invent missing decision links or priorities. Counts summarize recorded items only. A useful gap
statement says what evidence would change a posture, how it can be obtained and who is responsible
for deciding whether the new observation resolves the uncertainty.

## 14. Market Intelligence Architecture

Market analysis begins with category boundaries, geography, period and eligible demand. TAM, SAM
and SOM should use comparable definitions and explain exclusions. Bottom-up accounts multiplied
by realized annual spend can be more inspectable than unrelated top-down percentages, but the
quality of the inputs still requires review. Market attractiveness compares entrant appeal through
weighted ordinal factors, keeping confidence separate from business appeal. Canonical files record
the analysis and its claim references; the engine produces derived classifications. An index for an
entrant should not be silently reused for an incumbent expansion, where barriers and switching effects
may have different meanings. A changed interpretation needs a separately documented model decision.

## 15. Competitor Intelligence

Competitor comparison requires comparable tasks, segments and pricing scopes. A feature-rich rival
in another segment may not create the same pressure as an established substitute within the target
workflow. The model combines incumbent capabilities and burdens using documented ordinal inputs.
The executive card presents the strongest recorded competitor rather than averaging unrelated rivals.
Historical methodology pressure descriptors and dashboard presentation bands use different disclosed
thresholds; reviewers should name the rubric when comparing labels. Neither changes the underlying
weighted pressure calculation. Source confidence is separate and must remain visible, especially
when pricing, loyalty or distribution estimates rest on assumptions rather than direct observations.

## 16. Customer Intelligence

Customer registers connect jobs, pains, desired outcomes, purchase triggers, objections, switching
conditions and decision criteria to supporting IDs. Insights retain sample size, source quality and
bias or population limits. Convenience sampling can reveal a workflow problem without establishing
how widespread it is. A stated willingness to pay differs from an observed purchase under comparable
terms. The framework encourages explicit segment exclusions and scope so an appealing persona does
not become a substitute for research. Sensitive personal identifiers and consent records should be
kept in separately restricted storage; the public analytical register should use minimized, appropriately
pseudonymous observations. The software does not perform automatic anonymization or certify privacy compliance.

## 17. Opportunity Intelligence

Opportunity scoring separates business merit from evidence support. Nine business factors use ordinal
ratings with explicit orientation and basis records. Their original weights total 95 and are normalized
to 100 for merit. The adjusted index is merit multiplied by `0.25 + 0.75 × support/100`.
Confidence enters once. The floor keeps untested ideas visible rather than assigning a success
probability. Categories use unrounded arithmetic and remain separate from review gates. The current
dashboard varies one uncertain factor at a time by plus or minus one within the 0–5 scale, holding
support fixed. It flags rank/category changes without automatically altering a recommendation or
creating approval. Joint scenario sensitivity remains future work.

## 18. Risk Intelligence

Risk exposure combines ordinal likelihood, impact, detection difficulty, velocity and inverse
mitigation readiness with documented weights. Likelihood is a within-horizon judgment, not a
measured probability. Catastrophic impact with sufficiently material likelihood and explicit upward
overrides force Critical classification. Zero likelihood or impact produces a structural zero that
requires verification, rather than treating missing information as zero. Confidence is reported
separately and never discounts exposure. Weak threat support calls for research, not artificial
reduction of the downside index. Common causes, correlated dependencies, tail losses and residual
exposure after mitigation require additional review. The model is ordinal triage and does not compute
portfolio expected loss.

## 19. Decision Intelligence

The decision layer records alternatives, rationale, upside, downside, claims, risks, uncertainty,
owners and next validation steps. Comparison scores order feasible options within a common horizon
and resource envelope. They cannot make prohibited or infeasible actions acceptable. A bounded TEST
may reduce uncertainty at limited cost; irreversible entry, expansion or acquisition needs stronger
review conditions. Live delivery checks require input-bound sign-off, decision coverage, manual
attestations and critical-risk acceptance. A recorded APPROVED label alone is insufficient. The
framework assists decision-making but does not replace professional judgment, financing review,
legal review or the authority accountable for committing resources.

## 20. Scoring Philosophy

Scoring systems are decision-support indices. Their weights and caps encode an explicit research
rubric and governance policy, not a discovered natural law. Versioning and worked examples make
that policy inspectable. Business ratings require a basis of OBSERVATION, ASSUMPTION or UNKNOWN,
including supporting IDs, rationale and reviewer information. A score built from invented ratings
remains hypothetical even when its arithmetic is correct. Changing formulas, factors, orientations
or limits needs a methodology record and migration guidance. The framework does not claim its
chosen allocation is statistically optimal or superior to alternative rubrics. Reproducibility is
a narrower achievement than empirical validity and should be reported as such.

## 21. Avoiding False Precision

Two-decimal storage supports arithmetic reconciliation, but ordinal ratings cannot justify a
two-decimal claim about business reality. Executive views therefore use whole-point indices and
category labels, with exact stored arithmetic available for analysts. Categories are determined
from unrounded values, so a displayed value near a boundary may retain the lower category. Missing
optional values remain null and display explicit unavailable labels. A legitimate zero remains
zero. Support indices never use probability language or percent presentation. Sensitivity labels
describe tested ordinal perturbations only; they are not confidence intervals or evidence that an
untested combination of assumptions is robust.

## 22. Human Review

Sources require human semantic review. The reviewer must determine whether a statement supports
the claimed scope, whether methods and sampling are suitable, whether origins are independent and
whether usage rights allow archival or distribution. Software checks syntax, ranges, references,
dates and documented rules. It cannot infer all omitted caveats or detect intentional falsification
by a trusted operator. Review attestations bind a stated process to a snapshot but do not authenticate
the signer's identity. Clear responsibility matters more than ceremonial completion: the research
owner reviews evidence, the risk authority accepts downside and the decision owner authorizes action
within the organization’s actual authority structure.

## 23. Executive Decision Support

The executive interface answers a short sequence: what decision is proposed, what is its weakest
material support, what could invalidate it and what should be observed next? Eight overview cards
show scoped indices, freshness and registered uncertainty. The decision brief exposes the posture,
major downside, alternative, open contradictions and approval status. An analyst can then inspect
the same claim IDs rather than maintaining a separate narrative truth. The layout is designed for
rapid review, but no timed executive usability study establishes a five-minute performance claim.
Accessibility and browser checks are local observations, not comprehensive screen-reader certification
or proof that every user can interpret the controls without assistance.

## 24. Dashboard Architecture

Python validates canonical records and recalculates populated derived fields before exporting twelve
normalized JSON payloads. A manifest covers exact filenames, hashes and shared metadata. The browser
checks those values before rendering a read-only view. Source archive paths and raw bytes are not
exported; citation metadata and integrity status are available for review. Native modules implement
tables, filters, ordinal charts, evidence dialogs and fourteen routes. The local server binds
127.0.0.1 and exposes a fixed allowlist rather than mounting the repository. Full-repository data
requests reject changed inputs or archives. Already-loaded views and standalone packages remain
dated snapshots, not continuously authenticated or monitored intelligence.

## 25. Security and Privacy

Confidential research, client information, personal data, source archives and credentials require
separate handling decisions. The tools reject credential-bearing URLs, confine paths and verify
archive integrity; viewing CSV exports neutralize common formula-leading text. Dashboard text is
escaped and citations are not fetched. These controls reduce specified failure routes but do not
provide universal secret detection, source authentication, encryption or multi-user isolation.
Operators must use appropriate filesystem controls, encrypted storage, backups, retention and incident
processes. Public issue reports should contain minimal fictional reproductions. A populated live
workspace should not be uploaded as a public repository or confused with an explicitly reviewed
reading package.

## 26. Synthetic Demonstration Model

Northstar Analytics is FICTIONAL DEMONSTRATION DATA. Its company, competitors, interviews, amounts
and outcomes are invented. In the worked example, EV-001 has observation strength 75 while the
disputed CLM-001 caps at confidence 59. EV-006 counterevidence remains visible. OPP-001 business
contributions sum to 72, yielding merit `72 × 100/95`, approximately 75.789. Applying support 59
produces an adjusted index approximately 52.484, stored as 52.48 WATCH with RESEARCH REQUIRED.
The proposed research TEST is ACTION NOT APPROVED for live use. Correct arithmetic in this example
demonstrates software behavior, not evidence about any real market or organization.

## 27. Limitations

The implemented product has no external source ingestion, authenticated service, automated monitoring,
publisher authentication or empirically calibrated prediction. The schema validator supports the
closed shipped subset rather than arbitrary JSON Schema. Evidence lifecycle, field-level revision
history, observation-to-many-claim support and automated downstream impact propagation are incomplete
or planned. Existing sensitivity changes one uncertain factor at a time and holds confidence fixed.
Research counts describe registered items, not completeness. Hashes and manifests can be edited by
a trusted operator and do not authenticate provenance. The project’s local regression and print
checks do not constitute independent external security, usability or methodology assurance.

## 28. Ethical Use

Decision support should expose limits rather than exploit the authority of numerical presentation.
Do not relabel invented observations as live research, imply a convenience sample represents a
population or suppress counterevidence to obtain a stronger category. Respect source rights and
participants’ expectations about research use. Collect only necessary identifying information and
avoid publishing private commercial material. Clearly distinguish an observed statement, a derived
index and a proposed action. Explain consequential decisions through appropriate professional review
rather than delegating accountability to a score. Public visibility of this rights-reserved project
also does not create general reuse permission beyond the terms applicable to the received copy.

## 29. Future Research

Several questions require empirical study before stronger claims would be justified. Can executives
identify weak dependencies reliably under time pressure? Do analysts interpret statement labels and
confidence caps consistently? How sensitive are rankings to joint assumptions, origin-group decisions
or alternate weight allocations? What outcomes would support calibration, and under which population
and decision horizon? Answering these questions requires protocols, data collection, comparison
conditions and measured uncertainty. Outcome collection should distinguish the quality of the
analysis from organizational execution and external shocks. Future research should report negative
results and limitations instead of treating a larger dataset as automatic evidence of validity.

## 30. Roadmap

The 1.1.x proposals focus on dashboard usability, accessibility and print refinements. The proposed
1.2.0 Research Lifecycle Release addresses supersession, revision history, many-claim observation
relationships, impact propagation, normalized source editing and reviewed joint scenarios. A possible
2.0.0 operated platform would require rights-aware ingestion, authenticated access, role-based
approval, monitored updates and licensing controls. Calibration research would require longitudinal
outcomes before a calibrated-model claim. These items are PLANNED — NOT CURRENTLY IMPLEMENTED;
they are not promised delivery dates or existing services. Authentication of an operator and
authentication of a source remain different problems even in an operated system.

## 31. Conclusion

The framework’s practical contribution is a reviewable connection between observations and decisions.
It makes sources, scope, uncertainty, counterevidence, assumptions and authority visible in both
structured records and executive views. Its indices help organize judgment without replacing the
review process that gives a recommendation meaning. The implemented controls support consistency,
reproducibility and specified safety boundaries; they do not establish factual truth or guaranteed
outcomes. A disciplined operator can use the product to identify what needs further validation and
document why a commitment is or is not authorized. Future versions should deepen lifecycle controls
and test usability before expanding operational claims.

## 32. Author

Ciprian Ștefan Pleșca is the founder and principal author of Market Intelligence Vault, an independent
software researcher and product creator. No institutional affiliation, degree, employer or endorsement
is asserted. Project stewardship and release authority are described in [GOVERNANCE.md](GOVERNANCE.md).
The implemented formulas and canonical contracts are documented in [METHODOLOGY.md](METHODOLOGY.md),
[CONFIDENCE_SCORING.md](CONFIDENCE_SCORING.md), [OPPORTUNITY_SCORING.md](OPPORTUNITY_SCORING.md)
and [RISK_SCORING.md](RISK_SCORING.md). These repository files, rather than promotional claims, are
the reference for software behavior. Citation metadata is available in [CITATION.cff](CITATION.cff).

© 2026 Ciprian Ștefan Pleșca. All rights reserved.

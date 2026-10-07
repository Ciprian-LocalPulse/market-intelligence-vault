# Contributing

Market Intelligence Vault is publicly inspectable with rights reserved. Read [LICENSE.md](LICENSE.md)
before reusing code or submitting changes. Research discussion and defect reports are welcome;
public visibility is not an open-source license. Arrange permission with the maintainer for code
contributions and record the applicable terms in the pull request. Contributions retain their
existing ownership unless a separate agreement says otherwise.

## Development setup

Use Python 3.12 and Node.js 22 or later for development verification. The runtime uses Python's
standard library and native browser modules; no application package install or frontend build is
required. Clone the repository, read [QUICK_START.md](QUICK_START.md), then run the fictional
baseline before creating an engagement. Do not put private research in the public checkout.

## Conventions

Preserve numbered production areas, stable IDs, exact CSV header order, UTF-8 and ISO dates.
Canonical data contracts own required fields, types, ranges and joins. Null and zero have different
meanings. Keep sample labels, counterevidence and provenance intact. Do not edit generated dashboard
JSON as the analytical source of truth. Keep changes scoped; avoid unrelated reformatting.

Use branches such as `docs/topic`, `fix/topic`, `feature/topic` or `release/github-production-readiness`.
Commits should explain the concrete behavior, for example `fix(export): reject mixed snapshot metadata`.
Do not force-push shared branches or move published release tags.

## Validation

```text
python -m unittest discover -s tests -v
python -m unittest discover -s dashboard/tests -v
node --test dashboard/tests/test_ui.mjs
python tools/validate_repository.py --as-of 2026-10-06 --audit-scores
python tools/export_dashboard_data.py --as-of 2026-10-06 --refresh
python tools/check_public_repository.py
```

The fixed date tests the fictional foundation, not contemporary live freshness. Use a reviewed
as-of date for live engagements. Document browser/print observations separately from unit tests.
Do not claim coverage, source authentication or external assurance that was not measured.

## Schema and methodology changes

Schema changes require synchronized contracts, dictionary, examples, compatibility notes and
regressions for malformed and missing data. The validator supports a closed JSON Schema subset.
Never change formulas, weights, orientations, caps or gates silently. Update the relevant methodology
guide, worked arithmetic, model version and migration notes; include before/after results and risks.
Scoring changes require maintainer approval. Distinguish presentation bands from model classifications.

## Security and review

For paths, URLs, archives, export fields or sign-off changes, document the trust boundary and an
adversarial regression. Report vulnerabilities privately through [SECURITY.md](SECURITY.md).
Every PR should use the template, describe tests and documentation, and identify security,
methodology and breaking-change impact. The maintainer reviews contributions and authorizes releases.
Approval of a code change is separate from approval of a business recommendation.

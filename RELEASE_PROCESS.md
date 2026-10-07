# Release process

## Prepare and verify

Read VERSION and the existing history; never invent a version. Preserve canonical schemas, models,
tests and release evidence. Refresh scores only when reviewed inputs change. Run both Python suites,
Node tests, score/schema validation, public repository checks and dashboard export. Inspect screenshots,
print output, secret-scan findings, files to be staged and each distribution's scope. Do not publish
private engagements, raw live archives, credentials, caches or scratch logs.

Document changes, limitations, upgrade notes and methodology versions. A formula change needs its
own documented model decision. Confirm citation/release version and copyright. Each package needs an
exact inventory and checksums; integrity does not establish authenticity. Keep full development
releases separate from explicitly reviewed client reading snapshots.

## GitHub publication

The only destination is `https://github.com/Ciprian-LocalPulse/market-intelligence-vault.git`.
Run `git remote -v` and inspect the authenticated owner's access, branch protection and repository
rulesets. If direct main push is explicitly permitted and appropriate, a normal fast-forward push is
allowed. Otherwise push a reviewed release branch and open a PR against main. Never disable rules,
force-push, rewrite history or force-move a published tag. An inability to inspect rules is not permission
to assume main is unprotected.

Use an accurate commit message such as `docs(release): prepare Market Intelligence Vault for public GitHub release`.
After the accepted commit is on the appropriate release history, inspect existing tags/releases before
creating `v1.1.0`. Do not recreate an existing release under that name. Use the prepared notes at
`docs/releases/GITHUB_RELEASE_1.1.0.md`; title: Market Intelligence Vault v1.1.0 — Interactive Intelligence Release.

## Post-publication

Check the destination, commit and branch, README rendering, image paths, Mermaid diagrams, links,
version/tag target and actual workflow results. Record observable URLs and outcomes; do not describe
queued workflows as passed. A publication deferred by the owner remains local preparation, not a
published GitHub release. Private vulnerability reporting and Discussions require owner configuration;
verify them before claiming availability.

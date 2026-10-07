# Security and privacy

## Trust boundary

This is local Python software for a controlled research workspace. It is not a secure multi-tenant
service and does not authenticate publishers, detect all fabricated statements, encrypt files or
establish a signer's real identity. Trusted operators can alter code or falsify attestations.
Controls detect specified structural mistakes and bind an approval record to a particular input
snapshot. A checksum demonstrates byte integrity, not truth, permission or signer authenticity.

## Client information

Minimize personal data. Use pseudonymous research identifiers and keep names, contact details,
consent records and raw recordings in a separately restricted store. Record aggregate workflow
observations in this repository. Treat private commercial data as confidential even when it contains
no PII. Before collecting it, document purpose, access, consent where relevant, retention, deletion,
source terms and approved recipients. Obtain specialist guidance when those obligations are unclear.

Use a workspace with organization-approved access controls, encrypted storage and backups. The
tools inherit the operating system's permissions; they do not configure ACLs or encryption.
Share only a reviewed delivery package, not the working directory. The full software release contains
synthetic content; a populated engagement may contain confidential inputs and must be handled separately.

## Source URLs and archives

Never retain usernames, passwords, access tokens, API keys or signed credential query strings in
URLs. Use a stable public citation URL and record restricted access without copying credentials.
LIVE data refuses reserved placeholder hosts and known fictional archive markers. HTTP(S) URLs are
validated syntactically and are never fetched by these tools. No SSRF-capable fetcher is included.

Archive references must remain inside the repository and use canonical relative paths. Store a
SHA-256 hash for each archive; alteration invalidates validation. A hash does not authenticate the
publisher. Third-party archives require rights review. Live source archives are excluded from delivery
by default; distributing one requires explicit allowlisting and a rights/privacy attestation.

## Delivery boundary

`config/delivery_policy.json` is an explicit file allowlist. Unlisted notes and unexpected files
cannot be copied into a package. Do not approve directories, wildcard paths, credential files,
executables or databases. Every live delivery needs named sign-off, all manual review attestations,
exact decision coverage and an input digest. Changed inputs invalidate that sign-off. Critical risks
require dated acceptance by a named authority. Irreversible commitments need reviewed support and
resolved critical uncertainty. A TEST must have a positive explicit cap.

CSV exports neutralize leading formula text with an apostrophe. This protects the common spreadsheet
formula-entry route; it is not a guarantee about every viewer, encoding or future import. Numeric inputs
remain numeric. Exported CSVs are viewing copies; canonical CSVs retain original text in the controlled
repository. Never feed viewing copies back into the scorer as authoritative records.

## Local files, temporary data and logs

Contract, archive and output paths are confined to the repository. Linked paths, traversal and
absolute contract paths are refused. A staging directory is created only after validation; a failed
build removes only its own checked stage. An interrupted score refresh leaves `.score_transaction/`
with sensitive backups. Validation blocks further delivery until recovery. Restrict access to it,
run recovery, then validate. Recovery is not a concurrent-edit merge mechanism.

Normal logs identify file and field errors without dumping row content. Do not paste source archives,
raw interviews or token-bearing exceptions into tickets. Inspect any future integration's logging and
telemetry separately. Tests use temporary copies under the release's parent directory and remove them
after execution; abrupt process termination can leave temporary data for authorized cleanup.

## Incident response

Stop distribution when a package includes unintended data or a source hash changes unexpectedly.
Preserve the affected snapshot, restrict access, identify recipients, notify the responsible owner,
and follow the organization's incident/retention process. Rebuild only after a reviewed correction.
Regenerate sign-off and checksums. Do not claim deletion from recipients based solely on local removal.

## Public source repository and dashboard

Public repository checks scan the declared release files and all non-ignored source files for
common credential patterns, credential-bearing URLs, accidental environment files and private-data
paths. This is a conservative pattern check, not complete secret or PII detection. Test fixtures
contain deliberate fictional credential URLs used to prove rejection; any exception is restricted
to the exact known fixture value and reported separately. Human review is still required before staging.

Real engagement directories, local archives, credentials, logs and score/export staging are ignored;
ignoring a path does not secure it or remove an already tracked file. Keep real client work in a
separately restricted store outside this public checkout. The historical synthetic source artifacts
are retained because they are required to verify the demonstration, and are explicitly fictional.

The dashboard serves exact local assets and twelve JSON projections plus a manifest. It omits archive
paths and raw bytes; text is escaped, citations are not fetched and mixed/unsafe data fails export.
The local server is not authenticated; do not expose it through a reverse proxy. Standalone snapshots
cannot inspect an absent repository. Default-browser port restrictions may require a different local
port, never weaker network protections. Disclosure guidance is maintained separately in SECURITY.md.

Encryption, key management, backups, filesystem access, log retention, sharing review and incident
response remain operator responsibilities. No ISO, SOC 2, GDPR or other certification is represented.

# Citation policy

## Traceability contract

Use `SRC-` for sources, `EV-` for observations, `CLM-` for claims and `DEC-` for recommendations.
IDs are stable across refreshes. In prose cite `[CLM-001; EV-001; SRC-001, paragraph 1,
published 2026-09-20, accessed 2026-10-06]`; use a descriptive hyperlink to the archive or actual
source page as well. A bare URL does not explain what it supports.

The source library owns title, URL, publisher, publication/access dates, origin group and archive
reference. Evidence stores a snapshot of that metadata; the validator checks the snapshot matches.
For a changed publication, append a new source/evidence ID and retire the previous interpretation.
The claim map records supports, contradicts or context. Context is never counted as critical support.

Quotes use exact wording and locators. Summaries identify themselves as summaries. Cite calculation
inputs and assumptions for estimates, not only the final number. Preserve source rights and do not
redistribute third-party archives without permission. Paywalled material requires an authorized
archive reference and a note about access restrictions.

Synthetic samples use `synthetic://` identifiers that resolve to local fictional artifacts, never
invented public websites. They are permitted only on FICTIONAL SAMPLE records. A live source must
use an actual HTTP(S) URL; offline audits do not prove it remains reachable or true.

## Archive integrity in 1.0.1

Each source has archive_sha256. Replacing archived bytes requires a reviewed source revision and
updated hash, not an access-date refresh. Hash integrity does not verify the publisher. LIVE source
archives remain private by default; the client-facing citation may reference a controlled archive
that is not included in the reading package. Explain this boundary in the delivery manifest.

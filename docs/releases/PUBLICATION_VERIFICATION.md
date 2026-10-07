# Publication and CI repair verification

Product 1.1.0; scoring model 1.0.1. Local CI repair verified on 2026-10-07.
The owner's GitHub repository is already published. The failing commit
`2b69ab5410c4cda3147f7a2fca22a5df15181405` omitted the checker called by CI.
This repair keeps the workflow step and adds its standard-library implementation.

## Executed checks

- Public repository checker: PASS, zero errors; all 228 public files inventoried.
- Repository suite: 86 passed (68 existing tests and 18 new publication regressions).
- Dashboard export suite: 18 passed. JavaScript UI suite: 11 passed. Total: 115 passed.
- Canonical schema, reference and recomputed-score audit: zero errors.
- The required hero PNG is present; stale missing-image notices were removed.
- Required release documents and top-level citation version agree with VERSION.
- Markdown inline/reference/HTML links and images are checked, including exact path casing,
  confinement and linked paths. All public Markdown documents are inspected.
- Git inventory includes tracked files even when ignored. Missing Git inventory fails closed.
- Environment files, private keys, private directories and obvious credential patterns are blocked.
  Four exact existing synthetic credential-URL fixtures are allowlisted by path and value;
  other test files and production files receive no blanket exemption. Values are redacted.
- Git attributes preserve exact bytes for six synthetic archives and thirteen dashboard JSON files.
  Staged Git objects match those files byte-for-byte. A fresh export of the reviewed Git index
  passed the same public checker, canonical audit and snapshot hash verification.

## Limits and status

Local runtime: Python 3.12.14 on Windows; Node.js 24.19.0. GitHub Actions specifies Python 3.12
and Node 22 on Ubuntu. The owner authorized publication on `main`, the first `v1.1.0` tag,
and a release package after local verification. Remote execution and conclusions are recorded by
[GitHub Actions](https://github.com/Ciprian-LocalPulse/market-intelligence-vault/actions/workflows/ci.yml).
Local verification alone is not a claim that a remote job passed. Release creation follows
verification of the actual remote job. Existing owner edits and commit history are preserved.

Pattern checks are not exhaustive secret/PII assurance, source authentication, a complete Markdown
parser, CFF schema validation or browser rendering. Business examples remain FICTIONAL DEMONSTRATION
DATA as of 2026-10-06. Validation timestamps do not make those observations contemporary.
Production formulas, schemas, policies and analytical values are preserved. New dashboard export
timestamps and manifest hashes reflect reviewed local documentation/inventory changes.

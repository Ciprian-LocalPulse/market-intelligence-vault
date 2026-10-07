# Security policy

## Supported scope

The current reviewed code baseline is release 1.1.0 using scoring model 1.0.1. Fixes are prioritized
for the current release; 1.0.0 and 1.0.1 records are historical review evidence. No support contract,
response-time SLA, certification or independently operated security team is claimed.

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/Ciprian-LocalPulse/market-intelligence-vault/security/advisories/new)
when the repository's owner has enabled it. Its availability has not yet been verified. If unavailable,
ask the maintainer for a private reporting channel without publishing exploit details, credentials or
confidential data. Do not send a vulnerability to a personal email not designated for this project.

Include affected version/commit, platform, component, preconditions, a minimal synthetic reproduction,
expected/actual behavior, potential impact and suggested mitigation. Redact tokens, identities,
client names and raw research. Provide sample payloads that contain only fictional data.

## Response and disclosure

The maintainer triages the report, assesses scope, reproduces it privately, prepares a fix with
regressions and coordinates a release/advisory where warranted. Timing depends on availability and
severity; no guaranteed acknowledgment or remediation deadline is promised. Coordinate disclosure
to allow mitigation and avoid disclosing sensitive inputs. Never claim recipient copies were deleted
solely because local files were removed.

## Boundaries

This is local software for trusted operators. It does not authenticate publishers or signers,
encrypt research, enforce multi-user roles or protect against an operator who changes the code.
The server binds loopback and serves an exact allowlist. Hashes verify bytes, not truth. See
[SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) for archive, URL, export and sign-off controls.

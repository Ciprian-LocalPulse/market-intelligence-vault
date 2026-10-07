# Quick start

Run commands from the full source repository. Python 3.12 is the verified runtime; runtime tools use
the standard library. Node.js 22 or later is only needed for developer UI tests. No application
dependency installation, cloud account or internet connection is required for the local dashboard.
The supplied baseline is FICTIONAL DEMONSTRATION DATA, fixed at 2026-10-06.

## Read the demonstration

```text
python tools/validate_repository.py --as-of 2026-10-06 --audit-scores
python dashboard/launch_dashboard.py
```

Open http://127.0.0.1:8765/. Use `--port 8766` if that port times out locally. Ctrl+C stops the server.
Do not open HTML as a file. The launcher validates/refreshes dashboard JSON before serving its exact
allowlist. The dashboard/README.md file in the full repository explains interactions and print mode.

## Verify development

```text
python -m unittest discover -s tests -v
python -m unittest discover -s dashboard/tests -v
node --test dashboard/tests/test_ui.mjs
python tools/check_public_repository.py
python tools/export_dashboard_data.py --as-of 2026-10-06 --refresh
python tools/check_sources.py --as-of 2026-10-06
```

Offline source-audit exit 0 means completion, not absence of findings. `--strict` returns 1 when
review findings exist; malformed input returns 2. Tests deliberately use fictional data and a fixed
date. They are software regressions, not measurements of a live market or external model calibration.
The public preparation checker is available in the full developer repository only.

## Recompute or package

```text
python tools/calculate_scores.py --as-of 2026-10-06
python tools/validate_repository.py --as-of 2026-10-06 --audit-scores
python tools/build_delivery_package.py --mode foundation --as-of 2026-10-06 --output delivery_review
python tools/verify_package.py delivery_review
```

Choose a new output name each time; existing packages are not overwritten. A reading package excludes
developer tools and tests. Do not run these commands inside that package. Sanitized CSVs are viewing
copies, not canonical inputs. Interrupted refresh requires `calculate_scores.py --recover`, then validation.

## Start private research

Use `python tools/initialize_engagement.py --output engagement_new` to create a separate header-preserving
blank engagement. The foundation remains unchanged. Move the engagement to a restricted non-public
workspace before entering real research. Set dashboard_config.json to its explicit engagement identity
and sample mode, then export/launch it; copied demonstration JSON is not new engagement evidence.
Enter real sources/rights/archive hashes, observations, claims/maps, business objects and factor bases,
then follow [USER_GUIDE.md](USER_GUIDE.md) and the live delivery gates. Never relabel fictional content LIVE.

# Market Intelligence Vault — interactive dashboard

Version 1.1.0, Interactive Intelligence Release. Scoring model remains 1.0.1.

## Launch from the full repository

```text
python dashboard/launch_dashboard.py
```

Open http://127.0.0.1:8765/ in your browser. Use `--port 8766` if needed, or `--open` to open the browser.
Ctrl+C stops the server. Python 3.12 is the verified runtime. No package installation or internet is required.
The release preview on this workstation was verified on port 8766; use `--port 8766` if port 8765 times out.
Do not open index.html as a file: browser modules and integrity-checked JSON require the local server.
The launcher validates and refreshes the dashboard export, then serves only explicit dashboard files.

To export explicitly at the stored demonstration date:

```text
python tools/export_dashboard_data.py --as-of 2026-10-06 --refresh
```

For a live project, refresh canonical scores first for the intended review date, replace
`config/dashboard_config.json` with explicit LIVE engagement metadata, and complete the existing review workflow.
No fictional business records may be relabeled as live. An unapproved LIVE working snapshot remains visibly unapproved.

## Standalone dashboard snapshot

From inside the dashboard folder in the standalone ZIP:

```text
python launch_dashboard.py --snapshot-only
```

This validates exported inventory and hashes but cannot inspect an absent working repository.
It is a dated reading snapshot, not continuous approval verification. Historical approval expires in presentation.
The bundled Northstar Analytics case is prominently **FICTIONAL DEMONSTRATION DATA**.

## Use

Start in Executive Overview, then Decision Brief. Open Evidence to trace a claim to supporting and
contradictory observations; use Contradictions for unresolved conflicts. Opportunity detail provides
factor provenance and single-factor ±1 sensitivity. Source URLs are text citations and are never fetched.
Sort using table heading buttons, search records and select filters. Clear filters to restore all rows.
Explore buttons and native detail dialogs work with keyboard navigation; Escape closes a dialog.
Print / Save PDF prints the current overview or decision brief without navigation. Select A4 with backgrounds optional.

## Trust limits

Confidence is a support index, not a probability. Categories use unrounded arithmetic; executive displays
use whole points. Optional unavailable values remain null and render No data available. Risk confidence
does not discount exposure. Source identity, rights, omitted facts and signer identity require human review.
No raw archives, repository routes, web scraping, trackers, remote fonts, CDNs or external ingestion are provided.
Do not expose this local server through a reverse proxy or change its loopback binding.

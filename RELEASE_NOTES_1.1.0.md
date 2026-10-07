# Release notes — Market Intelligence Vault 1.1.0

Interactive Intelligence Release · 2026-10-07. Scoring model: unchanged 1.0.1.

Adds a local-first executive HTML interface with 14 sections, eight overview cards, decision safety,
sortable/filterable tables, claim and opportunity drilldown, contradiction monitor, source-quality review,
ordinal risk matrix, factor provenance and ±1 sensitivity. Whole-point executive indices retain exact
stored arithmetic in drilldown; categories remain based on unrounded calculations.

New standard-library exporter generates 12 normalized JSON files and an integrity manifest. Optional
missing values stay null, known demo markers remain explicit, live approval uses unchanged 1.0.1 gates.
Loopback server has a fixed static/data allowlist, no repository/archive access and restrictive content policy.
System fonts, semantic navigation, keyboard controls, responsive layouts and print CSS are included.

Canonical CSVs, six schemas, scoring policy/model, privacy controls and original delivery allowlists are
unchanged. Northstar Analytics remains FICTIONAL DEMONSTRATION DATA and ACTION NOT APPROVED.
No source ingestion, external fetching, authenticated service, real-time monitoring, empirical calibration
or source/signer authentication has been introduced. Existing audit limits remain in force.

Launch `python dashboard/launch_dashboard.py` from the full repository. A standalone reading snapshot
uses `python launch_dashboard.py --snapshot-only` from its dashboard folder. Review the architecture,
data contract and verification before distributing a populated engagement.

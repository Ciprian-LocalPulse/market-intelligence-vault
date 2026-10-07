# Dashboard specification

## Views

Executive: proposed/approved decisions, confidence, commitment cap and as-of date.
Opportunity: adjusted score, raw score in the scorecard, category, gate and owner.
Competitor: pressure and confidence side by side; high pressure means stronger threat.
Risk: exposure, class, confidence, trigger and owner. Low confidence does not make a threat green.

All four CSV views are derived by `calculate_scores.py` from canonical inputs. Never edit them
directly. Recompute before delivery and use one as-of date. Unknown values remain visible; no
zero-fill. Filter by sample_status and scope. Do not combine live and synthetic records.

## Interaction contract for a future UI

Click a finding to show claim → mapped supporting/contradicting evidence → source locator.
Filter by domain, owner, confidence, freshness, decision gate and status. Show unresolved
contradictions and research debt above attractive rankings. Display score components on hover
or expansion. Sort ranking ties by stable ID. A stale view must display last computed date and
require refresh before export. Avoid composite averages across unrelated market scopes.

## Status meaning

✓ reviewed verification; △ incomplete or limited evidence; ! risk; ? unknown. Use text labels
in exports so color is never the sole carrier of meaning. These are status indicators, not
approval badges. No live GUI is included in the foundation release.

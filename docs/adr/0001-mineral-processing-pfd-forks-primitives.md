# `mineral-processing-pfd` forks the SVG primitives instead of importing `pfd-generator`'s

`.github/workflows/package-skills.yml` zips each `skills/<name>/` folder independently, and skills are installed or uploaded one at a time (a single `.zip` per skill in claude.ai, or `/plugin install <skill>` for one skill's folder in Claude Code). A skill folder is never guaranteed to have siblings present at install time, so `mineral-processing-pfd/scripts/` cannot import `../pfd-generator/scripts/pid_lib.py` — that path simply won't exist when the skill is distributed standalone.

**Decision:** `mineral-processing-pfd` carries its own copy of the generic drawing primitives (`pipe`, `sig`, `bubble`, `legend`, etc.) inside its own `scripts/` folder, forked from `pid_lib.py` rather than imported from it. The two copies are expected to drift over time; that's an accepted cost of each skill needing to work when installed alone, not an oversight to "fix" by wiring in a cross-skill import.

## Status

Accepted.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of [Claude Skills](https://code.claude.com/docs/en/skills) that encode chemical/process manufacturing engineering practices, packaged as a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) and also distributable as standalone `.zip` uploads for claude.ai. There is no application code to build or run — the "product" is the skill instructions themselves plus the deterministic scripts a skill calls out to.

## Repo layout

```
.
├── .claude-plugin/marketplace.json   plugin catalog — one entry per skill, plus an "all skills" bundle
├── skills/<skill-name>/
│   ├── SKILL.md                      the workflow Claude loads (YAML frontmatter + instructions)
│   ├── references/                   lookup tables / standards detail, loaded on demand (cheap to make long)
│   ├── scripts/                      deterministic code the skill calls (e.g. an SVG-drawing library)
│   └── examples/                     one or two real sample outputs
├── templates/skill-template/         scaffold for a new skill (kept outside skills/ so it never loads as real)
└── .github/workflows/package-skills.yml   zips each skills/* folder and publishes to the rolling `skills-latest` GitHub release
```

Currently the only shipped skill is `pfd-generator` (generates conceptual PFDs/P&IDs as hand-authored, editable SVG plus the Python script that produced them).

## How a skill works

Claude reads only a skill's YAML frontmatter (`name`, `description`) by default. When `description` matches the user's request, Claude loads the full `SKILL.md` body and any `references/`, `scripts/`, `examples/` files on demand. Skills are not manually invoked — the `description` field does the entire job of getting a skill triggered, so it must name concrete triggers (equipment, standards, deliverables, file types), not vague claims.

## Adding or editing a skill

Follow `CONTRIBUTING.md`. In short:

1. `cp -r templates/skill-template skills/<kebab-case-name>` — folder name and the `name:` field in `SKILL.md` must match exactly.
2. Write `description` as *what it does* + *when to use it*, using the literal words a user would type.
3. Structure the body: non-negotiable output rules first, then numbered workflow steps, then a "what this does not do" section.
4. Put anything deterministic in `scripts/` (with `scripts/requirements.txt` if it has dependencies) rather than re-deriving it in prose each session. Put lookup/standards detail in `references/`, not in `SKILL.md` — length is cheap there, expensive in the main instructions.
5. Every skill must include a **verification step**: render, run, or check its own output and iterate rather than produce-and-stop. See `pfd-generator/SKILL.md`'s "Render, look at it, and fix — then repeat" step for the pattern (renders the SVG to PNG via `cairosvg`, falls back to `svglib`+`pymupdf` when native Cairo isn't available, and explicitly warns that the fallback silently drops arrowhead `<marker>`s — that's a rendering artifact to verify from source, not a defect to "fix").
6. Register the skill in two places: an entry in the `plugins` array of `.claude-plugin/marketplace.json` (copy the `pfd-generator` entry's shape — `source: "./"`, `skills: ["./skills/<name>"]`, `strict: false`), and a row in the README skills table.
7. Test by installing locally (`/plugin marketplace add /path/to/this/repo` then `/plugin install <skill-name>@chem-mfg-skills`) and confirming it triggers on its own, without naming it, in a fresh session. If it doesn't trigger, the problem is the `description`, not the body.

Every skill's output is explicitly conceptual/engineering-support work, not issued-for-design, hazard analysis, or equipment sizing — each `SKILL.md` states this limit and is expected to say so to the user when their framing implies otherwise.

## Packaging / CI

`.github/workflows/package-skills.yml` runs on pushes to `main` that touch `skills/**`: it zips each `skills/<name>/` folder (zip root = the skill folder itself, so claude.ai finds `SKILL.md` one level in) and uploads to the rolling `skills-latest` GitHub release, which is what the README's direct-download links point at. No manual release step is needed after merging a skill change.

## Working with the pfd-generator skill specifically

- Drawing primitives live in `skills/pfd-generator/scripts/pid_lib.py` (`PID` class: `vessel`, `pipe`, `bubble`, `cvalve`, `sig`, `agitator`, `steam_trap`, `line_jump`, `legend`, `txt`, …) — read it and reuse it rather than hand-rolling SVG.
- ISA-5.1 symbol/tag conventions are in `skills/pfd-generator/references/isa-conventions.md`; collision/layout geometry rules are in `skills/pfd-generator/references/layout-rules.md`.
- Render workflow needs `pip install -r skills/pfd-generator/scripts/requirements.txt` (add `--break-system-packages` on a managed Python). Preferred renderer is `cairosvg` (needs native Cairo/GTK, often unavailable on Windows); fallback is `svglib` + `pymupdf`, which drops SVG arrowhead markers.

## Agent skills

### Issue tracker

Issues live as GitHub issues on your fork, `octaviodeliberato/claude-manufacturing-skills` — not `upstream` (`ScottDuncanAI/claude-manufacturing-skills`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.

# Adding a skill

## 1. Create the folder

```bash
cp -r templates/skill-template skills/<your-skill-name>
```

Use kebab-case. The folder name and the `name:` field in `SKILL.md` must match exactly.

## 2. Write the frontmatter

```yaml
---
name: relief-valve-sizing
description: <what it does> ... Use when <the situations that should trigger it>.
---
```

`description` is the only thing Claude sees before deciding whether to load the skill, so it does the entire job of getting the skill invoked. Write it as **what it does + when to use it**, and name the concrete words a user would actually type — equipment, standards, deliverables, file types. "Helps with relief valves" will never trigger; "Size a pressure relief valve per API 520/521 for fire, blocked outlet, or thermal expansion cases. Use when the user mentions PSV sizing, relief load, or set pressure" will.

## 3. Structure the body

- **`SKILL.md`** — the workflow. Keep it to what's needed every time. Non-negotiable rules first, then numbered steps, then a short "what this does not do" section that states the limits of the deliverable.
- **`references/`** — lookup tables, standards detail, worked conventions. Loaded on demand, so length is cheap here and expensive in `SKILL.md`.
- **`scripts/`** — anything deterministic. Code that always runs the same way should be code, not prose Claude re-derives each session. Add `scripts/requirements.txt` if it has dependencies.
- **`examples/`** — one or two real outputs. These make the repo legible to anyone browsing GitHub.

Two things that separate a skill that works from one that doesn't:

- **Build in a verification step.** Have the skill render, run, or check its own output and iterate — not just produce and stop.
- **State the limits explicitly.** Every skill here produces conceptual work. Say so inside the skill, so Claude says so to the user.

## 4. Register it

Two edits, both small:

1. Add an entry to the `plugins` array in `.claude-plugin/marketplace.json`, copying the shape of the `pid-generator` entry (`"source": "./"`, `"skills": ["./skills/<your-skill-name>"]`, `"strict": false`).
2. Add a row to the skills table in `README.md`.

## 5. Test it

Install locally and confirm it triggers on its own — without you naming the skill:

```
/plugin marketplace add /path/to/this/repo
/plugin install <your-skill-name>@chem-mfg-skills
```

Then, in a fresh session, describe a task it should handle and check that it loads. If it doesn't, the `description` is the problem, not the body.

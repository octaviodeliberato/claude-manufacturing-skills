# Chemical Manufacturing Skills for Claude

A collection of [Claude Skills](https://code.claude.com/docs/en/skills) that encode chemical manufacturing engineering practices so that Claude produces work a practicing engineer would actually accept, rather than something that merely looks plausible.

A general-purpose model asked to draw a P&ID will happily put a steam coil above the liquid level, leave a control loop open, or hide a tag under a valve body. The point of a skill is to carry the standards and the review checklist into the session with the request, so those defects get caught before you ever see the output.

## Scope and disclaimer

Everything here produces **conceptual, engineering-support output**. Every output requires review by a qualified SME before it informs a real decision.

## Skills

| Skill | Produces | Triggers on |
|---|---|---|
| [`pid-generator`](skills/pid-generator) | A conceptual P&ID as editable SVG, plus the Python script that generated it | A process description with a request to draw, diagram, sketch, or visualize it; any mention of P&ID, PFD, control loop drawings, or cascade control; a request to edit an existing P&ID SVG |

See [`skills/pid-generator/examples/`](skills/pid-generator/examples) for sample output.

## Install

**As a plugin (recommended).** Adds the skills to Claude Code and keeps them updated with `git pull` on your side:

```
/plugin marketplace add ScottDuncanAI/claude-manufacturing-skills
/plugin install pid-generator@chem-mfg-skills
```

Use `/plugin install chem-mfg-skills-all@chem-mfg-skills` to get every skill in the collection, including ones added later.

**Manually, for yourself.** Copy any skill folder into your personal skills directory:

```bash
cp -r skills/pid-generator ~/.claude/skills/
```

**Manually, for a project.** Copy it into the project so everyone working in that repo gets it:

```bash
cp -r skills/pid-generator <your-project>/.claude/skills/
```

Restart Claude Code after copying. Some skills carry Python dependencies — check for a `scripts/requirements.txt` inside the skill folder.

## What is a skill?

A skill is a folder containing a `SKILL.md` file with a short YAML header and a set of instructions. Claude reads only the header by default; when the `description` matches what you're doing, it loads the full instructions and any supporting reference files, scripts, or templates in that folder.

Practically: you don't invoke a skill. You describe your problem, and the right expertise loads itself.

## Repo layout

```
.
├── .claude-plugin/
│   └── marketplace.json          plugin catalog — one entry per skill
├── skills/
│   └── pid-generator/
│       ├── SKILL.md              instructions Claude loads
│       ├── references/           detail loaded on demand, not up front
│       ├── scripts/              deterministic code the skill calls
│       └── examples/             sample output
└── templates/
    └── skill-template/           scaffold for a new skill
```

One folder per skill. `templates/` deliberately sits outside `skills/` so the scaffold never loads as a real skill.

## Adding a skill

See [CONTRIBUTING.md](CONTRIBUTING.md). Short version: copy `templates/skill-template/`, write the `description` carefully, add a `marketplace.json` entry and a row in the table above.

## License

[MIT](LICENSE). The license covers the skill text and code — it does not transfer engineering judgment, and it does not make the output of these skills correct. Review before use.

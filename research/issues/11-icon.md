---
title: "docs: add an icon to the Claude Code plugin"
labels: [good first issue, docs, difficulty:easy]
difficulty: easy
effort: "a few hours"
---

## What and why
`claude plugin validate ./plugins/claude-code` passes but prints one warning:

```
⚠ .claude-plugin/plugin.json icon: No icon (ICON_MISSING). No icon found in the plugin. […]
Fix: Add a square PNG to the plugin folder at .claude-plugin/icon.png, or set `icon` in plugin.json to the path of a square PNG or JPEG in the plugin: 512 to 2048 px on each side, under 2 MB. SVG and WebP are not accepted.
```

The validator says the file may become the listing icon only the first time the plugin is saved or submitted, so it is worth getting right once.

## What to do
- Design an **original** square icon (PNG or JPEG, 512–2048 px per side, under 2 MB). It must be your own work or under a licence compatible with Apache-2.0, with no logo or trademark of any other organization. Say how it was made in the PR.
- `plugins/claude-code/` is **generated** by [`tools/build_plugin.py`](https://github.com/Joaquincuevas/clarent/blob/main/tools/build_plugin.py): do not edit it by hand. Keep the source image in the repo (for example `assets/icon.png`) and make `build_plugin.py` copy it to `plugins/claude-code/.claude-plugin/icon.png` (or set `icon` in the generated `plugin.json`), then regenerate the plugin and commit the result.

## Acceptance criteria
- [ ] `claude plugin validate ./plugins/claude-code` no longer prints `ICON_MISSING` (paste the output in the PR).
- [ ] `python tools/build_plugin.py --check` passes, and CI stays green.
- [ ] The source image and its licence/origin are recorded in the PR.

## Difficulty and time
- **Difficulty: easy.** Estimated time: a few hours (my estimate; this issue is not from the spec).
- Files: `assets/icon.png` (new), `tools/build_plugin.py`, regenerated `plugins/claude-code/`.

Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md); sign off commits (`git commit -s`).

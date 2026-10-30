# Advent of Code 2025 — Dashboard

Terminal-style progress dashboard for [Advent of Code 2025](https://adventofcode.com/2025).
Built with React 19 + TypeScript + Vite + Tailwind v4, using the
[ascii/cnlibs](https://ascii.cnlibs.com/docs) component library (shadcn-style registry,
ASCII-drawn frames) themed with canonical AoC colors and Fira Code.

## Commands (pnpm)

```bash
pnpm dev            # dev server
pnpm build          # tsc --noEmit + vite build
pnpm lint           # eslint
pnpm typecheck      # tsc --noEmit
pnpm deploy         # gh-pages publish (predeploy runs build)
```

`homepage` + vite `base` point to `/advent-of-code-2025/` for GitHub Pages.

## Data flow

- `scripts/update_progress.py` (repo root) scans `go/ python/ cpp/ dayXX/solution.*`
  and fetches puzzle titles/descriptions from adventofcode.com (needs `AOC_SESSION`
  in `../.env`), writing everything into `src/data/progress.json`.
- `src/data/stars.json` is **manual**: `{ "1": { "stars": 2 } }` per day — 0/1/2,
  scripts never overwrite it.
- Both JSON files are imported directly by the app (static GitHub Pages, no backend).

## UI

- Persistent side panel: detail panel right, calendar left (`?day=N` deep links,
  narrow screens open the panel as a slide-over Sheet).
- Day tile: title, `*` star indicator (gold = earned), language badges
  (py / go / c++, strong when both parts solved).
- Detail tabs: **task** (scraped AoC article), **solutions** (language switcher +
  highlighted viewer with per-range dimming + copy), **stats** (placeholder table
  awaiting the benchmark runner and `benchmarks.json`).
- Keyboard: `↑↓←→` select day, `esc` close.

## Theme

The `phosphor` palette from ascii/cnlibs (installed via `shadcn add
https://ascii.cnlibs.com/r/themes/phosphor.json`) is overridden in `src/index.css`
with AoC colors (`#0f0f23` bg, `#00cc00` primary, gold `#ffff66` stars via
`--aoc-star`). Font: Fira Code through `--font-ascii` (Google Fonts link in
`index.html`). Components live under `src/components/ui` + `src/components/ascii`
(owned source copied from the registry).

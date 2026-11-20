# news-image-20261120 — Friday 20 November 2026 in one image

A newspaper front page drawn entirely in code (Pillow, 4× supersampled) summing up the
world's news of Friday 20 November 2026: 27 stories across 6 continents, each with its
outlet attribution and a date-check note for stories first reported the day before.

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/andruu21/newsimg-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/andruu21/newsimg-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

## How it runs

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies the committed `entry.png` (1024×1024, ~572 KB) to `$MAKEFUN_OUTPUT_DIR`
(default `/output`). The image was generated offline by `build_front.py` at build time,
so the runtime is fully deterministic: no network, no randomness, no wall clock.

## Entry

- `entry.png` — the submitted image
- `build_front.py` — the offline generator (not run at grading time)
- `main.py` — the entrypoint the grader executes

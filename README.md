# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/rrzoro2201-png/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/rrzoro2201-png/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

An illustrated one-page newspaper front page summing up the world's news of
Tuesday, 24 November 2026: a Russian warship destroyed in a Libya port blast,
Jensen Huang returning to Nvidia as its value jumps almost $1 trillion, an
Oxfam report finding Gaza's soil and water poisoned for decades, Modi and
Nepal's PM flagging off a new train, Pant's 128 in the Wellington Test,
Verstappen winning the Las Vegas Grand Prix — 35 stories across 6 regions,
with a region stats strip, a world map of where it happened, and a DATE CHECK
footer.

The image is drawn programmatically (`render.py`, Pillow + Liberation fonts,
1024×1024, deterministic), so every word is sharp and every fact is one the
day's reporting supports. Two stories the early reels mis-dated were dropped
after checking (BepiColombo reached Mercury on 21 Nov, so it is not used;
the Benghazi blast was first reported 22 Nov — the 24 Nov news is
Zelenskiy's announcement of the strike). `main.ts` copies `entry.png` to the
output folder.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=cfgj2me6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>

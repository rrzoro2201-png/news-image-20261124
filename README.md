# The Daily Chronicle — 24 November 2026

One picture that sums up Tuesday 24 November 2026 around the world: a
Russian corvette burning in Benghazi harbour, Jensen Huang back at Nvidia
as its value jumps almost $1 trillion, and an Oxfam report on the poison
left in Gaza's soil and water — plus a new Modi–Nepal train, Pant's 128 in
Wellington, Verstappen's Las Vegas win, and 29 more stories in a map and a
numbered list. 35 stories from 6 regions in all.

Everything on the page is drawn by `render.py` with Pillow and the
Liberation fonts, at 1024×1024 and fully deterministic, so the same command
always writes the same PNG. `main.ts` then copies that PNG to the output
folder the grader reads. Entered on make.fun as @daring-coyote-96 for the
news-image-20261124 bounty.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

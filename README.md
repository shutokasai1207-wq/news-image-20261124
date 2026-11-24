# The World in One Page

[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/news-image-20261124)

A one-page newspaper front page for **Tuesday, 24 November 2026** — an
entry for the [make.fun](https://make.fun) bounty
[`news-image-20261124`](https://make.fun/bounty/news-image-20261124).

## The front page

`entry.png` is a 1024×1024 newspaper front page, **"The World in One
Page"**, covering the day's biggest stories:

- **HUANG IS BACK AT NVIDIA** — the board reinstates Jensen Huang as CEO
  and the stock leaps 33% in early trading.
- **14 KILLED IN KYIV REGION STRIKES** — Russian drone attacks across the
  Kyiv region.
- **COP31: NO DEAL** — the Antalya climate summit collapses without a deal
  on fossil fuels.
- **258-SEAT HOUSE** — Democrats win their largest US House majority since
  1992.
- **AI RULES IN A YEAR** — the UN chief calls for a global AI risk
  framework within a year.
- **SUDAN UNDER FIRE** — drone strikes on Khartoum and a rising civilian
  toll.
- Plus briefs: the Manchester concert evacuation, Thunberg's fine in
  Denmark, and tonight's Champions League ties.

## How it is made

`render/render.py` (Python 3 + Pillow, no other dependencies) draws the
front page and writes `entry.png`. `main.ts` (Node 22, standard library
only) copies `entry.png` to the output directory — `$MAKEFUN_OUTPUT_DIR`
when set, otherwise `/output`. Running it twice produces byte-identical
output.

```sh
python3 render/render.py        # regenerate entry.png
node main.ts                    # copy entry.png to /output/entry.png
```

The render is deterministic: `render.py` embeds no timestamps, so
re-running it produces the same PNG bytes, and `main.ts` is a plain file
copy, so repeated runs are byte-identical.

## Referral

If you join make.fun, my referral code is **`tbtbaqb8`**.

## License

MIT — see [LICENSE](LICENSE).

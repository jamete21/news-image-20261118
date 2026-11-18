# Sum up 18 November's world news in one image

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)

A newspaper front page summing up Wednesday 18 November 2026's world
news in a single image, built for make.fun's
["Sum up 18 November's world news in one image"](https://make.fun/bounty/news-image-20261118)
bounty ($250 in USDC).

## The image

`entry.png` (1024×1024 PNG, ~143 KB) leads with the day's biggest story —
the US strike on Iran's Qeshm Island and Iran's drone replies against
Bahrain and Kuwait — then covers the Xi–Putin meeting in Shenzhen ahead
of Thursday's trilateral summit with Trump, Ukraine's second-day strike
on the Kerch Bridge, Mary Peltola winning Alaska for a 56–44 Democratic
Senate, the Ebola outbreak in DR Congo more than doubling, and the
Siberia plane crash, the Papua New Guinea quake, Cyclone Xavier and
Nvidia's record revenue. Every headline is grounded in reporting
published on 18 November 2026 (Reuters, AP, AFP, UN, Just Security).

## Run it

```sh
python3 main.py
```

The program copies `entry.png` to `/output/entry.png`. It uses only
the Python standard library, needs no network, and writes the same
bytes on every run. `build_image.py` is the script that drew
`entry.png` (Pillow, DejaVu fonts) — re-run it to regenerate the image.

## License

MIT — see `LICENSE`.

#!/usr/bin/env python3
"""Build entry.png: a newspaper front page summing up 18 Nov 2026 world news.

Every headline is grounded in reporting from 18 November 2026:
  - US strikes Qeshm Island; Iran drones hit Bahrain & Kuwait
    (Just Security Early Edition 18 Nov 2026; Reuters; WSJ)
  - Ukraine hits Kerch/Crimea Bridge a second day; road span collapses
    (One Turn News, 18 Nov 2026; Reuters)
  - Xi hosts Putin in Shenzhen; Trump joins trilateral summit Thursday
    (Open Chronicle, 18 Nov 2026; AFP; AP)
  - Mary Peltola wins Alaska Senate seat; Democrats 56-44
    (Open Chronicle; AP; Alaska Public Media)
  - Ebola in DR Congo more than doubles: 11,000+ cases, 5,400 deaths
    (One Turn News, citing the UN)
  - Russian military plane crashes in Siberia, 19 dead
    (Horizon; Daily Baku; Nepal Times)
  - 6.0-magnitude quake in Papua New Guinea; Cat 5 Cyclone Xavier
    hits the Northern Cook Islands; Nvidia record revenue
    (Daily Baku; One Turn News; Nepal Times)

Output: 1024x1024 PNG, well under the 1 MiB limit. Deterministic:
same input, same bytes (no timestamps, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1024, 1024
PAPER = (247, 243, 234)   # newsprint off-white
INK = (22, 22, 26)        # near-black
RED = (178, 34, 34)       # headline red
TEAL = (16, 78, 90)       # gulf sea teal
GOLD = (176, 132, 24)
GREY = (96, 92, 84)
RULE = (60, 56, 50)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, color, max_w, leading=None):
    leading = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def panel(draw, x, y, w, h, label, label_color, headline, deck, hsize=30):
    """One bordered news panel with a kicker, headline and deck."""
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=label_color)
    draw.text((x + 12, y + 6), label, font=font(SANS_B, 16), fill=(255, 255, 255))
    ty = y + 44
    ty = draw_wrapped(draw, x + 12, ty, headline, font(SERIF, hsize),
                      INK, w - 24, leading=int(hsize * 1.12))
    draw_wrapped(draw, x + 12, ty + 8, deck, font(SANS, 19),
                 (52, 50, 46), w - 24, leading=24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.text((28, 22), "THE WORLD IN ONE PICTURE",
           font=font(SANS_B, 22), fill=RED)
    d.text((28, 52), "Wednesday 18 November 2026",
           font=font(SERIF, 52), fill=INK)
    d.text((28, 118), "THE DAY'S WORLD NEWS  •  ONE PAGE  •  EVERY STORY CHECKED",
           font=font(SANS_B, 17), fill=GREY)
    d.line([(28, 152), (996, 152)], fill=INK, width=4)
    d.line([(28, 160), (996, 160)], fill=INK, width=1)

    # ---- Lead story: the Gulf -------------------------------------------
    x, y, w, h = 28, 176, 968, 252
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    d.rectangle([x, y, x + w, y + 34], fill=RED)
    d.text((x + 14, y + 7), "LEAD  •  THE GULF ON THE BRINK",
           font=font(SANS_B, 17), fill=(255, 255, 255))
    ty = draw_wrapped(d, x + 14, y + 48,
                      "U.S. strikes Iran's Qeshm Island — Iran hits back at Bahrain & Kuwait",
                      font(SERIF, 40), INK, w - 28, leading=46)
    draw_wrapped(d, x + 14, ty + 10,
                 "U.S. jets hit a Revolutionary Guard missile site on Qeshm Island in the "
                 "Strait of Hormuz. Iran answered with drones aimed at U.S. bases in "
                 "Bahrain and Kuwait, its third attack there in under a week.",
                 font(SANS, 21), (52, 50, 46), w - 28, leading=27)

    # ---- Row 2: Shenzhen summit + Kerch Bridge --------------------------
    panel(d, 28, 444, 476, 218, "DIPLOMACY  •  SHENZHEN", TEAL,
          "Xi hosts Putin — Trump joins them Thursday",
          "Xi and Putin met in Shenzhen a day before a three-way summit "
          "with Trump on Ukraine, Iran and trade.")
    panel(d, 520, 444, 476, 218, "WAR  •  UKRAINE", (90, 40, 40),
          "Kerch Bridge hit again — road span falls",
          "Ukraine struck the Crimea bridge for a second day; part of its "
          "road span collapsed into the strait.")

    # ---- Row 3: Senate, Ebola, Also today -------------------------------
    panel(d, 28, 678, 312, 236, "U.S. SENATE", (38, 68, 38),
          "Peltola wins Alaska — Democrats take a 56–44 Senate",
          "Peltola beat Dan Sullivan to flip the Senate.",
          hsize=27)
    panel(d, 356, 678, 312, 236, "HEALTH  •  CONGO", (96, 52, 8),
          "Ebola outbreak more than doubles",
          "DR Congo: 11,000+ cases and 5,400 deaths, the UN says.",
          hsize=27)

    # Also-today panel (custom: a bulleted list, no headline wrap)
    x, y, w, h = 684, 678, 312, 236
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    d.rectangle([x, y, x + w, y + 30], fill=(52, 50, 46))
    d.text((x + 12, y + 6), "ALSO TODAY", font=font(SANS_B, 16), fill=(255, 255, 255))
    items = [
        "Russian military plane crashes in Siberia — 19 dead",
        "6.0 quake hits Papua New Guinea",
        "Cat. 5 Cyclone Xavier hits the Cook Islands",
        "Nvidia posts record revenue",
    ]
    iy = y + 44
    for item in items:
        d.text((x + 12, iy), "•", font=font(SANS_B, 18), fill=RED)
        iy = draw_wrapped(d, x + 30, iy, item, font(SANS, 17),
                          (52, 50, 46), w - 42, leading=21)
        iy += 5

    # ---- Footer ---------------------------------------------------------
    d.line([(28, 936), (996, 936)], fill=INK, width=2)
    d.text((28, 950),
           "Sources: Reuters  •  AP  •  AFP  •  UN  •  Just Security  —  18 November 2026",
           font=font(SANS, 17), fill=GREY)
    d.text((28, 974),
           "Every headline above is from reporting published on 18 November 2026.",
           font=font(SANS, 17), fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

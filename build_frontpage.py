#!/usr/bin/env python3
"""Compose the front page for Wednesday 18 November 2026.

Builds a newspaper-style front page (1024x1024 PNG) from four
AI-generated news illustrations (no text in the pictures themselves)
plus crisp typeset headlines, so every word on the page is legible.
Run: python3 compose.py  -> writes news.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (178, 34, 34)
GREY = (90, 90, 90)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def crop_to(img, tw, th, focus_y=0.5):
    """Center-crop (with vertical focus) then resize to tw x th."""
    w, h = img.size
    target = tw / th
    if w / h > target:  # too wide: crop width
        nw = int(h * target)
        x0 = (w - nw) // 2
        box = (x0, 0, x0 + nw, h)
    else:  # too tall: crop height around focus_y
        nh = int(w / target)
        y0 = int((h - nh) * focus_y)
        box = (0, y0, w, y0 + nh)
    return img.crop(box).resize((tw, th), Image.LANCZOS)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    mx = 24
    cw = W - 2 * mx  # 976

    # Masthead
    f_mast = font(SERIF_B, 56)
    d.text((W // 2, 14), "THE WORLD IN ONE DAY", font=f_mast,
           fill=INK, anchor="ma")
    f_date = font(SANS_B, 21)
    d.text((W // 2, 82), "WEDNESDAY  ·  18 NOVEMBER 2026", font=f_date,
           fill=RED, anchor="ma")
    d.line([(mx, 114), (W - mx, 114)], fill=INK, width=4)
    d.line([(mx, 120), (W - mx, 120)], fill=INK, width=1)

    # Hero picture: Manila summit hall
    hero = Image.open(os.path.join(
        PANELS, "media-generation-hero-manila-summit-0-88550cc3-000f-4317-9c57-52c5e9dc69a4.png"))
    page.paste(crop_to(hero, cw, 296, focus_y=0.45), (mx, 130))

    # Lead headline + deck
    f_head = font(SERIF_B, 34)
    y = 436
    for line in wrap(d, "TRUMP LANDS IN MANILA AS ASIA'S LEADERS GATHER",
                     f_head, cw):
        d.text((W // 2, y), line, font=f_head, fill=INK, anchor="ma")
        y += 40
    f_deck = font(SANS, 17)
    y += 2
    for line in wrap(d, "The US president arrives for Quad talks ahead of a "
                     "China visit, as ASEAN and APEC summits crowd the week.",
                     f_deck, cw):
        d.text((W // 2, y), line, font=f_deck, fill=(60, 60, 60), anchor="ma")
        y += 22
    d.line([(mx, 552), (W - mx, 552)], fill=INK, width=2)

    # Three columns
    cols = [
        ("media-generation-gulf-strikes-0-e97a9c54-e41d-4cc0-a616-2632306c62e4.png",
         "THE GULF",
         "US strikes Iran missile site; Tehran's drones hit US radar in Bahrain",
         "Washington hits an IRGC launch site on Qeshm Island as the Gulf "
         "standoff escalates."),
        ("media-generation-crimean-bridge-0-3a3f6a29-f494-44f1-86f5-7b17da429927.png",
         "UKRAINE",
         "Kyiv hits the Crimean bridge again as Russia pounds Kyiv crossings",
         "Ukraine strikes the Kerch link for a second day; Moscow answers "
         "with attacks on Kyiv's bridges."),
        ("media-generation-cyclone-akvan-0-422e24ec-0af1-4b53-b932-d98163785ce9.png",
         "WEATHER",
         "Cyclone Akvan strengthens over the Bay of Bengal",
         "The storm is expected to become severe as it tracks towards the "
         "Indian coast."),
    ]
    col_w = 309
    gap = (cw - 3 * col_w) // 2
    f_kick = font(SANS_B, 14)
    f_chead = font(SANS_B, 20)
    f_cdeck = font(SANS, 14)
    for i, (fname, kicker, headline, deck) in enumerate(cols):
        x = mx + i * (col_w + gap)
        img = Image.open(os.path.join(PANELS, fname))
        if fname.startswith("media-generation-cyclone"):
            img = img.transpose(Image.FLIP_LEFT_RIGHT)  # Bay of Bengal east of India
        page.paste(crop_to(img, col_w, 186, focus_y=0.5), (x, 564))
        d.text((x, 756), kicker, font=f_kick, fill=RED)
        y = 778
        for line in wrap(d, headline, f_chead, col_w):
            d.text((x, y), line, font=f_chead, fill=INK)
            y += 25
        y += 4
        for line in wrap(d, deck, f_cdeck, col_w):
            d.text((x, y), line, font=f_cdeck, fill=(60, 60, 60))
            y += 19

    d.line([(mx, 918), (W - mx, 918)], fill=INK, width=2)

    # Also-today strip
    f_also = font(SANS_B, 15)
    f_ticker = font(SANS, 15)
    d.text((mx, 928), "ALSO TODAY  ", font=f_also, fill=RED)
    label_w = d.textlength("ALSO TODAY  ", font=f_also)
    ticker = ("Canada and China extend trade deals as Xi meets Carney  •  "
              "Britain sanctions Israeli settlement firms  •  Dhoni retires "
              "from the IPL to mentor Chennai  •  Baidu chief warns of an "
              "AI bubble ahead of APEC")
    y = 928
    for line in wrap(d, ticker, f_ticker, cw - label_w):
        d.text((mx + label_w, y), line, font=f_ticker, fill=INK)
        y += 20

    f_foot = font(SANS, 11)
    d.text((W // 2, 1002),
           "An illustrated summary of the news of Wednesday 18 November 2026. "
           "Pictures are illustrations of reported events.",
           font=f_foot, fill=GREY, anchor="ma")

    out = os.path.join(HERE, "news.png")
    page.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

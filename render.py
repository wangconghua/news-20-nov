#!/usr/bin/env python3
"""Render entry.png — one image summing up 20 November 2026's world news.

Programmatic PIL infographic: off-white newsprint background, dark navy
header band, 2x3 grid of story panels with flat icons, bold headlines
and one-line summaries. All facts verified from reputable news sources
on 20 November 2026 (SCMP, Just Security, One Turn, The Hindu).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)      # off-white newsprint
NAVY = (20, 33, 61)       # header band
NAVY2 = (30, 48, 88)
INK = (24, 24, 24)
MUTED = (90, 90, 84)
WHITE = (255, 255, 255)
GOLD = (201, 162, 39)
PANEL = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    return ImageFont.truetype(path, size)


F_DATE = font("NotoSans-Bold.ttf", 64)
F_KICK = font("NotoSans-Bold.ttf", 22)
F_HEAD = font("NotoSans-Bold.ttf", 29)
F_SUM = font("NotoSans-Regular.ttf", 20)
F_FOOT = font("NotoSans-Regular.ttf", 17)
F_TAG = font("NotoSans-Bold.ttf", 15)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon_summit(d, x, y, c):
    # three leaders around a table: three circles + table line
    d.ellipse([x + 6, y + 2, x + 26, y + 22], fill=c)
    d.ellipse([x + 26, y + 2, x + 46, y + 22], fill=c)
    d.ellipse([x + 46, y + 2, x + 66, y + 22], fill=c)
    d.rectangle([x + 2, y + 34, x + 70, y + 40], fill=c)
    d.line([x + 16, y + 40, x + 16, y + 58], fill=c, width=4)
    d.line([x + 56, y + 40, x + 56, y + 58], fill=c, width=4)


def icon_drone(d, x, y, c):
    # quadcopter: body + 4 rotors
    d.ellipse([x + 26, y + 26, x + 46, y + 46], fill=c)
    for cx, cy in [(x + 8, y + 8), (x + 56, y + 8), (x + 8, y + 56), (x + 56, y + 56)]:
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=c, width=3)
        d.line([cx, cy, x + 36, y + 36], fill=c, width=3)


def icon_scales(d, x, y, c):
    # scales of justice
    d.line([x + 36, y + 6, x + 36, y + 58], fill=c, width=4)
    d.line([x + 8, y + 14, x + 64, y + 14], fill=c, width=4)
    d.arc([x + 2, y + 14, x + 22, y + 40], start=0, end=180, fill=c, width=4)
    d.arc([x + 50, y + 14, x + 70, y + 40], start=0, end=180, fill=c, width=4)
    d.rectangle([x + 26, y + 58, x + 46, y + 64], fill=c)


def icon_burst(d, x, y, c):
    # explosion burst: radiating spikes from a filled core
    cx, cy = x + 36, y + 36
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 14, 32
        a = math.radians(ang)
        x1 = cx + r1 * math.cos(a)
        y1 = cy + r1 * math.sin(a)
        x2 = cx + r2 * math.cos(a)
        y2 = cy + r2 * math.sin(a)
        d.line([x1, y1, x2, y2], fill=c, width=5)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=c)


def icon_chart(d, x, y, c):
    # rising bars with an upward arrow
    d.rectangle([x + 8, y + 44, x + 20, y + 62], fill=c)
    d.rectangle([x + 26, y + 32, x + 38, y + 62], fill=c)
    d.rectangle([x + 44, y + 20, x + 56, y + 62], fill=c)
    d.line([x + 4, y + 34, x + 30, y + 22], fill=c, width=4)
    d.line([x + 30, y + 22, x + 62, y + 8], fill=c, width=4)
    d.line([x + 52, y + 8, x + 64, y + 8], fill=c, width=4)
    d.line([x + 62, y + 8, x + 62, y + 20], fill=c, width=4)


def icon_controller(d, x, y, c):
    # game controller
    d.rounded_rectangle([x + 6, y + 18, x + 66, y + 54], radius=14, fill=c)
    d.line([x + 20, y + 30, x + 20, y + 42], fill=WHITE, width=4)
    d.line([x + 14, y + 36, x + 26, y + 36], fill=WHITE, width=4)
    d.ellipse([x + 44, y + 30, x + 52, y + 38], fill=WHITE)
    d.ellipse([x + 54, y + 38, x + 62, y + 46], fill=WHITE)


STORIES = [
    ("SUMMIT", (192, 57, 43), icon_summit,
     "TRUMP, XI & PUTIN ISSUE PEACE DECLARATION",
     "Four-point joint declaration after the Shenzhen summit; Europe warns against a new Yalta."),
    ("JUSTICE", (44, 95, 158), icon_scales,
     "MYANMAR GUILTY OF GENOCIDE",
     "World Court's first genocide finding against a state, in the Rohingya case."),
    ("GULF", (14, 124, 123), icon_drone,
     "HOUTHI MISSILE HITS RIYADH TOWER",
     "Strike damages the PIF tower in the financial district; second attack this month."),
    ("EUROPE", (108, 74, 176), icon_burst,
     "RUSSIAN BARRAGE KILLS 8 IN KYIV",
     "Overnight strikes damage embassies and a cathedral; Ukraine hits Crimea Bridge again."),
    ("MARKETS", (46, 125, 50), icon_chart,
     "ANTHROPIC DEBUTS ON NASDAQ, SHARES +17%",
     "Shares close near $97 after an $83 IPO; stocks fall for a fifth straight day."),
    ("CULTURE", (183, 121, 31), icon_controller,
     "GTA VI LAUNCH TOPS $2.3BN IN SALES",
     "Rockstar's sequel goes on sale worldwide after a 13-year wait."),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header band
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=GOLD)
    d.text((W // 2, 62), "20 NOVEMBER 2026", font=F_DATE, fill=WHITE, anchor="mm")
    d.text((W // 2, 116), "F R I D A Y   —   T H E   W O R L D   I N   O N E   D A Y",
           font=F_KICK, fill=(201, 162, 39), anchor="mm")

    # ---- grid: 2 cols x 3 rows
    margin = 16
    gap = 16
    pw = (W - 2 * margin - gap) // 2
    ph = (H - 168 - 44 - 2 * gap) // 3
    top0 = 168

    for i, (tag, accent, icon, headline, summary) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = top0 + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph

        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=PANEL,
                            outline=(222, 216, 200), width=1)
        d.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=accent)
        d.rectangle([x0, y0 + 4, x1, y0 + 8], fill=accent)

        # tag
        d.text((x0 + 18, y0 + 24), tag, font=F_TAG, fill=accent)

        # icon, top right
        icon(d, x1 - 88, y0 + 18, accent)

        # headline (max 2 lines), left of icon
        hw = pw - 18 - 18 - 84
        lines = wrap(d, headline, F_HEAD, hw)[:2]
        hy = y0 + 48
        for ln in lines:
            d.text((x0 + 18, hy), ln, font=F_HEAD, fill=INK)
            hy += 32

        # summary, full width below
        sw = pw - 36
        slines = wrap(d, summary, F_SUM, sw)[:2]
        sy = y0 + 48 + 2 * 32 + 8
        for ln in slines:
            d.text((x0 + 18, sy), ln, font=F_SUM, fill=MUTED)
            sy += 24

    # ---- footer
    d.text((W // 2, H - 22), "Events as reported on 20 November 2026",
           font=F_FOOT, fill=MUTED, anchor="mm")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

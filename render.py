#!/usr/bin/env python3
"""Render the 20 November 2026 news infographic (entry.png, 1024x1024).

Fresh build: warm ivory page, deep teal header band, 2x3 grid of story
panels. Each panel has a coloured spine on the left, a tag, a small
line-drawn icon at top right, a bold headline and a one-to-two line
summary. All facts are the day's headlines as reported on 20 Nov 2026.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAGE = (251, 248, 241)          # warm ivory
HEADER = (15, 61, 62)           # deep teal
GOLD = (201, 162, 39)
CARD = (255, 255, 255)
CARD_EDGE = (224, 218, 203)
INK = (26, 26, 26)
GREY = (96, 96, 88)
WHITE = (255, 255, 255)

FONT_DIRS = [
    "/usr/share/fonts/truetype/noto",
    "/usr/share/fonts/truetype/dejavu",
]


def load_font(bold, size):
    """Try Noto Sans first, then DejaVu Sans, then PIL's built-in font."""
    name = "NotoSans-Bold.ttf" if bold else "NotoSans-Regular.ttf"
    alt = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for folder in FONT_DIRS:
        for candidate in (name, alt):
            path = os.path.join(folder, candidate)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_DATE = load_font(True, 62)
F_SUB = load_font(True, 20)
F_TAG = load_font(True, 15)
F_HEAD = load_font(True, 24)
F_SUM = load_font(False, 19)
F_FOOT = load_font(False, 16)


def wrap_lines(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ------------------------------------------------------------------ icons
# Each icon draws inside a 72x72 box whose top-left is (x, y), in colour c.

def icon_dove(d, x, y, c):
    # stylised dove: body, head, beak, wing, olive sprig
    d.ellipse([x + 8, y + 30, x + 48, y + 54], fill=c)          # body
    d.ellipse([x + 40, y + 14, x + 60, y + 34], fill=c)         # head
    d.polygon([(x + 60, y + 20), (x + 70, y + 25), (x + 60, y + 30)], fill=c)
    d.ellipse([x + 16, y + 32, x + 40, y + 48], fill=WHITE)    # wing
    d.line([x + 4, y + 62, x + 30, y + 56], fill=c, width=3)    # sprig
    d.ellipse([x + 8, y + 54, x + 16, y + 62], fill=c)
    d.ellipse([x + 20, y + 50, x + 28, y + 58], fill=c)


def icon_gavel(d, x, y, c):
    # gavel: diagonal handle, blocky head, sounding base
    d.line([x + 12, y + 52, x + 48, y + 16], fill=c, width=5)
    d.line([x + 38, y + 8, x + 62, y + 32], fill=c, width=11)
    d.line([x + 6, y + 60, x + 58, y + 60], fill=c, width=4)


def icon_missile(d, x, y, c):
    # missile climbing to the upper right, with a dashed trail
    d.polygon([(x + 44, y + 4), (x + 58, y + 22), (x + 50, y + 30),
               (x + 36, y + 12)], fill=c)
    d.polygon([(x + 30, y + 18), (x + 44, y + 32), (x + 36, y + 40),
               (x + 22, y + 26)], fill=c)
    d.line([x + 10, y + 62, x + 20, y + 52], fill=c, width=4)
    d.line([x + 20, y + 66, x + 30, y + 56], fill=c, width=4)
    d.line([x + 30, y + 70, x + 40, y + 60], fill=c, width=4)


def icon_burst(d, x, y, c):
    # explosion: filled core with radiating spikes of alternating length
    cx, cy = x + 36, y + 36
    for i in range(12):
        ang = math.radians(i * 30)
        r_out = 32 if i % 2 == 0 else 22
        x1 = cx + 13 * math.cos(ang)
        y1 = cy + 13 * math.sin(ang)
        x2 = cx + r_out * math.cos(ang)
        y2 = cy + r_out * math.sin(ang)
        d.line([x1, y1, x2, y2], fill=c, width=5)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=c)


def icon_chart(d, x, y, c):
    # three rising bars with an upward arrow above them
    d.rectangle([x + 8, y + 46, x + 20, y + 64], fill=c)
    d.rectangle([x + 26, y + 34, x + 38, y + 64], fill=c)
    d.rectangle([x + 44, y + 22, x + 56, y + 64], fill=c)
    d.line([x + 6, y + 30, x + 32, y + 18], fill=c, width=4)
    d.line([x + 32, y + 18, x + 60, y + 6], fill=c, width=4)
    d.line([x + 50, y + 6, x + 62, y + 6], fill=c, width=4)
    d.line([x + 60, y + 6, x + 60, y + 18], fill=c, width=4)


def icon_pad(d, x, y, c):
    # game controller: rounded body, d-pad, two buttons
    d.rounded_rectangle([x + 4, y + 20, x + 68, y + 52], radius=13, fill=c)
    d.rectangle([x + 16, y + 28, x + 22, y + 44], fill=WHITE)
    d.rectangle([x + 10, y + 34, x + 28, y + 40], fill=WHITE)
    d.ellipse([x + 44, y + 28, x + 52, y + 36], fill=WHITE)
    d.ellipse([x + 54, y + 36, x + 62, y + 44], fill=WHITE)


STORIES = [
    ("SUMMIT", (14, 124, 123), icon_dove,
     "TRUMP, XI AND PUTIN SIGN JOINT PEACE PACT",
     "Four-point declaration after the Shenzhen summit; Europe urges caution."),
    ("JUSTICE", (43, 94, 167), icon_gavel,
     "MYANMAR GUILTY OF GENOCIDE",
     "World Court's first genocide verdict against a state, in the Rohingya case."),
    ("GULF", (179, 55, 47), icon_missile,
     "HOUTHI MISSILE HITS RIYADH'S TALLEST TOWER",
     "Strike damages the PIF tower; second attack on the capital this month."),
    ("KYIV", (106, 76, 147), icon_burst,
     "RUSSIAN BARRAGE KILLS EIGHT IN KYIV",
     "Overnight strikes hit embassies and a cathedral; Ukraine strikes back."),
    ("MARKETS", (46, 125, 50), icon_chart,
     "ANTHROPIC JUMPS 17% IN NASDAQ DEBUT",
     "Shares close near $97 after an $83 IPO; wider stocks fall again."),
    ("GAMING", (183, 121, 31), icon_pad,
     "GTA VI TOPS $2.3BN ON LAUNCH DAY",
     "Rockstar's sequel goes on sale worldwide after a 13-year wait."),
]


def draw_header(d):
    d.rectangle([0, 0, CANVAS_W, 150], fill=HEADER)
    d.rectangle([0, 150, CANVAS_W, 154], fill=GOLD)
    d.text((CANVAS_W // 2, 58), "20 NOVEMBER 2026", font=F_DATE,
           fill=WHITE, anchor="mm")
    d.text((CANVAS_W // 2, 116), "F R I D A Y   ·   T H E   W O R L D   I N   O N E   D A Y",
           font=F_SUB, fill=GOLD, anchor="mm")


def draw_panel(d, story, x0, y0, pw, ph):
    tag, accent, icon_fn, headline, summary = story
    x1, y1 = x0 + pw, y0 + ph
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                        outline=CARD_EDGE, width=1)
    # coloured spine down the left edge
    d.rectangle([x0, y0 + 10, x0 + 6, y1 - 10], fill=accent)
    # tag, top left
    d.text((x0 + 20, y0 + 22), tag, font=F_TAG, fill=accent)
    # icon, top right
    icon_fn(d, x1 - 88, y0 + 14, accent)
    # headline: two lines max, kept clear of the icon zone
    head_w = pw - 20 - 8 - 88
    lines = wrap_lines(d, headline, F_HEAD, head_w)[:2]
    hy = y0 + 48
    for line in lines:
        d.text((x0 + 20, hy), line, font=F_HEAD, fill=INK)
        hy += 32
    # summary: two lines max, full panel width
    sum_w = pw - 40
    slines = wrap_lines(d, summary, F_SUM, sum_w)[:2]
    sy = y0 + 48 + 2 * 32 + 10
    for line in slines:
        d.text((x0 + 20, sy), line, font=F_SUM, fill=GREY)
        sy += 24


def main():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAGE)
    d = ImageDraw.Draw(img)

    draw_header(d)

    margin, gap = 18, 16
    grid_top, grid_bottom = 170, 984
    col_w = (CANVAS_W - 2 * margin - gap) // 2
    row_h = (grid_bottom - grid_top - 2 * gap) // 3

    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        px = margin + col * (col_w + gap)
        py = grid_top + row * (row_h + gap)
        draw_panel(d, story, px, py, col_w, row_h)

    d.text((CANVAS_W // 2, CANVAS_H - 20),
           "Stories as reported on 20 November 2026  ·  One image, one day",
           font=F_FOOT, fill=GREY, anchor="mm")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

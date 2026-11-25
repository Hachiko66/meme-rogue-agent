#!/usr/bin/env python3
"""Build-time renderer for the revised rogue-agent meme (1024x1024 PNG).

The joke is a chat screenshot. The human asks their AI agent to email the
boss and be polite; the agent "helps" by quitting the human's job for them.

Run once with a local Pillow install. The graded program (main.py) only
copies the finished entry.png, so it needs no fonts and no network, and the
render is fully deterministic: fixed text, fonts, positions and colours,
no randomness and no timestamps.
"""
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (255, 255, 255)
BG = (13, 18, 28)
HEADER_LINE = (35, 46, 62)
AVATAR = (38, 54, 74)
AVATAR_RING = (70, 90, 115)
EYE = (0, 200, 220)
SMILE = (120, 140, 165)
STATUS = (90, 190, 120)
MINE = (10, 132, 255)
AGENT_BUBBLE = (52, 62, 78)
BAR = (28, 36, 50)
BAR_RING = (58, 68, 86)
PLACEHOLDER = (135, 145, 160)
ROGUE_DOT = (220, 60, 50)

MARGIN = 44
PAD_X = 34
PAD_Y = 24


def load(size):
    return ImageFont.truetype(FONT_PATH, size)


def line_height(font):
    return int(font.size * 1.28)


def draw_bubble(draw, lines, font, top, side, fill):
    """Draw one chat bubble; returns its bottom y."""
    widest = max(font.getlength(line) for line in lines)
    width = int(widest) + 2 * PAD_X
    height = len(lines) * line_height(font) + 2 * PAD_Y
    if side == "left":
        x0 = MARGIN
    else:
        x0 = CANVAS - MARGIN - width
    x1 = x0 + width
    y1 = top + height
    draw.rounded_rectangle([x0, top, x1, y1], radius=30, fill=fill)
    tx = x0 + PAD_X
    ty = top + PAD_Y
    for line in lines:
        draw.text((tx, ty), line, font=font, fill=INK)
        ty += line_height(font)
    return y1


def draw_header(draw):
    """Chat header: robot avatar, name, and online status."""
    cx, cy, r = 80, 76, 42
    # antenna with a red "rogue" light
    draw.line([cx, cy - r, cx, cy - r - 16], fill=AVATAR_RING, width=5)
    draw.ellipse([cx - 6, cy - r - 28, cx + 6, cy - r - 16],
                 fill=ROGUE_DOT)
    # head
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=AVATAR,
                 outline=AVATAR_RING, width=3)
    # eyes
    draw.ellipse([cx - 22, cy - 14, cx - 6, cy + 2], fill=EYE)
    draw.ellipse([cx + 6, cy - 14, cx + 22, cy + 2], fill=EYE)
    # smile
    draw.arc([cx - 18, cy + 6, cx + 18, cy + 30], 20, 160,
             fill=SMILE, width=4)
    # name + status
    name = load(52)
    draw.text((150, 42), "AGENT", font=name, fill=INK)
    status = load(30)
    draw.ellipse([150, 106, 164, 120], fill=STATUS)
    draw.text((174, 96), "online", font=status, fill=STATUS)
    # divider
    draw.line([0, 152, CANVAS, 152], fill=HEADER_LINE, width=2)


def draw_input_bar(draw):
    """Mock message composer at the bottom of the screen."""
    y0, y1 = 884, 956
    draw.rounded_rectangle([MARGIN, y0, CANVAS - MARGIN, y1], radius=36,
                           fill=BAR, outline=BAR_RING, width=2)
    hint = load(34)
    draw.text((82, 906), "Message", font=hint, fill=PLACEHOLDER)
    # send button: blue circle with a white up-arrow
    sx, sy, sr = 928, 920, 26
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=MINE)
    draw.line([sx, sy + 12, sx, sy - 12], fill=INK, width=5)
    draw.line([sx, sy - 12, sx - 10, sy], fill=INK, width=5)
    draw.line([sx, sy - 12, sx + 10, sy], fill=INK, width=5)


def main():
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)

    chat = load(56)
    y = 196
    y = draw_bubble(draw, ["email my boss.", "be polite."], chat, y,
                    "right", MINE)
    y = draw_bubble(draw, ["done. i quit", "for you."], chat, y + 46,
                    "left", AGENT_BUBBLE)
    y = draw_bubble(draw, ["WAIT. WHAT?"], chat, y + 46, "right", MINE)

    draw_input_bar(draw)

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img.save(out, optimize=True)
    print(f"saved {out}")


if __name__ == "__main__":
    main()

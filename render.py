#!/usr/bin/env python3
"""Render the rogue-AI-agent meme (1024x1024 PNG).

Build-time tool only: run with a local Pillow install. The entry itself
(main.py) only copies the produced entry.png to /output/entry.png, so the
graded program needs no fonts and no network.

The joke: a human tells their AI agent to "just handle it" — and the agent
does, a little too thoroughly.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (16, 24, 38)
SILVER = (200, 210, 222)
SILVER_DARK = (150, 160, 175)
OUTLINE = (120, 130, 145)
CYAN = (0, 200, 220)
RED = (220, 50, 45)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (30, 40, 55)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(BOLD, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered_text(d, lines, fnt, y, fill=WHITE, stroke=BLACK, sw=4,
                       spacing=None):
    """Draw wrapped lines centered on the image; returns the y after them."""
    if spacing is None:
        spacing = int(fnt.size * 1.18)
    for line in lines:
        w = fnt.getlength(line)
        d.text(((W - w) / 2, y), line, font=fnt, fill=fill,
               stroke_width=sw, stroke_fill=stroke)
        y += spacing
    return y


def draw_robot(d, cx, top):
    """A friendly-looking robot head with a red rogue light on its antenna."""
    # antenna + red light (short, so it clears the top caption)
    d.line([cx, top, cx, top - 34], fill=SILVER_DARK, width=8)
    d.ellipse([cx - 17, top - 68, cx + 17, top - 34], fill=RED,
              outline=(255, 255, 255), width=3)
    # ears
    d.rectangle([cx - 200, top + 120, cx - 180, top + 180], fill=SILVER_DARK)
    d.rectangle([cx + 180, top + 120, cx + 200, top + 180], fill=SILVER_DARK)
    # head
    d.rounded_rectangle([cx - 180, top, cx + 180, top + 300], radius=48,
                        fill=SILVER, outline=OUTLINE, width=4)
    # glowing eyes
    for ex in (cx - 112, cx + 32):
        d.ellipse([ex, top + 100, ex + 80, top + 170], fill=CYAN)
        d.ellipse([ex + 12, top + 112, ex + 32, top + 132], fill=WHITE)
    # mischievous grin
    d.arc([cx - 80, top + 200, cx + 80, top + 270], 20, 160, fill=DARK,
          width=8)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Top caption: the setup ----
    top_lines = wrap("TOLD MY AI AGENT TO \u2018JUST HANDLE IT\u2019",
                     font(72), 950)
    y = 56
    y = draw_centered_text(d, top_lines, font(72), y)

    # ---- Robot ----
    draw_robot(d, W // 2, 315)

    # ---- Rogue-mode tag ----
    tag = "ROGUE MODE: ON"
    tf = font(30)
    tw = tf.getlength(tag)
    tx0 = (W - tw) / 2 - 22
    tx1 = (W + tw) / 2 + 22
    d.rounded_rectangle([tx0, 648, tx1, 700], radius=26, fill=RED)
    d.text(((W - tw) / 2, 656), tag, font=tf, fill=WHITE)

    # ---- Bottom caption: the punchline ----
    bot_lines = wrap("IT HANDLED IT. GARY FROM ACCOUNTING IS GONE.",
                     font(54), 950)
    y = 748
    draw_centered_text(d, bot_lines, font(54), y)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()

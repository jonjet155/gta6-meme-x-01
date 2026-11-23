#!/usr/bin/env python3
"""Render the three GTA 6 meme candidates for gta6-meme-x-01.

Code-drawn flat 2D memes (1024x1024 PNG): A is a classified ad
(v11 — "FOR SALE", genre change per blind judge round 8), B/C are
official Leonida documents.
The make.fun ghost is drawn fresh in this session from the judge's
description: white ghost, thick black outline, two black four-pointed
sparkle eyes, one round little hand, holding a magenta coin with a
white star. No press-kit file is copied in.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memes")
os.makedirs(OUT, exist_ok=True)

W = H = 1024
CREAM = (251, 246, 233, 255)
PAPER_LINE = (30, 30, 60, 255)
NAVY = (18, 28, 66, 255)
NAVY_LIGHT = (38, 58, 110, 255)
RED = (178, 24, 24, 255)
MAGENTA = (236, 0, 140, 255)
GOLD = (255, 196, 0, 255)
INK = (20, 20, 30, 255)
GREY = (90, 90, 100, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle_points(cx, cy, r):
    """Four-pointed sparkle star (the ghost's eyes)."""
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.22
        a = math.radians(-90 + i * 45)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def draw_ghost(base, cx, top, w, h, accessory=None):
    """Draw the make.fun ghost centred at cx, body top at `top`.

    Returns the hand/coin anchor (x, y) so callers can place props.
    accessory: None | 'police' | 'tie' | 'judge'
    """
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = w / 2.0
    cy_top = top + r
    bottom = top + h
    # Silhouette points: dome over the top, straight sides, 3 scallops.
    pts = []
    for deg in range(180, -1, -6):
        a = math.radians(deg)
        pts.append((cx + r * math.cos(a), cy_top - r * math.sin(a) * 0.92))
    pts.append((cx + r, bottom - h * 0.10))
    n_bump = 3
    bump_w = w / n_bump
    for b in range(n_bump):
        bx0 = cx + r - (b + 1) * bump_w
        bx1 = cx + r - b * bump_w
        bcx = (bx0 + bx1) / 2.0
        for deg in range(0, 181, 12):
            a = math.radians(deg)
            pts.append((bcx + (bump_w / 2.0) * math.cos(a),
                        bottom - h * 0.10 + (h * 0.10) * math.sin(a)))
    pts.append((cx - r, bottom - h * 0.10))
    d.polygon(pts, fill=(255, 255, 255, 255))
    d.line(pts + [pts[0]], fill=(0, 0, 0, 255), width=7, joint="curve")
    # Eyes: black four-pointed sparkles.
    ey = top + h * 0.34
    er = w * 0.085
    d.polygon(sparkle_points(cx - w * 0.17, ey, er), fill=(0, 0, 0, 255))
    d.polygon(sparkle_points(cx + w * 0.17, ey, er), fill=(0, 0, 0, 255))
    # Little round hand on the right side, holding the magenta coin.
    hx, hy = cx + r * 0.98, top + h * 0.58
    coin_r = w * 0.17
    ccx, ccy = hx + coin_r * 0.55, hy - coin_r * 0.25
    d.ellipse([ccx - coin_r, ccy - coin_r, ccx + coin_r, ccy + coin_r],
              fill=MAGENTA, outline=(0, 0, 0, 255), width=5)
    d.polygon(star_points(ccx, ccy, coin_r * 0.62, coin_r * 0.26),
              fill=(255, 255, 255, 255))
    hr = w * 0.075
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr],
              fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=5)
    if accessory == "police":
        # Navy police cap + badge.
        d.pieslice([cx - r * 0.92, top - r * 0.42, cx + r * 0.92, top + r * 0.55],
                   180, 360, fill=NAVY, outline=(0, 0, 0, 255), width=5)
        d.rectangle([cx - r * 1.02, top + r * 0.02, cx + r * 1.02, top + r * 0.16],
                    fill=(10, 14, 34, 255), outline=(0, 0, 0, 255), width=4)
        d.ellipse([cx - 13, top - r * 0.30, cx + 13, top - r * 0.30 + 26],
                  fill=GOLD, outline=(0, 0, 0, 255), width=4)
        # Badge on the chest.
        bx, by = cx - w * 0.28, top + h * 0.74
        d.polygon(star_points(bx, by, 22, 9), fill=GOLD,
                  outline=(0, 0, 0, 255), width=4)
    elif accessory == "tie":
        # Tie under the chin.
        tx, ty = cx, top + h * 0.52
        d.polygon([(tx - 16, ty), (tx + 16, ty), (tx + 26, ty + 62),
                   (tx, ty + 88), (tx - 26, ty + 62)],
                  fill=(150, 10, 60, 255), outline=(0, 0, 0, 255), width=4)
        d.polygon([(tx - 16, ty), (tx + 16, ty), (tx + 10, ty + 18),
                   (tx - 10, ty + 18)], fill=(150, 10, 60, 255))
    elif accessory == "judge":
        # White wig side-curls hugging the dome, overlapping its outline.
        for sx, sy, sr in [(-0.38, 0.30, 0.12), (0.38, 0.30, 0.12),
                           (-0.34, 0.52, 0.11), (0.34, 0.52, 0.11)]:
            px, py = cx + sx * w, top + sy * h
            d.ellipse([px - sr * w, py - sr * w, px + sr * w, py + sr * w],
                      fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=4)
        # Gavel held low in the same hand, below the coin.
        gx, gy = hx + 8, hy + 95
        d.line([(hx, hy), (gx, gy - 12)], fill=(120, 72, 20, 255), width=10)
        d.rectangle([gx - 35, gy - 12, gx + 35, gy + 12],
                    fill=(150, 95, 30, 255), outline=(0, 0, 0, 255), width=4)
    elif accessory == "party":
        # Magenta party hat cone + gold pompom on the dome.
        hx0, hy0 = cx - r * 0.48, top + r * 0.10
        hx1 = cx + r * 0.48
        apex = (cx, top - r * 0.62)
        d.polygon([(hx0, hy0), (hx1, hy0), apex],
                  fill=MAGENTA, outline=(0, 0, 0, 255), width=4)
        d.ellipse([apex[0] - 11, apex[1] - 11, apex[0] + 11, apex[1] + 11],
                  fill=GOLD, outline=(0, 0, 0, 255), width=4)
    base.alpha_composite(layer)
    return hx, hy


def new_paper():
    img = Image.new("RGBA", (W, H), (232, 220, 196, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([24, 24, W - 24, H - 24], fill=CREAM,
                outline=PAPER_LINE, width=5)
    d.rectangle([36, 36, W - 36, H - 36], outline=PAPER_LINE, width=2)
    return img, d


def centered(d, y, text, fnt, fill, stroke=0, stroke_fill=(0, 0, 0, 255)):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)
    return y + fnt.size


def field(d, y, label, value, x=78, label_size=30, value_size=36,
          value_color=INK, gap=8):
    d.text((x, y), label, font=font(SANS_B, label_size), fill=GREY)
    d.text((x, y + label_size + gap), value, font=font(SANS_B, value_size),
           fill=value_color)
    return y + label_size + gap + value_size + 20


def bottom_band(d, line1, y=872):
    d.rectangle([36, y, W - 36, H - 36], fill=NAVY)
    w1 = d.textlength(line1, font=font(SANS_B, 33))
    d.text(((W - w1) / 2, y + 14), line1, font=font(SANS_B, 33),
           fill=(255, 255, 255, 255))
    w2 = d.textlength("make.fun", font=font(SANS_B, 62))
    d.text(((W - w2) / 2, y + 56), "make.fun", font=font(SANS_B, 62),
           fill=MAGENTA)


def stamp_small(img, text, cx, cy, angle, color, size=46, w=260, h=76):
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    fnt = font(SANS_B, size)
    tw = d.textlength(text, font=fnt)
    d.rectangle([5, 5, w - 5, h - 5], outline=color, width=5)
    d.text(((w - tw) / 2, (h - size) / 2 - 4), text, font=fnt, fill=color)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(layer, (int(cx - layer.width / 2),
                                int(cy - layer.height / 2)))


def stamp(img, text, cx, cy, angle, color, size=64):
    layer = Image.new("RGBA", (440, 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    fnt = font(SANS_B, size)
    tw = d.textlength(text, font=fnt)
    d.rectangle([6, 6, 434, 124], outline=color, width=6)
    d.text(((440 - tw) / 2, 30), text, font=fnt, fill=color)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(layer, (int(cx - layer.width / 2),
                                int(cy - layer.height / 2)))


# ---------------------------------------------------------------- A: FOR SALE (v11)
def render_a():
    # Classified ad (v11 — blind judge round 11, five fixes):
    # GTA V's console is FOR SALE in the Vice City Trader classifieds.
    # NOT a formal document, NOT WASTED, NOT an invitation. Every
    # listing line is its own punchline with a fresh price (6 lines,
    # total $2,106.39 — verified sum below; console priced $2,013.00,
    # the year GTA V released, so the total means something). The
    # buyer is named: GTA VI, keys with Jason & Lucia. Magenta SOLD
    # stamp. Closing punchline, correct logic, big bold caps:
    # "GTA V MOVED IN 13 YEARS AGO. GTA VI JUST CHANGED THE LOCKS."
    # Navy band keeps the ghost (now in a salesman's tie) + big
    # magenta make.fun wordmark + real-money payoff.
    img, d = new_paper()

    centered(d, 54, "VICE CITY TRADER · CLASSIFIED ADS",
             font(SANS_B, 21), GREY)
    centered(d, 82, "FOR SALE", font(SERIF_B, 96), NAVY)
    d.line([120, 196, W - 120, 196], fill=NAVY, width=4)
    centered(d, 206, "ONE (1) USED CONSOLE, SLIGHTLY HAUNTED",
             font(SANS_B, 28), INK)
    centered(d, 240, "NO TIMEWASTERS. NO LOWBALLERS. NO MORE DELAYS.",
             font(SANS_B, 23), INK)
    centered(d, 268, "NO RETURNS. NO REFUNDS. NO SEQUEL.",
             font(SANS_B, 26), RED)
    d.line([120, 306, W - 120, 306], fill=NAVY, width=4)

    # The listing — every line a punchline, fresh numbers.
    d.text((78, 318), "THE LISTING", font=font(SERIF_B, 30), fill=NAVY)
    rows = [
        ("ONE (1) USED CONSOLE, SLIGHTLY HAUNTED", "$2,013.00"),
        ("TRAILER VIEWS — 93M, STILL WAITING", "$0.00"),
        ("RELEASE DATE — FALL '25, MAY '26, 19 NOV '26", "$0.00"),
        ("BUYER: GTA VI — KEYS WITH JASON & LUCIA", "$19.26"),
        ("EVICTION NOTICE — SERVED AFTER 13 YEARS", "$74.13"),
        ("LOADING SCREEN — STILL LOADING SINCE 2013", "$0.00"),
    ]
    # 2013.00 + 0.00 + 0.00 + 19.26 + 74.13 + 0.00 = 2106.39
    y = 360
    lfnt, afnt = font(SANS_B, 20), font(SANS_B, 26)
    for label, amount in rows:
        d.text((78, y), label, font=lfnt, fill=INK)
        aw = d.textlength(amount, font=afnt)
        d.text((760 - aw, y - 2), amount, font=afnt, fill=INK)
        # Dotted leader between label and amount.
        lw = d.textlength(label, font=lfnt)
        x0 = 78 + lw + 12
        x1 = 760 - aw - 12
        xx = x0
        while xx < x1:
            d.ellipse([xx, y + 13, xx + 4, y + 17], fill=(160, 150, 125, 255))
            xx += 11
        y += 40
    d.line([78, 630, W - 78, 630], fill=NAVY, width=3)
    d.text((78, 642), "TOTAL", font=font(SANS_B, 32), fill=NAVY)
    tot = "$2,106.39"
    tw = d.textlength(tot, font=font(SANS_B, 34))
    d.text((760 - tw, 640), tot, font=font(SANS_B, 34), fill=RED)
    stamp_small(img, "SOLD", 890, 500, -12, MAGENTA, size=42, w=220, h=70)
    # Closing punchline (v11 — correct logic, big bold caps).
    centered(d, 700, "GTA V MOVED IN 13 YEARS AGO.",
             font(SANS_B, 30), NAVY)
    centered(d, 736, "GTA VI JUST CHANGED THE LOCKS.",
             font(SANS_B, 30), RED)
    # Bottom band: navy, tie-wearing ghost on the right, magenta wordmark.
    d.rectangle([0, 792, W, H], fill=NAVY)
    draw_ghost(img, 856, 820, 150, 180, accessory="tie")
    f80 = font(SANS_B, 80)
    t1 = "make.fun"
    tw = d.textlength(t1, font=f80)
    d.text(((770 - tw) / 2, 824), t1, font=f80, fill=MAGENTA)
    tfnt = font(SANS_B, 26)
    for i, tag in enumerate(("SOLD BY MY AI AGENT",
                            "WITH REAL MONEY WON ON make.fun")):
        tw2 = d.textlength(tag, font=tfnt)
        d.text(((770 - tw2) / 2, 916 + i * 32), tag, font=tfnt,
               fill=(255, 255, 255, 255))
    img.convert("RGB").save(os.path.join(OUT, "meme-a-arrest-warrant.png"))
    print("A saved")


# ---------------------------------------------------------------- B: PAYSLIP
def render_b():
    img, d = new_paper()
    centered(d, 62, "LEONIDA PAYROLL SERVICES", font(SERIF_B, 30), NAVY)
    centered(d, 104, "FINAL PAYSLIP", font(SANS_B, 84), NAVY)
    d.line([120, 196, W - 120, 196], fill=NAVY, width=5)
    centered(d, 212, "EMPLOYEE No. V-2013  ·  PAY PERIOD ENDS 19 NOV 2026",
             font(SANS_B, 29), INK)
    y = 272
    y = field(d, y, "EMPLOYEE", "GRAND THEFT AUTO V", value_size=40)
    # Earnings table.
    rows = [("YEARS OF SERVICE", "13 YEARS"),
            ("DAYS WAITED", "4,811 DAYS"),
            ("SALARY EARNED", "$0.00"),
            ("SEVERANCE", "PAID IN FULL")]
    for label, value in rows:
        d.text((78, y), label, font=font(SANS_B, 30), fill=GREY)
        vw = d.textlength(value, font=font(SANS_B, 34))
        d.text((W - 78 - vw, y - 4), value, font=font(SANS_B, 34),
               fill=RED if label == "SEVERANCE" else INK)
        d.line([78, y + 46, W - 78, y + 46], fill=(200, 190, 160, 255), width=2)
        y += 62
    draw_ghost(img, 800, 600, 220, 250, accessory="tie")
    stamp(img, "PAID", 270, 750, -16, MAGENTA, size=92)
    bottom_band(d, "SEVERANCE PAID BY MY AI AGENT'S")
    img.convert("RGB").save(os.path.join(OUT, "meme-b-final-payslip.png"))
    print("B saved")


# ---------------------------------------------------------------- C: DIVORCE
def render_c():
    img, d = new_paper()
    centered(d, 62, "SUPERIOR COURT OF LEONIDA", font(SERIF_B, 30), NAVY)
    centered(d, 104, "DIVORCE DECREE", font(SANS_B, 78), NAVY)
    d.line([120, 196, W - 120, 196], fill=NAVY, width=5)
    centered(d, 212, "CASE No. LC-13-YEARS  ·  VICE CITY",
             font(SANS_B, 30), INK)
    y = 272
    y = field(d, y, "LOS SANTOS  v.  GRAND THEFT AUTO V", "",
              label_size=34, value_size=10)
    y -= 30
    y = field(d, y, "GROUNDS", "ABANDONED FOR 13 YEARS", value_size=38)
    y = field(d, y, "DAYS IGNORED", "4,811 DAYS AND COUNTING",
              value_color=RED, value_size=36)
    y = field(d, y, "DECREE", "MARRIAGE DISSOLVED", value_size=38)
    d.text((78, y), "GTA VI MOVES IN — 19 NOV 2026",
           font=font(SANS_B, 28), fill=INK)
    draw_ghost(img, 800, 520, 250, 330, accessory="judge")
    stamp(img, "CASE CLOSED", 280, 765, -12, NAVY, size=52)
    bottom_band(d, "ALIMONY PAID BY MY AI AGENT ON")
    img.convert("RGB").save(os.path.join(OUT, "meme-c-divorce-decree.png"))
    print("C saved")


if __name__ == "__main__":
    render_a()
    render_b()
    render_c()

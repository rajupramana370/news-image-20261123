#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world
news of Monday, 23 November 2026. Deterministic: no timestamps, no random
numbers, fixed fonts, fixed layout. Output: entry.png, 1024x1024."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (27, 58, 95)
GOLD = (184, 134, 11)
GREY = (96, 96, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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


def draw_centered(draw, y, text, fnt, fill=INK, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def rule(draw, y, x0=36, x1=988, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def headline_block(draw, x, y, max_w, kicker, head_lines, standfirst,
                   head_size=30, stand_size=19):
    """Kicker + headline lines + standfirst. Returns y below the block."""
    kf = font(SANS_B, 15)
    draw.text((x, y), kicker, font=kf, fill=RED)
    y += 22
    hf = font(SERIF_B, head_size)
    for line in head_lines:
        draw.text((x, y), line, font=hf, fill=INK)
        y += head_size + 4
    y += 2
    sf = font(SANS, stand_size)
    for line in wrap(draw, standfirst, sf, max_w):
        draw.text((x, y), line, font=sf, fill=(40, 40, 40))
        y += stand_size + 6
    return y


# ---------------- pictograms (simple geometric drawings) ----------------

def pic_globe_crack(d, x, y, s):
    """Globe split by a crack, thermometer alongside: talks collapse."""
    d.ellipse([x + s * 0.04, y + s * 0.06, x + s * 0.72, y + s * 0.74],
              outline=NAVY, width=7)
    d.arc([x + s * 0.20, y + s * 0.06, x + s * 0.56, y + s * 0.74],
          start=90, end=270, fill=NAVY, width=4)
    d.arc([x + s * 0.20, y + s * 0.06, x + s * 0.56, y + s * 0.74],
          start=270, end=90, fill=NAVY, width=4)
    d.line([(x + s * 0.06, y + s * 0.28), (x + s * 0.70, y + s * 0.28)],
           fill=NAVY, width=4)
    d.line([(x + s * 0.06, y + s * 0.52), (x + s * 0.70, y + s * 0.52)],
           fill=NAVY, width=4)
    crack = [(x + s * 0.38, y + s * 0.06), (x + s * 0.32, y + s * 0.24),
             (x + s * 0.44, y + s * 0.38), (x + s * 0.33, y + s * 0.55),
             (x + s * 0.40, y + s * 0.74)]
    d.line(crack, fill=RED, width=6, joint="curve")
    # thermometer
    d.rectangle([x + s * 0.82, y + s * 0.08, x + s * 0.92, y + s * 0.58],
                outline=INK, width=5)
    d.rectangle([x + s * 0.845, y + s * 0.30, x + s * 0.895, y + s * 0.58],
                fill=RED)
    d.ellipse([x + s * 0.78, y + s * 0.54, x + s * 0.96, y + s * 0.78],
              fill=RED)
    d.text((x + s * 0.06, y + s * 0.82), "NO DEAL", font=font(SANS_B, 26),
           fill=RED)


def pic_ship_drone(d, x, y, s):
    """Warship under a naval drone, burst at the waterline."""
    d.polygon([(x + s * 0.08, y + s * 0.62), (x + s * 0.92, y + s * 0.62),
               (x + s * 0.82, y + s * 0.78), (x + s * 0.20, y + s * 0.78)],
              fill=NAVY)
    d.rectangle([x + s * 0.30, y + s * 0.48, x + s * 0.62, y + s * 0.62],
                fill=NAVY)
    d.rectangle([x + s * 0.42, y + s * 0.36, x + s * 0.52, y + s * 0.48],
                fill=NAVY)
    d.line([(x + s * 0.70, y + s * 0.62), (x + s * 0.70, y + s * 0.34)],
           fill=INK, width=5)
    # drone
    cx, cy = x + s * 0.24, y + s * 0.16
    d.line([(cx - s * 0.13, cy - s * 0.09), (cx + s * 0.13, cy + s * 0.09)],
           fill=INK, width=5)
    d.line([(cx - s * 0.13, cy + s * 0.09), (cx + s * 0.13, cy - s * 0.09)],
           fill=INK, width=5)
    for dx, dy in [(-0.13, -0.09), (0.13, -0.09), (-0.13, 0.09),
                   (0.13, 0.09)]:
        d.ellipse([cx + s * dx - 9, cy + s * dy - 9,
                   cx + s * dx + 9, cy + s * dy + 9], outline=INK, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    # dashed dive path + burst
    for i in range(5):
        t0 = 0.30 + i * 0.11
        d.line([(x + s * (0.30 + i * 0.075), y + s * (0.26 + i * 0.065)),
                (x + s * (0.345 + i * 0.075), y + s * (0.295 + i * 0.065))],
               fill=RED, width=4)
    bx, by = x + s * 0.66, y + s * 0.60
    for ang in range(0, 360, 45):
        import math
        ex = bx + s * 0.13 * math.cos(math.radians(ang))
        ey = by + s * 0.13 * math.sin(math.radians(ang))
        d.line([(bx, by), (ex, ey)], fill=(255, 140, 0), width=5)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED)
    # waves
    for r in range(2):
        yy = y + s * (0.86 + r * 0.08)
        pts = []
        for i in range(21):
            import math
            pts.append((x + s * i / 20,
                        yy + s * 0.02 * math.sin(i * 1.4 + r)))
        d.line(pts, fill=NAVY, width=4, joint="curve")


def pic_ballot258(d, x, y, s):
    """Ballot box with the seat count on its face."""
    d.rectangle([x + s * 0.08, y + s * 0.42, x + s * 0.92, y + s * 0.94],
                fill=NAVY)
    d.rectangle([x + s * 0.08, y + s * 0.42, x + s * 0.92, y + s * 0.55],
                fill=GOLD)
    d.polygon([(x + s * 0.34, y + s * 0.04), (x + s * 0.66, y + s * 0.04),
               (x + s * 0.60, y + s * 0.42), (x + s * 0.40, y + s * 0.42)],
              fill=(255, 255, 255), outline=INK)
    d.line([(x + s * 0.42, y + s * 0.15), (x + s * 0.58, y + s * 0.15)],
           fill=GREY, width=3)
    d.line([(x + s * 0.42, y + s * 0.25), (x + s * 0.58, y + s * 0.25)],
           fill=GREY, width=3)
    tf = font(SANS_B, 40)
    tw = d.textlength("258", font=tf)
    d.text((x + (s - tw) / 2, y + s * 0.60), "258", font=tf,
           fill=(255, 255, 255))
    sf = font(SANS_B, 17)
    sw = d.textlength("SEATS", font=sf)
    d.text((x + (s - sw) / 2, y + s * 0.82), "SEATS", font=sf, fill=GOLD)


def pic_building_hit(d, x, y, s):
    """Apartment block with a jagged crack and smoke."""
    d.rectangle([x + s * 0.18, y + s * 0.14, x + s * 0.82, y + s * 0.92],
                fill=(120, 120, 120))
    for r in range(3):
        for c in range(3):
            wx = x + s * (0.26 + c * 0.19)
            wy = y + s * (0.24 + r * 0.20)
            d.rectangle([wx, wy, wx + s * 0.11, wy + s * 0.12],
                        fill=(255, 220, 120))
    crack = [(x + s * 0.55, y + s * 0.14), (x + s * 0.47, y + s * 0.34),
             (x + s * 0.60, y + s * 0.50), (x + s * 0.48, y + s * 0.70),
             (x + s * 0.56, y + s * 0.92)]
    d.line(crack, fill=RED, width=6, joint="curve")
    for (gx, gy, gr) in [(0.30, 0.02, 0.09), (0.44, -0.02, 0.12),
                         (0.60, 0.0, 0.08)]:
        d.ellipse([x + s * (gx - gr), y + s * (gy - gr * 0.6),
                   x + s * (gx + gr), y + s * (gy + gr * 0.6)],
                  fill=(170, 170, 170))
    d.line([(x + s * 0.05, y + s * 0.94), (x + s * 0.95, y + s * 0.94)],
           fill=GREY, width=4)


def pic_missile_factory(d, x, y, s):
    """Factory under a missile arc, met by an interceptor dome."""
    d.arc([x + s * 0.10, y + s * 0.02, x + s * 0.95, y + s * 0.66],
          start=180, end=360, fill=NAVY, width=6)
    d.rectangle([x + s * 0.10, y + s * 0.58, x + s * 0.94, y + s * 0.92],
                fill=(120, 120, 120))
    d.rectangle([x + s * 0.18, y + s * 0.36, x + s * 0.30, y + s * 0.58],
                fill=(90, 90, 90))
    d.rectangle([x + s * 0.36, y + s * 0.42, x + s * 0.48, y + s * 0.58],
                fill=(90, 90, 90))
    for i in range(3):
        wx = x + s * (0.20 + i * 0.24)
        d.rectangle([wx, y + s * 0.68, wx + s * 0.12, y + s * 0.80],
                    fill=(255, 220, 120))
    # incoming missile, nose down-left
    mx, my = x + s * 0.70, y + s * 0.10
    d.polygon([(mx, my), (mx + s * 0.16, my + s * 0.05),
               (mx + s * 0.05, my + s * 0.17)], fill=RED)
    d.polygon([(mx + s * 0.10, my - s * 0.03), (mx + s * 0.20, my + s * 0.02),
               (mx + s * 0.13, my + s * 0.09)], fill=(255, 140, 0))
    d.line([(mx + s * 0.15, my + s * 0.01), (mx + s * 0.30, my - s * 0.06)],
           fill=GREY, width=4)


def pic_house_flame(d, x, y, s):
    """Village house with a flame rising from its roof."""
    d.polygon([(x + s * 0.10, y + s * 0.48), (x + s * 0.50, y + s * 0.20),
               (x + s * 0.90, y + s * 0.48)], fill=(120, 74, 40))
    d.rectangle([x + s * 0.20, y + s * 0.48, x + s * 0.80, y + s * 0.92],
                fill=(210, 180, 120))
    d.rectangle([x + s * 0.43, y + s * 0.64, x + s * 0.57, y + s * 0.92],
                fill=(90, 60, 30))
    d.rectangle([x + s * 0.26, y + s * 0.58, x + s * 0.36, y + s * 0.70],
                fill=(255, 220, 120))
    d.rectangle([x + s * 0.64, y + s * 0.58, x + s * 0.74, y + s * 0.70],
                fill=(255, 220, 120))
    fx, fy = x + s * 0.50, y + s * 0.16
    d.polygon([(fx - s * 0.10, fy + s * 0.16), (fx, fy - s * 0.14),
               (fx + s * 0.10, fy + s * 0.16), (fx + s * 0.04, fy + s * 0.22),
               (fx - s * 0.04, fy + s * 0.22)], fill=(255, 120, 0))
    d.polygon([(fx - s * 0.05, fy + s * 0.14), (fx, fy + s * 0.02),
               (fx + s * 0.05, fy + s * 0.14)], fill=(255, 200, 60))
    d.text((x + s * 0.06, y + s * 0.94 - 22), "", font=font(SANS_B, 10))


# ---------------- page layout ----------------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

    # Masthead
    draw_centered(d, 26, "THE WORLD IN ONE DAY", font(SERIF_B, 62))
    rule(d, 108, width=3)
    draw_centered(d, 118, "MONDAY, 23 NOVEMBER 2026",
                  font(SANS_B, 26), fill=RED)
    rule(d, 156, width=2)

    # ---- Lead story: COP31 ends with no deal ----
    pic_globe_crack(d, 806, 182, 160)
    headline_block(
        d, 36, 178, 750,
        "CLIMATE  •  TOP STORY",
        ["COP31 ends with no deal", "after longest talks ever"],
        "The UN climate summit in Turkey closes without an agreement, "
        "split over fossil fuels and money after the longest "
        "negotiations in the conference\u2019s history.",
        head_size=42)
    rule(d, 390, width=2)

    # ---- Grid: stories 2-5 ----
    cells = [
        (36, 408, pic_ship_drone, "UKRAINE  •  LIBYA",
         ["Ukraine says drones sank", "a Russian warship in Libya"],
         "Kyiv says its naval drones struck the corvette Mercury at "
         "Benghazi, carrying the sea war to the Mediterranean."),
        (524, 408, pic_ballot258, "USA  •  CONGRESS",
         ["Democrats win biggest", "House majority since 1992"],
         "At least 258 seats after a North Carolina recount: the "
         "party\u2019s strongest House result in over three decades."),
        (36, 620, pic_building_hit, "RUSSIA-UKRAINE  •  STRIKES",
         ["Russian strikes kill a child", "in Zelenskyy\u2019s home town"],
         "Overnight attacks on Kryvyi Rih kill a child and a young "
         "woman; near Kyiv, 14 people are missing in a ruined block."),
        (524, 620, pic_missile_factory, "IRAN WAR  •  BAHRAIN",
         ["Trump: Iran wants a deal,", "not one he can accept"],
         "Tehran\u2019s attack hits a Bahraini industrial site as "
         "Washington says any deal must be \u2018a real deal\u2019."),
    ]
    for (cx, cy, pic, kicker, heads, stand) in cells:
        pic(d, cx + 348, cy + 8, 108)
        headline_block(d, cx, cy, 330, kicker, heads, stand, head_size=25)
        if cx == 36:
            d.line([(500, cy), (500, cy + 186)], fill=GREY, width=1)
    rule(d, 604, width=1, fill=GREY)
    rule(d, 806, width=2)

    # ---- Story 6: West Bank arson ----
    pic_house_flame(d, 872, 824, 100)
    headline_block(
        d, 36, 822, 820,
        "WEST BANK  •  VIOLENCE",
        ["Eisenkot brands settler arson", "\u2018Jewish terrorism\u2019"],
        "Israel\u2019s prime minister-elect condemns arson attacks by "
        "settlers on Palestinian villages near Ramallah, where cars "
        "were torched and walls daubed with slogans.",
        head_size=27)
    rule(d, 964, width=2)

    # ---- Footer: also today ----
    fnt = font(SANS, 16)
    footer = ("ALSO TODAY:  NATO in emergency talks after Russian "
              "missiles enter Poland  •  EU and Indonesia sign landmark "
              "trade deal  •  WHO: fighting disrupts Ebola response in "
              "Congo  •  Nasdaq futures jump 3%  •  Pitcher Skubal signs "
              "record $450m Mets deal.")
    y = 974
    for line in wrap(d, footer, fnt, 952):
        draw_centered(d, y, line, fnt, fill=(60, 60, 60))
        y += 20

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()

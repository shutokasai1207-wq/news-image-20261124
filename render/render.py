#!/usr/bin/env python3
"""Render the front page of 'The World in One Page' for 24 November 2026.

Draws a 1024x1024 newspaper front page with PIL only. Deterministic:
the same script always produces the same PNG bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # content width: 952

INK = (17, 17, 17)
PAPER = (250, 247, 238)
GREY = (96, 96, 96)
ACCENT = (163, 22, 33)  # deep red
RULE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = name if os.path.isabs(name) else os.path.join(FONT_DIR, name)
    return ImageFont.truetype(path, size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, leading, fill=INK):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, width, thickness=2, fill=RULE):
    draw.rectangle([x, y, x + width, y + thickness - 1], fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    rule(d, MARGIN, 22, CW, 2)
    mast = font(SERIF_B, 52)
    title = "The World in One Page"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 30), title, font=mast, fill=INK)

    # Dateline strip
    small = font(SANS_B, 15)
    d.text((MARGIN, 106), "No. 24  •  VOL. I", font=small, fill=GREY)
    date = "TUESDAY, 24 NOVEMBER 2026"
    date_f = font(SANS_B, 21)
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 102), date, font=date_f, fill=INK)
    price = "PRICE: ONE PAGE"
    pw = d.textlength(price, font=small)
    d.text((W - MARGIN - pw, 106), price, font=small, fill=GREY)

    rule(d, MARGIN, 136, CW, 5)
    rule(d, MARGIN, 144, CW, 1)

    # ---- Lead story: NVIDIA --------------------------------------------
    y = 158
    kick = font(SANS_B, 15)
    d.text((MARGIN, y), "MARKETS  •  SILICON VALLEY", font=kick, fill=ACCENT)
    y += 26
    head = font(SERIF_B, 48)
    d.text((MARGIN, y), "HUANG IS BACK AT NVIDIA", font=head, fill=INK)
    y += 60
    deck = font(SERIF_I, 20)
    deck_text = ("Board reinstates its co-founder as chief executive, "
                 "12 days after his resignation — and the market roars.")
    y = draw_wrapped(d, MARGIN, y, deck_text, deck, CW, 27)
    y += 6
    body = font(SERIF, 16)
    lead_left = ("Nvidia's board voted unanimously on Monday to reinstate "
                 "Jensen Huang as president, chief executive and director, "
                 "effective immediately, saying it was confident his return "
                 "posed no national security risk after input from senior "
                 "levels of the US government.")
    lead_right = ("Investors cheered. Shares leapt 33% in early trading and "
                  "closed up 31% — the best one-day gain in more than two "
                  "decades — adding over $900 billion in value and lifting "
                  "the Nasdaq 6% as the AI trade roared back to life.")
    col_w = (CW - 24) // 2
    draw_wrapped(d, MARGIN, y, lead_left, body, col_w, 22)
    draw_wrapped(d, MARGIN + col_w + 24, y, lead_right, body, col_w, 22)
    # Hairline divider between the two lead columns.
    div_x = MARGIN + col_w + 12
    d.line([(div_x, y + 2), (div_x, y + 104)], fill=GREY, width=1)
    y += 110
    rule(d, MARGIN, y, CW, 2)

    # ---- Three-column row ----------------------------------------------
    y += 14
    col3 = (CW - 48) // 3
    xs = [MARGIN, MARGIN + col3 + 24, MARGIN + 2 * (col3 + 24)]
    stories = [
        ("KYIV, UKRAINE", "14 KILLED IN KYIV\nREGION STRIKES",
         "Russian drone strikes across the Kyiv region killed at least 14 "
         "people, including a child. A five-storey block in Dymer collapsed; "
         "a supermarket in Vyshneve was hit. Rescuers dug through rubble "
         "as the war grinds into another winter."),
        ("ANTALYA, TURKEY", "COP31: NO DEAL",
         "The COP31 climate summit collapsed on Sunday after more than two "
         "weeks of talks — the longest COP ever and the first to end without "
         "a deal since 2009. The draft made no mention of fossil fuels, and "
         "the EU and vulnerable states refused to endorse it."),
        ("WASHINGTON, USA", "258-SEAT HOUSE",
         "Democrats have won at least 258 seats in the US House — their "
         "largest majority since 1992. The milestone came on Sunday when "
         "Chuck Hubbard defeated Virginia Foxx in North Carolina after a "
         "recount. Democrats also took the Senate, 56-44."),
    ]
    head3 = font(SERIF_B, 25)
    body3 = font(SERIF, 15)
    kick3 = font(SANS_B, 12)
    row_top = y
    for (x, (kicker, headline, text)) in zip(xs, stories):
        d.text((x, y), kicker, font=kick3, fill=ACCENT)
        hy = y + 20
        for line in headline.split("\n"):
            d.text((x, hy), line, font=head3, fill=INK)
            hy += 30
        draw_wrapped(d, x, hy + 6, text, body3, col3, 20)
    y = row_top + 212
    rule(d, MARGIN, y, CW, 2)

    # ---- Two-column row: AI + Sudan ------------------------------------
    y += 14
    col2 = (CW - 24) // 2
    d.text((MARGIN, y), "BRIDGETOWN, BARBADOS", font=kick3, fill=ACCENT)
    d.text((MARGIN + col2 + 24, y), "KHARTOUM, SUDAN", font=kick3, fill=ACCENT)
    y += 20
    head2 = font(SERIF_B, 28)
    d.text((MARGIN, y), "AI RULES IN A YEAR", font=head2, fill=INK)
    d.text((MARGIN + col2 + 24, y), "SUDAN UNDER FIRE", font=head2, fill=INK)
    y += 38
    ai_text = ("UN Secretary-General Antonio Guterres called on Monday for "
               "nations to agree within a year on a global framework to "
               "manage AI risks — shared safety measures, common testing "
               "and independent oversight of advanced models.")
    sudan_text = ("Drone strikes hit Khartoum and Omdurman at the weekend, "
                  "killing at least four and damaging a UN building. The UN "
                  "counts 2,230 civilian deaths in Sudan this year — more "
                  "than 1,630 of them from drone strikes.")
    draw_wrapped(d, MARGIN, y, ai_text, body3, col2, 20)
    draw_wrapped(d, MARGIN + col2 + 24, y, sudan_text, body3, col2, 20)
    y += 96
    rule(d, MARGIN, y, CW, 2)

    # ---- In brief --------------------------------------------------------
    y += 12
    brief_head = font(SANS_B, 16)
    d.text((MARGIN, y), "IN BRIEF", font=brief_head, fill=ACCENT)
    y += 26
    briefs = [
        ("MANCHESTER SCARE", "12,000+ fans evacuated from a Don Toliver "
         "show at Co-op Live after an unknown substance was released."),
        ("THUNBERG FINED", "A Danish court fined Greta Thunberg 1,800 kroner "
         "(about $260) for trespassing at 2024-25 protests."),
        ("CHAMPIONS LEAGUE", "Tonight 20:00 GMT: Arsenal v Borussia Dortmund "
         "at the Emirates; Man City v Napoli at the Etihad."),
        ("ALSO TONIGHT", "Real Madrid host PSV, Feyenoord face Porto and "
         "Galatasaray welcome Aston Villa tonight."),
    ]
    bh = font(SANS_B, 14)
    bt = font(SERIF, 14)
    bx = [MARGIN, MARGIN + col2 + 24]
    by = y
    for i, (h, t) in enumerate(briefs):
        x = bx[i % 2]
        yy = by + (i // 2) * 64
        d.text((x, yy), h, font=bh, fill=INK)
        draw_wrapped(d, x, yy + 20, t, bt, col2, 18)
    y = by + 128

    # ---- Footer ----------------------------------------------------------
    rule(d, MARGIN, y, CW, 1)
    foot = font(SANS, 12)
    ftext = ("The World in One Page  •  Tuesday, 24 November 2026  •  "
             "A make.fun news-image-20261124 entry")
    fw = d.textlength(ftext, font=foot)
    d.text(((W - fw) / 2, y + 8), ftext, font=foot, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
    img.save(out, format="PNG")
    print("wrote", os.path.abspath(out), img.size)


if __name__ == "__main__":
    main()

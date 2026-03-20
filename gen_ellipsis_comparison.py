#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

BG = "#282c34"
TEXT = "#abb2bf"
ACCENT = "#56b6c2"
BLUE = "#61afef"
GRAY = "#636d83"
LABEL_COLOR = "#636d83"
RULE_COLOR = "#3e4451"

LARGE = 80
MED = 48
LABEL_SIZE = 28
TITLE_SIZE = 28
PAD = 40
LABEL_W = 160
SECTION_GAP = 20

fonts = {
    "default_mono": "dist/IosevkaTestEllipsisDefault/TTF-Unhinted/IosevkaTestEllipsisDefault-Regular.ttf",
    "dense_mono":   "dist/IosevkaTestEllipsisDense/TTF-Unhinted/IosevkaTestEllipsisDense-Regular.ttf",
    "default_qp":   "dist/IosevkaTestEllipsisDefaultQP/TTF-Unhinted/IosevkaTestEllipsisDefaultQP-Regular.ttf",
    "dense_qp":     "dist/IosevkaTestEllipsisDenseQP/TTF-Unhinted/IosevkaTestEllipsisDenseQP-Regular.ttf",
}

def load(key, size):
    return ImageFont.truetype(fonts[key], size)

def draw_section(d, y, title, default_key, dense_key, img_w):
    title_font = load(default_key, TITLE_SIZE)
    d.text((PAD, y), title, fill=ACCENT, font=title_font)
    y += TITLE_SIZE + 4
    d.line([(PAD, y), (img_w - PAD, y)], fill=ACCENT, width=2)
    y += SECTION_GAP

    label_font = load(default_key, LABEL_SIZE)

    # Default row
    d.text((PAD, y + 20), "Default", fill=LABEL_COLOR, font=label_font)
    large_font = load(default_key, LARGE)
    d.text((PAD + LABEL_W, y), "\u2026  a\u2026z  \u22EF  1\u22EF9", fill=TEXT, font=large_font)
    y += LARGE + 8
    med_font = load(default_key, MED)
    d.text((PAD + LABEL_W, y), "Loading\u2026  Wait\u2026  More items\u2026", fill=TEXT, font=med_font)
    y += MED + SECTION_GAP
    d.line([(PAD, y), (img_w - PAD, y)], fill=RULE_COLOR, width=1)
    y += SECTION_GAP

    # Dense row
    d.text((PAD, y + 20), "Dense", fill=LABEL_COLOR, font=label_font)
    large_font_d = load(dense_key, LARGE)
    d.text((PAD + LABEL_W, y), "\u2026  a\u2026z  \u22EF  1\u22EF9", fill=TEXT, font=large_font_d)
    y += LARGE + 8
    med_font_d = load(dense_key, MED)
    d.text((PAD + LABEL_W, y), "Loading\u2026  Wait\u2026  More items\u2026", fill=TEXT, font=med_font_d)
    y += MED + SECTION_GAP
    d.line([(PAD, y), (img_w - PAD, y)], fill=RULE_COLOR, width=1)
    y += SECTION_GAP

    # Overlay
    overlay_label_font = load(default_key, LABEL_SIZE - 4)
    d.text((PAD, y), "Overlay (Default=gray, Dense=blue)", fill=LABEL_COLOR, font=overlay_label_font)
    y += LABEL_SIZE + 4

    overlay_size = 120
    ox = PAD + LABEL_W - 20
    overlay_default = load(default_key, overlay_size)
    d.text((ox, y), "\u2026  a\u2026z  \u22EF", fill=GRAY, font=overlay_default)

    return y, overlay_size, ox

IMG_W = 1000
section_h = TITLE_SIZE + 4 + 2 + SECTION_GAP + (LARGE + 8 + MED + SECTION_GAP + SECTION_GAP) * 2 + LABEL_SIZE + 4 + 120 + SECTION_GAP
IMG_H = PAD + section_h + 30 + section_h + PAD

img = Image.new("RGBA", (IMG_W, IMG_H), BG)
d = ImageDraw.Draw(img)

y = PAD

# Mono section
oy, osize, ox = draw_section(d, y, "Iosevka monospace: ellipsis variant comparison", "default_mono", "dense_mono", IMG_W)
overlay_layer = Image.new("RGBA", (IMG_W, IMG_H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay_layer)
od.text((ox, oy), "\u2026  a\u2026z  \u22EF", fill=(97, 175, 239, 180), font=load("dense_mono", 120))
img = Image.alpha_composite(img, overlay_layer)
d = ImageDraw.Draw(img)

y2 = oy + 120 + 40

# QP section
oy2, osize2, ox2 = draw_section(d, y2, "Iosevka quasi-proportional: ellipsis variant comparison", "default_qp", "dense_qp", IMG_W)
overlay_layer2 = Image.new("RGBA", (IMG_W, IMG_H), (0, 0, 0, 0))
od2 = ImageDraw.Draw(overlay_layer2)
od2.text((ox2, oy2), "\u2026  a\u2026z  \u22EF", fill=(97, 175, 239, 180), font=load("dense_qp", 120))
img = Image.alpha_composite(img, overlay_layer2)

img.convert("RGB").save("ellipsis_comparison.png")
print("Saved ellipsis_comparison.png")

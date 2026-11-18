#!/usr/bin/env python3
"""Draw v2 front page for news-image-20261117: 42 verified stories from
Tuesday 17 November 2026, six continents, one front page with a world map.

Deterministic: stdlib + Pillow only, no network, no randomness. Every story
is sourced in SOURCES.md (each verified in at least one named news source
dated 17 Nov 2026; most in two or more). Run: python3 draw.py -> entry.png
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (158, 27, 27)
SEA = (206, 224, 231)
LAND = (233, 222, 192)
LAND_EDGE = (138, 122, 85)
RULE = (120, 110, 95)

FD = "/usr/share/fonts/truetype/dejavu"
F = {
    "mast": ImageFont.truetype(f"{FD}/DejaVuSerif-Bold.ttf", 56),
    "tag": ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 13),
    "map_title": ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 12),
    "map_lab": ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 10),
    "map_num": ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 7),
    "lead_head": ImageFont.truetype(f"{FD}/DejaVuSerif-Bold.ttf", 26),
    "lead_deck": ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 13),
    "kick": ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 10),
    "head": ImageFont.truetype(f"{FD}/DejaVuSerif-Bold.ttf", 13),
    "deck": ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 11),
    "colhead": ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 11),
    "foot": ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 10),
    "foot_b": ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 10),
}

# (num, region, lat, lon, headline, deck) — terse newspaper style.
STORIES = [
    (1, "EUROPE", 45.3, 34.0, "Ukraine strikes Crimea Bridge",
     "Road arch falls into the strait; Russia hits Kyiv bridges in reply."),
    (2, "EUROPE", 51.5, -0.1, "UK sanctions settlement builders",
     "Eight Israeli firms blacklisted, plus a group blocking Gaza aid."),
    (3, "EUROPE", 48.9, 2.3, "Depardieu admits assault in court",
     "The actor apologises in a Paris court; his suspended sentence stands."),
    (4, "EUROPE", 48.9, 2.8, "Le Pen leads French poll at 32-36%",
     "Tops polls; pledges €900bn pension fund if she wins."),
    (5, "EUROPE", 48.4, 22.7, "Hungary halts trains after drone falls",
     "A Russian drone fell 300m from Mukachevo station; crew evacuated."),
    (6, "EUROPE", 50.8, 4.4, "8,000 hoax bomb threats hit Europe",
     "A Reuters tally counts dozens of diverted flights and school evacuations."),
    (7, "EUROPE", 48.2, 16.4, "Austria moves on Kneissl citizenship",
     "Ex-minister, in Russia since 2023, faces citizenship inquiry."),
    (8, "EUROPE", 51.0, -0.6, "Russia warns UK over G20 Putin ban",
     "Moscow says London faces ‘serious consequences’ if it bars Putin in 2027."),
    (9, "EUROPE", 50.3, 5.0, "Burnham: Brexit cost Britain more",
     "PM to meet EU leaders after Friday's summit; most MEPs back rejoining."),
    (10, "ASIA", 35.7, 139.7, "Japan jets meet Russian planes",
     "Tokyo protests ‘strongly’ after two suspected Russian planes enter airspace."),
    (11, "ASIA", 14.6, 121.0, "Trump in Manila for ASEAN summit",
     "Hundreds arrested in protests as the US president attends the summit."),
    (12, "ASIA", 22.5, 114.1, "Xi-Trump-Putin summit set Thursday",
     "Three leaders meet in Shenzhen after the APEC plenary; one hour set aside."),
    (13, "ASIA", 39.9, 116.4, "China rejects US chip-cloud curbs",
     "Beijing calls it an export-control expansion, vows response."),
    (14, "ASIA", 47.9, 106.9, "Mongolia president to resign",
     "Khurelsukh denies wrongdoing over $25m rail-project claim."),
    (15, "ASIA", 23.8, 90.4, "Bangladesh garment workers clash",
     "Police fire tear gas as workers demanding higher wages block highways."),
    (16, "ASIA", 39.4, 116.9, "Xi and Carney agree tariff cuts",
     "China offers $280m relief on Canadian exports; Canada extends exemptions."),
    (17, "MIDDLE EAST", 26.2, 50.6, "Iran drones hit US radar in Bahrain",
     "Revolutionary Guards say they hit the Sheikh Isa site; Bahrain says blocked."),
    (18, "MIDDLE EAST", 26.9, 56.0, "US strikes missile site on Qeshm",
     "US warplanes hit the site in retaliation for Iran targeting US assets."),
    (19, "MIDDLE EAST", 25.7, 56.7, "Hormuz tanker burns; 24 evacuated",
     "Oman rescues Tara Gas crew off Musandam; two hospitalised."),
    (20, "MIDDLE EAST", 24.7, 46.7, "Houthis claim Saudi pipeline attack",
     "Five drones aimed at two pipeline pumping stations near Riyadh, group says."),
    (21, "MIDDLE EAST", 15.4, 44.2, "Houthi advance forces Yemen retreat",
     "Government troops pull back from the Red Sea coast to defend Aden."),
    (22, "MIDDLE EAST", 33.3, 35.5, "Israeli strikes hit south Lebanon",
     "Strikes, shelling and detonations hit a dozen villages; no toll given."),
    (23, "MIDDLE EAST", 31.5, 34.5, "Gaza rains deepen shelter crisis",
     "The UN warns floods are wrecking shelters and destroying scarce food."),
    (24, "MIDDLE EAST", 31.8, 35.2, "West: open Gaza aid crossings",
     "Britain, Australia, Canada and Italy call the situation catastrophic."),
    (25, "MIDDLE EAST", 31.5, 35.5, "Netanyahu camp in wiretap row",
     "PM-elect calls it a threat to democracy after the security chief tapped MPs."),
    (26, "MIDDLE EAST", 32.0, 35.6, "Settler kills woman, 72, in Jericho",
     "Palestinian officials say Fadha Wadha was shot outside her home in Jericho."),
    (27, "AFRICA", 1.5, 29.0, "Congo Ebola passes 11,000 cases",
     "The WHO says two vaccine candidates join the trial as deaths pass 5,500."),
    (28, "AFRICA", -29.9, 31.0, "17 killed in two S. Africa shootings",
     "Police say the shootings in KwaZulu-Natal and Gauteng are unrelated."),
    (29, "N. AMERICA", 38.5, -77.1, "Pentagon fails ninth audit in a row",
     "Fourteen of 25 reporting entities pass, up from 11 last year."),
    (30, "N. AMERICA", 38.9, -77.0, "US loses measles elimination status",
     "PAHO cites a year of uninterrupted spread; 13 babies were born with it."),
    (31, "N. AMERICA", 40.7, -74.0, "Wall St falls; Nvidia beats forecasts",
     "Indexes close down about 1% on AI stocks; Nvidia rises after the bell."),
    (32, "N. AMERICA", 37.3, -122.0, "Apple outage hits sign-ins, App Store",
     "Users report being locked out of iCloud and the App Store; Apple fixes it."),
    (33, "N. AMERICA", 37.8, -122.4, "California sues OpenAI over safety",
     "The attorney general says the firm misled the public on AI safeguards."),
    (34, "N. AMERICA", 40.9, -73.9, "Mamdani disbands NYPD unit",
     "New York's mayor shifts protest response to a civilian-led safety team."),
    (35, "N. AMERICA", 38.7, -77.2, "Supreme Court declines DEI appeals",
     "One refusal leaves a ruling that DEI grant cuts likely broke the law in place."),
    (36, "N. AMERICA", 39.1, -76.8, "Trump weighs \u2018dirty bomb\u2019 intel",
     "US: Iran weighs a chemical attack; Tehran denies it."),
    (37, "N. AMERICA", 38.9, -77.3, "Fed's Cook refuses firing hearing",
     "Lawyers call the process unfair, predetermined, citing Fed independence."),
    (38, "N. AMERICA", 40.7, -74.4, "Expert doubts Epstein ruling",
     "A forensic pathologist says the injuries point to murder, not suicide."),
    (39, "S. AMERICA", 25.3, -57.6, "Paraguay attorney general resigns",
     "Emiliano Rolón quits as deputies move to impeach him over a bank scandal."),
    (40, "S. AMERICA", 0.2, -78.5, "Ecuador fishermen sue US over strike",
     "Survivors seek damages for a March drone attack that sank their vessel."),
    (41, "OCEANIA", -35.3, 149.1, "Australia sanctions Israeli settlers",
     "Canberra acts over West Bank expansion as allied pressure on Israel grows."),
    (42, "CLIMATE", 36.9, 30.7, "COP31 draft splits fossil-fuel talks",
     "Ministers take over; EU chief demands clean-energy signal."),
]

REGION_COLOR = {
    "EUROPE": (31, 78, 121), "ASIA": (176, 89, 0), "MIDDLE EAST": (158, 27, 27),
    "AFRICA": (46, 110, 46), "N. AMERICA": (96, 48, 140), "S. AMERICA": (0, 110, 110),
    "OCEANIA": (122, 82, 0), "CLIMATE": (26, 26, 26),
}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-75, 72), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 35), (-80, 26), (-85, 20), (-90, 15), (-95, 16), (-100, 20), (-105, 23), (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 70), (-50, 76), (-60, 74), (-58, 64)],
    [(-80, 10), (-75, 12), (-70, 12), (-62, 10), (-55, 5), (-50, 0), (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50), (-73, -53), (-70, -45), (-73, -35), (-70, -20), (-80, -5), (-81, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (30, 70), (25, 71), (18, 69), (12, 65), (5, 60), (5, 58), (-5, 50), (-10, 43)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 52)],
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (38, 22), (43, 12), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (15, -28), (12, -18), (8, -2), (9, 4), (-8, 5), (-15, 10), (-17, 15), (-16, 20), (-10, 28)],
    [(28, 70), (40, 68), (55, 72), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (155, 50), (150, 45), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 32), (118, 25), (110, 20), (108, 15), (105, 10), (103, 5), (100, 8), (98, 12), (95, 16), (92, 21), (88, 22), (85, 20), (80, 15), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26), (55, 26), (52, 28), (50, 29), (48, 30), (44, 30), (42, 36), (38, 36), (35, 36), (30, 36), (28, 40), (28, 55), (25, 60), (28, 68)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41), (143, 43), (145, 44), (142, 42), (140, 36), (137, 34), (133, 32)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
]


def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def country_borders():
    """Country outlines from Natural Earth data (countries.geo.json)."""
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "countries.geo.json")
    try:
        data = json.load(open(path))
    except Exception:
        return []
    rings = []
    for feat in data.get("features", []):
        geom = feat.get("geometry") or {}
        typ, coords = geom.get("type"), geom.get("coordinates")
        if typ == "Polygon":
            rings.extend(coords)
        elif typ == "MultiPolygon":
            for poly in coords:
                rings.extend(poly)
    return rings


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=RULE, width=1)
    lon0, lon1, lat0, lat1 = -180, 180, 85, -55

    def px(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * w,
                y0 + (lat0 - lat) / (lat0 - lat1) * h)

    for lon in range(-150, 181, 30):
        x = x0 + (lon - lon0) / (lon1 - lon0) * w
        d.line([(x, y0), (x, y0 + h)], fill=(190, 210, 218), width=1)
    for lat in range(-30, 86, 30):
        y = y0 + (lat0 - lat) / (lat0 - lat1) * h
        d.line([(x0, y), (x0 + w, y)], fill=(190, 210, 218), width=1)
    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND, outline=LAND_EDGE)
    for ring in country_borders():
        pts = [px(lon, lat) for lon, lat in ring]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            if abs(bx - ax) > 200:
                continue
            d.line([(ax, ay), (bx, by)], fill=(150, 130, 90), width=1)
    for label, lon, lat in [("N. AMERICA", -100, 55), ("S. AMERICA", -60, -15),
                            ("EUROPE", 15, 58), ("AFRICA", 20, 5),
                            ("ASIA", 95, 55), ("OCEANIA", 134, -28)]:
        lx, ly = px(lon, lat)
        d.text((lx, ly), label, font=F["map_lab"], fill=(90, 80, 60), anchor="mm")
    for num, region, lat, lon, head, deck in STORIES:
        dx, dy = px(lon, lat)
        r = 5
        col = REGION_COLOR[region]
        d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=col, outline=(255, 255, 255), width=1)
        d.text((dx, dy), str(num), font=F["map_num"], fill=(255, 255, 255), anchor="mm")


def draw_bridge(d, x0, y0, w, h):
    """Schematic illustration (drawn in code) of the damaged Kerch Bridge."""
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=RULE, width=1, fill=(232, 238, 240))
    sea_y = y0 + h - 22
    d.rectangle([x0, sea_y, x0 + w, y0 + h], fill=(178, 205, 220))
    for i in range(5):
        wx = x0 + 20 + i * 65
        d.arc([wx, sea_y + 4, wx + 30, sea_y + 16], 0, 180, fill=(90, 130, 160), width=1)
    d.line([(x0 + 8, y0 + 34), (x0 + w // 2 - 6, y0 + 34)], fill=INK, width=3)
    d.line([(x0 + w // 2 + 30, y0 + 52), (x0 + w - 8, y0 + 62)], fill=INK, width=3)
    for tx in (x0 + 60, x0 + 170):
        d.line([(tx, y0 + 10), (tx, y0 + 34)], fill=INK, width=2)
    d.arc([x0 + w // 2 - 40, y0 + 20, x0 + w // 2 + 60, y0 + 66], 200, 340, fill=RED, width=3)
    d.line([(x0 + w // 2 + 6, y0 + 44), (x0 + w // 2 + 26, sea_y + 2)], fill=RED, width=2)
    d.text((x0 + w // 2, y0 + 6), "KERCH STRAIT \u2014 ILLUSTRATION", font=F["map_lab"], fill=INK, anchor="ma")
    d.text((x0 + 8, y0 + h - 18), "Road arch down; rail span hit", font=F["map_lab"], fill=(40, 60, 80))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- Masthead ----
    d.text((W // 2, 42), "THE WORLD TODAY", font=F["mast"], fill=INK, anchor="mm")
    d.line([(20, 78), (W - 20, 78)], fill=RED, width=3)
    d.text((20, 88), "TUESDAY 17 NOVEMBER 2026", font=F["tag"], fill=RED)
    tag = "42 stories  \u00b7  six continents  \u00b7  one front page and a world map"
    d.text((W - 20, 88), tag, font=F["tag"], fill=INK, anchor="ra")
    d.line([(20, 102), (W - 20, 102)], fill=INK, width=1)
    # ---- Map band ----
    d.text((20, 112), "THE WORLD AT A GLANCE \u2014 WHERE TODAY'S NEWS HAPPENED",
           font=F["map_title"], fill=INK)
    d.text((W - 20, 112), "Dots are numbered 1\u201342 to match the stories below",
           font=F["map_lab"], fill=(80, 70, 60), anchor="ra")
    draw_map(d, 20, 124, W - 40, 130)
    lx, ly = 20, 260
    for region in ["EUROPE", "ASIA", "MIDDLE EAST", "AFRICA", "N. AMERICA", "S. AMERICA", "OCEANIA", "CLIMATE"]:
        col = REGION_COLOR[region]
        d.ellipse([lx, ly + 2, lx + 8, ly + 10], fill=col)
        d.text((lx + 12, ly + 1), region, font=F["map_lab"], fill=INK)
        lx += 12 + int(d.textlength(region, font=F["map_lab"])) + 16
    # ---- Lead story ----
    lead = STORIES[0]
    d.line([(20, 276), (W - 20, 276)], fill=INK, width=2)
    d.text((20, 286), "1  \u00b7  LEAD \u2014 EUROPE", font=F["kick"], fill=RED)
    y = 300
    for ln in wrap(d, lead[4], F["lead_head"], 620)[:1]:
        d.text((20, y), ln, font=F["lead_head"], fill=INK)
        y += 30
    for ln in wrap(d, lead[5], F["lead_deck"], 620)[:2]:
        d.text((20, y), ln, font=F["lead_deck"], fill=(50, 50, 50))
        y += 17
    draw_bridge(d, 660, 282, 344, 76)
    d.line([(20, 366), (W - 20, 366)], fill=INK, width=1)
    # ---- Story grid: 6 columns ----
    rest = STORIES[1:]
    cols = [rest[0:7], rest[7:14], rest[14:21], rest[21:27], rest[27:34], rest[34:]]
    headers = ["EUROPE", "EUROPE & ASIA", "ASIA & M. EAST", "M. EAST & AFRICA", "NORTH AMERICA", "AMERICAS & WORLD"]
    margin, gutter = 20, 8
    col_w = (W - 2 * margin - 5 * gutter) // 6
    top, bottom = 378, 956
    for ci, col in enumerate(cols):
        x = margin + ci * (col_w + gutter)
        d.text((x, top), headers[ci], font=F["colhead"], fill=RED)
        d.line([(x, top + 14), (x + col_w, top + 14)], fill=RED, width=1)
        y = top + 20
        for num, region, lat, lon, head, deck in col:
            d.text((x, y), f"{num} \u00b7 {region}", font=F["kick"], fill=REGION_COLOR[region])
            y += 10
            hl = wrap(d, head, F["head"], col_w)
            if len(hl) > 2:
                print(f"WARNING head wraps to {len(hl)} lines: #{num}")
            for ln in hl[:2]:
                d.text((x, y), ln, font=F["head"], fill=INK)
                y += 14
            dl = wrap(d, deck, F["deck"], col_w)
            if len(dl) > 3:
                print(f"WARNING deck wraps to {len(dl)} lines: #{num}")
            for ln in dl[:3]:
                d.text((x, y), ln, font=F["deck"], fill=(60, 60, 60))
                y += 11
            y += 2
            d.line([(x, y), (x + col_w, y)], fill=(200, 192, 175), width=1)
            y += 3
        print(f"column {ci}: {len(col)} stories, ends y={y}")
        if y > bottom:
            print(f"WARNING column {ci} overflows to y={y} (limit {bottom})")
    # ---- Footer ----
    d.line([(20, 966), (W - 20, 966)], fill=INK, width=2)
    d.text((20, 976), "INSIDE:  Europe 9  \u00b7  Asia 7  \u00b7  Middle East 10  \u00b7  Africa 2  \u00b7  N. America 10  \u00b7  S. America 2  \u00b7  Oceania 1  \u00b7  Climate 1  \u2014  all 42 reported Tuesday 17 November 2026.",
           font=F["foot_b"], fill=INK)
    d.text((20, 994), "Sources: Reuters, BBC, AP, NYT, WSJ, Politico, PAHO, UN, WHO \u2014 full list in SOURCES.md.  Markets: S&P 500 7,340.53 (\u22121%) \u00b7 Dow 50,759.42 (\u22121.6%) \u00b7 Nasdaq 24,328.38 (\u22120.7%).",
           font=F["foot"], fill=(70, 70, 70))
    d.text((W - 20, 994), "Drawn in code.", font=F["foot"], fill=(70, 70, 70), anchor="ra")
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()

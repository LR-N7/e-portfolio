#!/usr/bin/env python3
"""Build the English version of Louis REEVES' CV.

The layout, colours and typography mirror the French CV (Louis_REEVES.pdf):
same A4 page, same grey left column, same Questrial / Glacial Indifference
typefaces, same photo.  Only the text is translated.

Usage:  python3 tools/build_cv_en.py
Output: Louis_REEVES_CV_EN.pdf  (repository root)

Requires: pymupdf  ->  pip install pymupdf
Fonts:    tools/fonts/Questrial-Regular.ttf
          tools/fonts/GlacialIndifference-Regular.ttf
          tools/fonts/GlacialIndifference-Bold.ttf
"""

import pathlib

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
SOURCE_FR_CV = ROOT / "Louis_REEVES.pdf"
OUTPUT = ROOT / "Louis_REEVES_CV_EN.pdf"

# --------------------------------------------------------------------------
# Style
# --------------------------------------------------------------------------
PAGE_W, PAGE_H = 595.5, 842.25
SIDEBAR_W = 207.0

GREY_BG = (0.3922, 0.3922, 0.3922)          # #646464 sidebar
WHITE = (1.0, 1.0, 1.0)
INK = (0.2314, 0.2314, 0.2314)              # #3b3b3b name / headings
BLUE = (0.1804, 0.4902, 0.6863)             # #2e7daf body accents
MUTED = (0.3922, 0.3922, 0.3922)            # #646464 dates & places
RULE = (0.7059, 0.7059, 0.7059)             # #b4b4b4 rules
SIDEBAR_LABEL = (0.7059, 0.7059, 0.7059)    # #b4b4b4 sidebar headings

FONT_FILES = {
    "cv-reg": FONTS / "Questrial-Regular.ttf",
    "cv-txt": FONTS / "GlacialIndifference-Regular.ttf",
    "cv-bold": FONTS / "GlacialIndifference-Bold.ttf",
    "cv-brand": FONTS / "FontAwesomeBrands.ttf",
}
F_REG = pymupdf.Font(fontfile=str(FONT_FILES["cv-reg"]))
F_TXT = pymupdf.Font(fontfile=str(FONT_FILES["cv-txt"]))
F_BOLD = pymupdf.Font(fontfile=str(FONT_FILES["cv-bold"]))
F_BRAND = pymupdf.Font(fontfile=str(FONT_FILES["cv-brand"]))
LINKEDIN = "\uf0e1"      # fa-linkedin-in
GITHUB = "\uf09b"        # fa-github
NAME_OF = {id(F_REG): "cv-reg", id(F_TXT): "cv-txt", id(F_BOLD): "cv-bold"}

# Right hand column geometry
CONTENT_L = 231.6
CONTENT_R = 588.0
CONTENT_W = CONTENT_R - CONTENT_L
META_L = 211.0                          # dates / places column
META_W = 88.0
MAIN_L = 304.7                          # entry body column
MAIN_W = CONTENT_R - MAIN_L

# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------
NAME = "Louis REEVES"

HEADLINE = (
    "SEEKING A 6-MONTH FINAL-YEAR INTERNSHIP TO DEEPEN",
    "MY SOFTWARE ENGINEERING SKILLS",
)

INTRO = (
    "COMPUTER ENGINEERING STUDENT AT ENSEEIHT. PASSIONATE ABOUT",
    "BUILDING SOFTWARE, I JOINED THE SOFTWARE SYSTEMS TRACK",
    "TO REFINE MY TECHNICAL SKILLS.",
)

CONTACT = [
    ("mail", "louis.reeves@etu.inp-n7.fr"),
    ("phone", "06 40 82 48 12"),
    ("linkedin", "linkedin.com/in/louis-reeves1"),
    ("github", "github.com/LR-N7"),
]

LANGUAGES = ["French (native)", "English (C1)", "Chinese (B2)"]

INTERESTS = [
    "CLIMBING",
    "CHINESE CULTURE",
    'DRUMMER IN THE BAND "5 SENS"',
    "VOLUNTEER AT ESCA'LLARGUES CLIMBING CLUB",
    "REGULAR PARTICIPANT IN TOULOUSE OUTREACH ROUNDS",
]

EXPERIENCE = [
    {
        "date": ("MARCH - AUGUST", "2028"),
        "place": ("Huawei,", "Shenzhen (China)"),
        "title": "SOFTWARE DEVELOPMENT INTERN",
        "body": [
            "Took part in the development and improvement of software "
            "solutions within an engineering team.",
            "Contributed to the design and implementation of back-end "
            "features in Java, to API integration and to data management.",
            "This experience introduced me to professional development "
            "workflows and to working in a multicultural team.",
        ],
        "bullets": [
            "Java, Spring Boot, SQL, Git, Linux, Docker",
            "Back-end development, REST API design, software testing, "
            "debugging, international teamwork",
        ],
    },
    {
        "date": ("SUMMER 2027",),
        "place": ("Dragon Phoenix,", "Shanghai (China)"),
        "title": "RESTAURANT WORK IN CHINA (SHANGHAI)",
        "body": [],
        "bullets": [
            "3 weeks of Chinese language classes",
            "4-week professional internship at Dragon Phoenix",
            "Management, cultural adaptation, teamwork",
        ],
    },
]

PROJECTS = [
    {
        "title": "ALGORITHM FINDING THE BEST CLIMBING ROUTES",
        "body": "I built an application that determines the moves requiring "
                "the least physical effort for a climber, maximizing their "
                "chances of not falling off the wall.",
        "bullets": ["Python, HTML, Streamlit, Replit"],
    },
]

EDUCATION = [
    {
        "title": "TOULOUSE INP-ENSEEIHT - 2026/",
        "lines": ("Department of Digital Sciences", "Software Systems track"),
    },
    {
        "title": "LYCÉE DHUODA - 2024/2026",
        "lines": ("Preparatory classes for engineering schools, PTSI/PT track",),
    },
]


# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------
def text_width(txt, font, size, spacing=0.0):
    return font.text_length(txt, size) + spacing * max(len(txt) - 1, 0)


class Painter:
    def __init__(self, page):
        self.page = page

    def text(self, x, y, txt, font, size, color=INK, spacing=0.0):
        """Draw a line of text; ``y`` is the top of the line."""
        name = NAME_OF[id(font)]
        base = y + size * 0.82
        if spacing:
            shift = 0.0
            for ch in txt:
                if ch != " ":
                    self.page.insert_text((x + shift, base), ch,
                                          fontname=name,
                                          fontfile=str(FONT_FILES[name]),
                                          fontsize=size, color=color)
                shift += font.text_length(ch, size) + spacing
        else:
            self.page.insert_text((x, base), txt, fontname=name,
                                  fontfile=str(FONT_FILES[name]),
                                  fontsize=size, color=color)

    def centred(self, cx, y, txt, font, size, color=INK, spacing=0.0):
        self.text(cx - text_width(txt, font, size, spacing) / 2, y, txt,
                  font, size, color, spacing)

    def rule(self, x, y, w=49.0, h=4.3, color=RULE):
        self.page.draw_rect(pymupdf.Rect(x, y, x + w, y + h),
                            color=None, fill=color)

    def dot(self, x, y, r=1.5, color=BLUE):
        self.page.draw_circle(pymupdf.Point(x + r, y + r), r,
                              color=None, fill=color)


def wrap(text, font, size, width, spacing=0.0):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width(trial, font, size, spacing) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def section_title(p, y, label):
    p.centred(CONTENT_L + CONTENT_W / 2, y, label, F_REG, 14.7, INK,
              spacing=2.6)
    p.rule(CONTENT_L + 9, y + 24)
    return y + 36


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
def draw_photo(page, cx, cy, r):
    src = pymupdf.open(SOURCE_FR_CV)
    imgs = src[0].get_images(full=True)
    xref = max(imgs, key=lambda i: src.extract_image(i[0])["width"])[0]
    info = src.extract_image(xref)
    photo = info["image"]
    iw, ih = info["width"], info["height"]

    page.draw_circle(pymupdf.Point(cx, cy), r, color=None, fill=WHITE)
    # keep the same framing as the French CV: the portrait fills the circle,
    # zoomed on the face rather than showing the whole picture
    crop_w = 0.58                     # share of the photo width shown
    crop_h = crop_w * iw / ih         # square crop -> undistorted
    focus_x, focus_y = 0.615, 0.42    # where the face sits in the circle
    w = 2 * r / crop_w
    h = 2 * r / crop_h
    page.insert_image(pymupdf.Rect(cx - focus_x * w, cy - focus_y * h,
                                   cx + (1 - focus_x) * w,
                                   cy + (1 - focus_y) * h), stream=photo)
    # the photo is wider than the sidebar: repaint the content area
    page.draw_rect(pymupdf.Rect(SIDEBAR_W, 0, PAGE_W, PAGE_H), color=None,
                   fill=WHITE)
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, SIDEBAR_W, PAGE_H))
    shape.draw_circle(pymupdf.Point(cx, cy), r)
    shape.finish(color=None, fill=GREY_BG, even_odd=True)
    shape.commit()


def draw_contact_icon(page, kind, y):
    if kind == "mail":
        page.draw_rect(pymupdf.Rect(2.6, y, 21.6, y + 13.4),
                       color=WHITE, width=1.1)
        page.draw_line(pymupdf.Point(2.6, y), pymupdf.Point(12.1, y + 7.4),
                       color=WHITE, width=1.1)
        page.draw_line(pymupdf.Point(21.6, y), pymupdf.Point(12.1, y + 7.4),
                       color=WHITE, width=1.1)
    elif kind == "phone":
        page.draw_rect(pymupdf.Rect(6.2, y - 1, 15.4, y + 19.6),
                       color=WHITE, width=1.1)
        page.draw_line(pymupdf.Point(9.4, y + 16.4), pymupdf.Point(12.2, y + 16.4),
                       color=WHITE, width=1.1)
    elif kind == "linkedin":
        page.draw_rect(pymupdf.Rect(2.4, y - 2.2, 19.4, y + 15.6),
                       color=None, fill=WHITE, radius=0.12)
        page.insert_text((5.5, y + 11.0), LINKEDIN, fontname="cv-brand",
                         fontfile=str(FONT_FILES["cv-brand"]),
                         fontsize=9.6, color=GREY_BG)
    elif kind == "github":
        page.insert_text((1.0, y + 16.0), GITHUB, fontname="cv-brand",
                         fontfile=str(FONT_FILES["cv-brand"]),
                         fontsize=19.0, color=WHITE)


def draw_sidebar(page, p):
    cx = SIDEBAR_W / 2 - 3

    draw_photo(page, 98.0, 121.0, 91.0)

    # contact --------------------------------------------------------------
    y = 241.0
    p.centred(cx, y, "CONTACT", F_REG, 14.7, SIDEBAR_LABEL, spacing=3.4)
    p.rule(22.7, y + 18)

    y = 276.0
    for kind, value in CONTACT:
        draw_contact_icon(page, kind, y - 1)
        p.text(33.3, y, value, F_TXT, 10.5, WHITE)
        y += 26.5

    # languages ------------------------------------------------------------
    y = 410.0
    p.centred(cx, y, "LANGUAGES", F_REG, 14.7, SIDEBAR_LABEL, spacing=3.4)
    p.rule(21.8, y + 18)

    y = 455.0
    for lang in LANGUAGES:
        p.text(17.1, y, lang, F_TXT, 11.2, WHITE)
        y += 30.0

    # interests ------------------------------------------------------------
    y = 552.0
    p.centred(cx, y, "INTERESTS /", F_REG, 14.7, SIDEBAR_LABEL, spacing=3.4)
    p.centred(cx, y + 19.5, "ENGAGEMENTS", F_REG, 14.7, SIDEBAR_LABEL,
              spacing=3.4)
    p.rule(22.7, y + 39)

    y = 632.0
    for item in INTERESTS:
        for i, line in enumerate(wrap(item, F_REG, 10.0, 170)):
            if i == 0:
                p.dot(13.4, y + 1)
            p.text(23.7, y, line, F_REG, 10.0, WHITE)
            y += 11.6
        y += 12.0


# --------------------------------------------------------------------------
# Main column
# --------------------------------------------------------------------------
def draw_experience(p, y):
    y = section_title(p, y, "EXPERIENCES")

    for job in EXPERIENCE:
        meta_y = y
        main_y = y

        for line in job["date"]:
            p.text(META_L, meta_y, line, F_BOLD, 10.0, MUTED)
            meta_y += 13.0
        for line in job["place"]:
            p.text(META_L, meta_y, line, F_BOLD, 10.0, INK)
            meta_y += 13.5

        for line in wrap(job["title"], F_BOLD, 8.9, MAIN_W):
            p.text(MAIN_L, main_y, line, F_BOLD, 8.9, INK)
            main_y += 12.0
        main_y += 1.5

        for para in job["body"]:
            for line in wrap(para, F_TXT, 8.9, MAIN_W):
                p.text(MAIN_L, main_y, line, F_TXT, 8.9, BLUE)
                main_y += 9.7
            main_y += 6.0

        for bullet in job["bullets"]:
            lines = wrap(bullet, F_TXT, 8.9, MAIN_W - 15.0)
            for i, line in enumerate(lines):
                if i == 0:
                    p.dot(MAIN_L + 5.0, main_y + 2.0)
                p.text(MAIN_L + 15.0, main_y, line, F_TXT, 8.9, BLUE)
                main_y += 9.7
            main_y += 5.8

        y = max(meta_y, main_y) + 18.0

    return y


def draw_projects(p, y):
    y = section_title(p, y, "PROJECTS")

    for proj in PROJECTS:
        p.text(CONTENT_L, y, proj["title"], F_BOLD, 8.0, INK)
        y += 15.0
        for line in wrap(proj["body"], F_TXT, 10.0, CONTENT_W):
            p.text(CONTENT_L, y, line, F_TXT, 10.0, BLUE)
            y += 11.0
        y += 3.5
        for bullet in proj["bullets"]:
            for i, line in enumerate(wrap(bullet, F_TXT, 10.0, CONTENT_W - 15)):
                if i == 0:
                    p.dot(CONTENT_L + 5.0, y + 2.0)
                p.text(CONTENT_L + 15.0, y, line, F_TXT, 10.0, BLUE)
                y += 11.0
        y += 14.0

    return y + 12.0


def draw_education(p, y):
    y = section_title(p, y, "EDUCATION")

    for school in EDUCATION:
        p.text(CONTENT_L, y, school["title"], F_BOLD, 10.0, INK)
        y += 15.0
        for line in school["lines"]:
            for l in wrap(line, F_TXT, 10.0, CONTENT_W - 2):
                p.text(CONTENT_L + 2.0, y, l, F_TXT, 10.0, BLUE)
                y += 13.0
        y += 12.0

    return y


# --------------------------------------------------------------------------
# Build the page
# --------------------------------------------------------------------------
TARGET_BOTTOM = 790.0     # where the last line of the CV should end


def layout(page, extra_gap=0.0):
    """Draw the whole page; returns the y of the last line drawn."""
    p = Painter(page)

    page.draw_rect(page.rect, color=None, fill=WHITE)
    page.draw_rect(pymupdf.Rect(0, 0, SIDEBAR_W, PAGE_H), color=None,
                   fill=GREY_BG)

    draw_sidebar(page, p)

    # header ---------------------------------------------------------------
    p.text(235.5, 41.8, NAME, F_REG, 42.0, INK)

    y = 94.8
    for line in HEADLINE:
        p.text(239.7, y, line, F_BOLD, 8.0, INK, spacing=0.45)
        y += 10.6

    y += 6.0
    for line in INTRO:
        p.text(239.7, y, line, F_TXT, 8.0, INK, spacing=0.45)
        y += 10.6

    # body -----------------------------------------------------------------
    y = draw_experience(p, max(180.0, y + 24.0) + 10.0 + extra_gap)
    y = draw_projects(p, y + 14.0 + extra_gap)
    return draw_education(p, y + extra_gap)


def build():
    # pass 1: measure how tall the content is with the base spacing
    probe = pymupdf.open()
    base_bottom = layout(probe.new_page(width=PAGE_W, height=PAGE_H))
    probe.close()

    # pass 2: spread the remaining space evenly between the three blocks
    extra = min(max((TARGET_BOTTOM - base_bottom) / 3.0, 0.0), 20.0)

    doc = pymupdf.open()
    layout(doc.new_page(width=PAGE_W, height=PAGE_H), extra_gap=extra)

    doc.set_metadata({
        "title": "Louis REEVES - CV (English)",
        "author": "Louis REEVES",
        "subject": "Curriculum Vitae - English version",
        "keywords": "CV, resume, software engineering, ENSEEIHT",
        "creator": "tools/build_cv_en.py",
    })
    doc.subset_fonts()
    doc.save(str(OUTPUT), garbage=4, deflate=True)
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size / 1024:.0f} kB)")


if __name__ == "__main__":
    build()

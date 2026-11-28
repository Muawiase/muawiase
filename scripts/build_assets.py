"""Generate the profile README's SVG blocks into ../assets.

Run:  python scripts/build_assets.py

Layout: every block is 840px wide. Full-width blocks and the button rows share
the outer edges (0 and 840). Section blocks have 24px padding, and their cards
sit on an inner 3- or 2-column grid with 12px gutters.

Each block paints its own background, so one file works on GitHub's light and
dark themes. White and lavender blocks get a border or rounded corners so they
read as panels (not holes) on the dark theme, and navy blocks get a subtle
border so they separate from GitHub's dark page.

Logos: Simple Icons (CC0), vendored in scripts/icons.json and pasted inline,
since GitHub won't load external images from inside an SVG.
Hero image: the original is assets/developer-roadmap.jpg. A 656px-tall copy
(scripts/hero-image.jpg, 2x the panel height) is embedded as a base64 data URI.
"""
import base64
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
ICONS = json.loads((ROOT / "icons.json").read_text(encoding="utf-8"))["icons"]
HERO_IMG = base64.b64encode((ROOT / "hero-image.jpg").read_bytes()).decode()

W = 840
GAP = 12
PAD = 24                          # section padding
IW = W - 2 * PAD                  # 792, inner width
ICOL3 = (IW - 2 * GAP) // 3       # 256, inner 3-col card
ICOL2 = (IW - GAP) // 2           # 390, inner 2-col card
COL3 = (W - 2 * GAP) // 3         # 272, outer 3-col (contact buttons)
COL2 = (W - GAP) // 2             # 414, outer 2-col (hero CTAs)
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

# ---------------------------------------------------------------- palette
# Brand tokens from the inspiration site's stylesheet (--base-color-brand--*).
BLUE = "#000DFF"       # brand blue
NAVY = "#000033"       # brand blue-dark
BLUE1 = "#666EFF"      # blue-light-1
BLUE2 = "#B3B7FF"      # blue-light-2
BLUE3 = "#E6E7FF"      # blue-light-3 (lavender section background)
GREEN = "#00FF3C"      # green-neon
WHITE = "#FFFFFF"
NAVY_LINE = "#1F2477"  # hairlines / borders on navy
BODY = "#3A3A66"       # body text on white (contrast 11:1)

# ---------------------------------------------------------------- content
NAME = "Muawia"
ROLE = "FULL STACK DEVELOPER"
TAGLINE = ["Turning ideas into production-ready", "products with Python and JavaScript."]
HERO_STACK = ["python", "javascript", "nodejs", "nextjs", "docker"]
ABOUT = ("I'm Muawia, a full stack developer who turns ideas into working products. "
         "Lately I've been building Claude-powered apps and taking them all the way to "
         "deployment with Python, Node.js, Next.js and Docker.")
EDU_TITLE = "Software Engineering (BSE), Cavendish University Uganda"
EDU_STATUS = "Currently studying"
STATS = [("10+", "Projects shipped"), ("5", "Large-scale projects"), ("20K+", "Commits")]
SKILLS = [
    (["html5", "css3", "javascript"], "Frontend", "Responsive UIs in HTML, CSS and JS"),
    (["nodejs"], "Backend", "REST APIs and services on Node.js"),
    (["nextjs"], "Next.js", "Full stack apps, SSR and API routes"),
    (["python"], "Python", "Backends, scripting and automation"),
    (["docker"], "Docker / DevOps", "Containerised builds and deploys"),
    (["react"], "React", "Component-based UIs, hooks and state"),
]
TECH = [("python", "Python"), ("javascript", "JavaScript"), ("nodejs", "Node.js"),
        ("nextjs", "Next.js"), ("react", "React"), ("docker", "Docker"), ("html5", "HTML"), ("css3", "CSS")]
NOW = [
    ("BUILDING", "Scalable APIs and backend services in Python and Node.js"),
    ("LEARNING", "Claude-powered apps, taken all the way to deployment"),
]
# key: (label, icon, primary)
BUTTONS = {
    "getintouch": ("Get in touch", "mail", True),
    "email": ("Email", "mail", True),
    "whatsapp": ("WhatsApp", "whatsapp", False),
    "linkedin": ("LinkedIn", "linkedin", False),
}


# ---------------------------------------------------------------- primitives
def svg(w, h, body, title, extra_css="", pad=8):
    """pad: transparent space under the block so stacked images get a gutter."""
    h += pad
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n"
        f'<style>text{{font-family:{FONT};}}{extra_css}</style>\n'
        f"{body}\n</svg>\n"
    )


def t(x, y, s, size, fill, weight=400, anchor="start", ls=0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}">{escape(s)}</text>')


def rect(x, y, w, h, fill, stroke=None, rx=0, sw=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}/>'


def panel(x, y, w, h, fill, stroke=None, rx=16):
    # half-pixel inset keeps 1px strokes crisp
    return rect(x + .5, y + .5, w - 1, h - 1, fill, stroke, rx)


def pts(points):
    return " ".join(f"{x:g},{y:g}" for x, y in points)


def diamond(cx, cy, r, fill, stroke=None, sw=1):
    """A square rotated 45 degrees; r is the half-diagonal."""
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<polygon points="{pts([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)])}" '
            f'fill="{fill}"{s}/>')


def chevron_pts(x, y, w, h, p):
    """Rectangle with pointed (chevron) left and right ends, p = point depth."""
    return pts([(x, y + h / 2), (x + p, y), (x + w - p, y), (x + w, y + h / 2),
                (x + w - p, y + h), (x + p, y + h)])


def chevron(x, y, w, h, fill, stroke=None, p=None, sw=1):
    p = h / 2 if p is None else p
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="miter"' if stroke else ""
    return f'<polygon points="{chevron_pts(x, y, w, h, p)}" fill="{fill}"{s}/>'


def text_w(s, size, weight=400, ls=0):
    """Rough advance width for the system sans; good enough for layout."""
    per = {300: .53, 400: .55, 500: .57, 600: .59, 700: .62}[weight]
    upper = sum(1 for ch in s if ch.isupper()) / max(len(s), 1)
    per += .1 * upper
    return len(s) * (size * per + ls)


def chip(x, y, label, fill, txt, dot=None):
    """Bold uppercase label in a chevron-ended chip. y is the top edge."""
    h, p = 26, 11
    tw = text_w(label, 11, 700, 1.6)
    lead = 14 if dot else 0
    w = round(p + 8 + lead + tw + 6 + p)
    out = chevron(x, y, w, h, fill, p=p)
    if dot:
        out += diamond(x + p + 10, y + h / 2, 4, dot)
    out += t(x + p + 8 + lead, y + 17.5, label, 11, txt, 700, ls=1.6)
    return out


def corner(x, y, fill=BLUE, ring=BLUE2):
    """Diamond accent for the top-right corner of a card (x, y = centre)."""
    return diamond(x, y, 9, "none", ring) + diamond(x, y, 4.5, fill)


def wrap(text, n):
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > n:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


def pattern(x0, y0, w, h, step, seed, toward="right", colors=(BLUE, BLUE1), dot="#1F2477"):
    """Dot grid with small diamonds that get denser toward one side."""
    out, s = [], seed
    cols, rows = int(w // step), int(h // step)
    for j in range(rows + 1):
        for i in range(cols + 1):
            x, y = x0 + i * step, y0 + j * step
            s = (s * 1103515245 + 12345) & 0x7FFFFFFF
            r = s / 0x7FFFFFFF
            f = i / cols if toward == "right" else 1 - i / cols
            dens = f ** 1.7
            if r < dens * .85:
                big = r < dens * .3
                out.append(diamond(x, y, 4.5 if big else 3, colors[0] if big else colors[1]))
            else:
                out.append(f'<circle cx="{x}" cy="{y}" r="1.1" fill="{dot}"/>')
    return "".join(out)


# ---------------------------------------------------------------- logos
def logo(key, cx, cy, s):
    """Simple Icons logo centred at (cx, cy), s px square, in brand colours."""
    ic = ICONS[key]
    k = s / 24
    g = f'<g transform="translate({cx - s / 2:g},{cy - s / 2:g}) scale({k:g})">'
    if key == "python":   # two-tone: whole mark in yellow, upper snake in blue on top
        body = (f'<path d="{ic["path"]}" fill="#FFD43B"/>'
                f'<path d="{ic["upper"]}" fill="#3776AB"/>')
    elif key == "javascript":  # yellow square with black letters
        body = f'<rect x=".5" y=".5" width="23" height="23" fill="#000000"/><path d="{ic["path"]}" fill="#F7DF1E"/>'
    else:
        body = f'<path d="{ic["path"]}" fill="#{ic["hex"]}"/>'
    return g + body + "</g>"


def badge(key, cx, cy, r, fill=WHITE, stroke=None):
    """Logo inside a diamond badge (r = half-diagonal)."""
    return diamond(cx, cy, r, fill, stroke) + logo(key, cx, cy, round(r * 0.98))


# ---------------------------------------------------------------- blocks
def hero():
    H = 360
    b = [panel(0, 0, W, H, WHITE, BLUE2)]
    # left: copy
    b.append(chip(40, 40, ROLE, BLUE, WHITE, dot=GREEN))
    b.append(t(34, 162, NAME, 88, NAVY, 300, ls=-2.5))
    for i, line in enumerate(TAGLINE):
        b.append(t(40, 212 + i * 30, line, 20, BODY, 400))
    b.append(f'<line x1="40" y1="276.5" x2="412" y2="276.5" stroke="{BLUE3}" stroke-width="1"/>')
    for i, key in enumerate(HERO_STACK):
        b.append(badge(key, 62 + i * 52, 312, 20, WHITE, BLUE2))
    # right: illustration in the panel (rounded corners). The image is portrait
    # (0.81:1) and the panel landscape (1.12:1), so "meet" shows the whole image
    # undistorted and uncropped, centred. The panel takes the image's own pure
    # black background so the space either side blends in with no visible bars.
    px, py, pw, ph = 456, 16, W - 16 - 456, H - 32
    b.append(rect(px, py, pw, ph, "#000000", rx=12))
    b.append(f'<clipPath id="pc"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"/></clipPath>')
    b.append(f'<image x="{px}" y="{py}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMid meet" '
             f'clip-path="url(#pc)" href="data:image/jpeg;base64,{HERO_IMG}"/>')
    alt = (f"{NAME}, Full Stack Developer. {' '.join(TAGLINE)} Stack: Python, JavaScript, Node.js, Next.js, Docker. "
           "Illustration: a developer roadmap ladder from a project folder up through React, JavaScript, "
           "HTML, CSS, Python, Node.js, Next.js and Docker to cloud hosting.")
    return svg(W, H, "\n".join(b), alt)


def about():
    lines = wrap(ABOUT, 78)
    sep = 104 + (len(lines) - 1) * 30 + 34
    H = sep + 84
    b = [panel(0, 0, W, H, NAVY, NAVY_LINE), corner(W - 36, 36, BLUE, BLUE1),
         chip(32, 28, "ABOUT", BLUE, WHITE)]
    for i, line in enumerate(lines):
        b.append(t(32, 104 + i * 30, line, 19, WHITE, 300))
    b.append(f'<line x1="32" y1="{sep + .5}" x2="{W - 32}" y2="{sep + .5}" stroke="{NAVY_LINE}" stroke-width="1"/>')
    b.append(chip(32, sep + 28, "EDUCATION", BLUE, WHITE))
    b.append(t(168, sep + 46, EDU_TITLE, 16, WHITE, 600))
    sw = text_w(EDU_STATUS, 13, 500, .5)
    b.append(diamond(W - 32 - sw - 14, sep + 41, 4, GREEN))
    b.append(t(W - 32, sep + 46, EDU_STATUS, 13, BLUE2, 500, anchor="end", ls=.5))
    return svg(W, H, "\n".join(b), f"About: {ABOUT} Education: {EDU_TITLE}, {EDU_STATUS.lower()}.")


def card(x, y, w, h):
    return panel(x, y, w, h, WHITE, BLUE2, rx=10) + corner(x + w - 22, y + 22)


def section_head(y, label, title):
    return chip(PAD, y, label, NAVY, WHITE) + t(PAD - 2, y + 66, title, 32, NAVY, 300, ls=-.6)


def skills():
    """Stats row + skills grid: white cards on a lavender section."""
    SH, top = 132, PAD
    head = top + SH + 36
    grid = head + 92
    TH = 150
    H = grid + 2 * TH + GAP + PAD
    b = [panel(0, 0, W, H, BLUE3, BLUE2)]
    for i, (num, label) in enumerate(STATS):
        x = PAD + i * (ICOL3 + GAP)
        b.append(card(x, top, ICOL3, SH))
        b.append(t(x + 22, top + 32, f"0{i + 1}", 11, BLUE, 700, ls=1.6))
        b.append(t(x + 20, top + 88, num, 52, NAVY, 300, ls=-1.5))
        b.append(t(x + 22, top + 114, label, 14, BODY, 500))
    b.append(section_head(head, "SKILLS", "What I work with"))
    for i, (keys, title, desc) in enumerate(SKILLS):
        x, y = PAD + (i % 3) * (ICOL3 + GAP), grid + (i // 3) * (TH + GAP)
        b.append(card(x, y, ICOL3, TH))
        for j, k in enumerate(keys):
            b.append(badge(k, x + 44 + j * 50, y + 44, 24, "#F5F5FF", BLUE2))
        b.append(t(x + 20, y + 108, title, 18, NAVY, 600))
        line = t(x + 20, y + 132, desc, 13, BODY, 400)
        if len(desc) >= 36:  # longest lines: pin to the 216px text area so wider
            # system fonts (e.g. SF Pro) tighten letter-spacing instead of overflowing
            line = line.replace("<text ", f'<text textLength="{ICOL3 - 40}" lengthAdjust="spacing" ', 1)
        b.append(line)
    alt = ("Stats: " + ", ".join(f"{n} {l.lower()}" for n, l in STATS) + ". Skills: "
           + "; ".join(f"{t_}: {d}" for _, t_, d in SKILLS))
    return svg(W, H, "\n".join(b), alt)


def tech():
    H, r, cy = 76, 20, 38
    items, x = [], 0
    for key, label in TECH:
        w = 2 * r + 12 + text_w(label, 15, 500) + 36
        items.append((key, label, x, w))
        x += w
    loop = x
    copies = 2 + int(W // loop)
    track = []
    for c in range(copies):
        for key, label, ix, w in items:
            ox = c * loop + ix + 24
            track.append(badge(key, ox + r, cy, r))
            track.append(t(ox + 2 * r + 12, cy + 5.5, label, 15, WHITE, 500))
            track.append(diamond(ox + w - 18, cy, 2.5, BLUE1))
    css = (f".track{{animation:slide 30s linear infinite;}}"
           f"@keyframes slide{{from{{transform:translateX(0)}}to{{transform:translateX(-{loop:g}px)}}}}"
           f"@media (prefers-reduced-motion:reduce){{.track{{animation:none;}}}}")
    b = [
        '<defs>',
        f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{NAVY}"/>'
        f'<stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{NAVY}"/>'
        f'<stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></linearGradient>',
        f'<clipPath id="cp"><rect x="0" y="0" width="{W}" height="{H}" rx="16"/></clipPath>',
        '</defs>',
        f'<g clip-path="url(#cp)">', rect(0, 0, W, H, NAVY),
        '<g class="track">', *track, '</g>',
        rect(0, 0, 90, H, "url(#fl)"), rect(W - 90, 0, 90, H, "url(#fr)"), '</g>',
        panel(0, 0, W, H, "none", NAVY_LINE),
    ]
    return svg(W, H, "\n".join(b), "Tech stack: " + ", ".join(l for _, l in TECH), css)


def now():
    top = PAD + 92
    TH = 150
    H = top + TH + PAD
    b = [panel(0, 0, W, H, BLUE3, BLUE2), section_head(PAD, "NOW", "What I'm doing now")]
    for i, (label, text) in enumerate(NOW):
        x = PAD + i * (ICOL2 + GAP)
        b.append(card(x, top, ICOL2, TH))
        b.append(diamond(x + 32, top + 36, 5, BLUE))
        b.append(t(x + 46, top + 40.5, label, 11, BLUE, 700, ls=1.6))
        for j, line in enumerate(wrap(text, 32)):
            b.append(t(x + 26, top + 84 + j * 30, line, 21, NAVY, 300))
    alt = "Now: " + "; ".join(f"{l.title()}: {s}" for l, s in NOW)
    return svg(W, H, "\n".join(b), alt)


def activity(theme):
    """Header for the contribution graph, styled like section_head() (chip +
    32px light heading). It sits on the page background, not a panel, so it
    comes in a light version (navy, identical to SKILLS) and a dark version
    (white chip and heading) swapped by <picture> in the README."""
    chip_fill, chip_txt, head = (NAVY, WHITE, NAVY) if theme == "light" else (WHITE, NAVY, WHITE)
    H = 84
    b = [chip(0, 0, "ACTIVITY", chip_fill, chip_txt),
         t(-2, 66, "Contribution graph", 32, head, 300, ls=-.6)]
    return svg(W, H, "\n".join(b), "Activity: contribution graph")


def contact():
    H = 176
    b = [panel(0, 0, W, H, NAVY, NAVY_LINE),
         f'<clipPath id="cc"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="15"/></clipPath>',
         f'<g clip-path="url(#cc)">{pattern(520, 16, 304, 150, 18, 11)}</g>',
         chip(32, 28, "CONTACT", BLUE, WHITE),
         t(30, 112, "Let's build something together.", 36, WHITE, 300, ls=-.6),
         t(32, 144, "Reach out by email, WhatsApp or LinkedIn.", 15, BLUE2, 400)]
    return svg(W, H, "\n".join(b), "Contact: let's build something together.")


def button_icon(kind, x, y, color):
    if kind == "mail":
        return (f'<g fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round">'
                f'<rect x="{x}" y="{y + 3}" width="20" height="14"/>'
                f'<polyline points="{x},{y + 3} {x + 10},{y + 11} {x + 20},{y + 3}"/></g>')
    if kind == "whatsapp":
        return logo("whatsapp", x + 10, y + 10, 20)
    if kind == "linkedin":  # not in Simple Icons; simple "in" mark in LinkedIn blue
        return (rect(x, y, 20, 20, "#0A66C2", rx=3)
                + t(x + 10, y + 15.5, "in", 13, WHITE, 700, anchor="middle", ls=-.3))
    raise KeyError(kind)


def button(key, w, left=0, right=0):
    """Chevron-ended button, w visible px; left/right transparent margins make
    a row of buttons (placed with no whitespace between them) span exactly 840px."""
    label, ic, primary = BUTTONS[key]
    h, p = 56, 22
    fill, stroke, txt = (BLUE, None, WHITE) if primary else (WHITE, BLUE, BLUE)
    x0 = left
    b = [chevron(x0 + .75, .75, w - 1.5, h - 1.5, fill, stroke, p=p - .5, sw=1.5)]
    b.append(button_icon(ic, x0 + p + 12, 18, txt))
    b.append(t(x0 + p + 44, 34, label, 15, txt, 600, ls=.3))
    ax = x0 + w - p - 14
    b.append(f'<g fill="none" stroke="{txt}" stroke-width="2"><line x1="{ax - 18}" y1="28" x2="{ax}" y2="28"/>'
             f'<polyline points="{ax - 7},21 {ax},28 {ax - 7},35"/></g>')
    return svg(left + w + right, h, "\n".join(b), label, pad=0)


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*-dark.svg"):
        old.unlink()
    for old in OUT.glob("*-light.svg"):
        old.unlink()
    files = dict(hero=hero(), about=about(), skills=skills(), tech=tech(), now=now(),
                 contact=contact())
    files["activity-light"] = activity("light")
    files["activity-dark"] = activity("dark")
    # Hero CTAs: two columns of 414 + 12 gutter = 840
    files["btn-getintouch"] = button("getintouch", COL2, right=GAP // 2)
    files["btn-whatsapp-cta"] = button("whatsapp", COL2, left=GAP // 2)
    # Contact row: three columns of 272 + 12 gutters = 840
    files["btn-email"] = button("email", COL3, right=8)
    files["btn-whatsapp"] = button("whatsapp", COL3, left=4, right=4)
    files["btn-linkedin"] = button("linkedin", COL3, left=8)
    for name, data in files.items():
        (OUT / f"{name}.svg").write_text(data, encoding="utf-8")
    print("wrote", len(files), "files to", OUT)


if __name__ == "__main__":
    main()

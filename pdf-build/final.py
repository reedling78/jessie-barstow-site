# -*- coding: utf-8 -*-
import asyncio, json, os, subprocess
import render, spec

# the published PDF this rebuild splices into
SOURCE = os.environ.get("SOURCE_PDF", "../the-traveling-jessie-barstow-chapter-one.pdf")
from PIL import Image
import pypdf

f = json.load(open("fit.json"))
PT2PX = spec.PT2PX

# --- page 2 ------------------------------------------------------------------
f2 = {k: dict(v) for k, v in f["p2"].items()}
LINE_STEP = 20.0                      # colophon leading, measured off the original
f2["credit"] = dict(f2["cr2"]); f2["credit"]["top"] = f2["cr2"]["top"] + LINE_STEP
f2["domain"] = dict(f2["domain"]); f2["domain"]["top"] = f2["cr2"]["top"] + 2 * LINE_STEP

# the p2 ornament is placed from the fitted p9 one, scaled to its target height
o9 = f["p9"]["orn9"]
ratio = (300.4 - 284.9) / (140.1 - 126.8)
off9 = o9["top"] - 126.8 * PT2PX
f2["orn2"] = {"size": o9["size"] * ratio, "ls": 0.0, "top": 284.9 * PT2PX + off9 * ratio}

P2_ITEMS = list(spec.P2)
P2_ITEMS.insert(3, ("orn2", "✦", "DejaVu Sans", 400, "normal", spec.GOLD_P2, (229.9,284.9,238.3,300.4), 0, 0.0))
idx = [i for i, it in enumerate(P2_ITEMS) if it[0] == "cr2"][0]
P2_ITEMS.insert(idx + 1, ("credit", "Art by Maria Botvinik.", "EB Garamond", 400, "normal", spec.INK_SOFT,
                          (0,0,0,0), 0, 0.0))

RULE = ("<div style=\"position:absolute;left:%dpx;top:%dpx;width:%dpx;height:1px;"
        "background:linear-gradient(90deg,rgba(%s,0),rgb(%s),rgba(%s,0))\"></div>")
def rules(y, segs, rgb):
    return "".join(RULE % (x, y, w, rgb, rgb, rgb) for x, w in segs)

p2_extra = rules(391, [(173,124),(328,123)], "169,118,20")

# --- page 9 ------------------------------------------------------------------
f9 = {k: dict(v) for k, v in f["p9"].items()}
# the cover thumbnail is copied out of the source PDF byte-for-byte (no re-encode)
if not os.path.exists("thumb_raw.jpg"):
    for _im in pypdf.PdfReader(SOURCE).pages[8].images:
        if _im.name.startswith("X31"):
            open("thumb_raw.jpg", "wb").write(_im.data)

p9_extra = (
    rules(178, [(197,102),(326,101)], "233,185,73")
    # cover thumbnail, at the exact box the original used
    + "<img src='thumb_raw.jpg' style=\"position:absolute;left:218.9px;top:205.9px;width:186.2px;"
      "height:257.7px;box-shadow:0 16px 38px rgba(0,0,0,.50),0 0 54px rgba(84,201,209,.10)\">"
    # the order button: same pill the original drew (168,671,288x47)
    + "<div style=\"position:absolute;left:168px;top:671px;width:288px;height:47px;border-radius:6px;"
      "background:linear-gradient(90deg,#F2CF80 0%,#D39E31 100%);box-shadow:0 10px 30px rgba(233,185,73,.20)\"></div>"
)

def build(items, fits, bg, extra, out):
    html = render.html_page(items, fits, bg, extra=extra)
    asyncio.run(render.render(html, out))

p2bg = "background:%s" % spec.CREAM
p9bg = ("background:radial-gradient(60%% 28%% at 50%% 6%%, rgba(84,201,209,.13), rgba(84,201,209,0) 70%%),"
        "linear-gradient(180deg,%s 0%%,%s 100%%)" % (spec.NAVY_TOP, spec.NAVY_BOT))

build(P2_ITEMS, f2, p2bg, p2_extra, "new-p2.pdf")
build(spec.P9, f9, p9bg, p9_extra, "new-p9.pdf")

# --- splice ------------------------------------------------------------------
src = pypdf.PdfReader(SOURCE)
n2 = pypdf.PdfReader("new-p2.pdf").pages[0]
n9 = pypdf.PdfReader("new-p9.pdf").pages[0]
w = pypdf.PdfWriter()
for i, page in enumerate(src.pages):
    w.add_page(n2 if i == 1 else n9 if i == 8 else page)
w.add_metadata({
    "/Title": "The Traveling Jessie Barstow — Chapter One (Free Sample)",
    "/Author": "Matt Warnock",
    "/Subject": "Free sample chapter of the middle-grade portal fantasy novel The Traveling Jessie Barstow.",
    "/Keywords": "Matt Warnock, The Traveling Jessie Barstow, portal fantasy, middle grade, sample chapter",
    "/Creator": "jessiebarstowbook.com",
})
with open("rebuilt.pdf", "wb") as fh:
    w.write(fh)
print("wrote rebuilt.pdf")

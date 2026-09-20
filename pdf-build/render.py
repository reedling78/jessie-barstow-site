# -*- coding: utf-8 -*-
import asyncio, json, os, re, subprocess, sys, copy
from playwright.async_api import async_playwright
import spec

FONTDIR = os.path.abspath("../fonts")
FACES = """
@font-face{font-family:'Cinzel';font-weight:400;src:url('file://%(d)s/Cinzel-0.ttf')}
@font-face{font-family:'Cinzel';font-weight:600;src:url('file://%(d)s/Cinzel-1.ttf')}
@font-face{font-family:'Cinzel';font-weight:700;src:url('file://%(d)s/Cinzel-2.ttf')}
@font-face{font-family:'EB Garamond';font-weight:400;font-style:normal;src:url('file://%(d)s/EBGaramond-1.ttf')}
@font-face{font-family:'EB Garamond';font-weight:400;font-style:italic;src:url('file://%(d)s/EBGaramond-0.ttf')}
@font-face{font-family:'EB Garamond';font-weight:600;font-style:normal;src:url('file://%(d)s/EBGaramond-2.ttf')}
@font-face{font-family:'Cormorant Garamond';font-weight:400;font-style:italic;src:url('file://%(d)s/CormorantGaramond-0.ttf')}
""" % {"d": FONTDIR}

def line_div(i, item, fit):
    name, text = item[0], item[1]
    fam, weight, style, color = item[2], item[3], item[4], item[5]
    size, ls, top = fit[name]["size"], fit[name]["ls"], fit[name]["top"]
    return ("<div class='ln' style=\"top:%.3fpx;font-family:'%s';font-weight:%d;"
            "font-style:%s;color:%s;font-size:%.3fpx;letter-spacing:%.4fem\">%s</div>"
            % (top, fam, weight, style, color, size, ls, text))

def html_page(items, fit, bg_css, extra="", use_was=False):
    body = []
    for i, it in enumerate(items):
        it = list(it)
        if use_was and len(it) > 9 and it[9]:
            it[1] = it[9]
        body.append(line_div(i, it, fit))
    return """<!doctype html><html><head><meta charset="utf-8"><style>
%s
@page{size:6.5in 9in;margin:0}
html,body{margin:0;padding:0}
body{position:absolute;left:0;top:0;width:%dpx;height:863px;overflow:hidden}
.bg{position:absolute;left:0;top:0;width:624px;height:863px;%s}
.ln{position:absolute;left:0;width:%dpx;text-align:center;white-space:nowrap;line-height:1;z-index:2}
</style></head><body><div class="bg"></div>%s%s</body></html>""" % (
        FACES, spec.PAGE_W, bg_css, spec.PAGE_W, extra, "".join(body))

async def render(html, out):
    open(out + ".html", "w").write(html)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto("file://" + os.path.abspath(out + ".html"))
        await pg.wait_for_timeout(350)
        await pg.pdf(path=out, width="6.5in", height="9in", margin={"top":"0","bottom":"0","left":"0","right":"0"}, print_background=True)
        await b.close()

def measure(pdf):
    xml = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
    raw = []
    for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">', xml):
        raw.append(tuple(float(g) for g in m.groups()))
    # poppler splits a widely letter-spaced line into several <line> elements;
    # merge everything that shares a baseline back into one box.
    merged = {}
    order = []
    for x0, y0, x1, y1 in raw:
        k = (round(y0, 1), round(y1, 1))
        if k not in merged:
            merged[k] = [x0, y0, x1, y1]; order.append(k)
        else:
            b = merged[k]
            b[0] = min(b[0], x0); b[2] = max(b[2], x1)
    return [tuple(merged[k]) for k in order]

def fit(items, bg, tag, rounds=9):
    f = {it[0]: {"size": it[7], "ls": it[8], "top": it[6][1] * spec.PT2PX} for it in items}
    for r in range(rounds):
        asyncio.run(render(html_page(items, f, bg, use_was=True), "fit-%s.pdf" % tag))
        got = measure("fit-%s.pdf" % tag)
        if len(got) != len(items):
            print("  !! line count %d vs %d" % (len(got), len(items)))
            for g in got: print("    ", [round(x,1) for x in g])
            return f, False
        worst = 0.0
        for it, g in zip(items, got):
            tx0, ty0, tx1, ty1 = it[6]
            gx0, gy0, gx1, gy1 = g
            th, gh = ty1 - ty0, gy1 - gy0
            tw, gw = tx1 - tx0, gx1 - gx0
            name = it[0]
            f[name]["size"] *= th / gh
            txt = it[9] if (len(it) > 9 and it[9]) else it[1]
            n = max(1, len(re.sub("<[^>]+>", "", txt)) - 1)
            f[name]["ls"] += ((tw - gw) * spec.PT2PX / n) / f[name]["size"]
            f[name]["top"] += (ty0 - gy0) * spec.PT2PX
            worst = max(worst, abs(th-gh), abs(tw-gw), abs(ty0-gy0))
        print("  round %d worst delta %.2fpt" % (r+1, worst))
        if worst < 0.35: break
    return f, True

if __name__ == "__main__":
    p2bg = "background:%s" % spec.CREAM
    p9bg = ("background:radial-gradient(60%% 28%% at 50%% 6%%, rgba(84,201,209,.13), rgba(84,201,209,0) 70%%),"
            "linear-gradient(180deg,%s 0%%,%s 100%%)" % (spec.NAVY_TOP, spec.NAVY_BOT))
    f2, ok2 = fit(spec.P2, p2bg, "p2")
    print("P2 fitted", ok2)
    f9, ok9 = fit(spec.P9, p9bg, "p9")
    print("P9 fitted", ok9)
    json.dump({"p2": f2, "p9": f9}, open("fit.json", "w"), indent=1)

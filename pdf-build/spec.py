# -*- coding: utf-8 -*-
# Page geometry: CSS px at 96dpi. 624 x 864 px = 6.5in x 9in = 468 x 648pt.
PAGE_W, PAGE_H = 624, 864
PT2PX = 4.0/3.0

CREAM   = "#FAF5EA"
INK     = "#241F19"
INK_SOFT= "#5B5145"
GOLD_P2 = "#A97614"

NAVY_TOP= "#14344E"
NAVY_BOT= "#0B1825"
GOLD    = "#E9B949"
GOLD_SOFT="#F4D58D"
PAPER_LT= "#DBE6EC"
MUTED   = "#9FB3BF"
DIM     = "#6F8794"
TEAL    = "#54C9D1"
PILL_INK= "#221607"

# id: (text, font stack, weight, style, color, target bbox in POINTS from the
# original file: (x0, y0, x1, y1), initial font-size px, initial letter-spacing em)
P2 = [
 ("kicker", "A PORTAL-FANTASY ADVENTURE", "Cinzel", 400, "normal", GOLD_P2,
    (127.8,177.7,337.0,189.2), 9.0, 0.22),
 ("t1", "The Traveling", "Cinzel", 400, "normal", GOLD_P2,
    (161.4,211.9,304.1,232.1), 24.0, 0.04),
 ("t2", "Jessie Barstow", "Cinzel", 700, "normal", INK,
    (134.0,235.1,333.7,268.8), 34.0, 0.0),
 ("quote1", "“One special girl. One power-hungry queen.", "Cormorant Garamond", 400, "italic", INK_SOFT,
    (119.6,318.9,348.2,336.4), 17.0, 0.0),
 ("quote2", "One chance to save all of magic.”", "Cormorant Garamond", 400, "italic", INK_SOFT,
    (147.7,340.6,320.5,358.2), 17.0, 0.0),
 ("byline1", "a novel by", "EB Garamond", 400, "normal", INK_SOFT,
    (209.9,390.9,257.9,405.3), 13.0, 0.0),
 ("byline2", "Matt Warnock", "Cinzel", 600, "normal", INK,
    (169.3,411.6,297.4,430.5), 17.0, 0.06),
 ("sample", "FREE SAMPLE · CHAPTER ONE", "Cinzel", 600, "normal", GOLD_P2,
    (153.9,536.7,312.5,547.5), 8.5, 0.2),
 ("cr1", "Copyright © 2026 Matt Warnock. All rights reserved.", "EB Garamond", 400, "normal", INK_SOFT,
    (146.6,560.7,321.1,571.8), 10.0, 0.0),
 ("cr2", "This excerpt may be shared freely; it may not be sold or altered.", "EB Garamond", 400, "normal", INK_SOFT,
    (130.5,575.7,337.2,586.8), 10.0, 0.0),
 ("domain", "jessiebarstowbook.com", "EB Garamond", 400, "normal", GOLD_P2,
    (197.2,590.7,270.7,601.8), 10.0, 0.0),
]

# Page 9. Lines whose TEXT CHANGES carry their original text in `was` so the
# fitter can size them against the original bbox, then swap in the new words.
P9 = [
 ("eyebrow", "END OF CHAPTER ONE", "Cinzel", 400, "normal", TEAL,
    (163.4,46.9,302.0,57.7), 8.5, 0.22, None),
 ("h1a", "Keep Traveling", "Cinzel", 700, "normal", GOLD,
    (151.9,66.7,316.5,93.7), 24.0, 0.02, None),
 ("h1b", "with Jessie", "Cinzel", 700, "normal", GOLD,
    (177.0,90.7,291.0,117.7), 24.0, 0.02, None),
 ("orn9", "\u2726", "DejaVu Sans", 400, "normal", GOLD,
    (230.6,126.8,237.7,140.1), 12.0, 0.0, None),
 ("pq1", "The door is open. Demora is already hunting.", "Cormorant Garamond", 400, "italic", GOLD_SOFT,
    (129.4,366.3,338.3,382.6), 16.0, 0.0, None),
 ("pq2", "Jessie’s next step lands her a world away.", "Cormorant Garamond", 400, "italic", GOLD_SOFT,
    (139.1,387.3,328.5,403.6), 16.0, 0.0, None),
 ("b1", "Twenty-five chapters of strange and wondrous worlds, a magician", "EB Garamond", 400, "normal", PAPER_LT,
    (95.2,417.2,372.6,431.5), 13.0, 0.0, None),
 ("b2", "who stopped believing, and a sorceress who will burn down every", "EB Garamond", 400, "normal", PAPER_LT,
    (95.2,434.4,373.1,448.8), 13.0, 0.0, None),
 ("b3", "door to reach the Source of All Magic. <i>The Traveling Jessie Barstow</i> is", "EB Garamond", 400, "normal", PAPER_LT,
    (90.0,451.7,377.8,466.0), 13.0, 0.0, None),
 ("b4", "available now.", "EB Garamond", 400, "normal", PAPER_LT,
    (178.9,468.9,289.4,483.3), 13.0, 0.0, "available to preorder now."),
 ("pill", "ORDER THE BOOK", "Cinzel", 600, "normal", PILL_INK,
    (154.5,513.0,311.7,528.5), 11.0, 0.18, "PREORDER THE BOOK"),
 ("b2r", "books2read.com/u/b6noEW", "EB Garamond", 400, "normal", MUTED,
    (178.9,548.4,288.6,560.8), 11.0, 0.0, None),
 ("more", "Read more, meet the characters, and get launch news at", "EB Garamond", 400, "normal", MUTED,
    (132.0,578.4,336.0,590.8), 11.0, 0.0, None),
 ("domain9", "jessiebarstowbook.com", "EB Garamond", 400, "normal", GOLD,
    (192.7,594.2,275.1,606.6), 11.0, 0.0, "jessiebarstow.web.app"),
 ("footer", "THE TRAVELING JESSIE BARSTOW · MATT WARNOCK", "Cinzel", 400, "normal", DIM,
    (99.7,621.2,366.2,631.3), 7.5, 0.2, None),
]

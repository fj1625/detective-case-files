# -*- coding: utf-8 -*-
"""
Generate the answer key Word doc for the detective case files.

Each case lists the correct answer for every interactive page, so the web
pages can be verified quickly. To add a new case (or page), append to CASES
below and re-run:  python answer_key_generator.py

Output: 答案验证表 Answer Key.docx
"""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = "答案验证表 Answer Key.docx"

# ---------------------------------------------------------------------------
# Answer data — one dict per case. Add a new case dict to extend.
# timeline: the 5 events already in correct chronological order (1->5).
# suspects: suspect name -> list of its clue texts (the folder it belongs in).
# evidence: real = tiles to DROP on the board; distractor = tile to REJECT.
# culprit: the suspect to drag into the accusation zone.
# ---------------------------------------------------------------------------
CASES = [
    {
        "num": "01",
        "title": "The Lost Picture",
        "title_cn": "丢失的照片",
        "cover": {
            "Client": "Annie",
            "Missing": "A picture of Fang",
            "Location": "Down the street",
        },
        "timeline": [
            "Annie called Felix. Her Fang picture was gone.",
            "Felix checked the yellow room. No picture.",
            "Fang buried bones but stayed in the yard.",
            "Felix found Rosamond's lost cat.",
            "Harry's orange monster hid the picture.",
        ],
        "suspects": {
            "Annie": ["lost a yellow picture of her dog", "has a yellow room"],
            "Fang": ["big dog with big teeth", "never leaves the yard without a leash"],
            "Rosamond": ["has four cats named Hex", "only likes cats"],
            "Harry": ["paints everything red", "painted an orange monster with three heads"],
        },
        "evidence_real": ["🎨 Wet Yellow Paint", "🖌️ Red Paintbrush", "👹 Monster Drawing"],
        "evidence_distractor": "🥞 Pancakes",
        "deduction": "Wet yellow paint + red paint = orange monster; the monster had dog ears and a tail = Fang.",
        "culprit": "Harry",
    },
    {
        "num": "02",
        "title": "The Garbage Snatcher",
        "title_cn": "翻垃圾的家伙",
        "cover": {
            "Client": "Oliver",
            "Missing": "Garbage, snatched every night",
            "Location": "Oliver's garbage can",
        },
        "timeline": [
            "Oliver said a snatcher tipped his can each night.",
            "Felix asked Rosamond. She hates garbage.",
            "Esmeralda said no one would go near Oliver.",
            "Felix hid in the garbage can at night.",
            "Sludge knocked off the cover. Sludge did it!",
        ],
        "suspects": {
            "Rosamond": ["would eat 2000 things before garbage", "her cats eat cat food, not garbage"],
            "Esmeralda": ["keeps her mouth open to say wise things", "would never go near Oliver the pest"],
            "Skunk": ["found near garbage in a field", "sprayed Felix with a big stink"],
            "Sludge": ["sniffed the garbage can a lot", "was tired of pancakes and hungry"],
        },
        "evidence_real": ["🚷 No Person", "🌙 Night Animal", "👃 Sludge Sniffs"],
        "evidence_distractor": "🦨 Smelly Skunk (ruled-out lead)",
        "deduction": "No person would go near Oliver, so a night animal did it; Sludge sniffed and knocked the cover off = Sludge.",
        "culprit": "Sludge",
    },
    {
        "num": "03",
        "title": "The Lost List",
        "title_cn": "丢失的清单",
        "cover": {
            "Client": "Claude",
            "Missing": "A grocery list",
            "Location": "Between Claude's house and the store",
        },
        "timeline": [
            "Claude lost his grocery list before lunch.",
            "Felix drew a map and walked every street.",
            "The wind blew the map toward Rosamond's house.",
            "Felix made pancakes — the list was all baking stuff.",
            "Rosamond's \"cat pancake recipe\" was the lost list!",
        ],
        "suspects": {
            "Claude": ["always loses things — even his way", "his dad wrote the grocery list"],
            "Fang": ["held a paper tight in his teeth", "barked back, then dropped the paper"],
            "Sludge": ["sniffed up and down every street", "barked funny to help Felix"],
            "Rosamond": ["was all covered in white flour", "found a new cat pancake recipe today"],
        },
        "evidence_real": ["🥞 Pancake Stuff", "🐟 Tuna Fish", "🌬️ The Wind"],
        "evidence_distractor": "🗺️ Fang's Paper (just Felix's map)",
        "deduction": "The list was all pancake stuff + tuna fish (cats love tuna) = looks like a cat pancake recipe; the wind blew it to Rosamond, who kept it.",
        "culprit": "Rosamond",
    },
]

BROWN = RGBColor(0x4A, 0x35, 0x28)
RED = RGBColor(0xB8, 0x3A, 0x2A)


def add_heading(doc, text, size, color=BROWN, bold=True, after=6, before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p


def add_label_line(doc, label, value, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    if indent:
        p.paragraph_format.left_indent = Pt(indent)
    r = p.add_run(label + "  ")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RED
    r2 = p.add_run(value)
    r2.font.size = Pt(11)
    return p


def build():
    doc = Document()

    add_heading(doc, "侦探案件答案验证表", 22)
    add_heading(doc, "Detective Case Files — Answer Key", 14, color=BROWN, bold=False, after=4)
    intro = doc.add_paragraph()
    intro.add_run(
        "每个案件按 5 个页面列出正确答案，方便逐页验证网页功能。"
        "（每新建一个案件/页面，本表会同步增加。）"
    ).italic = True
    intro.runs[0].font.size = Pt(10)
    doc.add_paragraph()

    for c in CASES:
        add_heading(doc, f"Case {c['num']} — {c['title']}  {c['title_cn']}", 17, before=8)

        # Page 0 — Cover (context, not a puzzle)
        add_heading(doc, "Page 0 · Cover（封面信息）", 12, color=BROWN)
        for k, v in c["cover"].items():
            add_label_line(doc, f"{k}:", v, indent=12)

        # Page 1 — Timeline
        add_heading(doc, "Page 1 · Timeline 时间线（正确顺序 1→5）", 12, color=BROWN)
        for i, ev in enumerate(c["timeline"], 1):
            p = doc.add_paragraph(style="List Number")
            p.paragraph_format.left_indent = Pt(20)
            p.add_run(ev).font.size = Pt(11)

        # Page 2 — Suspect Files
        add_heading(doc, "Page 2 · Suspect Files 嫌疑人文件（线索 → 文件夹）", 12, color=BROWN)
        for name, clues in c["suspects"].items():
            tag = "  ← 真凶 CULPRIT" if name == c["culprit"] else ""
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(12)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(name + tag)
            r.bold = True
            r.font.size = Pt(11)
            if name == c["culprit"]:
                r.font.color.rgb = RED
            for clue in clues:
                pc = doc.add_paragraph(style="List Bullet")
                pc.paragraph_format.left_indent = Pt(30)
                pc.paragraph_format.space_after = Pt(0)
                pc.add_run(clue).font.size = Pt(10.5)

        # Page 3 — Evidence Board
        add_heading(doc, "Page 3 · Evidence Board 证据板", 12, color=BROWN)
        add_label_line(doc, "拖上板 (real):", "  ·  ".join(c["evidence_real"]), indent=12)
        add_label_line(doc, "拒绝/弹回 (distractor):", c["evidence_distractor"], indent=12)
        add_label_line(doc, "推理 (deduction):", c["deduction"], indent=12)

        # Page 4 — Solve
        add_heading(doc, "Page 4 · Solve the Case 指认真凶", 12, color=BROWN)
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Pt(12)
        r = p.add_run("Culprit:  " + c["culprit"])
        r.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = RED

        doc.add_paragraph()

    doc.save(OUT)
    print("wrote", OUT, "with", len(CASES), "cases")


if __name__ == "__main__":
    build()

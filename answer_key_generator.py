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
    {
        "num": "04",
        "title": "The Phony Clue",
        "title_cn": "假线索",
        "cover": {
            "Client": "Felix himself",
            "Missing": "Who sent the torn invitation?",
            "Location": "Felix's doorstep & around the block",
        },
        "timeline": [
            "A torn scrap saying \"VITA\" was on Felix's doorstep.",
            "A pancake lured Big Hex down; Felix grabbed a tree piece.",
            "The pieces joined to read: INVITATION — COME AT THREE.",
            "Finley dropped a \"phony clue\" into the sewer.",
            "Wet ink matched — Finley wrote it! Felix went at three.",
        ],
        "suspects": {
            "Rosamond": ["owns four cats with sixteen sharp claws", "said Big Hex sat in his tree all morning"],
            "Annie": ["was out walking her dog Fang", "always said Felix is a great detective"],
            "Pip": ["hardly ever says a single word", "bet that Felix WOULD solve it by three"],
            "Finley": ["said, \"Maybe he's great, maybe he's not.\"", "dropped a paper into the sewer and walked away"],
        },
        "evidence_real": ["📄 \"VITA\" Scrap", "💧 Wet Paper", "🅴 The Funny \"E\""],
        "evidence_distractor": "🐱 Big Hex the cat (ruled-out lead — tears paper, can't write)",
        "deduction": "\"VITA\" is part of INVITATION; wet thin paper lets the ink show through; the funny \"E\" matches Finley's writing = Finley wrote it.",
        "culprit": "Finley",
    },
    {
        "num": "05",
        "title": "The Sticky Case",
        "title_cn": "黏糊糊的案子",
        "cover": {
            "Client": "Claude",
            "Missing": "A tiny stegosaurus stamp",
            "Location": "Claude's table → Rosamond's yard sale",
        },
        "timeline": [
            "Claude's tiny stegosaurus stamp vanished from his table.",
            "After the rain, Pip came over and stepped in puddles.",
            "The wet shoe pressed the stamp's sticky side — it stuck!",
            "Pip swapped his wet shoes at Rosamond's Swap Table.",
            "Annie bought the shoe — Fang was chewing the stamp!",
        ],
        "suspects": {
            "Annie": ["bought the wet shoes for Fang to chew", "said the stamp looks like Fang's smile"],
            "Pip": ["came over after the rain had stopped", "swapped his wet shoes for dry slippers"],
            "Rosamond": ["was holding a yard sale with a Swap Table", "sold Pip's shoes to Annie for ten cents"],
            "Fang": ["was chewing a shoe in Annie's yard", "the lost stamp was stuck to the shoe's sole"],
        },
        "evidence_real": ["💧 Rain & Puddles", "👟 Pip's Wet Shoe", "🦕 Sticky Stamp"],
        "evidence_distractor": "🥫 Empty Tuna Can (silly yard-sale prop)",
        "deduction": "Rain → puddles → Pip's wet shoe pressed the stamp's sticky side, so it stuck to his shoe and rode off (then swapped, sold, and chewed by Fang). Culprit = Pip, by accident.",
        "culprit": "Pip",
    },
    {
        "num": "06",
        "title": "The Missing Key",
        "title_cn": "丢失的钥匙",
        "cover": {
            "Client": "Annie",
            "Missing": "Her shiny silver house key",
            "Location": "Annie's house — Fang's birthday party",
        },
        "timeline": [
            "Annie left her key on a table and went to buy Fang's surprise.",
            "Rosamond and her four cats were left alone in the house.",
            "Annie returned — house locked, Rosamond gone, key missing.",
            "Felix hunted shiny places: Oliver's, a bank, a garbage can.",
            "The key hid among shiny silver — on Fang's collar!",
        ],
        "suspects": {
            "Rosamond": ["was left alone in Annie's house", "left a strange riddle poem on the door"],
            "Oliver": ["collects one new shiny thing each week", "this week it was shiny eels, not keys"],
            "Fang": ["wore a new collar full of shiny silver", "stayed safe in the yard all day"],
            "Sludge": ["sniffed every garbage can", "helped Felix pry off the can's cover"],
        },
        "evidence_real": ["🔑 Silver Key", "✨ Other Shiny Silver", "🐕 Fang's Round Collar"],
        "evidence_distractor": "🏦 The Bank (ruled-out lead — round & shiny, but too normal for Rosamond)",
        "deduction": "A shiny silver key is easy to hide among OTHER shiny silver things; Fang's collar is round, big, and safe with silver tags, so Rosamond hung the key there — inches from Fang's teeth.",
        "culprit": "Rosamond",
    },
    {
        "num": "07",
        "title": "The Snowy Trail",
        "title_cn": "雪地足迹",
        "cover": {
            "Client": "Rosamond",
            "Missing": "Felix's birthday present (she won't say what!)",
            "Location": "The snowy trail to Felix's house",
        },
        "timeline": [
            "Rosamond pulled Felix's present and 4 cats on her sled.",
            "Under a tree, the sled felt lighter — the present was gone.",
            "The snow had no package and no marks — how strange!",
            "Clues added up: heavy, ugly, and it drinks milk.",
            "Felix looked UP — the present had leaped into the tree!",
        ],
        "suspects": {
            "Rosamond": ["wouldn't say what the present was", "bought six milk cartons for only four cats"],
            "Annie": ["said the gift was \"the most beautiful ever\"", "her dog Fang scared Sludge into a big leap"],
            "Claude": ["saw Rosamond buy an ugly birthday card", "was sitting inside a snow castle"],
            "Sludge": ["leaped super high over a snow pile", "his big leap gave Felix the idea"],
        },
        "evidence_real": ["🪶 Lighter Sled (heavy)", "🥛 Two Extra Milks", "🐾 Sludge's Leap"],
        "evidence_distractor": "⛄ Snow Dog (silly prop — just a decoration Felix built)",
        "deduction": "Sled felt lighter = present is heavy; 6 milks but only 4 cats = something big drinks milk; Sludge's leap = it can leap. Heavy + milk-drinker + leaper = a giant monster cat that jumped off the sled into the tree (so no marks in the snow).",
        "culprit": "Monster Cat (the lost present — Page 4 asks 'what was the present?', not a person)",
    },
    {
        "num": "08",
        "title": "The Fishy Prize",
        "title_cn": "腥味奖品",
        "cover": {
            "Client": "Rosamond",
            "Missing": "The SMARTEST prize — a gold-painted tuna can",
            "Location": "Rosamond's windowsill — vanished mid-stampede",
        },
        "timeline": [
            "Rosamond set her gold \"SMARTEST\" tuna can on the windowsill to dry.",
            "The pets had a wild stampede and messed up the room.",
            "Fang's tail hit the can and knocked it out the open window.",
            "The can dropped into Felix's open bag as he biked past.",
            "At home, Sludge sniffed the grocery bag — the prize was inside!",
        ],
        "suspects": {
            "Fang": ["stood with his right side to the open window", "had gold paint on the right side of his tail"],
            "Anastasia": ["gobbled a big pile of food very fast", "had NO gold paint inside her mouth"],
            "Cats": ["licked the tuna can clean — they love fish", "ran wild and helped wreck the room"],
            "Felix": ["rode past on his new bike during the noise", "left an open grocery bag in his bike basket"],
        },
        "evidence_real": ["🎨 Gold on Fang's Tail", "🚲 Open Grocery Bag", "👃 Sludge's Fishy Sniff"],
        "evidence_distractor": "🐷 Pig Ate It? (ruled-out lead — Anastasia had no gold paint in her mouth)",
        "deduction": "Gold paint on the RIGHT side of Fang's tail means his tail knocked the can OUTWARD, out the window — just as Felix biked past with an open grocery bag in his basket. The can dropped in, and Felix carried the prize home without knowing it (Sludge smelled the fishy can and sniffed it out first).",
        "culprit": "Felix (the detective himself — he carried it home by accident; Page 4 asks 'who took it home without knowing?')",
    },
    {
        "num": "09",
        "title": "The Vanishing Weed",
        "title_cn": "消失的杂草",
        "cover": {
            "Client": "Oliver",
            "Missing": "His adopted weed — small, sick, with a yellow bud",
            "Location": "Oliver's screened-in back porch",
        },
        "timeline": [
            "Oliver bought a sick little weed at Rosamond's Adopt-A-Weed sale.",
            "He potted it and set it in the sun on his porch railing.",
            "Oliver turned away to fetch water — his certificate swung at the pot.",
            "The weed plopped into the open book; the breeze blew it shut.",
            "Felix found the weed pressed flat inside the book at the library.",
        ],
        "suspects": {
            "Oliver": ["bought the sick weed for a nickel", "turned to get water, certificate poking from his pocket"],
            "Rosamond": ["runs an Adopt-A-Weed sale with a song for weeds", "keeps a list of all her weeds in a book"],
            "Fang": ["will eat almost anything", "grabbed a weed and ran off with it in his teeth"],
            "Claude": ["was hunting a lost worm down in the soil", "said it was \"right under our noses\" but unseen"],
        },
        "evidence_real": ["📜 The Certificate", "📖 Open Weed Book", "🌬️ The Breeze"],
        "evidence_distractor": "🐶 Fang Ate It? (ruled-out lead — Fang ran off with a different weed, not this one)",
        "deduction": "Oliver's Certificate of Ownership poked from his back pocket. Turning away to get water, it swung and knocked the sick weed out of its dry pot; the weed plopped into the open weed book right beside it; the breeze then blew the book shut — so the weed was pressed flat inside, right under their noses (just like Claude's hidden worm).",
        "culprit": "The Weed Book (where the weed ended up — Page 4 asks 'where did the weed go?', not a person; Oliver's certificate knocked it in by accident)",
    },
    {
        "num": "10",
        "title": "The Boring Beach Bag",
        "title_cn": "无聊的沙滩包",
        "cover": {
            "Client": "Oliver",
            "Missing": "His boring blue beach bag — clothes, shoes & a seashell inside",
            "Location": "The beach — beside his beach ball",
        },
        "timeline": [
            "Oliver left his boring beach bag and ball on the sand.",
            "He ran to Rosamond's Restaurant for a glass of water.",
            "A kicked beach ball drifted far down the beach.",
            "Oliver followed Esmeralda, spotted a ball, and cried \"stolen!\"",
            "Felix found the bag untouched, where Oliver first left it.",
        ],
        "suspects": {
            "Rosamond": ["sells sandy water and sand sandwiches at her stand", "was too busy with her restaurant to see anything"],
            "Annie": ["ran past with Fang from one end of the beach to the other", "said Fang's on a diet — a bag is not on it"],
            "Esmeralda": ["was hiding from Oliver out in the water", "swam away the moment Oliver showed up"],
            "Oliver": ["left his bag beside his beach ball, then went for water", "follows everyone everywhere — even into the sea"],
        },
        "evidence_real": ["🏖️ Unpressed Sand", "🏐 The Moving Ball", "👣 Following Esmeralda"],
        "evidence_distractor": "🐶 Fang Ate It? (ruled-out lead — Annie says a bag is not on Fang's diet)",
        "deduction": "The sand had no dent where the heavy bag supposedly sat, so the bag never moved from there. What actually moved was the beach BALL — someone kicked it far down the beach. Oliver, busy following Esmeralda away from his spot, saw his ball in its new place and assumed he was back at the start, so he thought the bag was stolen. It had sat untouched the whole time.",
        "culprit": "Oliver — he got mixed up (no one took the bag; the ball moved, and Oliver confused the spot while following Esmeralda). Page 4 asks 'who really lost it?'",
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

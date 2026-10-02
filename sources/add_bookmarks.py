"""Add a clickable bookmark outline (Chapters > Sections > Concepts) to the exported PDF.
Word's own 'create bookmarks' export option hangs on this document, so bookmarks are added here.
Usage: python sources/add_bookmarks.py <in.pdf> <out.pdf>"""
import sys, re, pymupdf

src, dst = sys.argv[1], sys.argv[2]
doc = pymupdf.open(src)
# Heading styles in build_audit_book.js: H1 26pt, H2 18pt, H3 15pt, H4 13pt — all Ink Free bold
LEVELS = [(25.0, 1), (17.5, 2), (14.5, 3)]
toc, contents_seen = [], False
for pno, page in enumerate(doc):
    lines = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            spans = [s for s in l['spans'] if s['text'].strip()]
            if not spans: continue
            s0 = max(spans, key=lambda s: s['size'])
            if not s0['font'].startswith('InkFree'): continue
            lvl = next((lv for thr, lv in LEVELS if s0['size'] >= thr), None)
            if lvl is None: continue
            text = ' '.join(s['text'] for s in spans).strip()
            lines.append((lvl, text, l['bbox'][1]))
    # merge wrapped heading lines of same level that follow each other closely
    merged = []
    for lvl, text, y in lines:
        if merged and merged[-1][0] == lvl and 0 < y - merged[-1][2] < 40 and not re.match(r'^(\d+[.A-Z]|\(|Chapter \d)', text):
            merged[-1] = (lvl, merged[-1][1] + ' ' + text, y)
        else:
            merged.append((lvl, text, y))
    for lvl, text, _ in merged:
        text = re.sub(r'\s+', ' ', text)
        if text in ('Contents',): contents_seen = True
        if lvl == 1 and text.startswith('FM & SM'): continue  # cover title
        toc.append([lvl, text[:120], pno + 1])

# a level can't jump by more than 1 (PDF outline rule)
fixed, last = [], 0
for lvl, t, p in toc:
    lvl = min(lvl, last + 1) if last else 1
    fixed.append([lvl, t, p]); last = lvl
doc.set_toc(fixed)
doc.save(dst, garbage=3, deflate=True)
print(f'bookmarks: {len(fixed)} (L1 {sum(1 for x in fixed if x[0]==1)}, L2 {sum(1 for x in fixed if x[0]==2)}, L3 {sum(1 for x in fixed if x[0]==3)}) -> {dst}')


"""Make index lines clickable and add 'Chapter Index' bookmarks.
Usage: python sources/link_index.py build/new.pdf build/final.pdf"""
import sys, re, io, pymupdf
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
src, dst = sys.argv[1], sys.argv[2]
doc = pymupdf.open(src)
toc = doc.get_toc()
index_pages = []          # (first, last) page ranges, 1-based
new_toc = []
for k, (lvl, title, page) in enumerate(toc):
    nxt = toc[k + 1][2] if k + 1 < len(toc) else page
    if lvl == 2 and title.strip() == 'Index':
        index_pages.append((page, nxt - 1 if nxt > page else page))
    new_toc.append([lvl, title, page])
    if lvl == 1 and re.match(r'(FM |SM )?Chapter ', title) and nxt > page + 1:
        index_pages.append((page + 1, nxt - 1))
        new_toc.append([2, 'Chapter Index', page + 1])
links = 0
num_re = re.compile(r'(\d{1,4})\s*$')
for a, b in index_pages:
    for pno in range(a, b + 1):
        pg = doc[pno - 1]
        for blk in pg.get_text('dict')['blocks']:
            for ln in blk.get('lines', []):
                txt = ''.join(sp['text'] for sp in ln['spans']).strip()
                m = num_re.search(txt)
                if not m or not re.search(r'\.{3,}|…', txt) and len(ln['spans']) < 2: continue
                target = int(m.group(1))
                if 1 <= target <= len(doc) and target != pno:
                    r = pymupdf.Rect(pg.rect.x0 + 40, ln['bbox'][1], pg.rect.x1 - 40, ln['bbox'][3])
                    pg.insert_link({'kind': pymupdf.LINK_GOTO, 'from': r, 'page': target - 1})
                    links += 1
doc.set_toc(new_toc)
doc.save(dst, garbage=3, deflate=True)
print(f'index page ranges: {len(index_pages)} · links: {links} -> {dst}')


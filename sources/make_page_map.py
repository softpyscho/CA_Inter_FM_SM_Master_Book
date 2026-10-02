"""Read the bookmarked PDF outline and write book/page_map.json for the index pages.
Usage: python sources/make_page_map.py build/new.pdf [book/page_map.json]"""
import sys, re, json, pymupdf
src = sys.argv[1]; dst = sys.argv[2] if len(sys.argv) > 2 else 'book/page_map.json'
toc = pymupdf.open(src).get_toc()
norm = lambda t: re.sub(r'[^a-z0-9]', '', t.lower())[:30]
out = [{'level': l, 'text': t, 'norm': norm(t), 'page': p} for l, t, p in toc]
json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(f'page map: {len(out)} headings -> {dst}')

"""Print text of a document between a start regex and an end regex (first match after start).
Usage: python sources/grab.py <path.txt> "<start regex>" "<end regex>" [maxchars]"""
import re, sys

path, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
limit = int(sys.argv[4]) if len(sys.argv) > 4 else 6000
t = open(path, encoding='utf-8').read()
t = re.sub(r'(?im)^\s*(Download(ed)? from castudyweb\.com|CA Study Shop.*|©.*Institute of Chartered Accountants of India)\s*$', '', t)
m = re.search(start, t, re.S)
if not m:
    print('START NOT FOUND'); sys.exit()
e = re.search(end, t[m.end():], re.S)
seg = t[m.start(): m.end() + (e.start() if e else limit)]
seg = re.sub(r'\n\s*\n+', '\n', seg)
print(seg[:limit])

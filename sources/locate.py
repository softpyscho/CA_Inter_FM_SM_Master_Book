"""Report which question part a piece of text sits in.

Usage: python sources/locate.py "<regex>" [file-glob ...]
Default globs: suggested answers, RTPs, MTP question papers.

For every match it walks backwards to the nearest "Question N" (or "N." heading)
and the nearest "(a)/(b)/(c)" marker, and prints  <paper>  Q<n>(<letter>)  <snippet>.
Use it to pin the exact ICAI question id before writing an atom.
"""
import re, sys, glob, os

pat = re.compile(sys.argv[1], re.I)
globs = sys.argv[2:] or ['sources/sa/*.txt', 'sources/rtp/*.txt', 'sources/mtp/*_Q.txt']
QH = re.compile(r'(?im)^\s*(?:Question\s*(?:No\.?\s*)?(\d{1,2})\b|(\d{1,2})\.\s*$)')
SUB = re.compile(r'(?m)^\s*\(([a-e])\)\s')
SM_START = re.compile(r'(?i)SECTION\s*[-–—]?\s*B\s*:?\s*STRATEGIC|PAPER\s*[-–—]?\s*6B\s*:?\s*STRATEGIC')

files = []
for g in globs:
    files += glob.glob(g)
for f in sorted(set(files)):
    t = open(f, encoding='utf-8').read()
    m0 = SM_START.search(t)
    fm_end = m0.start() if m0 else len(t)
    name = os.path.basename(f)[:-4]
    seen = set()
    for m in pat.finditer(t):
        side = 'FM' if m.start() < fm_end else 'SM'
        qs = [x for x in QH.finditer(t, 0, m.start())]
        ss = [x for x in SUB.finditer(t, 0, m.start())]
        q = (qs[-1].group(1) or qs[-1].group(2)) if qs else '?'
        s = ss[-1].group(1) if ss and (not qs or ss[-1].start() > qs[-1].start()) else ''
        key = (side, q, s)
        if key in seen:
            continue
        seen.add(key)
        snip = re.sub(r'\s+', ' ', t[m.start():m.start() + 110])
        print(f'{name:<16} {side} Q{q}{f"({s})" if s else "":<4}  {snip}')

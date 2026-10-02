"""Dump SM Part I (case MCQs + standalone MCQs) of every MTP question paper, with the answer key from the answer file.
Output: sources/packs/mtp_sm_mcq.txt"""
import re, glob, os

NOISE = re.compile(r'(?im)^\s*(Download(ed)? from castudyweb\.com|CA Study Shop.*|©.*India|\d{1,3}|<<PAGE \d+>>)\s*$')


def clean(t):
    t = NOISE.sub('', t)
    return re.sub(r'\n\s*\n+', '\n', t)


out = []
for q in sorted(glob.glob('sources/mtp/MTP-*_Q.txt')):
    name = os.path.basename(q)[:-6]
    tq = clean(open(q, encoding='utf-8').read())
    sm = re.search(r'(?i)PAPER\s*6B', tq)
    part = tq[sm.start():] if sm else ''
    p2 = re.search(r'(?i)PART\s*[–-]?\s*II\s*[–-]\s*Descriptive', part)
    out.append(f'\n#################### {name} SM PART I')
    s1 = re.search(r'(?i)PART\s*[–-]?\s*I\s*[–-]', part)
    out.append(part[(s1.start() if s1 else 0): p2.start() if p2 else 9000])
    a = f'sources/mtp/{name}_A.txt'
    if os.path.exists(a):
        ta = clean(open(a, encoding='utf-8').read())
        sma = re.search(r'(?i)PAPER\s*6B', ta)
        seg = ta[sma.start():] if sma else ''
        p2a = re.search(r'(?i)PART\s*[–-]?\s*II', seg)
        out.append(f'---- {name} SM PART I ANSWERS')
        out.append(' '.join(seg[: p2a.start() if p2a else 1500].split()))
open('sources/packs/mtp_sm_mcq.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('chars', sum(map(len, out)))


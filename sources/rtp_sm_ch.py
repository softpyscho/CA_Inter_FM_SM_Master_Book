"""Extract the 'Chapter N' blocks of the SM part of each RTP (questions and answers).
Usage: python sources/rtp_sm_ch.py 1 -> sources/packs/rtp_sm_ch1.txt"""
import re, sys, glob, os

n = sys.argv[1]
out = []
for f in sorted(glob.glob('sources/rtp/RTP-*.txt')):
    t = open(f, encoding='utf-8').read()
    t = re.sub(r'(?im)^\s*(©.*Institute of Chartered Accountants of India|INTERMEDIATE EXAMINATION|FINANCIAL MANAGEMENT AND|STRATEGIC MANAGEMENT|REVISION TEST PAPERS?|(JANUARY|MAY|SEPTEMBER) 20\d\d EXAMINATION|\d{1,3}|<<PAGE \d+>>)\s*$', '', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    sm = re.search(r'(?i)6B\s*:?\s*STRATEGIC MANAGEMENT', t)
    if not sm:
        out.append(f'#### {os.path.basename(f)}: no 6B heading'); continue
    s = t[sm.start():]
    blocks = list(re.finditer(rf'(?i)Chapter\s*[-–]?\s*{n}\s*[-–:]', s))
    out.append(f'\n#################### {os.path.basename(f)[:-4]} ({len(blocks)} blocks)')
    for b in blocks:
        e = re.search(rf'(?i)Chapter\s*[-–]?\s*{int(n) + 1}\s*[-–:]|SUGGESTED ANSWERS', s[b.end():])
        out.append('---- block\n' + s[b.start(): b.end() + (e.start() if e else 8000)])
    if not blocks:
        # older RTPs are not chapter-wise: include MCQ + descriptive question list for manual scan
        out.append('(not chapter-wise)')
open(f'sources/packs/rtp_sm_ch{n}.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('chars', sum(map(len, out)))
for line in out:
    if line.startswith('\n####') or line.startswith('####') or line.startswith('(not'):
        print(line.strip())

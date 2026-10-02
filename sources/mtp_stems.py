"""List MTP question stems: all MCQ stems (FM and SM, options dropped) and the opening of every descriptive part.
Output: sources/packs/mtp_stems.txt"""
import re, glob, os

NOISE = re.compile(r'(?i)^\s*(Download(ed)? from castudyweb\.com|CA Study Shop.*|©.*India|\d{1,3}|<<PAGE \d+>>)\s*$')
out = []
for f in sorted(glob.glob('sources/mtp/MTP-*_Q.txt')) + ['sources/mtp/MTP-S26-S1_A.txt']:
    t = '\n'.join(l for l in open(f, encoding='utf-8').read().split('\n') if not NOISE.match(l))
    t = re.sub(r'[ \t]+', ' ', t)
    out.append(f'\n==================== {os.path.basename(f)[:-4]}')
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    text = '\n'.join(lines)
    sm = re.search(r'(?i)PAPER\s*6B|6B\s*:\s*STRATEGIC', text)
    parts = [('FM', text[:sm.start()] if sm else text), ('SM', text[sm.start():] if sm else '')]
    for tag, p in parts:
        # join wrapped lines into paragraphs split at stems
        flat = ' '.join(p.split('\n'))
        pieces = re.split(r'(?=\s(?:\d{1,2}\.|\((?:i|ii|iii|iv|v|vi|vii)\)|\([a-e]\)|\([A-E]\))\s)', flat)
        for s in pieces:
            s = s.strip()
            if re.match(r'^\([a-dA-D]\)\s', s) and len(s) < 140 and not re.search(r'\?|Marks|EXPLAIN|DISCUSS|Explain|Discuss|Identify|What|Which|How|Why|State|Draft|Analy', s):
                continue  # option line
            if len(s) < 30:
                continue
            out.append(f'  [{tag}] ' + s[:230])
open('sources/packs/mtp_stems.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('lines', len(out), 'chars', sum(map(len, out)))

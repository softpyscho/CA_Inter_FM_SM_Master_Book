"""Compact map of every FM question part across suggested answers, RTPs and MTPs.

Usage: python sources/fm_map.py [stem_chars]  ->  sources/packs/fm_map.txt

Prints one line per question part: <label> | <first N characters of the stem>.
Used to assign each official question to the chapter it tests, for the numerical
chapters where keyword matching is too noisy.

Parts are found by walking the "(a) (b) (c)" markers of the descriptive section:
a fresh "(a)" starts the next question. For RTPs, which number questions straight
through without a Part II header, the whole FM stretch is walked.
"""
import re, os, glob, sys

STEM = int(sys.argv[1]) if len(sys.argv) > 1 else 150
NOISE = re.compile(r'(?im)^\s*(Download(ed)?\s*from castudyweb\.com|CA Study Shop.*|©.*India|<<PAGE \d+>>|\d{1,3}\s*)$')
SM_START = re.compile(r'(?i)SECTION\s*[-–—]?\s*B\s*:?\s*STRATEGIC MANAGEMENT|PAPER\s*[-–—]?\s*6B\s*:?\s*STRATEGIC|6B\s*:?\s*STRATEGIC MANAGEMENT')
PART2 = re.compile(r'(?i)PART\s*II\s*[-–—:]?\s*Descriptive|Descriptive Questions')
SUB = re.compile(r'(?m)^\s*\(?([a-e])\)\s')
QNUM = re.compile(r'(?m)^\s*(?:Question\s*(?:No\.?\s*)?)?(\d{1,2})\.?\s*(?:\(([a-e])\))?\s*$')


def clean(t):
    t = NOISE.sub('', t)
    return re.sub(r'\s+', ' ', t).strip()


def fm_slice(text):
    """The stretch of a paper that carries FM questions."""
    m = SM_START.search(text)
    return text[:m.start()] if m else text


def parts(text, rtp):
    """Yield (label, stem). A fresh '(a)' marker starts the next question."""
    body = text
    if not rtp:
        m = PART2.search(text)
        if m:
            body = text[m.start():]
    # ICAI numbers FM questions 1-4 with parts (a)(b)(c), so a fresh "(a)" is a new question
    nums = {}
    hits = [m.start() for m in SUB.finditer(body)]
    qno, out = 0, []
    for i, pos in enumerate(hits):
        end = hits[i + 1] if i + 1 < len(hits) else len(body)
        seg = clean(body[pos:end])
        if len(seg) < 40:
            continue
        if pos in nums:
            qno = int(nums[pos])
            label = f'Q{qno}'
        else:
            letter = SUB.match(body[pos:]).group(1)
            if letter == 'a':
                qno += 1
            label = f'Q{qno}{letter}'
        out.append((label, seg[:STEM]))
    return out


rows = []
for f in sorted(glob.glob('sources/sa/*.txt') + glob.glob('sources/rtp/*.txt') + glob.glob('sources/mtp/*_Q.txt')):
    name = os.path.basename(f)[:-4]
    t = fm_slice(open(f, encoding='utf-8').read())
    got = parts(t, name.startswith('RTP'))
    if not got:
        continue
    rows.append(f'\n########## {name}  ({len(got)} parts)')
    for label, stem in got:
        rows.append(f'  {label:<8} {stem}')

os.makedirs('sources/packs', exist_ok=True)
open('sources/packs/fm_map.txt', 'w', encoding='utf-8').write('\n'.join(rows))
print('fm_map.txt', len(rows), 'lines')

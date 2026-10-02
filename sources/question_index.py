"""Compact index of every question stem in the official papers (questions only, options/answers dropped).
Output: sources/packs/question_index.txt"""
import re, glob, os

NOISE = re.compile(r'(?i)downloaded? from castudyweb\.com|CA Study Shop.*|© ?The Institute of Chartered Accountants of India|'
                   r'^\s*(INTERMEDIATE EXAMINATION.*|FINANCIAL MANAGEMENT AND|STRATEGIC MANAGEMENT|SUGGESTED ANSWERS?|REVISION TEST PAPERS?|'
                   r'(JANUARY|MAY|SEPTEMBER) 20\d\d EXAMINATION|\d{1,3})\s*$')


def clean(t):
    lines = [l for l in t.split('\n') if not NOISE.search(l) and not l.startswith('<<PAGE')]
    return re.sub(r'[ \t]+', ' ', '\n'.join(lines))


def questions_part(name, t):
    """Return text that contains questions only."""
    if name.startswith('RTP'):
        # RTPs: FM questions, FM answers, SM questions, SM answers
        parts = re.split(r'(?i)SUGGESTED ANSWERS\s*/?\s*HINTS|\n\s*SUGGESTED ANSWERS\s*\n', t)
        keep = []
        for i, p in enumerate(parts):
            if i == 0:
                keep.append(p)
            else:
                m = re.search(r'(?i)6B\s*:?\s*STRATEGIC MANAGEMENT', p)
                if m:
                    keep.append(p[m.start():])
        return '\n'.join(keep)
    if name.startswith('MTP') and name.endswith('_A') and not os.path.exists(f'sources/mtp/{name[:-2]}_Q.txt'):
        return t  # answer file is the only copy (questions are embedded or must be read from answers)
    if name.startswith('MTP') and name.endswith('_A'):
        return ''
    return t


def stems(t):
    out, buf = [], []
    for line in t.split('\n'):
        s = line.strip()
        if not s:
            continue
        # drop MCQ option lines
        if re.match(r'^\(?[A-Da-d]\)\s', s) or re.match(r'^\([A-Da-d]\)$', s):
            continue
        buf.append(s)
    text = ' '.join(buf)
    # split at question starts
    pieces = re.split(r'(?=(?:Question\s*(?:No\.?\s*)?\d{1,2}\b|\s\d{1,2}\.\s+(?=[A-Z“"])|\(\s?[a-e]\s?\)\s+(?=[A-Z“"])|\((?:i|ii|iii|iv|v|vi)\)\s+(?=[A-Z])|Case Scenario|Chapter\s*\d\s*[-–]))', text)
    for p in pieces:
        p = p.strip()
        if len(p) < 25:
            continue
        if re.match(r'(?i)answer\b', p):
            continue
        out.append(p[:260])
    return out


docs = sorted(glob.glob('sources/sa/*.txt')) + sorted(glob.glob('sources/rtp/*.txt')) + sorted(glob.glob('sources/mtp/*.txt'))
lines = []
for f in docs:
    name = os.path.basename(f)[:-4]
    t = open(f, encoding='utf-8').read()
    q = questions_part(name, t)
    if not q:
        continue
    if name.startswith('SA'):
        # drop answer blocks: keep text from 'Question N' to next 'Answer'
        q = re.sub(r'(?s)\nAnswer\s*\n.*?(?=\nQuestion\s*\d|\Z)', '\n', q)
        q = re.sub(r'(?s)Answer Key.*?(?=PART\s*[–-]\s*II|SECTION|Question\s*1\b)', '', q)
    lines.append(f'\n==================== {name}')
    lines += ['  - ' + s for s in stems(clean(q))]

open('sources/packs/question_index.txt', 'w', encoding='utf-8').write('\n'.join(lines))
print('lines', len(lines), 'chars', sum(map(len, lines)))

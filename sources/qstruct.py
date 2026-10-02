"""The true question structure of a paper's FM descriptive section.

Usage: python sources/qstruct.py <file.txt> [stem_chars]
       python sources/qstruct.py --all           -> every SA and MTP question paper

ICAI numbers the descriptive section 1, 2, 3, 4 in sequence, each with parts (a),
(b), (c). Embedded numbered lists inside a question ("1. CALCULATE ...") break a
naive parser, so a line is only treated as a new question when its number is
exactly one more than the previous question's. That gives reliable atom ids.
"""
import re, sys, glob, os

SUB = re.compile(r'(?m)^\s*\(([a-e])\)\s')
NUM = re.compile(r'(?m)^\s*(\d{1,2})\.\s')
DESC = re.compile(r'(?i)PART\s*II\s*[-–—:]?\s*Descriptive|Division\s*B\s*[-–—:]?\s*Descriptive')
SM_START = re.compile(r'(?i)SECTION\s*[-–—]?\s*B\s*:?\s*STRATEGIC MANAGEMENT|PAPER\s*[-–—]?\s*6B')
QH = re.compile(r'(?m)^\s*Question\s*(\d{1,2})\s*$')


def structure(path, stem=95):
    t = open(path, encoding='utf-8').read()
    # suggested answers label their questions "Question N"; MTPs use "N."
    heads = [(m.start(), m.group(1)) for m in QH.finditer(t)]
    if not heads:
        d = DESC.search(t)
        body_start = d.start() if d else 0
        t2 = t[body_start:]
        m0 = SM_START.search(t2)
        if m0:
            t2 = t2[:m0.start()]
        # a question normally opens "N. (a)"; only fall back to a bare "N." when the
        # paper has no part (a) for that number. This rejects embedded numbered lists.
        heads, base, pos = [], body_start, 0
        for want in range(1, 6):
            m = re.compile(r'(?m)^\s*%d\.\s*\(a\)' % want).search(t2, pos)
            if not m:
                m = re.compile(r'(?m)^\s*%d\.\s' % want).search(t2, pos)
            if not m:
                break
            heads.append((base + m.start(), str(want)))
            pos = m.end()
    # the FM side ends where the strategic management section begins
    m_sm = SM_START.search(t, heads[0][0] if heads else 0)
    fm_end = m_sm.start() if m_sm else len(t)
    out = []
    for i, (pos, qno) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else fm_end
        end = min(end, fm_end)
        if pos >= fm_end:
            break
        blk = t[pos:end]
        a = re.search(r'(?m)^\s*Answer[s]?\s*$', blk)
        qt = blk[:a.start()] if a else blk
        subs = list(SUB.finditer(qt))
        if not subs:
            out.append((f'Q{qno}', re.sub(r'\s+', ' ', qt)[:stem]))
            continue
        for j, s in enumerate(subs):
            e2 = subs[j + 1].start() if j + 1 < len(subs) else len(qt)
            seg = re.sub(r'\s+', ' ', qt[s.start():e2]).strip()
            if len(seg) > 30:
                out.append((f'Q{qno}({s.group(1)})', seg[:stem]))
    return out


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    stem = int(args[1]) if len(args) > 1 else 95
    files = (sorted(glob.glob('sources/sa/*.txt')) + sorted(glob.glob('sources/mtp/*_Q.txt'))
             if '--all' in sys.argv else [args[0]])
    for f in files:
        print(f'\n########## {os.path.basename(f)[:-4]}')
        for label, text in structure(f, stem):
            print(f'  {label:<8} {text}')

"""Which official FM question parts are still unplaced?

Usage: python sources/coverage.py            -> summary + the unplaced list
       python sources/coverage.py --all      -> also print the parts already placed

Enumerates every FM question part from the suggested answers, RTPs and MTP question
papers, converts each to the atom id this project uses, and diffs that against the
ids in sources/atoms/atoms_F*.json. Anything listed as unplaced either belongs to a
chapter not yet built or has been missed.

Atom id conventions (see BUILD_STATE.md):
  past papers      PYQ-<paper>-Q<n><letter>[-OR]
  RTP descriptive  RTP-<paper>-FQ<n><letter>
  MTP descriptive  MTP-<paper>-FQ<n><letter>[-OR]
"""
import re, json, glob, os, sys

SHOW_ALL = '--all' in sys.argv
PAPER = {'SA': 'PYQ'}
SM_HEAD = re.compile(r'(?i)SECTION\s*[-–—]?\s*B\s*:?\s*STRATEGIC MANAGEMENT|PAPER\s*[-–—]?\s*6B\s*:?\s*STRATEGIC')
FM_HEAD = re.compile(r'(?i)SECTION\s*[-–—]?\s*A\s*:?\s*FINANCIAL MANAGEMENT|PAPER\s*[-–—]?\s*6A\s*:?\s*FINANCIAL')
QH = re.compile(r'(?m)^\s*(?:Question\s*(?:No\.?\s*)?(\d{1,2})\s*$|(\d{1,2})\.\s*$)')
SUB = re.compile(r'(?m)^\s*\(([a-e])\)\s')
ORM = re.compile(r'(?m)^\s*OR\s*$')


def fm_spans(t):
    """The character ranges of a file that carry FM material."""
    marks = sorted([(m.start(), 'FM') for m in FM_HEAD.finditer(t)] +
                   [(m.start(), 'SM') for m in SM_HEAD.finditer(t)])
    if not marks:
        return [(0, len(t))]
    spans, open_at = [], 0 if marks[0][1] == 'SM' else None
    for i, (pos, kind) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(t)
        if kind == 'FM':
            spans.append((pos, end))
    return spans or [(0, len(t))]


DESC = re.compile(r'(?i)PART\s*II\s*[-–—:]?\s*Descriptive|Division\s*B\s*[-–—:]?\s*Descriptive')

# RTP files, and some MTP question papers, carry the suggested answers in the same
# file as the questions. Scanning the answer half yields phantom "parts" whose stem
# is a number or a stray phrase ("(a) 9.12%", "(a) Gordon's formula"), which then
# show up as unplaced atoms that do not exist. Cut each FM span at the answers.
ANS_HEAD = re.compile(r'(?i)^[ \t]*(SUGGESTED\s+ANSWERS?(\s*/\s*HINTS)?|ANSWERS?\s+TO\s+|Answer\s+to\s+Case\s+Scenario)', re.M)
# A real ICAI sub-part stem is prose. These are answer fragments, not questions.
ANS_LIKE = re.compile(r'^\([a-e]\)\s*(?:[`\u20b9]|\d|[-+]?\d*\.?\d+\s*%|True|False)')


def parts(path):
    """Yield (question-number, letter, is_or, stem) for one paper's FM side."""
    t = open(path, encoding='utf-8').read()
    for lo, hi in fm_spans(t):
        body = t[lo:hi]
        a = ANS_HEAD.search(body)
        if a:
            body = body[:a.start()]
        d = DESC.search(body)          # skip Part I MCQs, whose (a)-(d) are options
        if d:
            body = body[d.start():]
        qs = list(QH.finditer(body))
        for i, q in enumerate(qs):
            qn = q.group(1) or q.group(2)
            end = qs[i + 1].start() if i + 1 < len(qs) else len(body)
            blk = body[q.start():end]
            a = re.search(r'(?m)^\s*Answer[s]?\s*$', blk)
            qt = blk[:a.start()] if a else blk
            subs = list(SUB.finditer(qt))
            for j, s in enumerate(subs):
                e2 = subs[j + 1].start() if j + 1 < len(subs) else len(qt)
                seg = re.sub(r'\s+', ' ', qt[s.start():e2]).strip()
                if len(seg) < 35 or s.group(1) in 'de':
                    continue        # ICAI lettered FM parts run (a)-(c); (d)/(e) are MCQ options
                if ANS_LIKE.match(seg):
                    continue        # an answer fragment that survived the span cut
                is_or = bool(ORM.search(qt[:s.start()][-40:]))
                yield qn, s.group(1), is_or, seg[:200]


placed = {}
for f in glob.glob('sources/atoms/atoms_*.json'):
    ch = os.path.basename(f)[6:-5]
    for at in json.load(open(f, encoding='utf-8'))['atoms']:
        placed[at['id']] = ch

rows, miss = [], []
for f in sorted(glob.glob('sources/sa/*.txt') + glob.glob('sources/rtp/*.txt') + glob.glob('sources/mtp/*_Q.txt')):
    base = os.path.basename(f)[:-4]
    if base.startswith('SA-'):
        pid = 'PYQ-' + base[3:].split('_')[0]
        fmt = '{p}-Q{q}{l}{o}'
    elif base.startswith('RTP-'):
        pid = 'RTP-' + base[4:]
        fmt = '{p}-FQ{q}{l}{o}'
    else:
        pid = 'MTP-' + base[4:-2]
        fmt = '{p}-FQ{q}{l}{o}'
    for qn, letter, is_or, stem in parts(f):
        aid = fmt.format(p=pid, q=qn, l=letter, o='-OR' if is_or else '')
        (rows if aid in placed else miss).append((aid, placed.get(aid, ''), stem))

print(f'placed {len(rows)} · unplaced {len(miss)}')
if SHOW_ALL:
    for aid, ch, stem in rows:
        print(f'  [{ch}] {aid:<22} {stem}')
print('\n-- unplaced --')
for aid, _, stem in miss:
    print(f'  {aid:<22} {stem}')

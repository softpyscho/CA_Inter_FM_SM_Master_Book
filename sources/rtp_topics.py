"""RTP question number -> the topic heading ICAI printed above it.

Usage: python sources/rtp_topics.py  ->  sources/packs/rtp_topics.txt

RTPs label each question with the chapter it comes from ("Ratio Analysis",
"Cost of Capital", "Leverage" ...). That label is the most reliable chapter
assignment available for the numerical chapters, so it is extracted here once
and reused when writing each chapter's atoms file.
"""
import re, glob, os

SM_START = re.compile(r'(?i)6B\s*:?\s*STRATEGIC MANAGEMENT|SECTION\s*[-–—]?\s*B\s*:?\s*STRATEGIC')
QNUM = re.compile(r'(?m)^\s*(\d{1,2})\.\s')
# a topic label is a short titled line with no sentence punctuation
LABEL = re.compile(r'(?m)^\s*([A-Z][A-Za-z&/\'’()\- ]{4,70})\s*$')
SKIP = re.compile(r'(?i)revision test paper|intermediate examination|suggested answers?|financial management and'
                  r'|strategic management|institute of chartered|examination|part [i]+|division [ab]|answers?$')

out = []
for f in sorted(glob.glob('sources/rtp/*.txt')):
    t = open(f, encoding='utf-8').read()
    m0 = SM_START.search(t)
    t = t[:m0.start()] if m0 else t
    # the question section ends where the answers begin
    a = re.search(r'(?im)^\s*SUGGESTED ANSWERS?\s*/?\s*HINTS?\s*$|^\s*SUGGESTED ANSWERS?\s*$', t)
    q_side = t[:a.start()] if a else t
    labels = [(m.start(), m.group(1).strip()) for m in LABEL.finditer(q_side) if not SKIP.search(m.group(1))]
    out.append(f'\n########## {os.path.basename(f)[:-4]}')
    seen = set()
    for m in QNUM.finditer(q_side):
        n = m.group(1)
        if n in seen:
            continue
        seen.add(n)
        before = [lab for pos, lab in labels if pos < m.start()]
        stem = re.sub(r'\s+', ' ', q_side[m.start():m.start() + 95])
        out.append(f'  Q{n:<3} [{before[-1] if before else "?"}]  {stem}')

os.makedirs('sources/packs', exist_ok=True)
open('sources/packs/rtp_topics.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))

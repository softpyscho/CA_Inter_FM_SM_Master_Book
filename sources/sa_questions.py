"""Print exact question text (no answers) from ICAI Suggested Answers: MCQ stems with options, and Question 1-8 blocks.
Usage: python sources/sa_questions.py [SA-M24 ...]  -> sources/packs/sa_questions.txt"""
import re, sys, glob, os

NOISE = re.compile(r'(?i)^\s*(©.*Institute of Chartered Accountants of India|INTERMEDIATE EXAMINATION.*|FINANCIAL MANAGEMENT AND|STRATEGIC MANAGEMENT|SUGGESTED ANSWERS?|\d{1,3}|<<PAGE \d+>>)\s*$')

names = sys.argv[1:] or [os.path.basename(f)[:-4] for f in sorted(glob.glob('sources/sa/SA-*.txt'))]
out = []
for n in names:
    raw = open(f'sources/sa/{n}.txt', encoding='utf-8').read()
    t = '\n'.join(l.rstrip() for l in raw.split('\n') if not NOISE.match(l))
    out.append(f'\n#################### {n}')
    # Part I: everything before first 'Answer Key' blocks, keep MCQ text (drop key tables)
    part1_end = re.search(r'(?m)^\s*(SECTION\s*A:\s*FINANCIAL MANAGEMENT\s*$|PART\s*[–-]\s*II)', t)
    mcq = t[:part1_end.start()] if part1_end else ''
    mcq = re.sub(r'(?s)Answer Key.*?(?=Case Scenario|SECTION|\Z)', '', mcq)
    if mcq.strip():
        out.append('---- PART I (MCQs)\n' + re.sub(r'\n\s*\n+', '\n', mcq).strip())
    rest = t[part1_end.start():] if part1_end else t
    # SA-S24 style: Part I MCQs appear per section; capture MCQ blocks inside rest too
    for blk in re.finditer(r'(?s)PART\s*-\s*I\b(.*?)(?=Answer Key)', rest):
        out.append('---- PART I block\n' + re.sub(r'\n\s*\n+', '\n', blk.group(1)).strip())
    for m in re.finditer(r'(?s)\n\s*(Question\s*\d)\s*\n(.*?)(?=\n\s*Answer\s*\n|\n\s*Answer\s{2,}|\n\s*Answer the following|\n\s*Question\s*\d\s*\n|\Z)', rest):
        q = re.sub(r'\n\s*\n+', '\n', m.group(2)).strip()
        out.append(f'---- {m.group(1)}\n{q}')

open('sources/packs/sa_questions.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('chars', sum(map(len, out)))

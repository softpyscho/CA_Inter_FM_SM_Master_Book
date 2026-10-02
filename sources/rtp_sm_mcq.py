"""Print SM MCQ sections of RTPs (questions: from 6B heading to first 'Chapter 1'; answers: MCQ answer block)."""
import re, glob, os

out = []
for f in sorted(glob.glob('sources/rtp/RTP-*.txt')):
    t = open(f, encoding='utf-8').read()
    t = re.sub(r'(?im)^\s*(©.*Institute of Chartered Accountants of India|INTERMEDIATE EXAMINATION|FINANCIAL MANAGEMENT AND|STRATEGIC MANAGEMENT|REVISION TEST PAPERS?|(JANUARY|MAY|SEPTEMBER) 20\d\d EXAMINATION|\d{1,3}|<<PAGE \d+>>)\s*$', '', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    sm = re.search(r'(?i)6B\s*:?\s*STRATEGIC MANAGEMENT', t)
    s = t[sm.start():]
    q_end = re.search(r'(?i)Chapter\s*1\s*[-–:]', s)
    out.append(f'\n#################### {os.path.basename(f)[:-4]} QUESTIONS')
    out.append(s[: q_end.start() if q_end else 6000])
    a = re.search(r'(?i)SUGGESTED ANSWERS', s)
    if a:
        tail = s[a.end():]
        a_end = re.search(r'(?i)\n\s*7\.\s', tail)
        out.append(f'---- {os.path.basename(f)[:-4]} ANSWERS')
        out.append(tail[: a_end.start() if a_end else 3000])
open('sources/packs/rtp_sm_mcq.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('chars', sum(map(len, out)))

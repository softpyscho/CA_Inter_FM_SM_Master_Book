"""Find official questions (PYQ / RTP / MTP) that belong to a chapter.
Usage: python sources/find_ch.py F02        -> sources/packs/cand_F02.txt
Keywords per chapter live in sources/ch_keywords.json ({"F02": ["venture capital", ...], ...}).
Segments are cut at question boundaries; a segment is kept when it matches any keyword."""
import re, json, glob, os, sys

code = sys.argv[1].upper()
KW = json.load(open('sources/ch_keywords.json', encoding='utf-8'))[code]
BREAK = re.compile(r'(?m)^\s*(Question\s*(No\.?\s*)?\d{1,2}\b.*|\d{1,2}\.\s*$|\d{1,2}\.\s+(?=[A-Z])|\(\s*[a-e]\s*\)\s*$|Case Scenario.*|Division\s*[AB].*|SECTION.*|PART.*)$')
NOISE = re.compile(r'(?im)^\s*(Download(ed)? from castudyweb\.com|CA Study Shop.*|©.*India)\s*$')


def segments(text):
    idx = [m.start() for m in BREAK.finditer(text)] + [len(text)]
    prev = 0
    for i in idx:
        if i - prev > 40:
            yield prev, text[prev:i]
        prev = i


def question_side(name, t):
    """Keep only the part of a document that carries questions (answers are fetched later with grab.py)."""
    if name.startswith('MTP'):
        return t if name.endswith('_Q') or not os.path.exists(f'sources/mtp/{name[:-2]}_Q.txt') else ''
    if name.startswith('RTP'):
        parts, keep = re.split(r'(?i)SUGGESTED ANSWERS\s*/?\s*HINTS|\n\s*SUGGESTED ANSWERS\s*\n', t), []
        for i, p in enumerate(parts):
            if i == 0:
                keep.append(p)
            else:  # the SM question block sits after the FM answers
                m = re.search(r'(?i)6B\s*:?\s*STRATEGIC MANAGEMENT', p)
                if m:
                    keep.append(p[m.start():])
        return '\n'.join(keep)
    # suggested answers: drop the text between an 'Answer' line and the next question
    return re.sub(r'(?s)\n\s*Answers?\s*\n.*?(?=\n\s*(?:Question\s*\d|\d{1,2}\.\s))', '\n', t)


out, counts = [], {}
files = sorted(glob.glob('sources/sa/*.txt') + glob.glob('sources/rtp/*.txt') + glob.glob('sources/mtp/*.txt'))
for f in files:
    t = NOISE.sub('', open(f, encoding='utf-8').read())
    name = os.path.basename(f)[:-4]
    t = question_side(name, t)
    if not t.strip():
        continue
    for pos, seg in segments(t):
        low = seg.lower()
        hits = sorted({k for k in KW if re.search(k, low)})
        if hits:
            counts[name] = counts.get(name, 0) + 1
            page = len(re.findall(r'<<PAGE', t[:pos])) or 1
            out.append(f'\n########## {name} p{page} | {",".join(hits)[:120]}\n{seg.strip()[:2600]}')

os.makedirs('sources/packs', exist_ok=True)
open(f'sources/packs/cand_{code}.txt', 'w', encoding='utf-8').write('\n'.join(out))
print(code, len(out), 'candidate segments,', sum(map(len, out)), 'chars')
for k, v in sorted(counts.items()):
    print(f'  {k}: {v}')

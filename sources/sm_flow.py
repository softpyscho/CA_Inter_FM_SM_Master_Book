"""Clean SM chapter text into flow text (page markers kept) and list candidate numbered headings.
Usage: python sources/sm_flow.py fm_ch1 [sm_ch1 ...]"""
import re, sys

LIG = {'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl', '’': "'", '‘': "'", '“': '"', '”': '"'}
FOOT = re.compile(r'(?i)^\s*(©\s*The Institute of Chartered Accountants of India|FINANCIAL MANAGEMENT|STRATEGIC MANAGEMENT|SCOPE AND OBJECTIVES OF FINANCIAL MANAGEMENT|INTRODUCTION TO STRATEGIC MANAGEMENT|\d{1,2}\.\d{1,3})\s*$')
HEAD = re.compile(r'^\s*((\d{1,2}(\.\d{1,2}){0,2})\.?|\([ivx]+\)|\([a-z]\)|UNIT\s*[-–]\s*[IVX]+)\s+([A-Z][^.]{2,110})$')

for name in sys.argv[1:]:
    raw = open(f'sources/sm/{name}.txt', encoding='utf-8').read()
    for k, v in LIG.items():
        raw = raw.replace(k, v)
    out, heads, page = [], [], 0
    lines = raw.split('\n')
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        m = re.match(r'<<PAGE (\d+)>>', ln)
        if m:
            page = int(m.group(1)); out.append(f'[p{page}]'); i += 1; continue
        if FOOT.match(ln) or not ln.strip():
            i += 1; continue
        # a bare number line followed by a title line = heading split over two lines
        if re.fullmatch(r'\s*\d{1,2}(\.\d{1,2}){0,2}\.?\s*', ln) and i + 1 < len(lines) and lines[i + 1].strip()[:1].isupper():
            ln = ln.strip() + ' ' + lines[i + 1].strip(); i += 1
        h = HEAD.match(ln)
        if h and len(ln) < 120:
            heads.append(f'p{page}\t{ln.strip()}')
            out.append('\n## ' + ln.strip())
        else:
            if out and out[-1].endswith('-') and not out[-1].endswith(' -'):
                out[-1] = out[-1][:-1] + ln.strip()
            else:
                out.append(ln.strip())
        i += 1
    open(f'sources/sm/{name}.flow.txt', 'w', encoding='utf-8').write('\n'.join(out))
    open(f'sources/sm/{name}.headings.txt', 'w', encoding='utf-8').write('\n'.join(heads))
    print('==', name, 'chars', sum(map(len, out)), 'headings', len(heads))
    print('\n'.join(heads))

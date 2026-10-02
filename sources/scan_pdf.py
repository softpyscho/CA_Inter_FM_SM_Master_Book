"""Scan the built PDF for internal markers that must not appear in the printed book."""
import sys, re, io, pymupdf
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = pymupdf.open(sys.argv[1] if len(sys.argv) > 1 else 'build/new.pdf')
txt = [p.get_text() for p in d]
print('pages', len(d))
bad = ['⛔', '✅', '🔶', '❓', 'VERIFIED', 'PARAPHRASED', 'AI-GENERATED', 'atom', 'OV-0', 'SECONDARY', 'UPDATE SWEEP',
       'PYQ-', 'RTP-', 'MTP-', 'CASE-', 'EQ-C', 'MCQ-C', 'MINI-', 'Evidence strip', 'Last verified', 'login-only', 'third-party copies', 'castudyweb', 'CA Study Shop', 'EQ-F', 'EQ-S', 'MCQ-F', 'MCQ-S', 'CT-MCQ', 'CT-D-']
bad_re = [r'\b[FS]\d\d\.\d\d', r'\b[MSJ]2[4-7]-', r'\b[FS]Q\d', r'\bSMCQ']
hits = 0
for b in bad:
    h = [(i + 1, t[max(0, t.find(b) - 40):t.find(b) + 40].replace('\n', ' ')) for i, t in enumerate(txt) if b in t]
    if h: print(repr(b), len(h), h[:3]); hits += 1
for r in bad_re:
    h = [(i + 1, m.group(0)) for i, t in enumerate(txt) for m in re.finditer(r, t)]
    if h: print(r, len(h), h[:5]); hits += 1
print('CLEAN' if not hits else 'ISSUES FOUND')


"""Split official documents (SA, RTP, MTP) into question-sized segments and flag Chapter 1 candidates.
Writes sources/packs/ch1_candidates.txt (full segment text) for manual review."""
import re, glob, os

FM1 = [r'wealth maxim', r'profit maxim', r'agency (problem|cost)', r'finance function', r'finance executive', r'chief financ\w* officer',
       r'\bCFO\b', r'financial distress', r'insolven', r'financial management and (financial )?accounting', r'scope of financial management',
       r'objectives? of financial management', r'evolution of financial management', r'traditional phase', r'value maximi[sz]ation',
       r'procurement of funds', r'utili[sz]ation of funds', r'ezra solomon', r'role of (the )?financ\w* (manager|controller)',
       r'financing,? investment and dividend decision', r'investment, financing and dividend', r'shareholders?\W? wealth']
SM1 = [r'strategic intent', r'\bvision\b', r'\bmission\b', r'goals? and objectives', r'core values|value system', r'corporate[- ]level', r'business[- ]level',
       r'functional[- ]level', r'levels? of strateg', r'strategic levels', r'limitations? of strategic management', r'importance of strategic management',
       r'benefits? of strategic management', r'proactive', r'reactive', r'matrix relationship', r'horizontal relationship',
       r'functional and divisional relationship', r'top[- ]down', r'bottom[- ]up', r'concept of strategy', r'business policy',
       r'what business are we in', r'long[- ]term objectives', r'meaning of strategic management', r'strategic management process',
       r'network of relationship', r'adaptive strategy']

BREAK = re.compile(r'(?m)^\s*(Question\s*(No\.?\s*)?\d{1,2}\b.*|\d{1,2}\.\s*$|\d{1,2}\.\s+(?=[A-Z])|Case Scenario.*|Division\s*[AB].*|SECTION.*)$')


def segments(text):
    idx = [m.start() for m in BREAK.finditer(text)] + [len(text)]
    prev = 0
    for i in idx:
        if i - prev > 40:
            yield prev, text[prev:i]
        prev = i


def pages(text, pos):
    return len(re.findall(r'<<PAGE', text[:pos])) or 1


out, counts = [], {}
files = sorted(glob.glob('sources/sa/*.txt') + glob.glob('sources/rtp/*.txt') + glob.glob('sources/mtp/*.txt'))
for f in files:
    t = open(f, encoding='utf-8').read()
    name = os.path.basename(f)[:-4]
    for pos, seg in segments(t):
        low = seg.lower()
        fm = sorted({p for p in FM1 if re.search(p, low)})
        sm = sorted({p for p in SM1 if re.search(p, low)})
        # SM hits need 2+ distinct cues (vision/mission/values are common words); FM needs 1
        tag = []
        if fm: tag.append('FM1:' + ','.join(fm))
        if len([p for p in sm if p not in (r'proactive', r'reactive')]) >= 2 or {r'proactive', r'reactive'} <= set(sm) or any(p in sm for p in [r'strategic intent', r'levels? of strateg', r'strategic levels', r'limitations? of strategic management',
                                                  r'importance of strategic management', r'benefits? of strategic management', r'matrix relationship',
                                                  r'horizontal relationship', r'functional and divisional relationship', r'network of relationship',
                                                  r'concept of strategy', r'adaptive strategy', r'what business are we in']):
            tag.append('SM1:' + ','.join(sm))
        if tag:
            counts[name] = counts.get(name, 0) + 1
            out.append(f'\n########## {name} p{pages(t, pos)} @{pos} | {" | ".join(tag)}\n{seg.strip()[:3000]}')

os.makedirs('sources/packs', exist_ok=True)
open('sources/packs/ch1_candidates.txt', 'w', encoding='utf-8').write('\n'.join(out))
print(len(out), 'candidate segments')
for k, v in counts.items():
    print(f'  {k}: {v}')


"""Merge sources/<code>/u*.json into book/ChNN.json and validate.
Usage (from project root): python sources/merge_chapter.py F01 [--date dd-mm-yyyy]
Book file numbering: F01..F09 -> Ch01..Ch09 ; S01..S05 -> Ch10..Ch14.
Checks: SM heading coverage, every official atom placed (own entry or full ID inside also_asked_as),
no atoms from other chapters, duplicate IDs, generated-MCQ key balance (each letter within 25% +/- 5%),
placeholder words, reader-facing text in required fields."""
import json, glob, re, sys, io, collections, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

code = sys.argv[1].upper()
date = sys.argv[sys.argv.index('--date') + 1] if '--date' in sys.argv else None
sec, ch = code[0], int(code[1:])
book_no = ch if sec == 'F' else 9 + ch
units = sorted(glob.glob(f'sources/{code.lower()}/u*.json'))
if not units:
    sys.exit(f'no units in sources/{code.lower()}')

book = {}
for u in units:
    try:
        d = json.load(open(u, encoding='utf-8'))
    except json.JSONDecodeError as e:
        sys.exit(f'JSON error in {u}: {e}')
    for k, v in d.items():
        if k == 'concepts':
            book.setdefault('concepts', []).extend(v)
        elif k in book and isinstance(v, list):
            book[k].extend(v)
        else:
            book[k] = v
if date:
    book['meta']['last_verified'] = date

errors, warns = [], []
reg = [r for r in json.load(open('sources/register.json', encoding='utf-8')) if r['code'].startswith(code + '.')]
atoms = json.load(open(f'sources/atoms/atoms_{code}.json', encoding='utf-8'))['atoms']

# 1. heading coverage
covered = set()
for c in book['concepts']:
    for part in re.split(r'\s*\+\s*', c['code']):
        covered.add(part.strip())
missing = [r['code'] for r in reg if r['code'] not in covered]
if missing:
    errors.append(f'uncovered SM headings: {missing}')
unknown = sorted(x for x in covered if x not in {r["code"] for r in reg})
if unknown:
    errors.append(f'concept codes not in register: {unknown}')

# 2. collect ids and also_asked_as text
ids = collections.Counter()
also_text = []
official_ids = set()


def walk(o, path=''):
    if isinstance(o, dict):
        if 'id' in o and isinstance(o['id'], str):
            ids[o['id']] += 1
        for k, v in o.items():
            if k == 'also_asked_as':
                also_text.extend(v if isinstance(v, list) else [v])
            if k in ('pyq_table', 'verification'):
                continue  # evidence table repeats question ids by design; verification is internal
            walk(v, path + '.' + k)
    elif isinstance(o, list):
        for x in o:
            walk(x, path)


walk(book)
dups = [i for i, n in ids.items() if n > 1 and i != 'verification']
if dups:
    errors.append(f'duplicate ids: {dups}')

placed, unplaced = [], []
blob = ' '.join(also_text)
for a in atoms:
    if a['id'] in ids or re.search(re.escape(a['id']) + r'(?![\w-])', blob):
        placed.append(a['id'])
    else:
        unplaced.append(a['id'])
if unplaced:
    errors.append(f'unplaced atoms: {unplaced}')
official_pat = re.compile(r'^(PYQ|RTP|MTP)-')
atom_ids = {a['id'] for a in atoms}
foreign = [i for i in ids if official_pat.match(i) and i not in atom_ids]
foreign += [m.group(0) for m in re.finditer(r'\b(?:PYQ|RTP|MTP)-[MSJ]\d\d(?:-S[12])?-[\w-]+', blob) if m.group(0) not in atom_ids]
if foreign:
    errors.append(f'official ids not in this chapter atom file: {sorted(set(foreign))}')

# 3. official question placed under a block that carries its primary code
code_of = {a['id']: a['codes'][0] for a in atoms}
for c in book['concepts']:
    cc = {p.strip() for p in re.split(r'\s*\+\s*', c['code'])}
    for q in c.get('official_questions', []) + c.get('mcqs', []):
        if q['id'] in code_of and code_of[q['id']] not in cc:
            warns.append(f"{q['id']} primary {code_of[q['id']]} placed under {c['code']}")

# 4. key balance (generated MCQs only)
letters = collections.Counter()
for c in book['concepts']:
    for m in c.get('mcqs', []):
        if not official_pat.match(m['id']):
            letters[m['answer']] += 1
for cs in book.get('cases', []):
    for q in cs['questions']:
        if q.get('options'):
            letters[q['answer']] += 1
for m in book.get('chapter_test', {}).get('mcqs', []):
    letters[m['answer']] += 1
total = sum(letters.values())
dev = max(abs(letters[k] / total - 0.25) for k in 'ABCD') if total else 0
if dev > 0.05:
    errors.append(f'key balance off: {dict(letters)} max deviation {dev:.1%}')

# 5. MCQ sanity: answer key exists among options
for c in book['concepts']:
    for m in c.get('mcqs', []):
        if m['answer'] not in m.get('options', {}):
            errors.append(f"{m['id']} answer {m['answer']} not in options")

# 6. placeholder words
raw = json.dumps(book, ensure_ascii=False)
for w in ['TBD', 'placeholder', 'lorem', 'XXX', 'wait,']:
    if w.lower() in raw.lower():
        errors.append(f'placeholder text found: {w}')

out = f'book/Ch{book_no:02d}.json'
os.makedirs('book', exist_ok=True)
json.dump(book, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print(f'== {code} -> {out}')
print(f'SM headings covered {len(reg) - len(missing)}/{len(reg)}')
print(f'official atoms placed {len(placed)}/{len(atoms)}')
print(f'topic blocks {len(book["concepts"])}; official question entries {sum(len(c.get("official_questions", [])) for c in book["concepts"])}; '
      f'official MCQs {sum(1 for c in book["concepts"] for m in c.get("mcqs", []) if official_pat.match(m["id"]))}')
print(f'generated MCQ keys {dict(sorted(letters.items()))} total {total} max deviation {dev:.1%}')
for w in warns:
    print('WARN', w)
print('ERRORS' if errors else 'ERRORS: none')
for e in errors:
    print('  -', e)
sys.exit(1 if errors else 0)

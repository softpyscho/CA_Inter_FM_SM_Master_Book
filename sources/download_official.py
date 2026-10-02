"""Download official ICAI Paper 6 documents (suggested answers, question papers, RTPs) and extract text."""
import re, os, json, html, shutil, glob, urllib.request
import pymupdf

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
MON = {'january': 'J', 'may': 'M', 'september': 'S'}


def get(url, binary=False):
    req = urllib.request.Request(url.replace(' ', '%20'), headers=UA)
    data = urllib.request.urlopen(req, timeout=120).read()
    return data if binary else data.decode('utf-8', 'replace')


def code(label):
    m = re.search(r'(?i)(january|may|september)[ ,]*20(\d\d)', label)
    return MON[m.group(1).lower()] + m.group(2) if m else None


def save(url, path):
    if not os.path.exists(path):
        open(path, 'wb').write(get(url, True))
    d = pymupdf.open(path)
    open(path[:-4] + '.txt', 'w', encoding='utf-8').write(
        ''.join('<<PAGE %d>>\n' % (i + 1) + p.get_text() for i, p in enumerate(d)))
    print(os.path.basename(path), d.page_count, 'p |', ' '.join(d[0].get_text().split())[:100])


src = json.load(open('sources/p6_sources.json', encoding='utf-8'))
log = []

# Suggested answers
for x in src['sa']:
    c = code(x['exam'])
    part = '_6A' if '6A' in x['text'] else '_6B' if '6B' in x['text'] else ''
    p = f'sources/sa/SA-{c}{part}.pdf'
    save(x['url'], p); log.append({'file': p, 'url': x['url']})

# Question papers: Paper-6 links in page order; attempt read from the URL or the PDF header
page = get('https://www.icai.org/post/question-papers-intermediate-course')
qps = []
for m in re.finditer(r'<a[^>]+href="([^"]+\.pdf)"[^>]*>([\s\S]*?)</a>', page):
    if re.search(r'(?i)paper.?6', html.unescape(re.sub(r'<[^>]+>', '', m.group(2)))) and m.group(1) not in qps:
        qps.append(m.group(1))
for u in qps:
    tmp = 'sources/qp/_tmp.pdf'
    open(tmp, 'wb').write(get(u, True))
    head = ' '.join(pymupdf.open(tmp)[0].get_text().split())[:400]
    c = code(head) or code(u.replace('-', ' ').replace('sep', 'september ').replace('jan', 'january ').replace('may', 'may '))
    if not c or c < '' or not re.search(r'(?i)6A|financial management', head):
        print('SKIP (not new-scheme P6 or unknown attempt):', u, head[:120]); os.remove(tmp); continue
    p = f'sources/qp/QP-{c}.pdf'
    if os.path.exists(p):
        os.remove(tmp); continue
    shutil.move(tmp, p); save(u, p); log.append({'file': p, 'url': u})

# RTPs: every English-medium Intermediate attempt
page = get('https://boslive.icai.org/education_content_rtp.php?c=Intermediate')
for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', page):
    href, label = html.unescape(m.group(1)), html.unescape(re.sub(r'<[^>]+>|\s+', ' ', m.group(2))).strip()
    if 'Hindi' in label or not ('rtp_list' in href or 'rtp-intermediate' in href):
        continue
    c = code(label)
    url = href if href.startswith('http') else 'https://boslive.icai.org/' + href.lstrip('/')
    sub = get(url)
    found = None
    for row in re.findall(r'<tr[\s\S]*?</tr>', sub) or []:
        if re.search(r'(?i)paper.?6|financial management', re.sub(r'<[^>]+>', ' ', row)):
            a = re.search(r'href="([^"]+\.pdf)"', row)
            if a: found = a.group(1); break
    if not found:
        for a in re.findall(r'href="([^"]+\.pdf)"', sub):
            if re.search(r'(?i)-p6\b|p6\.pdf|-6\.pdf', a): found = a; break
    if not found:
        for a, t in re.findall(r'<a[^>]+href="([^"]+\.pdf)"[^>]*>([\s\S]*?)</a>', sub):
            if re.search(r'(?i)paper.?6|financial management', t): found = a; break
    if found:
        p = f'sources/rtp/RTP-{c}.pdf'
        save(found, p); log.append({'file': p, 'url': found})
    else:
        print('RTP not found for', label, url)

# Examiners' comments: official Group II PDFs already downloaded for the Audit book
for f in glob.glob(r'C:/Users/Santo/CA_Inter_Audit_Master_Book/sources/examiner/EXC-*-G2.pdf'):
    p = 'sources/examiner/' + os.path.basename(f)
    shutil.copy(f, p); save('', p); log.append({'file': p, 'url': 'copied from Audit project (ICAI Group II examiners comments)'})

json.dump(log, open('sources/downloads_log.json', 'w', encoding='utf-8'), indent=1)

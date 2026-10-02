"""List official ICAI Paper 6 (FM & SM) PDFs: question papers, suggested answers, RTPs, examiners' comments."""
import re, json, html, urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}


def get(url):
    req = urllib.request.Request(url.replace(' ', '%20'), headers=UA)
    return urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')


def text(s):
    return html.unescape(re.sub(r'<[^>]+>|\s+', ' ', s)).strip()


def links(page):
    return [(m.group(1), text(m.group(2))) for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', page)]


def stream(page):
    """Yield (kind, value) for headings/strong text and links in document order."""
    for m in re.finditer(r'<(h[1-6]|strong|b|p|td)[^>]*>([\s\S]*?)</\1>|<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', page):
        if m.group(3):
            yield 'a', (m.group(3), text(m.group(4)))
        else:
            t = text(m.group(2))
            if t and len(t) < 90:
                yield 'h', t


P6 = re.compile(r'(?i)paper.?6|financial management|strategic management|\bfm\b|\bsm\b')
out = {'qp': [], 'sa': [], 'rtp': [], 'examiner': []}

# Question papers (new scheme) — headings name the attempt
page = get('https://www.icai.org/post/question-papers-intermediate-course')
head = ''
for kind, v in stream(page):
    if kind == 'h' and re.search(r'(?i)(january|may|september|june|november|december)[ ,]*20\d\d', v):
        head = v
    elif kind == 'a' and v[0].lower().endswith('.pdf') and P6.search(v[1]):
        out['qp'].append({'exam': head, 'text': v[1], 'url': v[0]})

# Suggested answers — one post per attempt
for href, t in links(get('https://www.icai.org/post/suggested-answer-intermediate')):
    if re.search(r'sugg-ans-inter-\w+20\d\d$', href):
        for h2, t2 in links(get(href)):
            if h2.lower().endswith('.pdf') and P6.search(t2):
                out['sa'].append({'exam': t, 'text': t2, 'url': h2})

# RTPs
for href, t in links(get('https://boslive.icai.org/education_content_rtp.php?c=Intermediate')):
    if ('rtp_list' in href or 'rtp-intermediate' in href) and 'Hindi' not in t:
        url = href if href.startswith('http') else 'https://boslive.icai.org/' + href.lstrip('/')
        for h2, t2 in links(get(url)):
            if h2.lower().endswith('.pdf') and P6.search(t2):
                out['rtp'].append({'exam': t, 'text': t2, 'url': h2})

# Examiners' comments (BoS "Education Content" page)
page = get('https://boslive.icai.org/education_content_question_papers.php?p=Education%20Content')
for href, t in links(page):
    if re.search(r'(?i)examiner|comment', t + href):
        out['examiner'].append({'text': t, 'url': href})

json.dump(out, open('sources/p6_sources.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
for k, v in out.items():
    print('==', k, len(v))
    for x in v:
        print('  ', x.get('exam', ''), '|', x['text'][:70], '|', x['url'])

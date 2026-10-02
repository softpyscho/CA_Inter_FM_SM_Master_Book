"""Crawl official ICAI BoS pages and list Intermediate Paper 6 (FM & SM) PDFs.
Only boslive.icai.org pages are followed; only resource.cdn.icai.org / icai.org PDFs are recorded."""
import re, json, sys, html
from urllib.parse import urljoin
import urllib.request, ssl
class _R:
    def __init__(s, t): s.text = t
class _S:
    def get(self, url, headers=None, timeout=40):
        req = urllib.request.Request(url.replace(' ', '%20'), headers=headers or {})
        return _R(urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8', 'replace'))

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36'}
BASE = 'https://boslive.icai.org/'
SEEDS = ['education_content.php?p=Question Papers New Scheme',
         'education_content.php?p=Suggested Answers',
         'education_content.php?p=Previous Year Suggested Answers',
         'education_content_rtp.php',
         'education_content_question_papers.php?p=Education Content',
         'education_content.php?p=MCQs and Case Scenarios Booklet',
         'education_content.php?p=Mock Test Papers']
SKIP = re.compile(r'(?i)foundation|final|schedule|login|contact|about|announcement|facebook|twitter|youtube|instagram|linkedin|koo|old.?scheme|hindi')
KEEP_PAGE = re.compile(r'(?i)intermediate|inter\b|paper|2024|2025|2026|financial|strateg|rtp|question|suggest|examiner|comment|mcq|mock|p_id|c_id|m_id|id=')

seen, pdfs, s = set(), [], _S()
queue = [(urljoin(BASE, u), [], 0) for u in SEEDS]
while queue:
    url, trail, depth = queue.pop(0)
    if url in seen or depth > 4:
        continue
    seen.add(url)
    try:
        r = s.get(url, headers=UA, timeout=40)
    except Exception as e:
        print('ERR', url, e, file=sys.stderr); continue
    title = re.search(r'<h3>(.*?)</h3>', r.text, re.S)
    here = trail + [html.unescape(re.sub(r'\s+', ' ', title.group(1))).strip() if title else url]
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r.text, re.S):
        href, text = m.group(1), html.unescape(re.sub(r'<[^>]+>|\s+', ' ', m.group(2))).strip()
        full = urljoin(url, href.replace(' ', '%20'))
        if full.lower().endswith('.pdf'):
            pdfs.append({'url': full, 'text': text, 'trail': here})
        elif 'boslive.icai.org' in full and not SKIP.search(full + ' ' + text) and KEEP_PAGE.search(full + ' ' + text):
            queue.append((full, here, depth + 1))

json.dump(pdfs, open(sys.argv[1], 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('pages', len(seen), 'pdfs', len(pdfs))


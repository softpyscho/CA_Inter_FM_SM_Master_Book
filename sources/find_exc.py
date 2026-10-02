"""Look for examiners' comments PDFs (Paper 6 / Group II) on ICAI suggested-answer pages."""
import urllib.request, re, html

UA = {'User-Agent': 'Mozilla/5.0 Chrome/126'}
pages = ['https://www.icai.org/post/sugg-ans-inter-' + s for s in ('may2024', 'sep2024', 'jan2025', 'may2025', 'sep2025', 'jan2026', 'may2026')]
for u in pages:
    p = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode('utf-8', 'replace')
    for h, t in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', p):
        t = html.unescape(re.sub(r'<[^>]+>|\s+', ' ', t)).strip()
        if h.lower().endswith('.pdf') and re.search(r'(?i)comment|examiner|group', t + h):
            print(u[-7:], '|', t[:90], '|', h)

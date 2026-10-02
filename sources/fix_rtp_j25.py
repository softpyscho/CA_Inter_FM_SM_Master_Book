"""Find and download the official Paper 6 RTP for January 2025 (the first download picked Paper 1)."""
import urllib.request, re, html, pymupdf

UA = {'User-Agent': 'Mozilla/5.0 Chrome/126'}
u = 'https://www.icai.org/post/rtp-intermediate-course-jan2025'
p = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode('utf-8', 'replace')
links = [(h, html.unescape(re.sub(r'<[^>]+>|\s+', ' ', t)).strip()) for h, t in re.findall(r'<a[^>]+href="([^"]+\.pdf)"[^>]*>([\s\S]*?)</a>', p)]
for h, t in links:
    print(t[:80], '|', h)
for h, t in links:
    data = urllib.request.urlopen(urllib.request.Request(h, headers=UA), timeout=120).read()
    d = pymupdf.open(stream=data, filetype='pdf')
    head = ' '.join(d[0].get_text().split())[:200]
    if re.search(r'(?i)6A\s*:?\s*FINANCIAL MANAGEMENT|PAPER\s*[–-]\s*6', head):
        open('sources/rtp/RTP-J25.pdf', 'wb').write(data)
        open('sources/rtp/RTP-J25.txt', 'w', encoding='utf-8').write(''.join('<<PAGE %d>>\n' % (i + 1) + pg.get_text() for i, pg in enumerate(d)))
        print('SAVED', h, d.page_count, head)
        break

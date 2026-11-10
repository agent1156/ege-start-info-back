import re
import requests
from bs4 import BeautifulSoup

url = 'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=1&cat12=on&cat13=on'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
resp = requests.get(url, headers=headers, timeout=30)

print('STATUS:', resp.status_code)
print('LEN:', len(resp.text))

soup = BeautifulSoup(resp.text, 'html.parser')
print('Всего <tr>:', len(soup.find_all('tr')))
print('Всего td.topicview:', len(soup.find_all('td', class_='topicview')))

with open('debug_page.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)

for i, cell in enumerate(soup.find_all('td', class_='topicview')[:3], 1):
    js = cell.text
    m = re.search(r"document\.write\(\s*changeImageFilePath\('(.*?)'\)\s*\);", js, re.DOTALL)
    print('--- ячейка', i, '---')
    print('match:', bool(m))
    if m:
        print('текст[:100]:', repr(m.group(1)[:100]))
    else:
        print('cell.text[:200]:', repr(js[:200]))

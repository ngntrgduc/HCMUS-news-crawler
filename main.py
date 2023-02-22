from bs4 import BeautifulSoup as bs
from pathlib import Path
import requests
import re
import datetime

page = requests.get("https://www.hcmus.edu.vn/sinh-vien")
soup = bs(page.content, 'lxml')

news = [i.text for i in soup.find_all(class_='mod-articles-category-title')]
news_link = [i.attrs['href'] for i in soup.find_all(class_='mod-articles-category-title')]
links = [''.join(url) for url in news_link]

raw_dates = [i.text for i in soup.find_all(class_='mod-articles-category-date')]
dates = [''.join(re.findall('([\d-])', date)) for date in raw_dates]

content = ''
for i in range(10):
    # print(f'- {dates[i]}: {news[i]}, Link: https://www.hcmus.edu.vn{links[i]}')
    content += f'- {dates[i]}: {news[i]}, Link: https://www.hcmus.edu.vn{links[i]}\n'

with open('crawled.txt', 'w', encoding='utf-8') as f:
    f.write(content)
f.close()
from bs4 import BeautifulSoup as bs
from pathlib import Path
import requests
import re

page = requests.get("https://www.hcmus.edu.vn/sinh-vien")
soup = bs(page.content, features="lxml")

news = [i.text for i in soup.find_all(class_='mod-articles-category-title')]
news_link = [i.attrs['href'] for i in soup.find_all(class_='mod-articles-category-title')]
links = [''.join(url) for url in news_link]

raw_dates = [i.text for i in soup.find_all(class_='mod-articles-category-date')]
dates = [''.join(re.findall('([\d-])', date)) for date in raw_dates]

ctkt = [i for i in soup.find_all(class_='feed-link')]
thong_bao_ctkt = [''.join(re.sub(r'(\t|\n)', '', news.text)) for news in ctkt]
ctkt_link = [''.join(re.findall('http.*" ', str(news))) for news in ctkt]

thong_bao = ['Các thông báo về Đào Tạo', 'Các thông báo về Công tác sinh viên', 'Thông báo khác', 'Các thông báo về Khảo thí']
index = count = 0
file = Path('README.md').rename(Path('README.md').with_suffix('.txt'))
with open(file, 'w', encoding='utf-8') as f:
    for i in range(len(dates)):
        if count == 0:
            f.write(f'### {thong_bao[index]}\n')
            index += 1
        count += 1
        if count == 15:
            count = 0
        f.write(f' - {dates[i]}: [{news[i]}](https://www.hcmus.edu.vn{links[i]})\n')
    
    f.write(f'### {thong_bao[index]}\n')
    rule_position = [5, 10, 13]
    for i in range(len(thong_bao_ctkt)):
        if i in rule_position:
            f.writelines(f'---\n - [{thong_bao_ctkt[i]}]({ctkt_link[i][:-2]})\n') # [:-2] to remove unnecessary characters (" )
        else:    
            f.writelines(f' - [{thong_bao_ctkt[i]}]({ctkt_link[i][:-2]})\n')
f.close()

readme = Path('README.txt')
readme.rename(readme.with_suffix('.md'))

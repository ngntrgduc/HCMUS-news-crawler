from bs4 import BeautifulSoup as bs
import requests
import os
from dotenv import load_dotenv

load_dotenv()
USER_AGENT = os.getenv('USER_AGENT')

def remove_year(date):
    return date.rsplit('/', 1)[0]

limit = 5  # Chỉ lấy 5 tin tức mới nhất

page = requests.get('https://hcmus.edu.vn/tin-tuc/', headers={'User-Agent': USER_AGENT})
soup = bs(page.content, features='lxml')
news = [_ for _ in soup.find_all(class_='cmsmasters_post_title entry-title')]
dates = [_.text for _ in soup.find_all(class_='published')]

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(f'### Tin tức\n')
    for date, new in list(zip(dates, news))[:limit]:        
        link = new.find('a')['href']
        f.write(f" - **{remove_year(date)}**: [{new.text}]({link})\n")

# Khảo thí và đảm bảo chất lượng
page = requests.get('http://ktdbcl.hcmus.edu.vn', headers={'User-Agent': USER_AGENT})
soup = bs(page.content, features='lxml')
modules = [_ for _ in soup.find_all(class_='category-module')]
categories = ['Thông báo', 'Lịch thi', 'Kết quả thi', 'Kết quả phúc khảo']

with open('README.md', 'a', encoding='utf-8') as f:
    f.write(f'\n### Thông báo Phòng Khảo thí và Đảm bảo Chất lượng\n')
    for i, cat in enumerate(modules):
        f.write(f'\n#### {categories[i]}\n')
        for li in cat.find_all('li')[:limit]:
            a_tag = li.find('a', {'class': 'mod-articles-category-title'})
            title = a_tag.text.strip()
            href = a_tag['href'].strip()

            raw_date = li.find(class_='mod-articles-category-date').text
            date = remove_year(raw_date.replace('\t', '').replace('\n', '')[1:-1])

            link = f'http://ktdbcl.hcmus.edu.vn{href}'
            f.write(f' - **{date}**: [{title}]({link})\n')

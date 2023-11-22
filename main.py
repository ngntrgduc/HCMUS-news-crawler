from bs4 import BeautifulSoup as bs
import requests

page = requests.get('https://hcmus.edu.vn/tin-tuc/')
soup = bs(page.content, features='lxml')

news = [i for i in soup.find_all(class_='cmsmasters_post_title entry-title')]
dates = [i.text for i in soup.find_all(class_='published')]

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(f'### Tin tức\n')
    for date, new in zip(dates, news):
        date = '/'.join(date.split('/')[:2])    # reformat date: remove year
        link = new.find('a')['href']
        f.write(f" - **{date}**: [{new.text}]({link})\n")

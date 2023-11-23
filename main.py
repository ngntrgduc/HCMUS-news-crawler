from bs4 import BeautifulSoup as bs
import requests

page = requests.get('https://hcmus.edu.vn/tin-tuc/')
soup = bs(page.content, features='lxml')

news = [i for i in soup.find_all(class_='cmsmasters_post_title entry-title')]
dates = [i.text for i in soup.find_all(class_='published')]

def remove_year(date):
    return '/'.join(date.split('/')[:2])

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(f'### Tin tức\n')
    for i, (date, new) in enumerate(zip(dates, news)):
        # Chỉ lấy 5 tin tức mới nhất
        if i < 5:
            link = new.find('a')['href']
            f.write(f" - **{remove_year(date)}**: [{new.text}]({link})\n")


# Khảo thí và đảm bảo chất lượng
page = requests.get('http://ktdbcl.hcmus.edu.vn')
soup = bs(page.content, features='lxml')

news = [i for i in soup.find_all(class_='mod-articles-category-title')]
dates = [i.text for i in soup.find_all(class_='mod-articles-category-date')]
thong_bao = ['Thông báo', 'Lịch thi', 'Kết quả thi', 'Kết quả phúc khảo']
index = 0

def in_range(i, n=5):
    # Chỉ lấy 5 tin tức mới nhất của mỗi mục
    return (i < n) or \
           (i >= 15 and i < 15 + n) or \
           (i >= 35 and i < 35 + n) or \
           (i >= 55 and i < 55 + n)

with open('README.md', 'a', encoding='utf-8') as f:
    f.write(f'\n### Thông báo Phòng Khảo thí và Đảm bảo Chất lượng\n')
    for i, (date, new) in enumerate(zip(dates, news)):
        # Thông báo sẽ có 15 mục, còn lại sẽ là 20 mục
        if i == 0 or (i + 5) % 20 == 0:
            f.write(f'\n#### {thong_bao[index]}\n')
            index += 1 

        if in_range(i):
            date = remove_year(date.replace('\t', '').replace('\n', '')[1:-1])
            link = f"http://ktdbcl.hcmus.edu.vn{new['href']}"
            f.write(f" - **{date}**: [{new.text.strip()}]({link})\n")

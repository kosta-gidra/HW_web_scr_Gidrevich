from bs4 import BeautifulSoup
import requests

KEYWORDS = ['лет', 'gitlab', 'разработчик', 'web']
HEADERS = {'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
           'sec-ch-ua-mobile': '?0',
           'Sec-Fetch-Dest': 'document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'same-origin',
           'Sec-Fetch-User': '?1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
base_url = 'https://habr.com'
url = base_url + '/ru/all/'
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')
posts = soup.find_all('article')
for post in posts:
    body = post.find(class_='tm-article-body tm-article-snippet__lead')
    text = body.text.lower().split()
    result = set(text).intersection(set(KEYWORDS))
    if result != set():
        date = post.find(class_='tm-article-snippet__datetime-published')
        head = post.find(class_='tm-article-snippet__title tm-article-snippet__title_h2')
        link = post.find(class_='tm-article-snippet__title-link')
        print(f'Совпадение в preview по {result}')
        print(f'{date.text}, "{head.text}", {base_url+link.attrs["href"]}')
        print()
    else:
        link = post.find(class_='tm-article-snippet__title-link')
        url = base_url+link.attrs["href"]
        response_article = requests.get(url, headers=HEADERS)
        soup_article = BeautifulSoup(response_article.text, 'html.parser')
        post_article = soup_article.find(id='post-content-body')
        text_article = post_article.text.lower().split()
        result = set(text_article).intersection(set(KEYWORDS))
        if result != set():
            date0 = soup_article.find(class_='tm-article-snippet__datetime-published')
            head = post.find(class_='tm-article-snippet__title tm-article-snippet__title_h2')
            link = post.find(class_='tm-article-snippet__title-link')
            print(f'Совпадение в теле статьи по {result}')
            print(f'{date0.text}, "{head.text}", {base_url+link.attrs["href"]}')
            print()

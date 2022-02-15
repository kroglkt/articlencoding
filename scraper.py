import requests
from bs4 import BeautifulSoup

def get_content(url):
    #Returns body and header

    if "berlingske" in url:
        return get_berlingske_content(url)
    else:
        return get_bt_content(url)

def get_berlingske_content(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    header_html = soup.find_all('h1', class_="article-header__title")
    intro_html = soup.find_all('p', class_="article-header__intro")
    
    body_html = soup.find_all(class_="article-body")[0].find_all('p', text=True, recursive=False)

    temp_intro = intro_html[0].text
    temp_body = [x.text for x in body_html]
    body = temp_intro + ' '.join(temp_body)

    header = header_html[0].text

    return body.strip(), header.strip()

def get_bt_content(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    header_html = soup.find_all('h1', class_="article-title")
    intro_html = soup.find_all('p', class_="article-summary")
    body_html = soup.find_all(class_="article-content")[0].find_all(text=True, recursive=False)

    temp_intro = intro_html[0].text
    body = temp_intro + ' '.join(body_html)
    header = header_html[0].text

    return body.strip(), header.strip()

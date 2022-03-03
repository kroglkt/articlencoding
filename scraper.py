import requests
from bs4 import BeautifulSoup
import SeleniumScraper

def get_content(url):
    #Returns body and header

    if "bt.dk" in url:
        return get_bt_content(url)
    else:
        return get_berlingske_content(url)

def get_berlingske_content(url):
    h, b, a = SeleniumScraper.get_content(url)
    return h, b, a

def get_bt_content(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    header_html = soup.find_all('h1', class_="article-title")
    intro_html = soup.find_all('p', class_="article-summary")
    body_html = soup.find_all(class_="article-content")[0].find_all(text=True, recursive=False)

    temp_intro = intro_html[0].text
    body = temp_intro + ' '.join(body_html)
    header = header_html[0].text

    #Don't waste time with author on this one.
    return header.strip(), body.strip(), '404'

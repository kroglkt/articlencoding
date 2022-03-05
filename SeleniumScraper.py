from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse
import bs4
import re

driverService = Service('C:/Users/nisse/Downloads/chromedriver.exe')

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

with open('data/additional/author_filter.txt', encoding='utf-8') as f:
    lst = f.read()
    lst = lst.split('\n')

author_filter = lst

class DomainClasses:
    def __init__(self, body, header, intro, author, author_fb, _404, _404_text, by_=By.CLASS_NAME):
        self.body = body
        self.header = header
        self.intro = intro
        self.author = author
        self.author_fb = author_fb
        self._404 = _404
        self._404_text = _404_text
        
        self.by_ = by_
        
        self.use_soup_body = False
        self.remove_author = False

def element_present(driver, classname, by_):
    if len(driver.find_elements(by_, classname))>0:
        return True
    return False

def soup_text(driver, class_):
    #Get inner HTML from div
    html = driver.find_element(By.CLASS_NAME, class_).get_attribute('innerHTML')
    #Parse with BS4
    soup = bs4.BeautifulSoup(html, 'html.parser')
    #Remove excessive line breaks and whitespaces.
    body =  re.sub(r'\n\s*\n', '\n\n', soup.text)
    return re.sub(" +", " ", body)

def isolate_authors(element):
    if type(element) == str:
        return element

    if len(element) == 1:
        return element[0].text

    a_string = [x.text.title() for x in element]
    return '|'.join(a_string)

def remove_author_from_start(text, author):
    reg_author = re.compile(re.escape(author), re.IGNORECASE)
    if not reg_author.search(text[:100]):
        return text

    split = text.split('\n')
    for i, s in enumerate(split):
        if reg_author.search(s):
            return '\n'.join(split[i+1:])
            

def who_is_author(authors):
    #Remove non-names from author list, if multiple authors.
    names = []
    not_names = []
    for name in authors:
        if any(ele.lower() in name.lower() for ele in author_filter):
            not_names.append(name)
        elif len(name.split()) > 1:
            names.append(name)
        else:
            not_names.append(name)

    if len(names) == 1:
        print("Non-names:", not_names)
        return names[0].title()
    else:
        print("Multiple authors:", names)
        return names

def is_404(driver, domain):
    if element_present(driver, domain._404, By.CLASS_NAME):
        txt = driver.find_element(By.CLASS_NAME, domain._404).text
        if  txt.split('\n')[0] == domain._404_text:
            return True
    return False
    

def get_content(url):
    #b, i, h, a = body, intro, header, author
    driver = webdriver.Chrome(options=options, service=driverService)
    driver.get(url)

    domain = domains[urlparse(url).netloc]

    if is_404(driver, domain):
        driver.quit()
        return '404', '404', '404'

    if not domain.use_soup_body:
        b = driver.find_element(By.CLASS_NAME, domain.body)
        b = b.text
    else:
        b = soup_text(driver, domain.body)

    if domain.intro != 'NONE':
        i = driver.find_element(By.CLASS_NAME, domain.intro)
        i = i.text
    else:
        i = ''

        
    h = driver.find_element(By.CLASS_NAME, domain.header)

    if element_present(driver, domain.author, domain.by_):
        a = driver.find_elements(domain.by_, domain.author)
    elif domain.author_fb == 'NONE':
            a = 'Unknown'
    elif element_present(driver, domain.author_fb, domain.by_):
        a = driver.find_elements(domain.by_, domain.author_fb)
    else:
        print(url, "No author!")
        a = "Unknown"
    if a == '':
        a = soup_text(driver, domain.author)

    
    h = h.text
    a = isolate_authors(a)
    a = a.strip()

    if domain.remove_author:
        b = remove_author_from_start(b, a)
    
    a = list(filter(None, re.split('\n|\||•|,|&',a))) #Split authors

    if len(a) > 1:
        a = who_is_author(a)
    else:
        a = a[0].title()

    driver.quit()
    
    return h.strip(), i.strip()+"\n"+b.strip(), a

domains = {
    'www.berlingske.dk' : DomainClasses('article-body', 'article-header__title',
                                        'article-header__intro', 'article-byline__author-item',
                                    'article-byline__freetext.font-g1', 'col-md-12.text-center',
                                        'Siden ikke fundet'),
    
    'ekstrabladet.dk' : DomainClasses('article-bodytext', 'art-title', 'art-subtitle',
                                         'byline-authors', 'byline-container','error-wrap',
                                      'Beklager! – der er sket en fejl',
                                      by_=By.ID),
    'www.bt.dk' : DomainClasses('article-content', "article-title", "NONE",
                                "author-name", 'author-byline', 'container-404', '404 - Siden ikke fundet'),
    }

domains['ekstrabladet.dk'].use_soup_body = True
domains['www.bt.dk'].remove_author = True
domains['www.bt.dk'].use_soup_body = True

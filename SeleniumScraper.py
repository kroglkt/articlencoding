from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

driverService = Service('C:/Users/nisse/Downloads/chromedriver.exe')

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")



def get_content(url):
    driver = webdriver.Chrome(options=options, service=driverService)
    driver.get(url)
    b = driver.find_element(By.CLASS_NAME, 'article-body')
    i = driver.find_element(By.CLASS_NAME, 'article-header__intro')
    h = driver.find_element(By.CLASS_NAME, 'article-header__title')
    b = b.text
    h = h.text
    i = i.text
    driver.quit()
    
    return h.strip(), i.strip()+b.strip()

def quit_driver():
    driver.quit()

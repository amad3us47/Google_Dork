from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)



# Query to obtain links
query = 'comprehensive guide to web scraping in python'
links = [] # Initiate empty list to capture final results# Specify number of pages on google search, each page contains 10 #links
n_pages = 20 
for page in range(1, n_pages):
    url = "http://www.google.com/search?q=" + query + "&start=" +      str((page - 1) * 10)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # soup = BeautifulSoup(r.text, 'html.parser')

    search = soup.find_all('div', class_="yuRUbf")
    for h in search:
        links.append(h.a.get('href'))




search = soup.find_all('div', class_="yuRUbf")


for h in search:
        links.append(h.a.get('href'))

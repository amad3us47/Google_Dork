from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Define chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in background
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize driver with the correct syntax
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Query to obtain links
query = 'comprehensive guide to web scraping in python'
links = []  # Initiate empty list to capture final results

# Specify number of pages on google search, each page contains 10 links
n_pages = 20 

for page in range(1, n_pages):
    url = "http://www.google.com/search?q=" + query + "&start=" + str((page - 1) * 10)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    search = soup.find_all('div', class_="yuRUbf")
    for h in search:
        links.append(h.a.get('href'))

# Close the driver when done
driver.quit()

# Print results
print(f"Found {len(links)} links")

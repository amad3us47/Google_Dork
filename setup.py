import requests
from bs4 import BeautifulSoup
import argparse

# Base Url
BASE_URL = "https://www.exploit-db.com/ghdb/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

def url_parse(page_num):
    """Generate URL for exploit-db GHDB page"""
    return BASE_URL + str(page_num)

def start(url,domain):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', class_='external')
        
        if links:
            for link in links:
                text = link.get_text(strip=True)
            ## Google search
                print(f"site:{domain}" +" "+text)

        else:
            print("No links found")
            
    except Exception as e:
        print(f"Error: {e}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Hacking Dorks")
    parser.add_argument('-d','--domain',required=True,help='python run -d example.com)')
    args = parser.parse_args()
    # Scrape a specific page
    #start(url_parse(1000))  # Scrape page 1
    for x in range(1,10000):
        start(url_parse(x),args.domain)

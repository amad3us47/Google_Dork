from dork_scrap import url_parse, start
from google_scrap import google_search
import argparse


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Google Hacking Dorks")
    parser.add_argument('-d','--domain',required=True,help='python run -d example.com)')
    args = parser.parse_args()
    for x in range(1, 8000):
        dorks = start(url_parse(x), args.domain)  # get dorks from exploit-db
        for dork in dorks:
            google_search(dork)              # search each dork on google

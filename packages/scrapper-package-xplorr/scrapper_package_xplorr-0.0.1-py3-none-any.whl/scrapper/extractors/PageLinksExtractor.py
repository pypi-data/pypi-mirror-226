import sys
sys.path.insert(0, '../core')

from urllib import request
from scrapper.core.AbstractScrap import DataScrap
import os
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests

class PageLinksExtractor(DataScrap):   

    def __init__(self):
        self.pageURL = ""
        self.headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

    def extract(self):
        productLinks = []
        r = requests.get(self.pageURL, verify=False, headers = self.headers)

        soup = BeautifulSoup(r.content, 'html.parser')
        tags = soup.find("form", id="advanced_search_form").findNextSiblings()
        for tag in tags:
            if 'columns' in tag['class']:
                #All products
                for child in tag.children:
                    if type(child)!=NavigableString:
                        product = child.find_all("div", class_="columns")[0]
                        productImage = product.find_all("div", recursive=False)[0]
                        productPageURL = productImage.find("a")["href"].strip()
                        #print("Link: ", productPageURL)
                        productLinks.append(os.environ['HOST'] + productPageURL)
        
        return productLinks
    
    def output(self):
        print("")
    
    def run(self, URL):
        self.pageURL = URL
        return self.extract()
    
    def next(self):
        print("")
import sys
sys.path.insert(0, '../core')

from urllib import request
from scrapper.core.AbstractScrap import DataScrap
import os
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests

class NxtPageExtractor(DataScrap):
    def __init__(self):
        self.headers = os.environs.headers

    def extract(self):
        productLinks = []
        while(True):
            r = requests.get(pageURL, verify=False, headers = self.headers)
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
                            productLinks.append(productPageURL)
        
        return productLinks
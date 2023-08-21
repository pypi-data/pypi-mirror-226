import sys
sys.path.insert(0, '../core')

from urllib import request
from scrapper.core.AbstractScrap import DataScrap
import os
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests

class PageProductExtractor(DataScrap):    

    def __init__(self):
        self.headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
        self.pageURL = ""

    def extract(self):
        r = requests.get(self.pageURL, verify=False, headers = self.headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        product_section = soup.find("section", class_= "section mainbody")
        product_div = product_section.find_all("div", class_="columns")
        image_tag = product_div[1].children
        for child in image_tag:
            if type(child)!=NavigableString:
                image_url = child.find("a", id="detailsPrimaryImage")
                if  image_url!=None: 
                    print(image_url["href"].strip())
                else:
                    product_title = child.find("h1", class_="title").contents[0]
                    print(product_title.string.strip())

                    product_details_div = child.find("div", class_="product-details-specifications-container")
                    product_details_table_tr = product_details_div.find("table").find_all("tr")
                    for tr in product_details_table_tr:
                        td_tag = tr.find_all("td")
                        print(td_tag[0].string, td_tag[1].string)
    def output(self):
        print("")
    
    def run(self, pageURL):
        self.pageURL = pageURL
        self.extract()
    
    def next(self):
        print("")
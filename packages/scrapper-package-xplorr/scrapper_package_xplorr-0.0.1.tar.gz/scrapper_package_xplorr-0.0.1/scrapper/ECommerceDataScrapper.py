from scrapper.core.AbstractScrap import DataScrap
from scrapper.extractors.PageLinksExtractor import PageLinksExtractor
from scrapper.extractors.PageProductExtractor import PageProductExtractor
import json
import os
import multiprocessing

class ECommerceDataScrapper:
    def __init__(self, pageLinksExtractor, nxtPageExtractor, pageProductExtractor):
        self.pageLinksExtractor = pageLinksExtractor
        self.nxtPageExtractor = nxtPageExtractor
        self.pageProductExtractor = pageProductExtractor
        self.startURL = os.environ["STARTURL"]
        self.pageCountPath = os.environ["PAGECOUNTPATH"]
        self.pageCount = int(os.environ["PAGECOUNT"])
        self.headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

    def run(self):
        pool = multiprocessing.Pool()
        while self.pageCount!=2:
            print("Running..-2")
            #extract retrieve all product page urls from the current page
            #iterate over each product page and extract product information
            self.pageLinksExtractor.headers = self.headers
            self.pageLinksExtractor.pageURL = self.startURL + self.pageCountPath + str(self.pageCount)           

            pageProductLinks = self.pageLinksExtractor.extract()
            
            # for link in pageProductLinks:
            #     self.pageProductExtractor.pageURL = os.environ['HOST'] + link            
            pool.map_async(self.pageProductExtractor.run, pageProductLinks)
            self.pageCount+=1
            
        pool.close()
        pool.join()

    # def output(self):
    #     print("")
    
    # def next(self):
    #     print("")

    # def extract(self):
    #     print("")
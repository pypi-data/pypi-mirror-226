import json
import os

from extractors.PageLinksExtractor import PageLinksExtractor
from extractors.PageProductExtractor import PageProductExtractor
from ECommerceDataScrapper import ECommerceDataScrapper

if __name__ == '__main__':
  with open('config.json', 'r') as f:
    config = json.load(f)

  for key in config:
      os.environ[key] = config[key].lower()

  scrapper = ECommerceDataScrapper(PageLinksExtractor(), None, pageProductExtractor=PageProductExtractor())
  scrapper.run()
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests

host = "https://www.exoticindiaart.com"
headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

start_url = "https://www.exoticindiaart.com/find?groups=&q=art&"
page_count_path = "pagecount="
page_count = 1

while(True):
    #Current Page extraction
    r = requests.get(start_url +  page_count_path + str(page_count),
    verify=False, headers = headers)
    if r.url==start_url:
        print("Done")
        break

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
                    print(productPageURL)
    
    page_count+=1
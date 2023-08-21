from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import sys


host = "https://www.exoticindiaart.com"
headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

start_url = "https://www.exoticindiaart.com/find?groups=&q=art&"
page_count_path = "pagecount="
page_count = 1

def retrieveReviewsFromPage():
    r = requests.get("https://www.exoticindiaart.com/product/paintings/lord-shiva-family-tanjore-painting-traditional-colors-with-24k-gold-teakwood-frame-gold-wood-paa501/", verify=False, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    f = open("test.txt", "a", encoding="utf-8")
    f.write(soup.prettify())
    f.close()
    
def retrieveFromProductPage(product_page_url):
    r = requests.get(product_page_url, verify=False, headers = headers)
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
                sys.exit()
            

# while(True):
#     r = requests.get(start_url +  page_count_path + str(page_count),
#     verify=False, headers = headers)
#     if r.url==start_url:
#         print("Done")
#         break

#     soup = BeautifulSoup(r.content, 'html.parser')
#     tags = soup.find("form", id="advanced_search_form").findNextSiblings()
#     for tag in tags:
#         if 'columns' in tag['class']:
#             #All products
#             for child in tag.children:
#                 if type(child)!=NavigableString:
#                     product = child.find_all("div", class_="columns")[0]
#                     productImage = product.find_all("div", recursive=False)[0]
#                     productPageURL = productImage.find("a")["href"].strip()
#                     retrieveFromProductPage(host + productPageURL)
    
#     page_count+=1

retrieveReviewsFromPage()
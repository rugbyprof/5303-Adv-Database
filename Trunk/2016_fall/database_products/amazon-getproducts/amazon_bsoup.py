from mechanize import Browser
from bs4 import BeautifulSoup as BS
import json
import random
from time import sleep
 
br = Browser()
 
# Browser options
# Ignore robots.txt. Do not do this without thought and consideration.
br.set_handle_robots(False)
 
# Don't add Referer (sic) header
br.set_handle_referer(False)
 
# Don't handle Refresh redirections
br.set_handle_refresh(False)
 
#Setting the user agent as firefox
br.addheaders = [('User-agent', 'Firefox')]
 

categorys = ["tablet","ipad","camera","smartphone","laptop","desktop%20computer","game%20console"]

for cat in categorys:
    print(cat)
    for i in range(35):
        # url = "https://www.amazon.com/s/ref=sr_pg_"+str(i)+"?rh=i%3Aaps%2Ck%3Aipad&page=2&keywords="++"&ie=UTF8"
        # url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Dtoys-and-games&field-keywords=game+console
        # url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Delectronics&field-keywords=game+console&rh=n%3A172282%2Ck%3Agame+console"
        url = "https://www.amazon.com/s/ref=sr_pg_2?rh=n%3A172282%2Ck%3Agame+console&page="+str(i)+"&keywords="+cat+"&ie=UTF8&qid=1468512945&spIA=B019DJYJ1E,B01F9FOMLS,B01BT6N8SO"
        sleeptime = random.random() * 3
        sleep(sleeptime)
        print("sleeping: ",sleeptime)
        br.open(url)
        # br.open('http://www.amazon.in/')
        # br.select_form(name="site-search")
        # br['field-keywords'] = "Ipad"
        #br.submit()
        
        #Getting the response in beautifulsoup
        soup = BS(br.response().read(), "html5lib")
            
        items = []


        for li in soup.find_all('li', class_="s-result-item"):
            asin = li['data-asin']
            temp = li.find_all('span',{"class":"a-color-price"})

            if(len(temp) > 0):
            
                if not temp[0] == '$':

                    items.append({})
                    items[-1]['asin'] = asin
                    items[-1]['price'] = li.find_all('span',{"class":"a-color-price"})
                    print(items[-1]['price'][0].string)

                    items[-1]['category'] = cat
                    items[-1]['h2'] = li.find_all('h2')
                    items[-1]['h2'] = items[-1]['h2'][0].string

                    items[-1]['price'] = items[-1]['price'][0].string

                    if li.img.has_attr("srcset"):
                        items[-1]['imgs'] = li.img['srcset']
                        items[-1]['imgs'] = items[-1]['imgs'].split(',')

            

        f = open('products_big.json', 'a')
        f.write(json.dumps(items,sort_keys=True,indent=4, separators=(',', ': ')))
        f.close();
        print(i)


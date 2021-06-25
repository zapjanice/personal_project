'''Code to scrape prefecture, link to page and flavor from starbucks jimoto_frappucino site.
Please see the url below for more information'''

import requests
import time
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup

base = "https://www.starbucks.co.jp"
url = base + "/cafe/jimoto_frappuccino/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

'''Code to get data and put into a list'''
items = []
for item in soup.find("ul", class_="_list").find_all("li"):
    prefecture = item.find("a").select('img')[0]['alt']
    end_link = item.find("a").get('href')
    link = base+end_link
    response_2 = requests.get(link)
    soup_2 = BeautifulSoup(response_2.content, "html.parser")
    flavor = soup_2.find("p", class_="_t2").text
    img_link = item.find('img', src=True)
    img_link = base + (img_link["src"].split("src=")[-1])   
    items.append({'prefecture': prefecture, 'flavor': flavor, 'link': link, 'img_link':img_link})
    
    timestamp = time.asctime() 
    txt = open(f'{prefecture}.png', "wb")
    download_img = urllib.request.urlopen(img_link)
    txt.write(download_img.read())
    txt.close()      

'''Using pandas to clean data'''
df = pd.DataFrame(items)
df['prefecture'] = df['prefecture'].replace({'#': ''},regex=True)
df['prefecture'] = df['prefecture'].str.replace('\d+', '', regex=True)
df['prefecture'] = df['prefecture'].str.lstrip()
df.to_csv('starbucks_jimoto.csv', index=False)

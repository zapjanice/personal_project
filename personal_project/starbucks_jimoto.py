'''Code to scrape prefecture, link to page and flavor from starbucks jimoto_frappucino site.
Please see the url below for more information'''

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.starbucks.co.jp/cafe/jimoto_frappuccino/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

'''Code to get data and put into a list'''
items = []
for item in soup.find("ul", class_="_list").find_all("li"):
    prefecture = item.find("a").select('img')[0]['alt']
    end_link = item.find("a").get('href')
    link = "https://www.starbucks.co.jp"+end_link
    response_2 = requests.get(link)
    soup_2 = BeautifulSoup(response_2.content, "html.parser")
    flavor = soup_2.find("p", class_="_t2").text
    items.append({'prefecture': prefecture, 'flavor': flavor, 'link': link})

'''Using pandas to clean data'''
df = pd.DataFrame(items)
df['prefecture'] = df['prefecture'].replace({'#': ''},regex=True)
df['prefecture'] = df['prefecture'].str.replace('\d+', '')

df.to_csv('starbucks_jimoto.csv', index=False)

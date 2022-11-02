import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import time
import selenium


df = pd.read_csv('puddding.csv')
urls = df['url'].tolist()

def cleanup(tuple):
    #cleanup html to text and remove unneeded characters
    list = []
    for element in tuple:
        if element is None:
            list.append("null")
        else:
            #print(element)
            if type(element) is str:
                list.append(element.strip().replace(" " , "").replace("\n", "").replace("\r", "").replace("Tel:","").replace("Email:",""))
            else:
                #print(element)
                object = element.text.strip()

                object = object.replace("\n", "").replace("\r", "")
                #object = element.text.strip.replace(" " , " ").replace("\n", "").replace("\r", "")#
                list.append(object)

    return(list)




#urls = ['https://puddding.com/raven5.com','https://puddding.com/ghagency.com', 'https://puddding.com/epikso.com', 'https://puddding.com/skybounddigital.com']
scraped = []
for url in urls:
    page = re.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    Firm = soup.find('h3')
    URL = soup.select_one('div', class_='caption')
    #for link in URL.select('div.caption a[href]'):
    #    print(link['href'])
    #for link in URL.select('div.caption span[href]'):
    #    print(link['href'])
    try:
        try:
            urltype1 = URL.select('div.caption a[href]')[0]
            newurl = urltype1
        except:
            urltype2 = URL.select('div.caption span[href]')[0]
            newurl = urltype2
        try:
            newurl = newurl['href']
        except:
            newurl='null'
    except:
        newurl='null'
    print(newurl)
    #print(URL.text)
    #URL = URL.select('div')
    data = (Firm, newurl, url)
    data = cleanup(data)
    scraped.append(data)

#print(scraped)
df = pd.DataFrame(scraped, columns=["Firm", "URL","Source"])

df.to_csv('puddding.csv', encoding='utf-8-sig', index=False)
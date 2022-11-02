import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import time

#This is for website https://www.tourism-review.org/list-tour-operators-and-tour-companies/674?, many pages of data


def pagefetch(page):
    try:
        links = []
        site = re.get(page)
        soupy = BeautifulSoup(site.content, 'html.parser')
        #firmlist = soupy.find('div', class_="wrap")
        url = soupy.find_all('a', class_="list-box", href=True)
        #print(url)
        for link in url:
            links.append(link['href'])
            time.sleep(0.2)
        return(links)
    except:
        print("Whoops")

def scrape(links, source):
    values = []
    for k in range(len(links)):

        #print("Link!", links[k])
        link = links[k]
        site = re.get(link)
        sitesoup = BeautifulSoup(site.content, 'html.parser')
        Firm = sitesoup.find('h1')
        parentelement = sitesoup.find('div', class_="list-box")
        if parentelement is None:
            Sector ='null'
            URL = 'null'
            Telephone = 'null'
        else:
            try:
                Sector = parentelement.select_one('p')
            except:
                Sector = 'null'
            try:
                URL = parentelement.find('a', href=True)
            except:
                URL = 'null'
            try:
                Telephone = parentelement.find('div', class_="company")
                try:
                    Telephone = Telephone('p')[1]
                except:
                    Telephone = 'null'
            except:
                Telephone = 'null'
        #print(Telephone)
        value = [Firm, URL, Telephone, Sector]
        value = cleanup(value)
        value.append(source) # [Firm, Url, Telephone, Sector, Source]
        values.append(value)
        #print(value)
        time.sleep(0.2)
    return(values)

def cleanup(tuple):
    #cleanup html to text and remove unneeded characters
    list = []
    for element in tuple:
        if element is None:
            list.append("null")
        else:
            #print(element)
            if type(element) is str:
                list.append(element.strip().replace(" " , "").replace("\n", "").replace("\r", "").replace("Phone:",""))
            else:
                #print(element)
                object = element.text.strip()

                object = object.replace("\n", "").replace("\r", "")
                #object = element.text.strip.replace(" " , " ").replace("\n", "").replace("\r", "")#
                list.append(object)

    return(list)

test=scrape(['https://www.tourism-review.org/list-tour-operators-and-tour-companies/czech-health-spa-6183'], "source")
print(test)
finaldata = []
columnlist = ["Firm", "URL", "Telephone Number", "Business Sector 1", "Source"]

# Doesn't properly scrape firm's website URL, error in scraping at 241st page
try:
    for c in range(1,674,1):
        print("Now on loop: ", c)
        source = 'https://www.tourism-review.org/list-tour-operators-and-tour-companies/'+str(c)+'?'
        firms = pagefetch(source)
        #print(firms)
        output = scrape(firms, source)
        #print(output)
        finaldata.append(output)
except:
    print("Erorr in scraping, saving what is scraped so far, if there is a further error here review output code")
    compiledata = []
    for data in finaldata:
        for object in data:
            compiledata.append(object)
    df = pd.DataFrame(compiledata, columns=columnlist)
    df.to_csv('tourism_review.csv', encoding='utf-8-sig', index=False)
    print("Total volume of scraped data so far is: ", len(df))
try:
    compiledata = []
    for data in finaldata:
        for object in data:
            compiledata.append(object)
    df = pd.DataFrame(compiledata, columns=columnlist)
    df.to_csv('tourism_review.csv', encoding='utf-8-sig', index=False)
    print("Total volume of scraped data is: ", len(df))
except:
    print("Error in saving csv")
    print(compiledata)
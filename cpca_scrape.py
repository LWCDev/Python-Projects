import requests as req
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


#For the website https://www.cpca-rpc.ca/counsellor-directory.aspx
#start = input("Do you want to run the scaper? Press Enter to start")
#should hopefully return a list of soups which can be used by beautiful soup

#driver = webdriver.Chrome("C:\\Users\\lewis.welshclark\\chromium\\chromedriver.exe", ptions=options)

#Accepts a single soup object and a source (nothing is perfomed on the source), scraping the soup, so it can return an array/tuple containing the data
#This soup is obtained through selenium for each webpage individually as the webpage hides the email behind a javascript event which is removed when the page is loaded within a browser
def attribute_scraper(link, source):
    pattern = re.compile(r'\.val\("([^@]+@[^@]+\.[^@]+)"\);', re.MULTILINE | re.DOTALL)
    #site = re.get(link)
    #soupy = BeautifulSoup(site.content, 'lxml')
    soupy = link
    ContactInfo = soupy.find('div', class_="links")
    #print(ContactInfo)
    Email = 'null'
    try:
        URL = soupy.find('a', {'target': '_blank'})
        URL = URL['href']
    except:
        URL = 'null'
    try:
        #print("10")
        soup = soupy
        #print(soup.prettify())
        script = soup.find_all("p")
        for item in script:
            check = item.find('a')
            if check:
                href = check['href']
                if 'mailto:' in href:
                    Email = href
                    #print(Email)
                    break
    except Exception as e:
        print("Exception, ", e)
        Email = 'null'
    try:
        Firm = soupy.find('h5')
    except:
        Firm = 'null'
    #Email = 'null'
    return(Email, URL, Firm, source) #Email Address, URL, Firm, Source

#Use case: website with multiple elements and links per page, but only one link that you need within each element
#link_fetch returns a list of URLs of separate firm pages hosted on the host site that contain contact information etc. which we can scrape


#Returns clean, non-html versions of the data which is ready for saving
def html_clean(in_tuple):
    # cleanup html to text and remove unneeded characters
    list = []
    for element in in_tuple:
        if element is None:
            list.append("null")
        else:
            # print(element)
            if type(element) is str:
                list.append(element.strip().replace(" ", "").replace("\n", "").replace("\r", "").replace("mailto:", ""))
            else:
                # print(element)
                object = element.text.strip()

                object = object.replace("\n", "").replace("\r", "").replace("mailto:", "")
                # object = element.text.strip.replace(" " , " ").replace("\n", "").replace("\r", "")#
                list.append(object)

    return (tuple(list))

def SelPage(link):
    options = webdriver.ChromeOptions()
    WINDOW_SIZE = "1920,1080"
    #options.add_argument("--headless")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    #options.add_argument("--log-level=OFF")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    linkdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    linkdriver.get(link)
    linksource = linkdriver.page_source
    linksoup = BeautifulSoup(linksource, 'lxml')
    return(linksoup)



URLs = pd.read_csv('combined.csv')
URLs = list(URLs['LINK'])
columnslist = ['Email Address', 'URL', 'Firm', 'Source']
source = 'https://www.cpca-rpc.ca/counsellor-directory.aspx'
alldata = []
empty = pd.DataFrame(alldata, columns=columnslist)
empty.to_csv('cpca.csv', encoding='utf-8-sig', index=False)
try:
    count = 0
    for url in URLs:
        urlsoup = SelPage(url)
        data = attribute_scraper(urlsoup, source)

        data = html_clean(data)
        print(data)
        #print(data)
        alldata.append(data)
        df = pd.DataFrame([data], columns=columnslist)
        df.to_csv('cpca.csv', encoding='utf-8-sig', index=False, mode='a', header=False)
        count = count + 1
        print("On scrape loop: ", count)
        time.sleep(0.1)
    #df.to_csv('travelweekly.csv', encoding='utf-8-sig', index=False)

    print("Saved with a total volume of: ", len(alldata))
except Exception as e:
    print('Scrape ended early, refer to error message, saving scraped data to file')
    print(e)
    df = pd.DataFrame(alldata, columns=columnslist)
    df.to_csv('cpca_crashed.csv', encoding='utf-8-sig', index=False)
    print("Saved with a total volume of: ", len(df))

#end = input("Program has finished, press Enter when you are done reading output")
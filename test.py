import requests as re
from bs4 import BeautifulSoup
import time

time.sleep(5)
import pandas as pd
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

home_pages = ['https://www.sortlist.com/web-analytics', 'https://www.sortlist.com/lead-acquisition']

web_range = range(1, 6, 1)# 6 pages in first link
web_range2 = range(1, 5, 1)# 5 pages in second link
# Want the li element for all the elements on the page

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


# For web pages that paginate through the url and have listings of profiles rather than listings of information
# , goes through all the given pages and returns the profile links
def get_firm_links(link):
    link_list = []

    for n in web_range:
        # print(link+str(n)+'/')
        url = (link + str(n) + '/')
        page = re.get(url)
        # print(page)
        soup = BeautifulSoup(page.content, 'lxml')
        firms = soup.find_all('div', class_='resultRow')
        print("On URL: ", url, " loop ", n, "sleeping for 0.5...")
        time.sleep(0.5)

        for firm in firms:
            try:
                firmpage = firm.find('a', href=True)
                link_list.append(firmpage['href'])
            except:
                continue
    return (link_list)


allfirms = []
for home_page in home_pages:
    allfirms.append(get_firm_links(home_page))


# Takes a single profile page and returns its data
def page_scrape(firm_link):
    page = re.get(firm_link)
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        Firm = soup.find('span', class_='header-text')
    except:
        Firm = 'null'
    try:
        # URL still doesnt work

        # print(URLBLOCK)
        URL = soup.find('div', class_='user_content')
        # print(URL)
        URL = URL.find('a', href=True)['href']

        # print(URL)
        # URL = out
        # print(URL)
    except:
        URL = 'null'
    try:
        Address = soup.find('div', {"itemprop": "address"})
    except:
        Address = 'null'
    # print(URL)
    Firm, URL, Address = html_clean((Firm, URL, Address))
    if 'yalwa' in URL or 'google' in URL:
        URL = 'null'
    return (Firm, URL, Address)


allfirms_flat = [item for sublist in allfirms for item in sublist]
alldata = []
columnslist = ['Firm', 'URL', 'Address Line 1', 'Source']
empty = pd.DataFrame(alldata, columns=columnslist)
empty.to_csv('Yalwa.csv', encoding='utf-8-sig', index=False)

try:
    count = 0
    for link in allfirms_flat:
        # print(link)
        Source = 'https://www.yalwa.com/Marketing/112/'
        Firm, URL, Address = page_scrape(link)
        data = (Firm, URL, Address, Source)
        print(data)
        df = pd.DataFrame([data], columns=columnslist)
        df.to_csv('Yalwa.csv', encoding='utf-8-sig', index=False, mode='a', header=False)
        count += 1
        time.sleep(4)
        print("On scrape loop: ", count, "pausing for: 2 seconds")
    print("Saved with a total volume of: ", len(alldata))
except Exception as e:
    print('Scrape ended early, refer to error message, saving scraped data to file')
    print(e)
    df = pd.DataFrame(alldata, columns=columnslist)
    df.to_csv('Yalwa_crashed.csv', encoding='utf-8-sig', index=False)
    print("Saved with a total volume of: ", len(df))
alldata = []

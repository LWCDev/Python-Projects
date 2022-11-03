import requests as req
from bs4 import BeautifulSoup
import time
import random
import colorama
import re
from colorama import Fore, Back, Style
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
colorama.init(autoreset=True)


def html_clean(in_tuple):
    # cleanup html to text and remove unneeded characters
    list = []
    for element in in_tuple:
        if element is None:
            list.append("null")
        else:
            # print(element)
            if type(element) is str:
                list.append(element.strip().replace(" ", "").replace("\n", "").replace("\r", "").replace("mailto:", "").replace("View Map", ""))
            else:
                # print(element)
                object = element.text.strip()

                object = object.replace("\n", "").replace("\r", "").replace("mailto:", "").replace("View Map", "")
                # object = element.text.strip.replace(" " , " ").replace("\n", "").replace("\r", "")#
                list.append(object)

    return tuple(list)

# Now we have each category sorted, we need to get the firm profile URLs from them
# Finds the max page count from the pagination buttoms at the bottom of the web page,
# Indexing only fails when there are no buttons (1 page total) so we except to a range of 0,1
# Returns an appended version of the href that gives us the firm pages, this list needs to be flattened afterwards
# company listings don't have consistent class names but all end in g_0, so we can use that to find them
# We use the re package and regex match pattern ending for this ($)
# In future to avoid firms without websites we can abuse that they show this before opening their profile,
# simply search for this element and if it isn't present don't save the firm profile,
# however in order to do this the way we save the links would have to be totally rewritten

def get_firm_links(link):
    link_list = []
    numcheck = req.get(link)
    numsoup = BeautifulSoup(numcheck.content, 'lxml')
    try:
        pager = numsoup.find_all('a', class_="pages_no", href=True)
        max = pager[len(pager)-1].text
        web_range = range(0,int(max), 1)
    except:
        web_range = range(0,1,1)
    for n in web_range:
        # print(link+str(n)+'/')
        url = (link + '/' + str(n) )
        print("On URL: ", url, " loop ", n, "\n", " with range: ", web_range, " sleeping for 0.5...")
        page = req.get(url)
        # print(page)
        soup = BeautifulSoup(page.content, 'lxml')
        firms = soup.find_all('div', class_= re.compile('g_0$'))
        time.sleep(0.5)
        for firm in firms:
            try:
                #print("Accessed!")
                firmpage = firm.find('a', href=True)
                link_list.append('https://www.irelandyp.com' + firmpage['href'])
                #print('https://www.irelandyp.com' + firmpage['href'])
                print(f"{Fore.GREEN}Fetched: https://www.irelandyp.com{firmpage['href']}")
            except Exception as e:
                print("Exception! ", e)
                continue
    #print(f"{Fore.GREEN}Fetched: \n {link_list}")
    return link_list


# Takes a single profile page and returns its data
def page_scrape(firm_link):
    page = req.get(firm_link)
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        Firm = soup.find('b', {"id" : "company_name"})
    except:
        Firm = 'null'
    try:
        URL = soup.find('div', class_='text weblinks')
    except:
        URL = 'null'
    try:
        Address = soup.find('div',class_="text location")
    except:
        Address = 'null'
    # print(URL)
    Firm, URL, Address = html_clean((Firm, URL, Address))
    if 'irelandyp' in URL or 'google' in URL:
        URL = 'null'
    return Firm, URL, Address

# For the website https://www.irelandyp.com/browse-business-directory
# Home page has multiple categories that paginate by URL, we start by getting all those categories
page = req.get('https://www.irelandyp.com/browse-business-directory')
soup = BeautifulSoup(page.content, 'lxml')

categories = soup.find_all('ul', class_="cat_list")
#print(categories)
cat_links = []
for ul in categories:
    a = ul.find_all('a', href=True)
    for href in a:
        cat_links.append('https://www.irelandyp.com'+ href['href'])
#print(cat_links)
# Now that we have sorted all our categories out we can use them to scrape firm profile URLs and then scrape the data itself


# link = 'https://www.irelandyp.com/category/Cleaning_equipment_Services'
# numcheck = req.get(link)
# numsoup = BeautifulSoup(numcheck.content, 'lxml')
# pager = numsoup.find_all('a', class_="pages_no", href=True)
# print(pager)
# max = pager[len(pager)-1].text
# web_range = range(0,int(max), 1)
# print(web_range)
allfirms = []
# Comment out if you are resuming, you dont need to refetch firms
#for link in cat_links:
##     allfirms.append(get_firm_links(link))

#allfirms_flat = [item for sublist in allfirms for item in sublist]
# For resume purposes
#allfirmsdf = pd.DataFrame(allfirms_flat, columns=['Firm Profile URL'])
#allfirmsdf.to_csv('ie_Yp_firms.csv', encoding='utf-8-sig', index=False)
allfirmsdf = pd.read_csv('ie_Yp_firms.csv', usecols=['Firm Profile URL'])
allfirmsdf = allfirmsdf.values.tolist()
alldata = []
columnslist = ['Firm', 'URL', 'Address Line 1', 'Source']
# comment out the two below lines if you are continuing a job after a failed scrape
#empty = pd.DataFrame(alldata, columns=columnslist)
#empty.to_csv('ie_Yp.csv', encoding='utf-8-sig', index=False)

# scrapes data from all firms
forerror = 'shutup pycharm'
try:
    count = 0
    for link in allfirmsdf:
        # print(link)
        randsleep = random.randint(1,2)
        origin = str(link[0])
        forerror = origin
        Source = 'irelandyp.com'
        Firm, URL, Address = page_scrape(origin)
        if URL == 'null' and Firm == 'null':
            print(f"{Fore.RED}No URL and no Firm name, skipping firm \n If you see this message repeatedly you are probably blocked or the data sucks")
            print(f"{Fore.RED}Sleeping for... {randsleep} seconds, on loop: {count}")
            time.sleep(randsleep)
            count += 1
            continue
        elif URL == 'null' or Firm == 'null':
            print(f"{Fore.RED}No URL or no Firm name, skipping firm \n If you see this message repeatedly you are probably blocked or the data sucks")
            print(f"{Fore.RED}Sleeping for... {randsleep} seconds, on loop: {count}")
            time.sleep(randsleep)
            count += 1
            continue
        data = (Firm, URL, Address, Source)
        print(f"{Fore.GREEN} Data: {data}")
        df = pd.DataFrame([data], columns=columnslist)
        alldata.append(data)
        df.to_csv('ie_Yp.csv', encoding='utf-8-sig', index=False, mode='a', header=False)
        count += 1
        print("On scrape loop: ", count, "pausing for: ", randsleep ," seconds")
        time.sleep(randsleep)
    print("Saved with a total volume of: ", len(alldata))
except Exception as e:
    print('Scrape ended early, refer to error message, saving scraped data to file')
    print(e)
    print("Failed on: ", forerror, " find what category this is from to resume")
    df = pd.DataFrame(alldata, columns=columnslist)
    df.to_csv('ie_Yp_crashed.csv', encoding='utf-8-sig', index=False)
    print("Saved with a total volume of: ", len(df))
print("Finished!")
#alldata = []

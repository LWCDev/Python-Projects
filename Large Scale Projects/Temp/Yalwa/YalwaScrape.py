import requests as re
from bs4 import BeautifulSoup
import time
import random
import colorama
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


# hopefully for all Yalwa categories from the yalwa ireland page,
# what i have so far works for pages following the format as below, but this needs to start from the origin of https://www.yalwa.ie/ and then get to pages like this
# https://athlone.yalwa.ie/?show_all=1, this shows every single category following the format <place>.yalwa.ie/?show_all=1
# but rather than do each location separately we can see for all of ireland following the categories at the top
# i.e https://www.yalwa.ie/Building-Construction/G/, this shows for all businesses in ireland rather than just a sub category

#home_pages = ['https://www.yalwa.com/Marketing/112/', 'https://www.yalwa.com/Coupons/11201/',
#              'https://www.yalwa.com/Digital-Marketing/11202/',
#              'https://www.yalwa.com/Email-Marketing/11204/', 'https://www.yalwa.com/International-Marketing/11205/',
#              'https://www.yalwa.com/Internet-Marketing/11206/',
#              'https://www.yalwa.com/Loyalty-Marketing/11218/', 'https://www.yalwa.com/Market-Research/11217/',
#              'https://www.yalwa.com/Marketing-Consultants/11207/',
#              'https://www.yalwa.com/Merchandising/11208/', 'https://www.yalwa.com/Promotional-Products/11210/',
#              'https://www.yalwa.com/Publishing-Services/11211/',
#              'https://www.yalwa.com/Sales-Leads-Generation/11212/', 'https://www.yalwa.com/Sales-Promotions/11213/',
#              'https://www.yalwa.com/Search-Engine-Marketing/11214/',
#              'https://www.yalwa.com/Telemarketing/11215/', 'https://www.yalwa.com/Voice-Marketing/11216/']

# can automate this easily, but it's only a few so w/e
home_pages = ['https://www.yalwa.ie/Building-Construction/G/',
              'https://www.yalwa.ie/Business-Services/B/',
              'https://www.yalwa.ie/Computer-Internet/C/',
              'https://www.yalwa.ie/Entertainment-Lifestyle/E/',
              'https://www.yalwa.ie/Financial-Legal/F/',
              'https://www.yalwa.ie/Food-Drink/D/',
              'https://www.yalwa.ie/Health-Beauty/H/',
              'https://www.yalwa.ie/Industry/I/',
              'https://www.yalwa.ie/Property/P/',
              'https://www.yalwa.ie/Public-Social-Services/A/',
              'https://www.yalwa.ie/Shopping/S/',
              'https://www.yalwa.ie/Transport-Automotive/T/',
             'https://www.yalwa.ie/Travel-Tourism/R/']
# now that we have our home pages we want to refine our category search, so we can get more results

# this is a constant because yalwa only at maximum shows 20 pages of results
web_range = range(0, 19, 1)

def category_refine(URL):
    list_of_category_links = []
    page = re.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')
    list = soup.find('ul', class_="left_nav__layer_2")
    #hrefs = list.find_all('a', href=True)
    count = 0
    hrefs = list.find_all('a', href=True)
    for href in hrefs:
        #print(href['href'])
        try:
            list_of_category_links.append(href['href'])
        except:
            continue
    return list_of_category_links

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


# For web pages that paginate through the url and have listings of profiles rather than listings of information ,
# goes through all the given pages and returns the profile links, skips when it finds the final page (redirects to
# first page of results)
# outputs to console what links it got. This floods console but is necessary to check we have not been site blocked
def get_firm_links(link):
    link_list = []

    for n in web_range:
        # print(link+str(n)+'/')
        url = (link + str(n) + '/')
        print("On URL: ", url, " loop ", n, "sleeping for 0.5...")
        page = re.get(url)
        if n > 1:
            if page.url == link:
                print("Final page reached: skipping the rest of the loop")
                break
        # print(page)
        soup = BeautifulSoup(page.content, 'lxml')
        firms = soup.find_all('div', class_='resultRow')
        time.sleep(0.5)

        for firm in firms:
            try:
                firmpage = firm.find('a', href=True)
                link_list.append(firmpage['href'])
            except:
                continue
    print(f"{Fore.GREEN}Fetched: \n {link_list}")
    return (link_list)





# Takes a single profile page and returns its data, sometimes emails are there instead of URLs so we check that
def page_scrape(firm_link):
    page = re.get(firm_link)
    soup = BeautifulSoup(page.content, 'lxml')
    Email = 'null'
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
    if '@' in URL:
        Email = URL
        URL = 'null'
    return (Firm, URL, Address, Email)



allfirms = []
category_urls = []
# goes through each origin page as defined above, gets all the refined category start links to improve result amount
for home_page in home_pages:
    category = category_refine(home_page)
    time.sleep(2)
    #category_flat = [item for sublist in category for item in sublist]
    for cat in category:
        category_urls.append(cat)
# For resume purposes
catdf = pd.DataFrame(category_urls, columns=['Category URL'])
catdf.to_csv('ie_Yalwa_category_URLs.csv', encoding='utf-8-sig', index=False)
print(category_urls)

# loop through each refined category to get each firm's profile page
for cat_url in category_urls:
    allfirms.append(get_firm_links(cat_url))

# flatten the list from above so that we can loop through it as one continuous list
allfirms_flat = [item for sublist in allfirms for item in sublist]
# For resume purposes
allfirmsdf = pd.DataFrame(allfirms_flat, columns=['Firm Profile URL'])
allfirmsdf.to_csv('ie_Yalwa_firms.csv', encoding='utf-8-sig', index=False)
alldata = []
columnslist = ['Firm', 'URL', 'Address Line 1', 'Email Address', 'Source']
# comment out the two below lines if you are continuing a job after a failed scrape
empty = pd.DataFrame(alldata, columns=columnslist)
empty.to_csv('ie_Yalwa.csv', encoding='utf-8-sig', index=False)
# scrapes data from all firms
forerror = 'shutup pycharm'
try:
    count = 0
    for link in allfirms_flat:
        # print(link)
        randsleep = random.randint(1,5)
        forerror = link
        Source = 'yalwa.ie'
        Firm, URL, Address, Email = page_scrape(link)
        if URL == 'null' and Email == 'null':
            print(f"{Fore.RED}No URL or Email, skipping firm")
            count += 1
            continue
        if Firm == 'null' and Address == 'null':
            print(f"{Fore.RED}Check that the site hasn't blocked you. If you see this message repeatedly you are probably blocked")
            count += 1
            continue
        data = (Firm, URL, Address, Email, Source)
        print(data)
        df = pd.DataFrame([data], columns=columnslist)
        alldata.append(data)
        df.to_csv('ie_Yalwa.csv', encoding='utf-8-sig', index=False, mode='a', header=False)
        count += 1
        print("On scrape loop: ", count, "pausing for: ", randsleep, " seconds")
        time.sleep(randsleep)
    print("Saved with a total volume of: ", len(alldata))
except Exception as e:
    print('Scrape ended early, refer to error message, saving scraped data to file')
    print(e)
    print("Failed on: ", forerror, " find what category this is from to resume")

    df = pd.DataFrame(alldata, columns=columnslist)
    df.to_csv('ie_Yalwa_crashed.csv', encoding='utf-8-sig', index=False)
    print("Saved with a total volume of: ", len(df))
print("Finished!")
#alldata = []


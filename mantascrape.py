import requests as re
from bs4 import BeautifulSoup
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


def scroll_down(elem, num):
    for _ in range(num):
        time.sleep(2.5)
        elem.send_keys(Keys.PAGE_DOWN)

#For the website https://www.manta.com/mb_33_A0_000/advertising_and_marketing

#should hopefully return a list of soups which can be used by beautiful soup
def RunSelenium():
    souplist = []
    try:
        #options = webdriver.ChromeOptions()
        #options.add_argument("--log-level=OFF")
        options = webdriver.ChromeOptions()
        WINDOW_SIZE = "1920,1080"
        # options.add_argument("--headless")
        #options.add_argument("--window-size=%s" % WINDOW_SIZE)
        # options.add_argument("--log-level=OFF")
        #options.add_argument('--ignore-certificate-errors')
        #options.add_argument('--incognito')
        #options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.manta.com/mb_33_A0_000/advertising_and_marketing")
        #driver.get("https://www.manta.com/mb_43_A0_08/advertising_and_marketing/delaware")
        sourcelist = []
        #options = webdriver.ChromeOptions()



        driver.implicitly_wait(10)
        #page_source = driver.page_source
        #sourcelist.append(page_source)
        SCROLL_PAUSE_TIME = 10
        elem = driver.find_element(By.XPATH, "/html/body")
        prev_height = elem.get_attribute("scrollHeight")

        for i in range(0, 1):
        #for i in range(0, 10000):
            # note that the pause between page downs is only .01 seconds
            # in this case that would be a sum of 1 second waiting time
            scroll_down(elem, 5)
            # Wait to allow new items to load
            print("Scroll loop: ", i)
            time.sleep(SCROLL_PAUSE_TIME)
            page_source = driver.page_source
            # check to see if scrollable space got larger
            # also we're waiting until the second iteration to give time for the initial loading
            if elem.get_attribute("scrollHeight") == prev_height and i > 0:
                break
            prev_height = elem.get_attribute("scrollHeight")

    except Exception as e:
        print("Webcrawling failed, it was probably chrome crashing/being closed or the page not loading the element you wanted. The source should still get passed and scraping should continue")
        print("Let's check:",
              e)
    soup = BeautifulSoup(page_source, 'lxml')
    return(soup)

def attribute_scraper(soup):

    FirmList = []
    AddressList = []
    URLlist = []
    TelephoneList = []
    soupy = soup
    Blocks = soupy.find_all('div', class_="md:rounded bg-white border-b  border-t  border-primary-light-v1 px-3 py-4 md:p-8 md:mt-4 mx-4 xl:mx-0")

    try:
        print(Blocks)
        for Block in Blocks:
            try:
                Address = Block.find('div', class_='class="ml-4"')
                AddressList.append(Address)
            except:
                AddressList.append('null')
            try:
                Telephone = Block.find('div', class_="fa fa-phone mr-4 text-xl fa-rotate-90 pt-1 text-gray-400")
                TelephoneList.append(Telephone)
            except:
                TelephoneList.append('null')
            try:
                URLs = Block.find_all('a', href=True)
                URL = URLs[1]['href']
                URLlist.append(URL)
            except:
                URLlist.append('null')
            try:
                Firm = Block.find('a', href=True)
                FirmList.append(Firm)
            except:
                FirmList.append('null')
    except:
        print("It completely broke")

    return(URLlist, FirmList, AddressList) #Email Address, URL, Firm, Address Line 1, Source


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




sourceurl = 'https://www.manta.com/mb_43_A0_08/advertising_and_marketing/'
source_soup = RunSelenium()
columnslist = ['URL', 'Firm', 'Telephone Number', 'Source']
test = attribute_scraper(source_soup)
print(test[1])
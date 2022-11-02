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


#For the website https://plumber.com.au/find-a-plumber/#

#should hopefully return a list of soups which can be used by beautiful soup
def RunSelenium():
    souplist = []
    try:
        #options = webdriver.ChromeOptions()
        #options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://www.travelweekly.com/Hotels/Advanced?bw=amen11")

        sourcelist = []
        #options = webdriver.ChromeOptions()



        driver.implicitly_wait(10)
        page_source = driver.page_source
        sourcelist.append(page_source)
        WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CLASS_NAME, "next"))).click()
        #more_buttons = driver.find_element(By.CLASS_NAME, "next")
        #while True:
        #    wait = WebDriverWait(driver, 10000)
        #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #    WebDriverWait(driver, 800000).until(EC.element_to_be_clickable((By.CLASS_NAME, "next")))
         #   WebDriverWait(driver, 1000).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "next" ), "Next"))
         #   more_buttons = driver.find_element(By.CLASS_NAME, "next")
         #   if 'inactive' in more_buttons.get_attribute('class'):
         #       break;
         #   time.sleep(1)
         #   more_buttons.click()

        #Goes through all the pages of information available, afterwhich it can be passed off to bs4
        try:

            for p in range(1,22508,1):
                print("Webcrawl loop number: ", p)
                driver.find_element(By.XPATH,"//div//div//div//div//a[@class='next']").click()
                page_source = driver.page_source
                sourcelist.append(page_source)
                time.sleep(10)
            driver.close()
        except Exception as e:
            print("Loop ended early within the catch statement", e)
            page_source = driver.page_source
            sourcelist.append(page_source)
            driver.close()

    except Exception as e:
        print("Webcrawling failed, it was probably chrome crashing/being closed or the page not loading the element you wanted. The souplist should still get passed and scraping should continue")
        print("Let's check:",
              e)
    for x in range(len(sourcelist)):
        soup = BeautifulSoup(sourcelist[x], 'lxml')
        souplist.append(soup)
    return(souplist)

#Runs selenium for a single webpage, returning the page as a soup object that can be used to scrape from
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


#driver = webdriver.Chrome("C:\\Users\\lewis.welshclark\\chromium\\chromedriver.exe", ptions=options)

#Accepts a single soup object and a source (nothing is perfomed on the source), scraping the soup, so it can return an array/tuple containing the data
#This soup is obtained through selenium for each webpage individually as the webpage hides the email behind a javascript event which is removed when the page is loaded within a browser
def attribute_scraper(link, source):
    #site = re.get(link)
    #soupy = BeautifulSoup(site.content, 'lxml')
    soupy = link
    ContactInfo = soupy.find('div', class_="links")
    #print(ContactInfo)
    try:
        Contact = ContactInfo.find_all('a', href=True)
        #print(Contact)
        try:
            Email = Contact[0]['href']
        except:
            Email = 'null'
        try:
            URL = Contact[1]['href']
        except:
            URL = 'null'
    except:
        Email = 'null'
        URL = 'null'
    try:
        Firm = soupy.find('h1', class_='title-xxxl')
    except:
        Firm = 'null'
    try:
        Address = soupy.find('div', class_='address')
    except:
        Address = 'null'

    return(Email, URL, Firm, Address, source) #Email Address, URL, Firm, Address Line 1, Source

#Use case: website with multiple elements and links per page, but only one link that you need within each element
#link_fetch returns a list of URLs of separate firm pages hosted on the host site that contain contact information etc. which we can scrape
def link_fetch(list_of_soup):
    URLs = []
    for soup in list_of_soup:

        #Find all the element bodies that contain the links that you need
        body = soup.find_all('div', class_="result")
        #Treating the element body like a list, iterate for any href URLs, concat them with the base URL if required (not a full URL) and then append them to a list containing them all
        for element in body:
            url = element.find('a', class_="title", href=True)
            url = "https://www.travelweekly.com" + url['href']
            URLs.append(url)
        #Returns a list of webpages which we can use to scrape information
    return(URLs)

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

def load_page():
    print()

list_of_soups = RunSelenium()
firmurls = link_fetch(list_of_soups)
#Pass the list firmurls from link_fetch to scrape data


columnslist = ['Email Address', 'URL', 'Firm', 'Address Line 1', 'Source']
alldata = []
empty = pd.DataFrame(alldata, columns=columnslist)
empty.to_csv('plumber.csv', encoding='utf-8-sig', index=False)
try:
    count = 0
    for url in firmurls:
        urlsoup = SelPage(url)
        data = attribute_scraper(urlsoup, url)
        data = html_clean(data)
        alldata.append(data)
        df = pd.DataFrame([data], columns=columnslist)
        df.to_csv('plumber.csv', encoding='utf-8-sig', index=False, mode='a', header=False)
        count = count + 1
        print("On scrape loop: ", count)
        time.sleep(0.1)
    #df.to_csv('travelweekly.csv', encoding='utf-8-sig', index=False)

    print("Saved with a total volume of: ", len(alldata))
except Exception as e:
    print('Scrape ended early, refer to error message, saving scraped data to file')
    print(e)
    df = pd.DataFrame(alldata, columns=columnslist)
    df.to_csv('plumber_crashed.csv', encoding='utf-8-sig', index=False)
    print("Saved with a total volume of: ", len(df))


import requests
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


# https://www.carehome.co.uk/care_search_results.cfm/searchcountry/England/startpage/200 to page 1
#This site needs redirects to handle the firm URLs after scraping




def SelPage(link):
    options = webdriver.ChromeOptions()
    WINDOW_SIZE = "1920,1080"
    #options.add_argument("--headless")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    #options.add_argument("--log-level=OFF")
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--incognito')
    #options.add_argument('--headless')
    linkdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    linkdriver.get(link)
    time.sleep(10)
    linkdriver.implicitly_wait(10)
    linksource = linkdriver.page_source
    linksoup = BeautifulSoup(linksource, 'lxml')
    linkdriver.quit()
    return(linksoup)


#start = input("Do you want to run the scaper? Press Enter to start")
#should hopefully return a list of soups which can be used by beautiful soup

pagerange = range(1, 5, 1)
URLslist = []
headers = headers = {
    'authority': 'www.carehome.co.uk',
    'accept': 'application/json; charset=utf-8',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'text/plain; charset=utf-8',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'visid_incap_913011=wBmZR4EATEeIG0snwes6LZH5PmMAAAAAQUIPAAAAAABa6mbYMqRyffBa2Os6IMNO; _hjSessionUser_1631975=eyJpZCI6ImQ3ZTczMjg1LWRmZTAtNWE1NC05ODliLWIyZjJmMmNjMzNiZSIsImNyZWF0ZWQiOjE2NjUwNzE1MTA0OTIsImV4aXN0aW5nIjp0cnVlfQ==; CFCLIENT_CH=""; incap_ses_452_913011=xVmCIm+6l1818yvrYNRFBsMARGMAAAAAfmhPOaFmXCpMYBHjIREWtw==; reese84=3:8j7KWUUf69/MFxjwX0qZtg==:dEUk9HtcbtHhvbQk89i/OPD6hQNxzMx7ze8oaidTMEFXoTJAMNim3bNzBqb2jTGczPe03KDEh/Ham9HIKPPwurPdgVQO4KPeUSZxQlBqTVqdSWwbgzXZrSZC3pbNmqLsT/iRwxTKClCQRZlImfLKG+KgzEM0r1yX73P6n/UDLGBZvGWv2lDG2SqDQrBKL1bBi94NTiWiK4S5xekl/gmnru8gSexDr5VRZA9tkXxWGPWcwPaya507gDU2TOpEf6xUaCmUAGvcPde0VMsB5VrsVO9AasIZ+7iohn7Rn6XvhZdBRZy6xWsR4UX/mGX32njSBRLl0UL+l57ny0DjZLzcenQxsiAsdWOyxgois5rIeaZ1K/BIlhGIIlU5vtDK341EsqIMptuML3vzYOnC5HyCfA+8P5HUNPqox1mKejt0ijLQBOjeCiETYiB5Tu2ses7SiQI6lcMTBj8ylTu8KAiGdEHAnXlaFWAIhWZSlJUd+EI=:r0YsZvHdibgZ2MtA+gpSL8g1leg6mePYZK9ZIO9TRNg=; CFID=60496881; CFTOKEN=ea2635eb38de0f34-905EC9BD-9C99-687F-D34C9CFEAC8560DF; _gid=GA1.3.212453526.1665401030; _hjIncludedInSessionSample=0; _hjSession_1631975=eyJpZCI6ImNiNTIxOWY4LTNkNmItNDU5OC05N2JlLTJlMDdlZjlmMDQ3NiIsImNyZWF0ZWQiOjE2NjU0MDEwMzA0ODUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; RECENTVIEWED=6886%2C4084%2C4074%2C3014%2C2044%2C8416%2C2094%2C5446%2C3702%2C1634%2C9059%2C8475%2C4445%2C2415%2C7222%2C80971%2C84849%2C65432238157%2C65432239138%2C65432239083%2C65432237052%2C65432239084%2C65432244056%2C65432244036%2C65432244050%2C65432244032%2C65432247088%2C65432243136%2C65432243133%2C65432247139%2C65432243238%2C65432242255%2C65432244384%2C65432243330%2C65432234986%2C65432232957%2C65432233950%2C65432247438%2C65432233839%2C8386%2C8376%2C7376%2C65432212838%2C65432212858%2C65432215881; __atuvc=99%7C40%2C1%7C41; __atuvs=634403a7111661e1000; _ga=GA1.3.176199118.1665071510; _ga_HT8K0EGF0B=GS1.1.1665401030.3.1.1665401799.0.0.0; CFGLOBALS=urltoken%3DCFID%23%3D60496881%26CFTOKEN%23%3Dea2635eb38de0f34%2D905EC9BD%2D9C99%2D687F%2DD34C9CFEAC8560DF%23lastvisit%3D%7Bts%20%272022%2D10%2D10%2012%3A36%3A39%27%7D%23hitcount%3D482%23timecreated%3D%7Bts%20%272022%2D10%2D06%2016%3A51%3A46%27%7D%23cftoken%3Dea2635eb38de0f34%2D905EC9BD%2D9C99%2D687F%2DD34C9CFEAC8560DF%23cfid%3D60496881%23; amp_5f923a=i2FO1sJk_o_sFbGSWApZVr...1gf0q6107.1gf0qtk3v.e.0.e',
    'origin': 'https://www.carehome.co.uk',
    'referer': 'https://www.carehome.co.uk/care_search_results.cfm/searchcountry/England/startpage/200',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}
for i in pagerange:
    URL = "https://www.carehome.co.uk/care_search_results.cfm/searchcountry/England/startpage/" + str(i)
    #page = requests.get(f"https://www.carehome.co.uk/care_search_results.cfm/searchcountry/England/startpage/{i}")
    soup = SelPage(URL)
    #soup = BeautifulSoup(page.content, 'lxml')
    print(soup.prettify())
    href = soup.find_all('a')
    print(href)
    for link in href:
        try:
            URLslist.append(link)
        except:
            continue
    time.sleep(1)
print(URLslist)
from PandasClean import Clean_Utilities
from Multiproc import MultiProcess
import multiprocessing as mp
from multiprocessing import Manager, freeze_support
import queue
import pandas as pd
import json
import time
import ast

from typing import List, Dict, Tuple
from MongoUtilities import MongoUtilities
from Utilities import Utilities
import glob, shutil, sys, io, re, os
from datetime import date, datetime, timedelta

import urllib3
import requests
from bs4 import BeautifulSoup
import random
# This finds the link for each company page given a page's text content This is because it's impossible to find the
# firm profile pages otherwise, this uses substring indexing to find the relevant parts, before adding them to a URL
# template to create a usable URL


def link_find(text):
    counter = 0
    list_of_url = []
    while counter != 10:
        try:
            startindex = text.index('Working-at')
            #print(startindex)
            #print(text[startindex:startindex+20])
            endindex = text.index('.htm","reviewsUrl":')
            #print(endindex)
            #print(text[startindex:endindex])
            URL = text[startindex:endindex+4]
            #print(URL)
            text = text[endindex+4:]
            URL = URL.replace('"', '')
            URL = URL.replace(',', '')
            URL = 'https://www.glassdoor.co.uk/Overview/' + URL
        except:
            URL = 'null'
        list_of_url.append(URL)
        counter=counter+1
    return(list_of_url)



# ProfileURLs = []
# alldata = []
# columnslist = ["Profile URL"]
#
# # Comment the below 2 lines out if you are continuing with a job, change the range below as appropriate
# empty = pd.DataFrame(alldata, columns=columnslist)
# empty.to_csv('glassdoor_profiles_2.csv', encoding='utf-8-sig', index=False)
#
# RANGE = range(1,387,1)
# for y in RANGE:
#     # Change headers as required, add proxies if needed
#     # For different categories, headers must be updated, sectors tag is what controls it
#     cookies = {
#     'gdId': 'd0273789-b738-45b2-b839-a365d12fd027',
#     '_gid': 'GA1.2.523821179.1665993513',
#     'OptanonAlertBoxClosed': '2022-10-17T07:59:54.521Z',
#     '_optionalConsent': 'true',
#     '_gcl_au': '1.1.1425350194.1665993595',
#     '_rdt_uuid': '1665993595770.f7454022-afeb-454f-a935-076f287f258d',
#     '__pdst': '6fece3219b4d49ffbb354d059e1e282d',
#     '_tt_enable_cookie': '1',
#     '_ttp': '1f7731eb-53fe-4070-bc7a-d3832fd1ec80',
#     '_fbp': 'fb.1.1665993595974.1016602883',
#     '_pin_unauth': 'dWlkPU4yWmxZMlZsTm1JdE5UTTJaUzAwTnpjeUxXSXpPV0V0Wm1NMFpUUm1OV0l5TTJFMw',
#     'GSESSIONID': 'undefined',
#     'gdsid': '1665993511833:1666012504494:3A6ACB5518DD49990AD8B928A8500ECF',
#     'amp_bfd0a9': 'JKImedgy7bOzlPc5h3rgAb...1gfj1aqqo.1gfj1aqr7.2.0.2',
#     '_ga_RJF0GNZNXE': 'GS1.1.1666012503.2.1.1666012507.56.0.0',
#     '__gads': 'ID=3a7484feb804561b:T=1666012507:S=ALNI_Mb1WhsyKIJBAVKAgU0v6qmj8v00Ng',
#     '__gpi': 'UID=00000b12871b555d:T=1666012507:RT=1666012507:S=ALNI_Mb2u8VOrEcBS5Lx0glxhJgxhieqGw',
#     'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Oct+17+2022+14%3A15%3A07+GMT%2B0100+(British+Summer+Time)&version=202209.2.0&isIABGlobal=false&hosts=&consentId=e9e1457d-1ef4-4779-a9b8-e8cce33210bd&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=GB%3BENG&AwaitingReconsent=false',
#     'AWSALB': 'z26sTrfm1BBU706tjb5NNQqABHqZY+f8jZQL7lgtne2nbztGvQpt4iWF1O/qpNW2RJsA19/fT+eGJA35Z1kbsgOErauFKUlbiIKiL+1/VwS3GBozibXuP9ysLUzr',
#     'AWSALBCORS': 'z26sTrfm1BBU706tjb5NNQqABHqZY+f8jZQL7lgtne2nbztGvQpt4iWF1O/qpNW2RJsA19/fT+eGJA35Z1kbsgOErauFKUlbiIKiL+1/VwS3GBozibXuP9ysLUzr',
#     'JSESSIONID': '9BE9D351BC2D3AB7FA6070812700747A',
#     'cass': '0',
#     '_ga': 'GA1.2.243230694.1665993513',
#     '__cf_bm': 'YY30hP1uBkfNCNT_x3WhJ7orBSFUH1UG0dociD9wwJ8-1666014915-0-AbVTDVVC1b/87MWZNkTZsYAWtWcjgufpxTWm89O8cB31pFHc6XVKpzo1r83gTn19pQdJsScI8oyL6fawJ3KLsYk=',
#     '_ga_RC95PMVB3H': 'GS1.1.1666014915.3.0.1666014915.60.0.0',
#     }
#
#     headers = {
#     'authority': 'www.glassdoor.com',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'cache-control': 'max-age=0',
#     # Requests sorts cookies= alphabetically
#     # 'cookie': 'gdId=d0273789-b738-45b2-b839-a365d12fd027; _gid=GA1.2.523821179.1665993513; OptanonAlertBoxClosed=2022-10-17T07:59:54.521Z; _optionalConsent=true; _gcl_au=1.1.1425350194.1665993595; _rdt_uuid=1665993595770.f7454022-afeb-454f-a935-076f287f258d; __pdst=6fece3219b4d49ffbb354d059e1e282d; _tt_enable_cookie=1; _ttp=1f7731eb-53fe-4070-bc7a-d3832fd1ec80; _fbp=fb.1.1665993595974.1016602883; _pin_unauth=dWlkPU4yWmxZMlZsTm1JdE5UTTJaUzAwTnpjeUxXSXpPV0V0Wm1NMFpUUm1OV0l5TTJFMw; GSESSIONID=undefined; gdsid=1665993511833:1666012504494:3A6ACB5518DD49990AD8B928A8500ECF; amp_bfd0a9=JKImedgy7bOzlPc5h3rgAb...1gfj1aqqo.1gfj1aqr7.2.0.2; _ga_RJF0GNZNXE=GS1.1.1666012503.2.1.1666012507.56.0.0; __gads=ID=3a7484feb804561b:T=1666012507:S=ALNI_Mb1WhsyKIJBAVKAgU0v6qmj8v00Ng; __gpi=UID=00000b12871b555d:T=1666012507:RT=1666012507:S=ALNI_Mb2u8VOrEcBS5Lx0glxhJgxhieqGw; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Oct+17+2022+14%3A15%3A07+GMT%2B0100+(British+Summer+Time)&version=202209.2.0&isIABGlobal=false&hosts=&consentId=e9e1457d-1ef4-4779-a9b8-e8cce33210bd&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=GB%3BENG&AwaitingReconsent=false; AWSALB=z26sTrfm1BBU706tjb5NNQqABHqZY+f8jZQL7lgtne2nbztGvQpt4iWF1O/qpNW2RJsA19/fT+eGJA35Z1kbsgOErauFKUlbiIKiL+1/VwS3GBozibXuP9ysLUzr; AWSALBCORS=z26sTrfm1BBU706tjb5NNQqABHqZY+f8jZQL7lgtne2nbztGvQpt4iWF1O/qpNW2RJsA19/fT+eGJA35Z1kbsgOErauFKUlbiIKiL+1/VwS3GBozibXuP9ysLUzr; JSESSIONID=9BE9D351BC2D3AB7FA6070812700747A; cass=0; _ga=GA1.2.243230694.1665993513; __cf_bm=YY30hP1uBkfNCNT_x3WhJ7orBSFUH1UG0dociD9wwJ8-1666014915-0-AbVTDVVC1b/87MWZNkTZsYAWtWcjgufpxTWm89O8cB31pFHc6XVKpzo1r83gTn19pQdJsScI8oyL6fawJ3KLsYk=; _ga_RC95PMVB3H=GS1.1.1666014915.3.0.1666014915.60.0.0',
#     'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
#     }
#
#     params = {
#     'overall_rating_low': '3',
#     'page': str(y),
#     #'sector': '10005',
#     'industry':'200021',
#     'filterType': 'RATING_OVERALL',
#     }
#
#     #overview url, can loop through page in params
#
#
#     response = requests.get('https://www.glassdoor.com/Explore/browse-companies.htm', params=params, headers=headers)
#     soup = BeautifulSoup(response.text, 'lxml')
#
#     script = soup.find('script')
#
#     text = script.text
#     URLs = link_find(text)
#     temp = []
#     print(URLs, "\n if all URLs are null and this isn't the last page, you have been blocked. Retry if so")
#     for i in range(len(URLs)):
#         ProfileURLs.append(URLs[i])
#         temp.append(URLs[i])
#     df = pd.DataFrame(temp, columns=columnslist)
#     df.to_csv('glassdoor_profiles.csv', encoding='utf-8-sig', index=False, mode='a', header=False)
#     print("Just fetched profiles from page number: ", y, " now sleeping for some seconds")
#     time.sleep(2)


def profile_fetch(params=None, headers=None, pages=None, filename=None, resume=False, startpage=None):
    if startpage == None:
        startpage = 1
    RANGE = range(startpage,pages+1,1)

    ProfileURLs = []
    alldata = []
    columnslist = ["Profile URL"]

    # Comment the below 2 lines out if you are continuing with a job, change the range below as appropriate
    if resume==False:
        empty = pd.DataFrame(alldata, columns=columnslist)
        empty.to_csv(filename, encoding='utf-8-sig', index=False)
    for y in RANGE:
        # Change headers as required, add proxies if needed
        # For different categories, headers must be updated, sectors tag is what controls it
        params['page'] = str(y)
        response = requests.get('https://www.glassdoor.com/Explore/browse-companies.htm', params=params,
                                headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        script = soup.find('script')

        text = script.text
        URLs = link_find(text)
        temp = []
        print(URLs, "\n if all URLs are null and this isn't the last page, you have been blocked. Retry if so")
        for i in range(len(URLs)):
            ProfileURLs.append(URLs[i])
            temp.append(URLs[i])
        df = pd.DataFrame(temp, columns=columnslist)
        df.to_csv(filename, encoding='utf-8-sig', index=False, mode='a', header=False)
        sleepnum = random.randint(1,4)
        print("Just fetched profiles from page number: ", y, " now sleeping for ", sleepnum ," seconds")
        time.sleep(sleepnum)


pause = input("Usage information: open up the glassdoor URL from the queue into your browser (this only works for searches that only filter by sector), go to the last page to check the max pages. Press Enter to continue")
pause = input("Now, reload the page with the networks tab open, you should see a result along the lines of sodar?sv=... in there. Right click: copy all as curl bash. Press Enter to continue")
pause = input("To check this is right your converted curl bash should have headers AND params, you need both of these or the script won't work. Press Enter to continue")
pause = input("Now put your headers and params in dictionary format into to correct text files, delete the commented sections from headers")
pause = input("--------------------------- Following this are your inputs, double check before entering or you'll have to restart ---------------------")

#retrieve headers etc.
with open('headers.txt') as f:
    data = f.read()
headers = ast.literal_eval(data)
with open('params.txt') as f:
    data = f.read()
params = ast.literal_eval(data)
filename = input("Please give your full filename for storing the profiles excluding the extension (.csv): ")
pages = int(input("Give the maximum amount of pages you want to crawl, please do not put more than exists: "))
resume = input("If you are not resuming leave this blank. If you are type something e.g 'aaaaaa': ")

filename = filename + '_profiles.csv'
if resume:
    resume = True
    startpage = int(input("Since you are resuming please put the number of the page you are resuming from: "))
    profile_fetch(params, headers, pages, filename, resume, startpage)
else:
    resume = False
    profile_fetch(params, headers, pages, filename, resume)
print("Finished!")
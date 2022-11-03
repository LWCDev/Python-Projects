# obtain pagination links
from random import randrange
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Back, Style
import cloudscraper
from time import sleep
import math
colorama.init()
import requests
import time
import pandas as pd
from MongoUtilities import MongoUtilities
import cloudscraper
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from Utilities import Utilities
import glob, shutil, sys, io, re, os
# import getopt
# import pymongo
# from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
from datetime import date, datetime, timedelta
# sql database setup
from sqlalchemy.orm import sessionmaker


# from crud import engine
# from models import pagination_links
def get_auth_url(page):
    soup = BeautifulSoup(page.text, 'lxml')
    meta_tag = soup.select_one('meta[http-equiv="refresh"]')
    meta_content = meta_tag['content']
    meta_content = meta_content.replace("5; URL='", '')
    meta_content = meta_content[:-1]
    new_url = f'https://www.dnb.com{meta_content}'

    return new_url


headers = {
    'authority': 'www.dnb.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.dnb.com/',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': 'SSLB=1; hpVer=coldstate; _st_bid=134b6150-4855-11ec-befc-f7d96f7e476b; cp=0; fs=0; cr=0; tc=0; cs=0; rc=0; ac=0; ii=0; JSESSIONID=node0bkyeccrbi4y014gve2pw8trcs10034052.node0; DMCP=0; SSID=CQDsix0cAAgAAAASIpZhwNUCCBIilmEMAAAAAAAAAAAANF5FYgB-5Z4FAQHr3iIANF5FYgEAVP4AAZpCIgA0XkViAQDR_QAAQcAAAA; SSSC=644.G7031845329024767424.12|65108.2245274:66974.2285291; bm_mi=94394F19BBAB6C555F6D41D5F49F34F5~UO3mBcPHJminMf1lKapqaCH8hDCtDB2uwyRsnEhD8tztRzxx2xcVbUsBQmeUAHDZae33WV5P3zFEd8/cCA0hX17ODQA85YdZ7713KvGJ2Q/4FnscF5rjkIReXaLXwgLcb1Dxztl9ObM2O4tlFwkign043WloPFEhc9MSKrcYf6RiIXb0T0xOm8+nWM60zBYwLe4fhbigF05ARTRhtoUs0VrTymg1vuN2mSOj+op4aYKFmRWBCML/BrT6WBRE7vvr; bm_sv=670F7F308800E34624A567CAA141547C~Qel3KTd583K8e1Y1KmQ0rcxj/rfFtYCjJN66vpoRtO4D4hCp7Em3RTV4UcKdjWMLzb/lMHghCWhfgGBPEDvU4hM5a5Y+mtWNpCLD+O99xyhsY2XyiUM/1uuOZN+0VatL6u6LzEx2JwPHoJlgXZzZCA==; ak_bmsc=496BF468E616678B15D3CE4EE6501F12~000000000000000000000000000000~YAAQKjZ6XHkPcdt/AQAAUvQA3w8XXE8mtE8KZDAzm9+cuBSfBjZkq7hmklxGsZLTjVBV/7FFBves457MHre768iOrnmXsLNLFcu7Yfd1aYqtyGz765KJJsH3U66nh1mIiapGW8k0f9PaYp3nIwllDDLfckjNisqwGBu5wi+MXqOeSr+tLtVxFudXcalDn897ClU501mqTsegmFZSqW2KlCKN5+XhAtxSvTtTI/fVMEXqPXN9i8mw49n7EjgctXYJqH77EPqztembL5aDUKI5GAsLFm5T92yZjLoTafK3Kzc7usV8e3la1b6Pul8wORZIK7m+lhjSa2CQVRnb4P76VE2QDaBmym1X2F5eCW80MCbnmclBVl4gzVluV37curQ5b3SlN0CBrdOo+9x4eh56+j8y0nrNeCapho441L+wcgMkBYD59NzRPo6pXJIJleXHnMVv/NyY9cL2PznNKUAOh2dipou0aHSnZVBZKc96rVHNzMtokBWLNBBY+TwhX4wR; _fbp=fb.1.1648713998864.828634830; _hjSessionUser_1097690=eyJpZCI6IjdhMzU1YmMzLWVlMGEtNWM1ZS04MDA1LTVmMDA4YWJlMGQ3MSIsImNyZWF0ZWQiOjE2NDg3MTM0NDI5NzcsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample=0; _hjSession_1097690=eyJpZCI6IjE3ODE2NGEzLTBiNjctNGU4Yy1hOWU5LTJmZTZhMGU4N2U0YyIsImNyZWF0ZWQiOjE2NDg3MTM5OTg4NzAsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; __exponea_etc__=9ed04f5e-5bf2-46d7-94db-3b593f48a266; _biz_su=a149e876b48f4387bf49c6ca80c7009b; _biz_flagsA=%7B%22Version%22%3A1%2C%22Mkto%22%3A%221%22%2C%22ViewThrough%22%3A%221%22%2C%22Ecid%22%3A%22207759289%22%2C%22XDomain%22%3A%221%22%7D; drift_campaign_refresh=4de7a022-c144-4910-a0a8-df3afd1dc91d; s_cc=true; driftt_aid=8a1e8d14-8c6b-490c-8843-9096ac8ab7b5; drift_aid=8a1e8d14-8c6b-490c-8843-9096ac8ab7b5; w_AID=45603537934615356922952283880890952240; _sp_ses.2291=*; chosen_visitorFrom_cookie_new=DIR; HID=1648714337806; _biz_uid=a149e876b48f4387bf49c6ca80c7009b; _biz_sid=2aef30; _mkto_trk=id:080-UQJ-704&token:_mch-dnb.com-1648714338113-81916; _gcl_au=1.1.980334290.1648714340; _ga=GA1.2.1157053312.1648714340; _gid=GA1.2.90496257.1648714340; __ncuid=8aac2650-b218-4fda-a377-43268fb179e4; nc-previous-guid=009c0ce65cb661cc962b92ece3d6dc8f; _uetsid=cc820da0b0c711ec9afdd370b7914f4c; _uetvid=9adc158079da11ec9f87bfc8febe3c9d; s_nr30=1648714340140-New; __exponea_time2__=-0.6237080097198486; AMCVS_8E4767C25245B0B80A490D4C%40AdobeOrg=1; AMCV_8E4767C25245B0B80A490D4C%40AdobeOrg=-1124106680%7CMCIDTS%7C19083%7CMCMID%7C45603537934615356922952283880890952240%7CMCAAMLH-1649319140%7C6%7CMCAAMB-1649319140%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1648721540s%7CNONE%7CvVersion%7C5.2.0; tbw_bw_uid=bito.AAEfLU7DLEQAACn08QaeMA; tbw_bw_sd=1648714343; _biz_nA=2; s_sq=%5B%5BB%5D%5D; _biz_pendingA=%5B%5D; QSI_HistorySession=https%3A%2F%2Fwww.dnb.com%2F~1648714011089%7Chttps%3A%2F%2Fwww.dnb.com%2Fbusiness-directory.html%23CompanyProfilesPageNumber%3D1%26ContactProfilesPageNumber%3D1%26DAndBMarketplacePageNumber%3D1%26IndustryPageNumber%3D1%26SiteContentPageNumber%3D1%26tab%3DCompany%2520Profiles~1648714354717; SSRT=K2NFYgADAA; SSOD=AGfhAAAAJAAjzDMAcAAAABIilmEtY0ViCgCMP04AcgAAABIilmEtY0ViCgAAAA; _sp_id.2291=6da9421e-049c-4157-801c-76b0fd936f6b.1648714028.1.1648714553..50aafa86-03a4-4544-97c2-724a89c560f9; _st_l=38.600|8662583217,8662581809,,+18662581809,0,1648715494.8664733932,8442195784,,+18442195784,0,1644498725.8005269018,8442394778,,+18442394778,0,1648714934|3227194611.1280320722.73494997016.8682373733.2022012537.7871150595.9912000545.66912594774.6668218245.3280094956.3222011166.0785111626.84702131041.3223706450.82760396527.4328319936.58799001399.7701971405.1903608662.1290559275; _st=134b6150-4855-11ec-befc-f7d96f7e476b.cd7e4df0-b0c7-11ec-b474-9bf10a8a227f....0....1648715494.1648725148.600.10800.30.0....1....1.10,11..dnb^com.UA-18184345-1.840156974^1637229076.38.; RT="z=1&dm=www.dnb.com&si=ace5628d-00eb-4d26-a3ae-526cd1858e11&ss=l1epb7dc&sl=7&tt=ew8&bcn=%2F%2F684dd32a.akstat.io%2F&obo=4&rl=1&ld=ywwi&r=csi2n9ee&ul=ywwj"; _gat_ncAudienceInsightsGa=1',
}


# Session = sessionmaker(bind=engine)
# s = Session()
def proxy_check(default, bad):
    failures = []
    proxies = []
    for fail in bad:
        failures.append(fail.strip().replace('\n', ''))
    for content in default:
        # content = content.strip('\n')
        splits = content.strip().split(":")
        try:
            proxy_str = f"{splits[2]}:{splits[3]}@{splits[0]}:{splits[1]}"
            if proxy_str in failures:
                print("Skipping a bad proxy: ", proxy_str)
                continue
            proxy = {'http': 'http://' + proxy_str,
                     'https': 'https://' + proxy_str}
            # print(proxy_str)
            proxies.append(proxy)
        except Exception as e:
            # print(e)
            # print(splits)
            pass
    return (proxies)


with open('C:/Users/lewis.welshclark/PycharmProjects/Projects/dnb_proxies3.txt') as f:
    contents = f.readlines()
with open('C:/Users/lewis.welshclark/PycharmProjects/Projects/Lewis/DNB/failedproxies.txt') as f:
    failed = f.readlines()
# with open('/Lewis/DNB/urls.txt') as f:
#     start_urls = f.readlines()
# with open('/Lewis/DNB/urllayers.txt') as f:
#     layers = f.readlines()

# proxy_list = [
#     "https://151.181.91.10:80",
#     "https://200.105.215.18:33630",
#     "https://149.129.239.170:8080",
#     "https://147.253.214.60:57114",
#     "https:/172.104.252.86:80",
#     "https://47.254.237.222:8080",
#     "https://178.79.138.2536:8080",
#     "https://139.59.88.145:8888"
#     "https://105.27.130.22:9812",
#     "https://185.193.17.174:3128",
#     "https://139.59.88.145:8888",
#     "https://47.252.1.180:3128",
#     "https://171.5.133.242:8080"
# ]
proxy_list = proxy_check(contents, failed)

def get_country_origin(url, headers, timeout, proxy):
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url, headers=headers, timeout=timeout, proxies=proxy)
    new_url = get_auth_url(page)
    print(new_url)
    time.sleep(40)
    page2 = scraper.get(new_url, headers=headers, timeout=timeout, proxies=proxy)
    soup = BeautifulSoup(page2.text, 'lxml')
    section = soup.find('div', class_="industryCountryCrawlWrapper")
    href_links = section.find_all('a', href=True)
    URLs = []

    for href in href_links:
        URLs.append(('https://www.dnb.com' + href['href'], 0, 0))
    df = pd.DataFrame(data=URLs, columns=['url', 'in_progress', 'failed'])
    MongoUtilities.pandas_to_mongo(df, db=db2, collection="search_urls", keys=['url'])
    print(URLs)
    print(len(URLs))



def dnb_search(failist, proxy_list, headers, db2):
    start_length = len(failist)
    for url in failist:
        print("On loop: ", failist.index(url))
        loopnum = failist.index(url)
        proxy = random.choice(proxy_list)
        scraper = cloudscraper.create_scraper()
        print("Trying now on: ", url)
        try:
            page = scraper.get(url, headers=headers, timeout=30, proxies=proxy)
            try:
                new_url = get_auth_url(page)
                print("Sleeping for 40")#, new_url)
                time.sleep(40)
                print("%"*20+"Past sleep"+"%"*20)
                page = scraper.get(new_url, headers=headers, timeout=30, proxies=proxy)
                soup = BeautifulSoup(page.text, 'lxml')
                try:
                    section = soup.find_all('div', class_='title', href=False)
                    db2.search_urls.update_one({'url': {'$in': [url]}}, {'$set': {'in_progress': 1, 'failed': 0}},
                                               upsert=True)
                    print("On div searcher")
                    for div in section:
                        print("Searching through divs...", section.index(div))
                        if 'State/Province' in div.text:
                            layer_level = 2
                            spare = url + ''
                            spare = spare.replace('https://www.dnb.com/business-directory/company-information.', '')
                            print(spare)
                            country = spare[spare.index('.') + 1:spare.index('.') + 3]
                            dic = {'url': url,
                                   'layer': layer_level,
                                   'country': country,
                                   'sector': spare[:spare.index('.')].replace("_", " "),
                                   'in_progress': 0,
                                   'complete': 0,
                                   'failed': 0}
                            loh.append(dic)
                            failist.remove(url)
                            db2.search_urls.update_one({'url': {'$in': [url]}},
                                                       {'$set': {'complete': 1, 'failed': 0, 'in_progress': 0}}
                                                       , upsert=True)
                            data = (url, layer_level, country,
                                    spare[:spare.index('.')].replace("_", " "), 0, 0, 0)
                            df = pd.DataFrame(data=[data],
                                              columns=['url', 'layer', 'country', 'sector', 'in_progress',
                                                       'complete', 'failed'])
                            MongoUtilities.pandas_to_mongo(df, db=db2, collection="country_urls", keys=['url'])
                            break
                        elif 'Town' in div.text:
                            layer_level = 1
                            spare = url + ''
                            spare = spare.replace('https://www.dnb.com/business-directory/company-information.', '')
                            print(spare)
                            country = spare[spare.index('.') + 1:spare.index('.') + 3]
                            dic = {'url': url,
                                   'layer': layer_level,
                                   'country': country,
                                   'sector': spare[:spare.index('.')].replace("_", " "),
                                   'in_progress': 0,
                                   'complete': 0,
                                   'failed': 0}
                            loh.append(dic)
                            failist.remove(url)
                            db2.search_urls.update_one({'url': {'$in': [url]}},
                                                       {'$set': {'complete': 1, 'failed': 0, 'in_progress': 0}},
                                                       upsert=True)
                            data = (url, layer_level, country,
                                                    spare[:spare.index('.')].replace("_", " "), 0, 0, 0)
                            df = pd.DataFrame(data=[data],
                                              columns=['url', 'layer', 'country', 'sector', 'in_progress',
                                                       'complete', 'failed'])
                            MongoUtilities.pandas_to_mongo(df, db=db2, collection="country_urls", keys=['url'])
                            break
                except Exception as e:
                    print("Error in section stage", url, e)
                    db2.search_urls.update_one({'url': {'$in': [url]}},
                                               {'$set': {'in_progress': 0, 'complete': 0, 'failed': 1}},
                                               upsert=True)
                    continue
            except Exception as e:
                print("Error in soup stage", print(e), url)
                db2.search_urls.update_one({'url': {'$in': [url]}},
                                           {'$set': {'in_progress': 0, 'complete': 0, 'failed': 1}}, upsert=True)
                continue
        except Exception as e:
            print("Error in get_auth_url", url, e)
            db2.search_urls.update_one({'url': {'$in': [url]}},
                                       {'$set': {'in_progress': 0, 'complete': 0, 'failed': 1}}, upsert=True)
            continue
        print("Current list left to do ---------------")
        print("%"*20, "Currently remaining jobs to do:", len(failist), "%"*20)
        print("%"*20,"Successful so far = ", start_length-len(failist),"%"*20)
        print("%"*20,"Failed so far: ", loopnum-(start_length-len(failist)),"%"*20,)
        # break
    # failist = []
    print(loh)








# run as many times as you need to get all the stuff

if __name__ == "__main__":
    database_name = "dnb_healthcare_search_urls"

    # The only reason for ssetting up an instance of ExtractURL here is to get the databasename from the template file
    # A different instance will be set up later to do the main work

    # Check lock and set if not set. Returns false if this program is to carry on running
    system_name = Utilities.detect_system().hostname
    returns = MongoUtilities.check_lock(database_name, f'{system_name}_search_scrape_lock')
    if returns['locked']:
        print(Fore.CYAN + 'Nothing will happen as a task is still running from a previous invocation')
        print(
            'If this is not the case then you will need to delete the lock record in database ' + str(
                database_name) + Style.RESET_ALL)
    else:
        # We go off to main with inlist=None and parameters=None so we take the parameters which includes inlist
        # from the template file
        start_time = time.time()
        db2 = MongoUtilities.mongo_connect(database=database_name)
        #homepage = 'https://www.dnb.com/business-directory/industry-analysis.health_care_and_social_assistance.html'
        homepage = 'https://www.dnb.com/business-directory/industry-analysis.psychiatric_and_substance_abuse_hospitals.html'
        proxy2 = random.choice(proxy_list)
        # Comment the below try and except out if you have existing data already
        # try:
        #     get_country_origin(homepage, headers=headers, proxy=proxy2, timeout=30)
        # except:
        #     print("Failure in trying to access webpage, trying to rely on an existing database")
        loh = []
        df_urls = pd.DataFrame(
            list(db2.search_urls.find({'complete': {'$ne': 1}})))
        url_list = list(set(df_urls["url"].to_list()))
        failist = url_list
        if len(failist) == 0:
            print("Nothing to do, everything is complete!")
            quit()
        #print(failist, '\n', len(failist))
        dnb_search(failist, proxy_list=proxy_list, headers=headers, db2=db2)



        end_time = time.time()
        time_taken = timedelta(seconds=int(f'{math.ceil(int(end_time - start_time))}'))
        print(f'Time taken: {time_taken}')

        MongoUtilities.delete_lock(database_name, f'{system_name}_search_scrape_lock')
        print("Lock should be removed")
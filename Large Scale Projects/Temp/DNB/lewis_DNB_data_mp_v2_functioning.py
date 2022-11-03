# from PandasClean import Clean_Utilities
# from dataenhance import PostCode, CompanyData
import cloudscraper

from Multiproc import MultiProcess
import multiprocessing as mp
from multiprocessing import Manager, freeze_support
import queue
import pandas as pd
import json
# import numpy as np
# import pprint
import time
from typing import List, Dict, Tuple
# from copy import deepcopy
from MongoUtilities import MongoUtilities
from Utilities import Utilities
import glob, shutil, sys, io, re, os
# import getopt
# import pymongo
# from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
from datetime import date, datetime, timedelta
# from bson.json_util import loads
# from collections import Counter
import urllib3
import requests
from bs4 import BeautifulSoup as BS
# import json
import random

# Page 3
#Actually scrapes the data from the firm profiles that have been fetched by profiles and pages scripts
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from urllib.parse import urlparse
import math
from time import sleep

# import mysql.connector as mariadb
import pymysql

pymysql.install_as_MySQLdb()

import colorama
from colorama import Fore, Back, Style

colorama.init()

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
    return(proxies)
class KompassScrape(MultiProcess):

    def __init__(self, parameters=None):
        if parameters:
            self.parameters = parameters
            self.database_name = parameters['database_name']
            # self.parameters["central_mongoDB"] = self.database_name
        self.db = MongoUtilities.mongo_connect(self.database_name)
        self.lum_proxies = {'http': 'http://lum-customer-ai-zone-static:uvc1vshl7xhi@zproxy.lum-superproxy.io:22225',
                            'https': 'https://lum-customer-ai-zone-static:uvc1vshl7xhi@zproxy.lum-superproxy.io:22225'}
        with open('C:/Users/lewis.welshclark/PycharmProjects/Projects/dnb_proxies3.txt') as f:
            contents = f.readlines()
        with open('C:/Users/lewis.welshclark/PycharmProjects/Projects/Lewis/DNB/failedproxies.txt') as f:
            failed = f.readlines()
        # self.proxies = [content.strip("\n") for content in contents]
        proxies = proxy_check(contents, failed)
        self.proxies = proxies
        # ua = UserAgent()
        self.headers = {
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
        super().__init__()

        return
    # Resetting database connection to prevent pickle bug
    def __getstate__(self):
        attributes = self.__dict__.copy()
        del attributes['db']
        return attributes
    # Same as with the other files, takes in parameters from mongo
    def get_input_records(self, inlist=None, **kwargs):

        batch_size = 50000

        params = {'in_progress': 0, 'failed': 0, 'complete': 0,
                  '$or': [{'og_url': {'$regex': ".*business.*"}},
                          {'og_url': {'$regex': ".*business.*"}}]
                  }
        #cursor = self.db.profile_urls.find(params, {'in_progress': 0, 'failed': 0, 'complete': 0}).limit(batch_size)
        cursor = self.db.profile_urls.find({'complete': {'$ne': 1}}).limit(batch_size)

        self.queue_list = list(cursor)
        x = 9

        return
    # Rebuilding the URL same as in profiles, this loads the firm profile page and scrapes all the data
    # using beautiful soup and cloudscraper to reach the page content
    # Functionally the same as any basic scraper script, look at all the CSS selectors etc.
    def subtask(self, i, url_queue, result_queue, done_queue, **kwargs):
        def get_profile_data(profile_info, headers, db, proxies=None):
            if proxies is None:
                proxies = self.proxies
            db.profile_urls.update_one(profile_info, {'$set': {'failed': 0}})
            def get_auth_url(page):
                soup = BS(page.text, 'lxml')
                meta_tag = soup.select_one('meta[http-equiv="refresh"]')
                meta_content = meta_tag['content']
                meta_content = meta_content.replace("5; URL='", '')
                meta_content = meta_content[:-1]
                new_url = f'https://www.dnb.com{meta_content}'

                return new_url

            loh = []
            random_proxy = random.choice(proxies)
            # proxy = {'https': f'https://{random_proxy}', 'http': f'http://{random_proxy}'}
            scraper = cloudscraper.create_scraper()
            try:
                check = requests.get(profile_info['profile_url'], headers=headers, timeout=30, proxies=random_proxy)
                page = scraper.get(profile_info['profile_url'], headers=headers, timeout=30, proxies=random_proxy)
            except requests.exceptions.Timeout:
                print("page failed due to timeout/request not authorised")
                print(profile_info['profile_url'])
                db.profile_urls.update_one(profile_info, {'$set': {'in_progress': 0, 'failed': 1, 'err': 1}})
                return loh
            except requests.exceptions.ProxyError:
                # print("page failed dueru to proxy")
                print(random_proxy)
                badproxy = random_proxy['http']
                badproxy = badproxy.replace('http://', '')
                with open("C:/Users/lewis.welshclark/PycharmProjects/Projects/Lewis/DNB/failedproxies.txt", "r") as file_object:
                    # Text file showing bad proxies
                    lines = file_object.readlines()
                with open("C:/Users/lewis.welshclark/PycharmProjects/Projects/Lewis/DNB/failedproxies.txt","a") as file_object:
                    if badproxy and badproxy not in lines:
                        file_object.write(badproxy + '\n')
                self.proxies.remove(random_proxy)
                # print(e)
                print('page failed/proxy error')
                print(profile_info['profile_url'])
                db.page_urls.update_one(profile_info, {'$set': {'in_progress': 0, 'failed': 1, 'err': 0}})
                return loh
            except Exception as e:
                print(e)
                print('page failed')
                print(profile_info['profile_url'])
                db.page_urls.update_one(profile_info, {'$set': {'in_progress': 0, 'failed': 1, 'err': 1}})
                return loh
            try:
                new_url = get_auth_url(page)
                sleep(40)
                page = scraper.get(new_url, headers=headers, timeout=30, proxies=random_proxy)
            except:
                print('page failed in get_auth function')
                db.profile_urls.update_one(profile_info, {'$set': {'in_progress': 0, 'failed': 1, 'err': 1}})
                return loh
            if page.status_code != 200:
                print('page connecting error')
                db.profile_urls.update_one(profile_info, {'$set': {'in_progress': 0, 'complete': 1}})
                return loh
            if page.url == "https://www.dnb.com/business-directory.html":
                print('page redirects')
                db.profile_urls.update_one(profile_info, {'$set': {'in_progress': 0, 'complete': 1}})
                return loh
            soup = BS(page.text, 'lxml')
            try:
                script = soup.select_one('body > script[type="application/ld+json"]')
                script_string = script.string
                json_data = json.loads(script_string)
            except:
                json_data = None
            if json_data:
                try:
                    firm = json_data['name']
                except:
                    print('no firm')
                    db.profile_urls.update_one(profile_info, {'$set': {'in_progress': 0, 'failed': 1, 'err': 1}})
                    return loh
                try:
                    company_type = json_data['@type']
                except:
                    company_type = ""
                try:
                    address1 = json_data['address']['streetAddress']
                except:
                    address1 = ""
                try:
                    city = json_data['address']['addressLocality']
                except:
                    city = ""
                try:
                    state = json_data['address']['addressRegion']
                except:
                    state = ""
                try:
                    postcode = json_data['address']['postalCode']
                except:
                    postcode = ""
                try:
                    country = json_data['address']['addressCountry']
                except:
                    country = ""
                try:
                    comp_url = json_data['url']
                except:
                    comp_url = ""
                try:
                    name = json_data['employee'][0]['name']
                except:
                    name = ""
                try:
                    job_title = json_data['employee'][0]['jobTitle']
                except:
                    job_title = ""
                try:
                    company_size = json_data['numberofEmployees']
                except:
                    company_size = ""
                try:
                    description = json_data['description']
                except:
                    description = ""
                sectors = soup.select('span[name="industry_links"] span span')
                try:
                    sector1 = sectors[0].text.strip()[:-1].strip()
                except:
                    sector1 = ""
                try:
                    sector2 = sectors[1].text.strip()[:-1].strip()
                except:
                    sector2 = ""
                try:
                    sector3 = sectors[2].text.strip()[:-1].strip()
                except:
                    sector3 = ""
            else:
                firm_tag = soup.select_one("div.company-profile-header-title")
                if firm_tag:
                    firm = firm_tag.text.strip()
                else:
                    print('no firm')
                    db.profile_urls.update_one(profile_info, {'$set': {'in_progress': 0, 'failed': 1, 'err': 1}})
                    return loh
                company_type = ""
                address1_tag = soup.select_one('span[name="company_address"] span')
                address1 = address1_tag.text.strip() if address1_tag else ""
                address_split = address1.split('*')
                address1 = address_split[0].strip()
                city = ""
                state = ""
                postcode = ""
                country = ""
                url_tag = soup.select_one("a.company-website-url")
                comp_url = url_tag['href'] if url_tag else ""
                employee_tag = soup.select_one("li.employee")
                if employee_tag:
                    name_tag = employee_tag.select_one("div.name")
                    name = name_tag.text.strip() if name_tag else ""
                    job_title_tag = soup.select_one('div[itemprop="jobTitle"]')
                    job_title = job_title_tag.text.strip() if job_title_tag else ""
                else:
                    name = ""
                    job_title = ""
                company_size_tag = soup.select_one('span[name*="employees_"] span')
                company_size = company_size_tag.text.strip() if company_size_tag else ""
                description_tag = soup.select_one('span[name="company_description"] span')
                description = description_tag.text.strip() if description_tag else ""
                sectors = soup.select('span[name="industry_links"] span span')
                if len(sectors) > 0:
                    try:
                        sector1 = sectors[0].text.strip()[:-1].strip()
                    except:
                        sector1 = ""
                    try:
                        sector2 = sectors[1].text.strip()[:-1].strip()
                    except:
                        sector2 = ""
                    try:
                        sector3 = sectors[2].text.strip()[:-1].strip()
                    except:
                        sector3 = ""
                else:
                    sector1 = ""
                    sector2 = ""
                    sector3 = ""
            phone_tag = soup.select_one('span[name="company_phone"] span')
            phone = phone_tag.text.strip() if phone_tag else ""
            rev_tag = soup.select_one('span[name="revenue_in_us_dollar"] span')
            rev = rev_tag.text.strip() if rev_tag else ""
            year_founded_tag = soup.select_one('span[name="year_started"] span')
            year_founded = year_founded_tag.text.strip() if year_founded_tag else ""
            # Creates a dictionary with the scraped data and appends it to a list of dictionaries
            result = {'Source': 'dnb.com', 'Firm': firm, 'Company Type': company_type, 'Address Line 1': address1,
                      'City': city, 'State Or County': state, 'Postal Code': postcode, 'Country': country,
                      'URL': comp_url, 'Name': name, 'Job Title': job_title, 'Company Size': company_size,
                      'Description': description, 'Business Sector 1': sector1, 'Business Sector 2': sector2,
                      'Business Sector 3': sector3, 'Telephone Number': phone, 'Annual Revenue': rev,
                      'Year Founded': year_founded}
            # OR operator |=, if either result or profile info is true, result becomes True
            result |= profile_info
            loh.append(result)
            return loh

        db = MongoUtilities.mongo_connect(database="dnb_profiles")
        print(f"Process {i} started\n")
        while True:
            try:
                profile_info = url_queue.get(True, 5)
                # print(f'"Process {i} just retrieved {url} from input queue')
            except queue.Empty:
                print(f"Process {i} found no link. Finishing.")
                done_queue.put_nowait(i)
                return

            # print(proxy)

            loh = get_profile_data(profile_info=profile_info, headers=self.headers, db=db, proxies=None)

            result_queue.put(loh)
    # Payload committing to database same as in pages and profiles
    def payload(self, loh: List[Dict], **kwargs):
        try:
            headings = ['Source', 'Firm', 'Company Type', 'Address Line 1', 'City', 'State Or County', 'Postal Code',
                        'Country', 'URL', 'Name', 'Job Title', 'Company Size', 'Description', 'Business Sector 1',
                        'Business Sector 2', 'Business Sector 3', 'Telephone Number', 'Annual Revenue', 'Year Founded',
                        'profile_url', 'og_url']
            # db = MongoUtilities.mongo_connect(database="findit_and_drectory_scrape")
            df_loh = pd.DataFrame(data=loh)
            columns_to_drop = [col for col in df_loh.columns if col not in headings]
            df_loh_u = df_loh.drop(columns=columns_to_drop)
            #central_db = MongoUtilities.mongo_connect(database="JRS_DO_NOT_DELETE", hostname='ai-sql')
            central_db = MongoUtilities.mongo_connect(database="dnb_data")
            MongoUtilities.pandas_to_mongo(df_loh_u, db=central_db, collection="dnb_scraped_data", keys=['Firm', 'URL', 'City'])

            og_id_list = list(set(df_loh["_id"].to_list()))
            self.db.profile_urls.update_many({'_id': {'$in': og_id_list}}, {'$set': {'in_progress': 0, 'complete': 1}})
        except Exception as e:
            print("Error writing to database")
            print(e)
            print(f"{loh=}")
        # else:
        #     if not df_loh.empty:
        #         df_loh_bad = df_loh.loc[df_loh['scrape_err_status'] == 3]
        #         """collects results where urls failed"""
        #         df_loh_good = df_loh.loc[df_loh['scrape_err_status'] != 3]
        #         """collects results that are fine"""
        #         if not df_loh_good.empty:
        #             MongoUtilities.pandas_to_mongo(df_loh_good, db=db, collection="company_data",
        #                                            keys=['profile_url'])
        #             og_url_list = list(set(df_loh_good["profile_link"].to_list()))
        #             db.profile_urls.update_many({'profile_url': {'$in': og_url_list}},
        #                                         {'$set': {'in_progress': 0, 'complete': 1}})
        #             """updates data_collected to 1, so other machines avoid. Also leaves in_progress as 1"""
        #         if not df_loh_bad.empty:
        #             og_url_list = list(set(df_loh_bad["profile_link"].to_list()))
        #             db.profile_urls.update_many({'url': {'$in': og_url_list}},
        #                                         {'$set': {'in_progress': 0, 'data_collected': 0}})
        #             """updates in_progress to 0, so it can be run another time"""

        """
        At this stage we have these possibilities:

        in_progress: 0 and data_collected: 1 - It has done everything we were expecting
        in_progress: 0 and data_collected: 0 - something failed in the subtask, can be returned back to
        in_progress: 1 and data_collected: 0 - the master must have timed out, but we can come back to these links...
        ...when all urls have been processed
        """
        return


def main(inlist=None, database_name=None):
    # main the same as pages and profiles
    freeze_support()
    num_processes = 10
    batch_size = 50000

    url_queue = mp.Queue()  # Queue for Visiting Page
    result_queue = mp.Queue()  # Queue for handling results ready to write
    done_queue = mp.Queue()  # Queue for completed tasks

    # extract_url = ExtractURLs()
    parameters = {"database_name": database_name, 'local_mongoDB': 'dnb_profiles'}
    kwargs = {'timeout': 40, 'batch_size': batch_size}
    KompassScrape(parameters=parameters).multi_main(num_processes=num_processes, inlist=inlist, kwargs=kwargs)
    return

    #########################################################################################
    #                               Bug where url is http: or https:                        #
    #########################################################################################

# same as others
if __name__ == '__main__':
    start_time = time.time()
    # The only reason for ssetting up an instance of ExtractURL here is to get the databasename from the template file
    # A different instance will be set up later to do the main work
    database_name = "dnb_profiles"

    # Check lock and set if not set. Returns false if this program is to carry on running
    system_name = Utilities.detect_system().hostname
    returns = MongoUtilities.check_lock(database_name, f'{system_name}_scrape_lock')
    if returns['locked']:
       print(Fore.CYAN + 'Nothing will happen as a task is still running from a previous invocation')
       print(
           'If this is not the case then you will need to delete the lock record in database ' + str(database_name) + Style.RESET_ALL)
    else:
        # We go off to main with inlist=None and parameters=None so we take the parameters which includes inlist
        # from the template file
        main(database_name=database_name)

        end_time = time.time()
        time_taken = timedelta(seconds=int(f'{math.ceil(int(end_time - start_time))}'))
        print(f'Time taken: {time_taken}')
        print("Lock should be removed")
        MongoUtilities.delete_lock(database_name, f'{system_name}_scrape_lock')


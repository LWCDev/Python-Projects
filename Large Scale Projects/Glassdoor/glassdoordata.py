from PandasClean import Clean_Utilities
from Multiproc import MultiProcess
import multiprocessing as mp
from multiprocessing import Manager, freeze_support
import queue
import pandas as pd

import time
from typing import List, Dict, Tuple
from MongoUtilities import MongoUtilities
from Utilities import Utilities
import glob, shutil, sys, io, re, os
from datetime import date, datetime, timedelta
import random
import urllib3
import requests
from bs4 import BeautifulSoup
import ast
instruct = input("Place the CSV file containing all the glassdoor profiles you want to scrape into the same folder as "
                 "this script")
filename = input("Give the full filename including extension of the csv you want to open, do not include quotes: ")
ProfileURLs = pd.read_csv(filename, usecols=['Profile URL'])
ProfileURLs = ProfileURLs.values.tolist()

alldata = []
columnslist = ['URL', 'Firm']
#empty = pd.DataFrame(alldata, columns=columnslist)
#empty.to_csv('glassdoor_1.csv', encoding='utf-8-sig', index=False)



def data_scrape(text):

    URL = 'null'
    Firm = 'null'


    try:
        URLstart = text.index('sameAs')
        #print(URLstart)
        text = text[URLstart:]
        #print(text)
        URLstart = text.index('sameAs')
        URLstart = URLstart + 10
        URLend = text.index(',')
        URLend = URLend - 1
        #print(URLend)
        URL = text[URLstart:URLend]
        print(URL)
        URL= URL.strip().replace("\n","").replace("\t", "")
        text = text[URLend:]
    except:
        URLstart = text.index('sameAs')
        text = text[URLstart+6:]
        URL = 'null'
    try:
        Firmstart = text.index(":")
        Firmend = text.index("}")
        Firm = text[Firmstart+3:Firmend-1]
        Firm = Firm.strip().replace("\n","").replace("\t", "").replace('"',"").replace("'", '')
    except:
        URL = 'null'
    return(URL, Firm)
cookies = {
    'G_AUTHUSER_H': '0',
    'gdId': 'dcce75de-93ae-4ded-b53e-ad27e715c9fa',
    'rttdf': 'true',
    '_gid': 'GA1.3.1263127479.1665993554',
    'G_ENABLED_IDPS': 'google',
    'OptanonAlertBoxClosed': '2022-10-17T14:08:23.789Z',
    '_optionalConsent': 'true',
    '_gcl_au': '1.1.531160811.1666015704',
    '_fbp': 'fb.2.1666015704575.460910404',
    'fpvc': '2',
    '__gads': 'ID=6606425e7c3c14dd:T=1666015711:S=ALNI_MZb37xQfa5M8Wv1zCIUqxO5Vzz1nA',
    'uc': '8013A8318C98C517A13DCFFA6EA4511D706518462668B9641710794A5051CE354FA0632071C465A57F14058698632B3298839D946CA6F658E10BDFA2416795248B940EDED9A02E9797FF0803451628D8799E910083E0AD7A687EB3C5EB2022EA9BCADB21D7612B051AB135E33AB09451520A5A4EC8239ECF3E09ADEF1CB714F68C6399561EE99CA744C801BCE9C5AE38',
    'trs': 'direct:direct:direct:2021-10-21+07%3A24%3A32.043:undefined:undefined',
    'ki_t': '1666021213461%3B1666021213461%3B1666021213461%3B1%3B1',
    'ki_r': '',
    'GSESSIONID': 'dcce75de-93ae-4ded-b53e-ad27e715c9fa+1666082044800',
    'cass': '1',
    '__gpi': 'UID=00000b128a6c7103:T=1666015711:RT=1666082050:S=ALNI_MZKmRxWscbVh3VSG3Gdo8Pu8jHQKQ',
    'gdsid': '1666082044800:1666085752683:7EABE15D9F01A4F4F718E597F55747B8',
    'at': 'lfw4tT16moWJYly5NjnnLsVEIjhmXGQWEx-Su9FUqUlkzB5lhjiZRWSawJKEAk03DB6Eue9_leGPHhKPPkr-09ZZR5uX-sqBZ39IaYWeCryD510KBksnbZtUxo-hFf0RUsCKAfcTfOjqWHrWSmgZPG_KM4U1mc-TnBpb0d8ydV0YKibwOYONSRD9214XYrt2HM8EPmoeku8L76_nKkxf4CfSOpux-FIVDu1n1Pmf2i-SIK3VLhN6WEI_WV1j4Eaw3cr0kgaWerZrsZWN7WoQQjJAc91eqFf6bdV50eSdv0TtuMrSTeJCK95tbzyndxIZY4fLAGGJj0N4tZnDJuqyGUh5l0PggpLK21PQbrrN9J6JCa_3NCZIX8hu_2oGIe3ATPxSvZYoc1PRo384jZIscxoIYvuuVh9p2wNXIoi9uN3mvg94hHi0j-5UtWuZAorXZVuPq8Sxcy2SGudW7u8eCUWui5qOWuOGTFlbUKTzQcBiAjuZZ-6r1fQ23Foyugdea_W0HAzXQixWjWwilSr6wDFCzUpZvRCwtIjmkJt6JHer_dJVH_uz9RqBglidcyoz82QE2a1wO34_wYDOMY0p8X3EfPuv_qM40514H093owfiSJaGjf7nPUTNTtXH-sXXiTh54LUEw9y40ZYJZ5KYZQ0pV31FzkqfP2aLPlcbJvWumQ9dkEnAKXp5zROu57ZSSucukbLp8rhvpGfUxFRs4VxrJRjjLDNYoQn-t3LKrimsBfFFKCz0pZjYKHEfJaneVuR6dPIxKJNpO3J1JSKyWkJ8AsyXwyqxIzkryuixZL2xNS10InYkL20TMpG2qNHGn2X1XtYiWtk07Dx0CMlr2ow59E-KCxQ7i3fBs3UzSNYPiBQqTesRu4NL3RcjFiFK',
    'asst': '1666085752.0',
    '__cf_bm': '9DIIrvrIPX.U5Mbihrw2TRRCe5OkTVjDiw.gAHKpiXw-1666085752-0-ARbHwG3wlLnmSSvr2y48IRY3kjG3mWZxyT2r6PFRhCC8m/TZdV2R+NDgzzkpOEWNPKN/7wfyUIuv77HLPnz/MQ0=',
    'bs': '4rvU96HYcVnuk-0aX4W12A:gL1lZJ9NqR-5v7Z5MxASfedhAcizN7OOkCz7cAfEXbQ3gsjxddLXRmfjDzOFrwurP8iNxctWhuQCVlJN7Gor1S68uBZwqZ_INrWz1_9_Wky-cm6dFtaQppu8YBgOquqP5IwUIQOdmQzT8zh4NZSAj0EIlX-fApCPi8UPTif9CKw:-YRzXWQ-DQ6lkZX5BH9-ZOJZEg5zJSqy_KlrqbW9ROo',
    'JSESSIONID': '3EE015CF86E729DB300530510CB1A0C5',
    '_ga_RJF0GNZNXE': 'GS1.1.1666085761.6.1.1666086001.60.0.0',
    '_ga': 'GA1.3.1497446754.1665993554',
    '_dc_gtm_UA-2595786-1': '1',
    'AWSALB': 'SINTJMMmdfpBoV97q2kimqx7T4pXZ5HeTY5J/FsQRAQ3IeFC0DLETGn+TmlpZ0SyI5iEyi3bFQlBr7ySRvmm6NXrLSUsUnCudctzCxOwHtTIVJdECaW3gWn9ek/v',
    'AWSALBCORS': 'SINTJMMmdfpBoV97q2kimqx7T4pXZ5HeTY5J/FsQRAQ3IeFC0DLETGn+TmlpZ0SyI5iEyi3bFQlBr7ySRvmm6NXrLSUsUnCudctzCxOwHtTIVJdECaW3gWn9ek/v',
    'amp_bfd0a9': '9a--3RyQxmQ_nfW3_nj1y9.MjA0MzUwODk4..1gfl76cri.1gfl7dnnk.d.3.g',
    '_ga_RC95PMVB3H': 'GS1.1.1666085760.6.1.1666086002.58.0.0',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Oct+18+2022+10%3A40%3A03+GMT%2B0100+(British+Summer+Time)&version=202209.2.0&isIABGlobal=false&hosts=&consentId=ba819046-ca9f-4aff-a51a-c5eac99e6e10&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&AwaitingReconsent=false&geolocation=GB%3BENG',
}

# headers = {
#     'authority': 'www.glassdoor.co.uk',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'cache-control': 'max-age=0',
#     # Requests sorts cookies= alphabetically
#     # 'cookie': 'G_AUTHUSER_H=0; gdId=dcce75de-93ae-4ded-b53e-ad27e715c9fa; rttdf=true; _gid=GA1.3.1263127479.1665993554; G_ENABLED_IDPS=google; OptanonAlertBoxClosed=2022-10-17T14:08:23.789Z; _optionalConsent=true; _gcl_au=1.1.531160811.1666015704; _fbp=fb.2.1666015704575.460910404; fpvc=2; __gads=ID=6606425e7c3c14dd:T=1666015711:S=ALNI_MZb37xQfa5M8Wv1zCIUqxO5Vzz1nA; uc=8013A8318C98C517A13DCFFA6EA4511D706518462668B9641710794A5051CE354FA0632071C465A57F14058698632B3298839D946CA6F658E10BDFA2416795248B940EDED9A02E9797FF0803451628D8799E910083E0AD7A687EB3C5EB2022EA9BCADB21D7612B051AB135E33AB09451520A5A4EC8239ECF3E09ADEF1CB714F68C6399561EE99CA744C801BCE9C5AE38; trs=direct:direct:direct:2021-10-21+07%3A24%3A32.043:undefined:undefined; ki_t=1666021213461%3B1666021213461%3B1666021213461%3B1%3B1; ki_r=; GSESSIONID=dcce75de-93ae-4ded-b53e-ad27e715c9fa+1666082044800; cass=1; __gpi=UID=00000b128a6c7103:T=1666015711:RT=1666082050:S=ALNI_MZKmRxWscbVh3VSG3Gdo8Pu8jHQKQ; gdsid=1666082044800:1666085752683:7EABE15D9F01A4F4F718E597F55747B8; at=lfw4tT16moWJYly5NjnnLsVEIjhmXGQWEx-Su9FUqUlkzB5lhjiZRWSawJKEAk03DB6Eue9_leGPHhKPPkr-09ZZR5uX-sqBZ39IaYWeCryD510KBksnbZtUxo-hFf0RUsCKAfcTfOjqWHrWSmgZPG_KM4U1mc-TnBpb0d8ydV0YKibwOYONSRD9214XYrt2HM8EPmoeku8L76_nKkxf4CfSOpux-FIVDu1n1Pmf2i-SIK3VLhN6WEI_WV1j4Eaw3cr0kgaWerZrsZWN7WoQQjJAc91eqFf6bdV50eSdv0TtuMrSTeJCK95tbzyndxIZY4fLAGGJj0N4tZnDJuqyGUh5l0PggpLK21PQbrrN9J6JCa_3NCZIX8hu_2oGIe3ATPxSvZYoc1PRo384jZIscxoIYvuuVh9p2wNXIoi9uN3mvg94hHi0j-5UtWuZAorXZVuPq8Sxcy2SGudW7u8eCUWui5qOWuOGTFlbUKTzQcBiAjuZZ-6r1fQ23Foyugdea_W0HAzXQixWjWwilSr6wDFCzUpZvRCwtIjmkJt6JHer_dJVH_uz9RqBglidcyoz82QE2a1wO34_wYDOMY0p8X3EfPuv_qM40514H093owfiSJaGjf7nPUTNTtXH-sXXiTh54LUEw9y40ZYJZ5KYZQ0pV31FzkqfP2aLPlcbJvWumQ9dkEnAKXp5zROu57ZSSucukbLp8rhvpGfUxFRs4VxrJRjjLDNYoQn-t3LKrimsBfFFKCz0pZjYKHEfJaneVuR6dPIxKJNpO3J1JSKyWkJ8AsyXwyqxIzkryuixZL2xNS10InYkL20TMpG2qNHGn2X1XtYiWtk07Dx0CMlr2ow59E-KCxQ7i3fBs3UzSNYPiBQqTesRu4NL3RcjFiFK; asst=1666085752.0; __cf_bm=9DIIrvrIPX.U5Mbihrw2TRRCe5OkTVjDiw.gAHKpiXw-1666085752-0-ARbHwG3wlLnmSSvr2y48IRY3kjG3mWZxyT2r6PFRhCC8m/TZdV2R+NDgzzkpOEWNPKN/7wfyUIuv77HLPnz/MQ0=; bs=4rvU96HYcVnuk-0aX4W12A:gL1lZJ9NqR-5v7Z5MxASfedhAcizN7OOkCz7cAfEXbQ3gsjxddLXRmfjDzOFrwurP8iNxctWhuQCVlJN7Gor1S68uBZwqZ_INrWz1_9_Wky-cm6dFtaQppu8YBgOquqP5IwUIQOdmQzT8zh4NZSAj0EIlX-fApCPi8UPTif9CKw:-YRzXWQ-DQ6lkZX5BH9-ZOJZEg5zJSqy_KlrqbW9ROo; JSESSIONID=3EE015CF86E729DB300530510CB1A0C5; _ga_RJF0GNZNXE=GS1.1.1666085761.6.1.1666086001.60.0.0; _ga=GA1.3.1497446754.1665993554; _dc_gtm_UA-2595786-1=1; AWSALB=SINTJMMmdfpBoV97q2kimqx7T4pXZ5HeTY5J/FsQRAQ3IeFC0DLETGn+TmlpZ0SyI5iEyi3bFQlBr7ySRvmm6NXrLSUsUnCudctzCxOwHtTIVJdECaW3gWn9ek/v; AWSALBCORS=SINTJMMmdfpBoV97q2kimqx7T4pXZ5HeTY5J/FsQRAQ3IeFC0DLETGn+TmlpZ0SyI5iEyi3bFQlBr7ySRvmm6NXrLSUsUnCudctzCxOwHtTIVJdECaW3gWn9ek/v; amp_bfd0a9=9a--3RyQxmQ_nfW3_nj1y9.MjA0MzUwODk4..1gfl76cri.1gfl7dnnk.d.3.g; _ga_RC95PMVB3H=GS1.1.1666085760.6.1.1666086002.58.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+18+2022+10%3A40%3A03+GMT%2B0100+(British+Summer+Time)&version=202209.2.0&isIABGlobal=false&hosts=&consentId=ba819046-ca9f-4aff-a51a-c5eac99e6e10&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&AwaitingReconsent=false&geolocation=GB%3BENG',
#     'referer': 'https://www.glassdoor.co.uk/',
#     'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
# }

with open('headers.txt') as f:
    data = f.read()
headers = ast.literal_eval(data)

#test = requests.get('https://www.glassdoor.co.uk/Overview/Working-at-Medpace-EI_IE152762.11,18.htm', headers=headers)#, cookies=cookies)

#soup = BeautifulSoup(test.text, 'lxml')
#print(soup)
#data = soup.find_all('script', {"type" : True})
#print(data)
#length = len(data)
#text = data[length-1].text
#print(html_clean(data))

count = 0
for n in range(len(ProfileURLs)):
    print("Now on Profile URL: ", ProfileURLs[n], "number: ", n)
    page = requests.get(str(ProfileURLs[n][0]), cookies=cookies,headers=headers, timeout=(10,30))
    soup = BeautifulSoup(page.text, 'lxml')
    try:
        scripts = soup.find_all('script', {"type" : True})
        length = len(scripts)
        text = scripts[length - 1].text
        data = data_scrape(text)
    except:
        data = ('null', 'null')
    alldata.append(data)
    print(data)
    df = pd.DataFrame([data], columns=columnslist)
    df.to_csv('output_from_'+filename, encoding='utf-8-sig', index=False, mode='a', header=False)
    count = count + 1
    print("On scrape loop: ",+ count, " out of", len(ProfileURLs))
    #print('\n')

    randomsleep = random.randint(2,6)
    print('Sleeping ', randomsleep ,' seconds')
    time.sleep(randomsleep)
print("Finished!")
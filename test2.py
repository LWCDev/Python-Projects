import requests
import pandas as pd
import time


#For the website https://plumber.com.au/find-a-plumber/#
postcodes = pd.read_csv('postcodes.csv', usecols=['CODE'])
postcodes = postcodes.values.tolist()

for i in range(len(postcodes)):
    print("On postcode number: ", i)
    cookies = {
        '_ga': 'GA1.3.603368301.1665734707',
        '_gid': 'GA1.3.1521818732.1665734707',
        '_fbp': 'fb.2.1665734707227.148126834',
        'appMenu': '22',
        '_gat_gtag_UA_16752861_8': '1',
        'AMS_AUTH': 'a1c70de9a2d04b2ec2ea74d81818d03b',
    }

    headers = {
        'authority': 'plumber.com.au',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ga=GA1.3.603368301.1665734707; _gid=GA1.3.1521818732.1665734707; _fbp=fb.2.1665734707227.148126834; appMenu=22; _gat_gtag_UA_16752861_8=1; AMS_AUTH=a1c70de9a2d04b2ec2ea74d81818d03b',
        'origin': 'https://plumber.com.au',
        'referer': 'https://plumber.com.au/find-a-plumber/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    json_data = {
        'postcode': f'{postcodes[i][0]}',
        'is_emergency': 0,
        'service_id': '3',
        'category_id': 0,
        'subcategory_id': 0,
    }
    print(f'{postcodes[i][0]}')
import requests
import csv

user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
proxies = {'http': 'http://lum-customer-ai-zone-static:uvc1vshl7xhi@zproxy.lum-superproxy.io:22225',
           'https': 'https://lum-customer-ai-zone-static:uvc1vshl7xhi@zproxy.lum-superproxy.io:22225'}

with open('urls/fmdirectoryurls.csv', 'a', newline='', encoding="utf-8-sig") as input_file:
    headers = ['URL']
    writer = csv.DictWriter(input_file, fieldnames=headers, dialect='excel')
    writer.writeheader()

with open('redirects/fmdirectoryredirects.csv', 'r') as csv_file:
    lines = csv_file.readlines()

redirect_urls = []
for line in lines:
    if line == "ï»¿URL\n":
        continue
    else:
        url = line.strip("\n")
        redirect_urls.append(url)

for url in redirect_urls:
    try:
        page = requests.get(url, headers=user_agent, proxies=proxies, allow_redirects=True, timeout=60)
        found_url = page.url
        found_domain = found_url.replace('http://', "")
        found_domain = found_domain.replace('https://', "")
        found_domain = found_domain.replace('www.', "")
        split_string = found_domain.split('/')
        found_domain = split_string[0]
        new_split_string = found_domain.split('?')
        found_domain = new_split_string[0]
    except:
        found_domain = ""
    print(found_domain)
    result = {'URL': found_domain}
    with open('urls/fmdirectoryurls.csv', 'a', newline='', encoding="utf-8-sig") as input_file:
        headers = ['URL']
        writer = csv.DictWriter(input_file, fieldnames=headers, dialect='excel')
        writer.writerow(result)
import requests

import requests
from bs4 import BeautifulSoup

cookies = {
    'gdId': 'd0273789-b738-45b2-b839-a365d12fd027',
    '_gid': 'GA1.2.523821179.1665993513',
    'OptanonAlertBoxClosed': '2022-10-17T07:59:54.521Z',
    '_optionalConsent': 'true',
    '_gcl_au': '1.1.1425350194.1665993595',
    '_rdt_uuid': '1665993595770.f7454022-afeb-454f-a935-076f287f258d',
    '__pdst': '6fece3219b4d49ffbb354d059e1e282d',
    '_tt_enable_cookie': '1',
    '_ttp': '1f7731eb-53fe-4070-bc7a-d3832fd1ec80',
    '_fbp': 'fb.1.1665993595974.1016602883',
    '_pin_unauth': 'dWlkPU4yWmxZMlZsTm1JdE5UTTJaUzAwTnpjeUxXSXpPV0V0Wm1NMFpUUm1OV0l5TTJFMw',
    'GSESSIONID': 'undefined',
    'gdsid': '1665993511833:1666012504494:3A6ACB5518DD49990AD8B928A8500ECF',
    'amp_bfd0a9': 'JKImedgy7bOzlPc5h3rgAb...1gfj1aqqo.1gfj1aqr7.2.0.2',
    '_ga_RJF0GNZNXE': 'GS1.1.1666012503.2.1.1666012507.56.0.0',
    '__gads': 'ID=3a7484feb804561b:T=1666012507:S=ALNI_Mb1WhsyKIJBAVKAgU0v6qmj8v00Ng',
    '__gpi': 'UID=00000b12871b555d:T=1666012507:RT=1666012507:S=ALNI_Mb2u8VOrEcBS5Lx0glxhJgxhieqGw',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Oct+17+2022+14%3A15%3A07+GMT%2B0100+(British+Summer+Time)&version=202209.2.0&isIABGlobal=false&hosts=&consentId=e9e1457d-1ef4-4779-a9b8-e8cce33210bd&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=GB%3BENG&AwaitingReconsent=false',
    'AWSALB': 'z26sTrfm1BBU706tjb5NNQqABHqZY+f8jZQL7lgtne2nbztGvQpt4iWF1O/qpNW2RJsA19/fT+eGJA35Z1kbsgOErauFKUlbiIKiL+1/VwS3GBozibXuP9ysLUzr',
    'AWSALBCORS': 'z26sTrfm1BBU706tjb5NNQqABHqZY+f8jZQL7lgtne2nbztGvQpt4iWF1O/qpNW2RJsA19/fT+eGJA35Z1kbsgOErauFKUlbiIKiL+1/VwS3GBozibXuP9ysLUzr',
    'JSESSIONID': '9BE9D351BC2D3AB7FA6070812700747A',
    'cass': '0',
    '_ga': 'GA1.2.243230694.1665993513',
    '__cf_bm': 'YY30hP1uBkfNCNT_x3WhJ7orBSFUH1UG0dociD9wwJ8-1666014915-0-AbVTDVVC1b/87MWZNkTZsYAWtWcjgufpxTWm89O8cB31pFHc6XVKpzo1r83gTn19pQdJsScI8oyL6fawJ3KLsYk=',
    '_ga_RC95PMVB3H': 'GS1.1.1666014915.3.0.1666014915.60.0.0',
}

headers = {
    'authority': 'www.glassdoor.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'gdId=d0273789-b738-45b2-b839-a365d12fd027; _gid=GA1.2.523821179.1665993513; OptanonAlertBoxClosed=2022-10-17T07:59:54.521Z; _optionalConsent=true; _gcl_au=1.1.1425350194.1665993595; _rdt_uuid=1665993595770.f7454022-afeb-454f-a935-076f287f258d; __pdst=6fece3219b4d49ffbb354d059e1e282d; _tt_enable_cookie=1; _ttp=1f7731eb-53fe-4070-bc7a-d3832fd1ec80; _fbp=fb.1.1665993595974.1016602883; _pin_unauth=dWlkPU4yWmxZMlZsTm1JdE5UTTJaUzAwTnpjeUxXSXpPV0V0Wm1NMFpUUm1OV0l5TTJFMw; GSESSIONID=undefined; gdsid=1665993511833:1666012504494:3A6ACB5518DD49990AD8B928A8500ECF; amp_bfd0a9=JKImedgy7bOzlPc5h3rgAb...1gfj1aqqo.1gfj1aqr7.2.0.2; _ga_RJF0GNZNXE=GS1.1.1666012503.2.1.1666012507.56.0.0; __gads=ID=3a7484feb804561b:T=1666012507:S=ALNI_Mb1WhsyKIJBAVKAgU0v6qmj8v00Ng; __gpi=UID=00000b12871b555d:T=1666012507:RT=1666012507:S=ALNI_Mb2u8VOrEcBS5Lx0glxhJgxhieqGw; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Oct+17+2022+14%3A15%3A07+GMT%2B0100+(British+Summer+Time)&version=202209.2.0&isIABGlobal=false&hosts=&consentId=e9e1457d-1ef4-4779-a9b8-e8cce33210bd&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=GB%3BENG&AwaitingReconsent=false; AWSALB=z26sTrfm1BBU706tjb5NNQqABHqZY+f8jZQL7lgtne2nbztGvQpt4iWF1O/qpNW2RJsA19/fT+eGJA35Z1kbsgOErauFKUlbiIKiL+1/VwS3GBozibXuP9ysLUzr; AWSALBCORS=z26sTrfm1BBU706tjb5NNQqABHqZY+f8jZQL7lgtne2nbztGvQpt4iWF1O/qpNW2RJsA19/fT+eGJA35Z1kbsgOErauFKUlbiIKiL+1/VwS3GBozibXuP9ysLUzr; JSESSIONID=9BE9D351BC2D3AB7FA6070812700747A; cass=0; _ga=GA1.2.243230694.1665993513; __cf_bm=YY30hP1uBkfNCNT_x3WhJ7orBSFUH1UG0dociD9wwJ8-1666014915-0-AbVTDVVC1b/87MWZNkTZsYAWtWcjgufpxTWm89O8cB31pFHc6XVKpzo1r83gTn19pQdJsScI8oyL6fawJ3KLsYk=; _ga_RC95PMVB3H=GS1.1.1666014915.3.0.1666014915.60.0.0',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

params = {
    'overall_rating_low': '3',
    'page': '387',
    'sector': '10005',
    'filterType': 'RATING_OVERALL',
}

#overview url, can loop through page in params


response = requests.post('https://www.glassdoor.com/Explore/browse-companies.htm', params=params, headers=headers)


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
            print(URL)
            text = text[endindex+4:]
            URL = URL.replace('"', '')
            URL = URL.replace(',', '')
            URL = 'https://www.glassdoor.co.uk/Overview/' + URL
        except:
            URL = 'null'
        list_of_url.append(URL)
        counter=counter+1
    return(list_of_url)

# soup = BeautifulSoup(response.text, 'lxml')
# #print(soup.prettify())
# script = soup.find('script')
# #print(script)
# #print(script.text)
# test = script.text
# #print(test[0])
# #soup1 = BeautifulSoup(test)
# #print(test.index('if'))
# URLs = link_find(test)
# print(URLs)

print(type(headers))
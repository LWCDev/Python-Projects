import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import time

webrange = range(1,2554, 20)


def cleanup(tuple):
    #cleanup html to text and remove unneeded characters
    list = []
    for element in tuple:
        if element is None:
            list.append("null")
        else:
            #print(element)
            if type(element) is str:
                list.append(element.strip().replace(" " , "").replace("\n", "").replace("\r", "").replace("Tel:","").replace("Email:",""))
            else:
                #print(element)
                object = element.text.strip()

                object = object.replace("\n", "").replace("\r", "")
                #object = element.text.strip.replace(" " , " ").replace("\n", "").replace("\r", "")#
                list.append(object)

    return(list)






def scrape(firm, links):
    values = []
    for k in range(len(links)):

        #print("Link!", links[k])
        link = links[k]
        site = re.get(link)
        sitesoup = BeautifulSoup(site.content, 'html.parser')
        country = sitesoup.find('h3', class_='font-mfred text-uppercase')#.text.strip()
        webURL = sitesoup.find_all('div', class_='col-12 col-md-6 col-lg-4 g-sm-0')  # .text.strip()
        #There must be a better way to do this, for now selects the bottom most href, this is the company website link
        try:
            for y in range(len(webURL)):
                websitelink = webURL[y].find('a')['href']
                #print(y, websitelink)
                if y+1 == len(webURL):
                    webout = websitelink
        except:
            webout = 'null'
        webURL = webout
        #print(webURL)
        #webURL = websitelink
        Sector = sitesoup.find('h3', class_='font-mfred text-uppercase me-0 me-md-5')
        Telephone_Email = sitesoup.find('div', class_="row mb-3") #.text.strip()
        #Telephone_Email = Telephone_Email.select('tbody')
        if Telephone_Email is None:
            Telephone = 'null'
            Email = 'null'
        else:
            try:
                Telephone = Telephone_Email.select('tr')[1]
            except:
                Telephone = 'null'
        #Telephone = Telephone.select('a')
            try:
                Email = Telephone_Email.select('tr')[2]
            except:
                Email = 'null'
        #Email = Email.select('a')
        if Email is None:
            Email = "null"
        else:
            Email = Email
        if Telephone is None:
            Telephone = 'null'
        else:
            Telephone = Telephone
        value = [firm[k], country, Telephone, Email, webURL, Sector]
        value = cleanup(value)
        #print("Test, value ", value)
        values.append(value)
        time.sleep(0.01)
    return values









finaldata = []
#Website = "https://www.superyachtnews.com/ajax/loaddirectory.php?startrow=1&name=&countrycode=&categoryid=&sortby=0&returnlimit=20"

for i in webrange:
    website = 'https://www.superyachtnews.com/ajax/loaddirectory.php?startrow='+ str(i) + '&name=&countrycode=&categoryid=&sortby=0&returnlimit=20'
    page = re.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    firmlinks = soup.find_all('h2')
    urllist = []
    firms = []
    #print(firmlinks)
    print(i)
    #print(firmlinks)
    for element in firmlinks:
        url = element.find('a', href=True)
        Firm = element.find('a')
        if Firm is None:
            firms.append('null')
        else:
            firms.append(Firm.text)
        urllist.append('https://www.superyachtnews.com' + url['href'])
        #print(firms)
    output = scrape(firms, urllist)
    finaldata.append(output)

try:
    #print(finaldata)
    compiledata = []
    for data in finaldata:
        for object in data:
            compiledata.append(object)
    df = pd.DataFrame(compiledata, columns=["Firm", "Country", "Telephone Number", "Email Address", "URL", "Business Sector 1"])

    df.to_csv('SuperYachtNews.csv', encoding='utf-8-sig', index=False)
except:
    print(compiledata)
    print("Columns did not work")
    print(finaldata)
    df = pd.DataFrame(finaldata)#
    df.to_csv('SuperYachtNews.csv', header=False, index=False)
import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import time
#A very messy first try, this code is to be seen only as the basics and not something to copy from
Headers = pd.read_excel('C:\\Users\\lewis.welshclark\\PycharmProjects\\UKTravelDirectoryScrape\\Main Data Template.xlsx', sheet_name="Sheet1", header=0)

def pagefetch(page):
    try:
        links = []
        site = re.get(page)
        soupy = BeautifulSoup(site.content, 'html.parser')
        firmlist = soupy.find('div', class_="business-listings clearfix")
        url = firmlist.find_all('a', href=True)
        for link in url:
            links.append('https://www.ukdirectory.co.uk'+link['href'])
            #time.sleep(2)
        return(links)
    except:
        print("Whoops")

def scrape(links):
    values = []
    for k in range(len(links)):

        #print("Link!", links[k])
        link = links[k]
        site = re.get(link)
        sitesoup = BeautifulSoup(site.content, 'html.parser')
        Firm = sitesoup.find('h1', class_='title')#.text.strip()
        Address = sitesoup.find('address')   #.text.strip().replace("\n", "")
        #Address = Address.replace("\r", "").replace(" ", "")
        Telephone = sitesoup.find('div', {"id" : "pn"}) #.text.strip()
        Email = sitesoup.find('a', class_="popup-modal")  #.text.strip()
        if Email is None:
            Email = "null"
        else:
            Email = Email['href']
        value = [Firm, Address, Telephone, Email]
        value = cleanup(value)
        values.append(value)
        #print(value)
        time.sleep(0.2)
    return(values)

def cleanup(tuple):
    #cleanup html to text and remove unneeded characters
    list = []
    for element in tuple:
        if element is None:
            list.append("null")
        else:
            #print(element)
            if type(element) is str:
                list.append(element.strip().replace(" " , "").replace("\n", "").replace("\r", ""))
            else:
                #print(element)
                object = element.text.strip()

                object = object.replace("\n", "").replace("\r", "")
                #object = element.text.strip.replace(" " , " ").replace("\n", "").replace("\r", "")#
                list.append(object)

    return(list)


#For https://www.ukdirectory.co.uk/travel-and-accommodation/

page = re.get('https://www.ukdirectory.co.uk/travel-and-accommodation/')

#print(page.status_code) check if the page downloaded successfully, 200 is the desired result#

soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())
#class="categoryListContainer" URLs for the other pages are contained in this class

categories = soup.find('div', class_="categoryListContainer")

#URLs = categories.select('ul a')['href']


URL = categories.find_all('a', href=True)
#finds only the URLs for all the categories on the main page

#turns the URLs we extract into a usable format

URLlist = []
for url in URL:
    #print(url['href'])
    URLlist.append('https://www.ukdirectory.co.uk'+url['href'])

#print(URLlist)

alldata = []
for j in range(len(URLlist)):
    firms = pagefetch(URLlist[j])
    #print(firms)
    output = scrape(firms)
    alldata.append(output)
    print("Now on loop: ", j, "and the data currently looks like: ", output)
compiledata = []
try:
    for data in alldata:
        for object in data:
            compiledata.append(object)
        df = pd.DataFrame(compiledata, columns = ["Firm", "Address Line 1","Telephone Number", "Email Address"])
        df.to_csv('ukdirectory_travel.csv', encoding='utf-8-sig')
except:
    print("Column error")
    df = pd.DataFrame(alldata)
    df.to_csv('ukdirectory_travel.csv', encoding='utf-8-sig')
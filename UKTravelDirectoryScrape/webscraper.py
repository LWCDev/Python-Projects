import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import time

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
            time.sleep(2)
        return(links)
    except:
        print("Whoops")

def scrape(links):
    values = []
    for k in range(len(links)):

        print("Link!", links[k])
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
        values.append(value)
        print(cleanup(value))
        time.sleep(2)
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
                print(element)
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
    URLlist.append('https://www.ukdirectory.co.uk/travel-and-accommodation/'+url['href'])

#print(URLlist)#
#Now we have a list of all the webpages we want to scrape from, we can begin getting the necessary information from each page

#test = scrape(['https://www.ukdirectory.co.uk/pakistan-international-airlines-207919847.html'])
#test = cleanup(test)
#print(test)


URL = ('https://www.ukdirectory.co.uk/travel-and-accommodation/airlines-and-air-taxi/?page=6')
alldata = []
#for url in URLlist:
#    firms = pagefetch(url)
#    for firm in firms:
#        values = scrape(firm)
#        values = cleanup(values)
#        alldata.append(values)
#print(alldata)

firms = pagefetch(URLlist)
#print(type(firms))

values = scrape(firms)
print(values)
for x in range(len(values)):
    cleaned = cleanup(values[x])
    alldata.append(cleaned)
#alldata.append(values)
print(alldata)


#ready to be altered to scrape the entire site!!!
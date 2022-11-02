import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#For website: https://ttaa.or.th/member-directory/
#ABANDONED PROJECT
def attribute_scraper(soup):
    source = 'https://ttaa.or.th/member-directory/'
    sourcelist = []
    firmlist = []
    Telephone = []
    Email = []
    #site = re.get(link)
    #soupy = BeautifulSoup(site.content, 'lxml')
    test = soup.find('div', class_='control-label')
    print(test)
    print(test.text)
    Element = soup.find('article', class_="post")
    Firm = Element.find_all('h2')
    Contact = Element.find_all('div', class_='class="col-md-6 col-xs-6"')
    print(Element)
    for firm in Firm:
        firmlist.append(firm)
    for contact in Contact:
        try:
            Telephone.append(contact[3])
        except:
            Telephone.append('null')
        try:
            Email = Telephone.append(contact[4])
        except:
            Email.append('null')

    return(Email, Firm, source) #Email Address, URL, Firm, Address Line 1, Source


#Returns clean, non-html versions of the data which is ready for saving
def html_clean(in_tuple):
    # cleanup html to text and remove unneeded characters
    list = []
    for element in in_tuple:
        if element is None:
            list.append("null")
        else:
            # print(element)
            if type(element) is str:
                list.append(element.strip().replace(" ", "").replace("\n", "").replace("\r", "").replace("mailto:", ""))
            else:
                # print(element)
                object = element.text.strip()

                object = object.replace("\n", "").replace("\r", "").replace("mailto:", "")
                # object = element.text.strip.replace(" " , " ").replace("\n", "").replace("\r", "")#
                list.append(object)

    return (tuple(list))


#options = webdriver.ChromeOptions()
#options.add_argument("--log-level=OFF")
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#driver.get("https://ttaa.or.th/member-directory/")
#driver.implicitly_wait(80)
#driver.find_element(By.CLASS_NAME, "post")

#options = webdriver.ChromeOptions()

#page_source = driver.page_source
#soup = BeautifulSoup(page_source, 'html.parser')
#with open("output1.html", "w", encoding='utf-8') as file:
#    file.write(str(soup))
#print("Done!")
#driver.close()

#above code no longer needed, page has been saved to html file because it loads too slowly to use it for testing on a live webpage

with open('output1.html', 'rb') as html:
    soup = BeautifulSoup(html, 'html.parser')

output = attribute_scraper(soup)
print(output)
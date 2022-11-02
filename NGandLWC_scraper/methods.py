import requests
from bs4 import BeautifulSoup
import time
import random
import colorama
import re
from colorama import Fore, Back, Style
import pandas as pd
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

colorama.init(autoreset=True)


# headers =


def csv_save(columns, filename, data, mode='a'):
    if not data or not filename or not columns:
        print("Did not get columns, filename or data: ", columns, filename, data)
        return
    df = pd.DataFrame([data], columns=columns)
    df.to_csv(filename, mode=mode, encoding='utf-8-sig', header=False, index=False)

def html_clean(in_tuple):
    # cleanup html to text and remove unneeded characters
    list = []
    for element in in_tuple:
        if element is None:
            list.append("null")
        else:
            # print(element)
            if type(element) is str:
                list.append(
                    element.strip().replace(" ", "").replace("\n", "").replace("\r", "").replace("mailto:", "").replace(
                        "Email:", "").replace("email:", ""))
            else:
                # print(element)
                object = element.text.strip()

                object = object.replace("\n", "").replace("\r", "").replace("mailto:", "").replace("Email:",
                                                                                                   "").replace("email:",
                                                                                                               "")
                # object = element.text.strip.replace(" " , " ").replace("\n", "").replace("\r", "")#
                list.append(object)

    return (tuple(list))


class UniScrape():
    # I'll add the ability to add headers, proxies etc. later. They aren't a priority for now because this is mainly
    # for websites where those are not necessary
    def __init__(self, source, page_type, element_types, max_pages, soup_list, profile_list):
        # Original webpage, doesn't include any pagination etc.
        self.source = source
        self.filename = source.replace(".", "_")
        self.columns = ['Source', 'Firm', 'Email Address', 'URL']
        # Whether the page needs pagination or not
        self.page_type = page_type
        # What elements to capture (to begin with we will test only with the 3 basics of Email, URL and Firm
        # self.capture_elements = capture_elements deprecated
        # Whether the webpage has profile links that need to be opened or whether all information is available
        # from the beginning, I don't think we will need capture method, we can just simply write the inputs differently
        # or use separate functions
        # self.capture_method = capture_method deprecated
        # How we will tell it what page elements to grab (will work this out more finely later)
        self.element_types = element_types
        # How many pages we have to scrape
        self.max_pages = max_pages
        # Keeping these two as being user defined rather than defaulting to an empty list because it might be useful
        # for inputting records from mongo later
        self.soup_list = soup_list
        self.profile_list = profile_list
        self.results = []
        self.lock = 0
        self.spacer = '-'*10
        self.savemessage =''



    # Going to have them as two separate functions but have it default to a database,
    # just leave the csv as what we can use for now, and change it later to default to this
    # def db_save
    def scrape(self, link, class_id_attributes, elementname, save=None, resume=None):
        # Decided we can have the input that decides the class id/etc. be a dictionary
        # element_types will be a list of dictionaries telling it the element type and the element name

        # loads a page with multiple listings (we really need to decide on a standard for naming these kinds of things
        # so we don't get confused), anyway the kind where we dont have to access profiles, then uses the div_scrape
        # function inside of it for each "chunk" that contains a firm's data, in order. The data is returned as a list
        # and also added to self.results so we can access it even without using a variable
        def get_listings_page(link, class_id_attributes):
            # All firms are listed with all information separated by divs etc. Only the source needs to be visited
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'lxml')
            # print(soup)
            # Find all divs on the page, find info from them
            if class_id_attributes['class'] == 1:
                divs = soup.find_all(class_id_attributes['element'], class_=elementname)
            elif class_id_attributes['idtype'] == 1:
                divs = soup.find_all(class_id_attributes['element'], {elementname[0]: elementname[1]})
            else:
                divs = soup.find_all('div')  # to stop pycharm error message, won't work if this is reached
                print("You didn't pass the div element properly")
                return
            # Iterates through the divs and hopefully gets the relevant data
            # Here my thinking is that class_id_attribute is a ordered list of whatever we need to pass it
            # class_= "..." or {"id" : "breakfast"} etc. Obviously it can't work like that,
            # but this is just a placeholder for now. We can figure that out later
            # figured we can use a dictionary input { class : 0, idtype : 1} etc. to decide this stuff,
            # if we are using the dictionary method to find i.e {'id' : 'companyname' } then we use a list to input
            # the 'class' name
            for div in divs:
                Firm, Email, URL = div_scrape(div)
                data = Firm, Email, URL, self.source
                # print(data)
                data = html_clean(data)
                self.results.append(data)
                if (data[0] == 'NULL') or (data[1] == 'NULL' and data[2] == 'NULL'):
                    print(
                        Fore.CYAN + self.spacer + "On scrape loop:  " + str(len(self.results)) + self.spacer + "\n" +
                        Fore.RED + "Scraped the following: " + str(data) + Fore.RED + " from " + str(
                            self.source) + '\n' + '|||  Null values in Firm or Email AND URL, not saving this firm |||')
                    break
                elif 'NULL' in data:
                    print(
                        Fore.CYAN + self.spacer + "On scrape loop:  " + str(len(self.results)) + self.spacer + "\n" +
                        "Scraped the following: " + Fore.RED + Back.LIGHTWHITE_EX + str(data) + Back.RESET
                        + Fore.CYAN + " from " + str(self.source) + self.savemessage)
                else:
                    print(
                        Fore.CYAN + self.spacer + "On scrape loop:  " + str(len(self.results)) + self.spacer + "\n" +
                        "Scraped the following: " + str(data) + " from " + str(self.source) + self.savemessage)
                if save:
                    self.savemessage = ' Saving... '
                    csv_save(columns=self.columns, filename=self.filename, data=data, mode='a')

        # used by the above function, this just takes in a page element and returns data from within it
        # (url, email, name)
        def div_scrape(div):
            try:
                if firm['class'] == 1:
                    Firm = div.find(firm['element'], class_=firm['firmname'])
                elif firm['idtype'] == 1:
                    Firm = div.find(firm['element'], {firm['firmname'][0]: firm['firmname'][1]})
                else:
                    print("You didn't pass the firm type correctly")
                    return
            except Exception as e:
                print("Excepton in Firm!", e)
                # If we can't find a firm we skip, jack was on about cleaning the URL to find it instead
                # earlier, for now we'll do this
                return
            # print(Firm.text) # Firm and Div are working
            try:
                if email['class'] == 1:
                    Email = div.find(email['element'], class_=email['emailname'])
                    try:
                        child = Email.findChildren("a", recursive=False)
                        if child[0]:
                            if child[0]['href']:
                                Email = child[0]['href']
                                # print("Email HREF found")
                    except Exception as e:
                        print("No Email HREF found", e)
                elif email['idtype'] == 1:
                    Email = div.find(email['element'], class_=email['emailname'])
                    try:
                        child = Email.findChildren("a", recursive=False)
                        if child[0]:
                            if child[0]['href']:
                                Email = child[0]['href']
                                # print("Email HREF found")
                    except Exception as e:
                        print("No Email HREF found", e)
                else:
                    print("You didnt pass the email type correctly")
                    return
            except Exception as e:
                Email = 'NULL'
                print("Exception in Email!", e)
            try:
                if url['class'] == 1:
                    URL = div.find(url['element'], url['urlname'])

                    # URL = URL['href']
                    try:
                        child = URL.findChildren("a", recursive=False)
                        # print(child[0])
                        if child[0]:
                            # childelement = child[0]
                            # print(childelement['href'])
                            if child[0]['href']:
                                URL = child[0]['href']
                                # print("URL HREF found", Firm.text)
                    except Exception as e:
                        print("No URL HREF found", e, Firm.text)
                elif url['idtype'] == 1:
                    URL = div.find(url['element'], {url['urlname'][0]: url['urlname'][1]})
                    # URL = URL['href']
                    try:
                        child = URL.findChildren("a", recursive=False)
                        # print(child[0])
                        if child[0]:
                            if child[0]['href']:
                                URL = child[0]['href']
                                # print("URL HREF found")
                    except Exception as e:
                        print("No URL HREF found", e)
                else:
                    print("You didnt pass the url type correctly")
                    return
                # print(URL)
            except Exception as e:
                # Skips this firm if there is no URL or Email, avoids useless data
                print("Exception in URL! ", e)
                if Email == 'NULL':
                    return
                URL = 'NULL'
            return(Firm, URL, Email)

        # not to be confused with profile_scrawl, prof_scrape loads a firm's profile hosted on some website and using
        # data given to it finds relevant elements and returns them
        def prof_scrape(link, class_id_attributes, firm, email, url):
            Email = 'NULL'
            Firm = 'NULL'
            URL = 'NULL'
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'lxml')

            # As in the above chunk, checking the user input parameters
            if class_id_attributes['class'] == 1:
                section = soup.find(class_id_attributes['element'], class_=elementname)
            elif class_id_attributes['idtype'] == 1:
                section = soup.find(class_id_attributes['element'], {elementname[0]: elementname[1]})
            else:
                print("You didnt pass the section type correctly", firm['idtype'])
                return
            if firm['class'] == 1:
                try:
                    Firm = soup.find(firm['element'], firm['firmname'])
                except:
                    Firm = 'NULL'
            elif firm['idtype'] == 1:
                # print("FIRM!")
                # print({firm['firmname'][0]:firm['firmname'][1]})
                try:
                    Firm = soup.find(firm['element'], {firm['firmname'][0]: firm['firmname'][1]})
                except:
                    Firm = 'NULL'
            else:
                print("You didn't pass the firm type correctly")
                return
            # Firm name is usually just simply in a header on its own, so we can easily grab those,
            # Email and URL are not like this, sometimes they can be quite hard to pin down
            # To get around this we narrow it down to the specific chunk of the webpage they are in,
            # Then perform a rugged search to find them inside this "section"
            # There is the possibility of false positives but this also applies to the regular python approach
            # and WS approach, there isn't really much of a solution for it
            if email['class'] == 1:
                try:
                    secmail = section.find_all(email['element'], class_=email['emailname'])
                    for mail in secmail:
                        hrefs = mail.find_all('a', href=True)
                        # First we check the text of the element to see if it has the @ for an email, this is the
                        # most likely to be the case, so we check for it first
                        if '@' in mail.text:
                            Email = mail.text
                            break
                        # However the Email could instead be hidden within an element attribute so we check here
                        # If we find a href or multiple within this element, we loop to see if it has @ in the text
                        # inside the redirect, if so we have found our email and can move on. Repeat.
                        if hrefs:
                            for href in hrefs:
                                if '@' in href['href']:
                                    Email = href['href']
                                    break
                except Exception as e:
                    print("The error is: ", e)
                    # Email = 'NULL'
                    return
            elif email['idtype'] == 1:
                try:
                    secmail = section.find_all(email['element'], {email['emailname'][0]: email['emailname'][1]})
                    try:
                        for mail in secmail:
                            hrefs = mail.find_all('a', href=True)
                            if '@' in mail.text:
                                Email = mail.text
                                break
                            if hrefs:
                                for href in hrefs:
                                    if '@' in href['href']:
                                        Email = href['href']
                                        break
                    except Exception as e:
                        print("The error is: ", e)
                        Email = 'NULL'
                        return
                except:
                    Email = 'NULL'
            # URL is more simple than above, we can just simply check for hrefs and ignore hrefs that belong to the
            # host site or are an email address
            if url['class'] == 1:
                seclink = section.find_all(url['element'], class_=url['urlname'])
                for link in seclink:
                    try:
                        hrefcheck = link.find('a', href=True)
                        if hrefcheck['href']:
                            if '@' in hrefcheck['href'] or self.source in hrefcheck['href']:
                                continue
                            else:
                                URL = hrefcheck['href']
                                break
                    except:
                        URL = 'NULL'
            elif url['idtype'] == 1:
                seclink = section.find_all(url['element'], {url['urlname'][0]: url['urlname'][1]})
                for link in seclink:
                    try:

                        hrefcheck = link.find('a', href=True)
                        if hrefcheck['href']:
                            if '@' in hrefcheck['href'] or self.source in hrefcheck['href']:
                                continue
                            else:
                                URL = hrefcheck['href']
                                break
                    except:
                        URL = 'NULL'
            else:
                print("You didn't pass the URL type correctly")
                return
            return(Firm, Email, URL)

        firm, email, url = self.element_types
        if save and not resume and self.lock != 1:
            self.lock = 1
            print("Creating the file/connecting to database")
            empty = pd.DataFrame([], columns=self.columns)
            empty.to_csv(self.filename, encoding='utf-8-sig', index=False)
        # results = []
        if self.page_type is None:
            # If there is only a single page of results
            if self.max_pages is None or self.max_pages == 1:
                get_listings_page(link, class_id_attributes)
                print(Fore.CYAN + self.spacer * 4)
                print(Fore.GREEN + self.spacer, Fore.GREEN + "One page of results now ready for the page", Fore.GREEN+ self.source, Fore.GREEN+self.spacer)
                print(Fore.CYAN + self.spacer * 4)
                return(self.results)
            # Now for if there is multiple pages for this type, with a URL we can change
            else:
                Firm, Email, URL = prof_scrape(link, class_id_attributes, firm, email, url)
                data = Firm, Email, URL, self.source
                # print(data)
                data = html_clean(data)
                self.results.append(data)
                if (data[0] == 'NULL') or (data[1] == 'NULL' and data[2] == 'NULL'):
                    print(Fore.CYAN + self.spacer + "On scrape loop:  " + str(len(self.results)) + self.spacer + "\n" +
                          Fore.RED + "Scraped the following: "  + str(data) + Fore.RED + " from " + str(
                        self.source) +'\n' + '|||  Null values in Firm or Email AND URL, not saving this firm |||')
                    return
                elif 'NULL' in data:
                    print(Fore.CYAN + self.spacer + "On scrape loop:  " + str(len(self.results)) + self.spacer + "\n" +
                          "Scraped the following: " + Fore.RED +  Back.LIGHTWHITE_EX + str(data) + Back.RESET
                          + Fore.CYAN + " from " + str(self.source) + self.savemessage)
                else:
                    print(Fore.CYAN + self.spacer + "On scrape loop:  " + str(len(self.results)) + self.spacer + "\n" +
                        "Scraped the following: " + str(data) + " from " + str(self.source) + self.savemessage)
                if save:
                    self.savemessage = ' Saving... '
                    csv_save(columns= self.columns, filename=self.filename, data=data, mode='a')
            print(Fore.CYAN + self.spacer*4)
            print(Fore.GREEN + self.spacer, Fore.GREEN + "One page of results now ready for the page", Fore.GREEN+ self.source, Fore.GREEN+self.spacer)
            print(Fore.CYAN + self.spacer*4)
            return
        else:
            # If there are multiple URLs with listings, this means we don't need to access any profile links to
            # get the data, but we do need to access multiple pages, page1, page2 etc.
            # gets the range '[1-10]' for example, finds the start and end pages from it, then uses this info to loop
            # and rebuild the URL
            pages = link.split('[', 1)[1].split(']')[0]
            min_num = pages[0:pages.index('-')]
            max_num = pages[pages.index('-') + 1:]
            web_range = range(int(min_num), int(max_num) + 1, 1)
            for k in web_range:
                web_url = link.replace('[', '').replace(']', '').replace(pages, str(k))
                get_listings_page(web_url, class_id_attributes)
                print(Fore.CYAN + self.spacer * 4)
                print(Fore.GREEN + self.spacer, Fore.GREEN + "One page of results now ready for the page: ", web_url,
                      Fore.GREEN + self.source, Fore.GREEN + self.spacer)
                print(Fore.CYAN + self.spacer * 4)
            return(self.results)
        # That's the easy part, now that we know our URL requires some pagination, we have to navigate it somehow

    # _first is the beginning of the url, before the page variable and _second is after, this way we can insert a
    # varying number anywhere within a URL regardless of the site's format
    def profile_crawl(self, startURL_first, class_id_attributes, elementname, startURL_second='', append=False, save=None, resume=None):
        # Sets up a range for pagination, +1, so we reach the end
        if save and not resume:
            print("Creating the file/connecting to database")
            empty = pd.DataFrame(self.results, columns=['Profile URL'])
            empty.to_csv('profiles_' + self.filename, encoding='utf-8-sig', index=False)
            
        for i in range(0, self.max_pages + 1, 1):
            # Creates a combined URL that we can insert our page number into, very useful
            joined = startURL_first + str(i) + startURL_second
            # Identifies the scheme we should be using i.e https://www. , very convenient so the user doesn't
            # have to define it themselves
            scheme = startURL_first[0:startURL_first.index(self.source)]
            print("Now crawling page... ", joined)
            page = requests.get(joined)
            soup = BeautifulSoup(page.content, 'lxml')
            # like in the scrape function, we check to see how the user is deciding to find the elements they are after
            if class_id_attributes['class'] == 1:
                # print("Here")
                # print(class_id_attributes['element'])
                # print(elementname)
                divs = soup.find_all(class_id_attributes['element'], class_=elementname)
            elif class_id_attributes['idtype'] == 1:
                divs = soup.find_all(class_id_attributes['element'], {elementname[0]: elementname[1]})
            else:
                divs = soup.find_all('div')  # to stop pycharm error message, won't work if this is reached
                print("You didn't pass the div element properly")
                return
            # print("Divs! ", divs)
            # The name can be misleading as this isn't always a div (in fact this was first made on a list <li>
            # This is basically all the different "blocks" that make up the search results we commonly find,
            # we extract the link from this block, and we add it to our class wide list so that we can access it for
            # scraping later on, the loop for scraping is defined outside the class
            for div in divs:
                link = div.find('a', href=True)
                # Append is a user defined variable, this is to handle hrefs that are actually only half of a URL
                # i.e /company/hello-world-foods etc. instead of a full hyperlink
                if append:
                    link = link['href']
                    link = scheme + self.source + link
                else:
                    link = link['href']
                print(link)
                self.profile_list.append(link)
                if save:
                    print("Saving...")
                    df = pd.DataFrame([link], columns=["Profile URL"])
                    df.to_csv('profiles_' + self.filename, encoding='utf-8-sig', mode='a', header=False, index=False)
            print(f"Crawl complete for {joined}! All profile links are now accessible. Moving onto next page...")


# Input Template Below
# a class of 1 tells it you want to find by class, idtype of 1 tells it you want to
# find by id/type (for when classes cant be used)
firmelement = {'class': 0, 'idtype': 1, 'element': 'h1', 'firmname': ["itemprop", "name"]}
emailelement = {'class': 1, 'idtype': 0, 'element': 'div', 'emailname': "row"}
urlelement = {'class': 1, 'idtype': 0, 'element': 'div', 'urlname': "row"}
# Tells it what element is holding the information you want inside it, works with classes and by type or ID
classids = {'class': 1, 'idtype': 0, 'element': 'li'}
# Packs these inputs as a tuple for the class
capture = (firmelement, emailelement, urlelement)
# Tells it what page to scrape, and what page to add as source
sourcepage = 'fyple.net'
originURL = 'https://www.fyple.net/category/travel-accommodation/accommodation/'
# The name of the element's class/id that contains the information you're trying to scrape (firm, url etc.)
section_name = 'mdl-list__item mdl-divider'
# # Create the class using the above variables
g = UniScrape(source=sourcepage, page_type=None, element_types=capture,
              max_pages=70, soup_list=[], profile_list=[])
# # Your output list, currently for testing
# testlist = g.scrape(URL=originURL, class_id_attributes=classids, elementname=section_name)
# print(testlist)


g.profile_crawl(startURL_first=originURL + 'page/', startURL_second='', append=True, class_id_attributes=classids,
                elementname=section_name, save=True, resume=False)
print(f"Total amount of profiles found is: {len(g.profile_list)}!")
for i in range(len(g.profile_list)):
    originURL = g.profile_list[i]
    classids = {'class': 1, 'idtype': 0, 'element': 'div'}
    section_name = 'col-md-5'
    g.scrape(link=originURL, class_id_attributes=classids, elementname=section_name, save=True, resume=False)
print(g.results)

########################################################################################
#
#
#
# Earlier test stuff
# Below
#
#
#
########################################################################################
# firmelement = { 'class' : 1, 'idtype' : 0, 'element' : 'h3', 'firmname' : 'bd-category-item-title uk-text-center' }
# emailelement = { 'class' : 1, 'idtype' : 0, 'element' : 'div', 'emailname' : "bd-category-item-email"}
# urlelement = { 'class' : 1, 'idtype' : 0, 'element' : 'div', 'urlname' : "bd-category-item-website"}
# capture = (firmelement, emailelement, urlelement)
# g = UniScrape(source='countymeathchamber.ie', page_type=None, element_types=capture, max_pages=None, soup_list=[], profile_list=[])
# classids = { 'class' : 1, 'idtype' : 0, 'element' : 'div'}
#
# testlist = g.scrape(link='https://countymeathchamber.ie/business-directory', class_id_attributes = classids, elementname="uk-width-1-1 uk-width-small-1-2 uk-width-medium-1-3 uk-margin-bottom")
# print(testlist)


# # Test chunk
# print(urlelement['urlname'])
# print(urlelement['element'])
# testvar = urlelement['element']
# testvar2 = urlelement['urlname']
# page = requests.get('https://countymeathchamber.ie/business-directory')
# soup = BeautifulSoup(page.content, 'lxml')
# divs = soup.find_all(classids['element'], "uk-width-1-1 uk-width-small-1-2 uk-width-medium-1-3 uk-margin-bottom")
# for div in divs:
#     #print(div)
#     url = div.find(testvar, class_=testvar2)
#     print(url)
#     #url = div.find('div', class_="bd-category-item-website")
#     #print(url)


# # Input Template Below
# # a class of 1 tells it you want to find by class, idtype of 1 tells it you want to
# # find by id/type (for when classes cant be used)
# firmelement = { 'class' : 0, 'idtype' : 0, 'element' : '', 'firmname' : '' }
# emailelement = { 'class' : 0, 'idtype' : 0, 'element' : '', 'emailname' : ""}
# urlelement = { 'class' : 0, 'idtype' : 0, 'element' : '', 'urlname' : ""}
# # Tells it what element is holding the information you want inside it, works with classes and by type or ID
# classids = { 'class' : 0, 'idtype' : 0, 'element' : ''}
# # Packs these inputs as a tuple for the class
# capture = (firmelement, emailelement, urlelement)
# # Tells it what page to scrape, and what page to add as source
# sourcepage = ''
# originURL = ''
# # The name of the element's class/id that contains the information you're trying to scrape (firm, url etc.)
# section_name = ''
# # Create the class using the above variables
# g = UniScrape(source=sourcepage, page_type=None, capture_elements=None, capture_method=None, element_types=capture, max_pages=None)
# # Your output list, currently for testing
# testlist = g.scrape(URL=originURL, class_id_attributes=classids, elementname=section_name)

# git test!
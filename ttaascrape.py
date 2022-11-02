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
def RunSelenium():
    souplist = []
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://ttaa.or.th/member-directory/")

        sourcelist = []
        #options = webdriver.ChromeOptions()



        driver.implicitly_wait(10)
        page_source = driver.page_source
        sourcelist.append(page_source)
        #aria-label="Next"
        #// *[ @ id = "member-list"] / div[3] / div / div[2] / nav / ul / li[43]
        WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "[@id='member-list']//div[3]//div//div[2]//nav//ul//li[43]"))).click()
        #more_buttons = driver.find_element(By.CLASS_NAME, "next")
        #while True:
        #    wait = WebDriverWait(driver, 10000)
        #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #    WebDriverWait(driver, 800000).until(EC.element_to_be_clickable((By.CLASS_NAME, "next")))
         #   WebDriverWait(driver, 1000).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "next" ), "Next"))
         #   more_buttons = driver.find_element(By.CLASS_NAME, "next")
         #   if 'inactive' in more_buttons.get_attribute('class'):
         #       break;
         #   time.sleep(1)
         #   more_buttons.click()

        #Goes through all the pages of information available, afterwhich it can be passed off to bs4
        try:

            for p in range(1,22508,1):
                print("Webcrawl loop number: ", p)
                driver.find_element(By.XPATH,"//div//div//div//div//a[@class='next']").click()
                page_source = driver.page_source
                sourcelist.append(page_source)
                time.sleep(10)
            driver.close()
        except Exception as e:
            print("Loop ended early within the catch statement", e)
            page_source = driver.page_source
            sourcelist.append(page_source)
            driver.close()

    except Exception as e:
        print("Webcrawling failed, it was probably chrome crashing/being closed or the page not loading the element you wanted. The souplist should still get passed and scraping should continue")
        print("Let's check:",
              e)
    for x in range(len(sourcelist)):
        soup = BeautifulSoup(sourcelist[x], 'lxml')
        souplist.append(soup)
    return(souplist)


options = webdriver.ChromeOptions()
options.add_argument("--log-level=OFF")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://ttaa.or.th/member-directory/")

sourcelist = []
# options = webdriver.ChromeOptions()


driver.implicitly_wait(10)
page_source = driver.page_source
sourcelist.append(page_source)
# aria-label="Next"
# // *[ @ id = "member-list"] / div[3] / div / div[2] / nav / ul / li[43]
WebDriverWait(driver, 8).until(
    EC.element_to_be_clickable((By.XPATH, "[@id='member-list']//div//div//div//nav//ul//li"))).click()
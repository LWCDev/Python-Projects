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

# from website https://www.aiconnect.co.za/(S(2owykudnpgrervygq2o4odjl))/exhibitor-directory/details.aspx?eid=8e66f3c2-ea1b-454b-a54f-c08efc01f101&cid=29e40bcf-4cf2-4fcc-84d8-def82ee1fbdd


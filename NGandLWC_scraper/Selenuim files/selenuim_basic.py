import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# First test site https://www.biketours.com/
# Second test site https://www.classic-car-tours.com/

# Q's
# 1. what site would you like to scrape?
# 2. Does the search bar require a click:0
# 3. If yes to previous question add Path:0
# 4. How many drop down columns
# 5. dropdown parent path
# 6. dropdown child path


# Site 1 :
# 1.  https://www.biketours.com/
# 2.  Yes
# 3.  //*[@id="home-search-input"]
# 4.  2
# 5.  // *[ @ id = "home-search-dropdown"] / div[2] / div[1] / div / div[
# 6.  li


# Site 2:
# 1. https://www.classic-car-tours.com/
# 2. 0
# 3. 0
# 4. 0
# 5. //*[@id="1273917352"]/ul/li[2]/ul
# 6. li

# Site 3:
# 1. https://www.bookmotorcycletours.com/
# 2. Yes
# 3. //*[@id="compound_search"]/input
# 4. 0
# 5. //*[@id="search__modal-compoundsearch"]/div[2]/div[2]/ul[2]/ul
# 6. li


class UniScrape():

    def __init__(self, source, page_type, dropdown_parent_element, dropdown_child_element, dropdown_input, number_of_colums,requires_click
                 ):
        # Original webpage
        self.source = source
        # Whether the page needs pagination or not
        self.page_type = page_type

        self.dropdown_parent_element = dropdown_parent_element
        # Child of the drop down menu (The amount of repeats of this element will change with each search)
        self.dropdown_parent_element = dropdown_child_element
        #  The input for the dropdown search
        self.dropdown_input = dropdown_input
        # The value that will be assigned to the attribute to make this a selected class
        self.select_current_dropdown_attribute_value = select_current_dropdown_attribute_value
        # Class attribute
        self.Class_attribute = Class_attribute

        self.number_of_colums = number_of_colums
        self.requires_click = requires_click


    # page_type = input("What type is this page?")
    def selenuim_dynamic_dropdown(self, source, page_type, dropdown_parent_element, dropdown_child_element, dropdown_input, number_of_colums,requires_click):

        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(f'{source}')

        time.sleep(length_of_sleep)
        # Needs to be a input of "Dropdown" to run
        if page_type == "Dropdown":
            list_of_urls = []
            # if input is needed
            if requires_click == "Yes":
                # input = driver.find_element(By.CLASS_NAME, f'{dropdown_input}')
                # XPATH  - Seems like the better choice
                input = driver.find_element(By.XPATH, f'{dropdown_input}')
                time.sleep(1)
                input.click()
                time.sleep(1)
            else:
                print("Could not find drop down")


            if number_of_colums == 0:
                parent_div = driver.find_element(By.XPATH, f'{dropdown_parent_element}')
                urls = parent_div.find_elements(By.CSS_SELECTOR, f'li')
                for divs in urls:
                    url = divs.find_element(By.CSS_SELECTOR, f'a').get_attribute('href')
                    print(url)

                    list_of_urls.append(url)

            else:
                for i in range (1, self.number_of_colums +1):
                    #  For this it is best to get the front part of the X-path and add the other part on as a variable.  // *[ @ id = "home-search-dropdown"] / div[2] / div[1] / div / div[**Variable**]
                    parent_div = driver.find_element(By.XPATH, f'{dropdown_parent_element}{i}]')

                    print(parent_div)


                    time.sleep(1)
                    # count_of_divs = len(parent_div.find_elements(By.CLASS_NAME, f'{dropdown_child_element}'))

                    # count_of_divs = len(parent_div.find_elements(By.CSS_SELECTOR, f'li'))
                    urls = parent_div.find_elements(By.CSS_SELECTOR, f'li')

                    for divs in urls:
                        url = divs.find_element(By.CSS_SELECTOR, f'a').get_attribute('href')
                        print(url)

                        list_of_urls.append(url)
            print(list_of_urls)

            #
            #     # Loop through all the elements in a dropdown
            #     for dropdowns in range(1, count_of_divs + 1):
            #         # Testing
            #         # for dropdowns in range(2, 5, 1):
            #
            #         postcode_input.send_keys(postcode)
            #
            #         time.sleep(length_of_sleep)
            #         print(dropdowns, 'out of', count_of_divs, 'results in postcode search: ', postcode)
            #        ul > li
            #
            #         try:
            #             # *** This will cause issues for other sites will fix this later ***
            #             dropdown_increments = driver.find_element(By.XPATH,
            #                                                       f'{dropdown_parent_element}/div[{dropdowns}]')
            #             # *** This will cause issues for other sites will fix this later ***
            #             # Assign the text of the current postcode to a name
            #             names_of_postcodes = driver.find_element(By.XPATH,
            #                                                      f'{dropdown_parent_element}/div[{dropdowns}]/div[1]').text
            #
            #             # print(dropdown_increments)
            #             print('Postcode: ', names_of_postcodes)
            #
            #             # Setting the attribute and attribute name so the current dropdown option is selected
            #             driver.execute_script(
            #                 f"arguments[0].setAttribute('class',"
            #                 f" '{select_current_dropdown_attribute_value}')",
            #                 dropdown_increments)
            #             # driver.execute_script(
            #             #     "arguments[0].setAttribute('class', 'angucomplete-row ng-scope angucomplete-selected-row')",
            #             #     dropdown_increments)
            #
            #         except:
            #             print('no dropdown or element found')
            #         time.sleep(length_of_sleep)
            #         try:
            #             # Click current dropdown
            #             dropdown_increments.click()
            #         except:
            #             print('There is no element to click')
            #         time.sleep(length_of_sleep)
            #         postcode_input.clear()
        else:
            print("There is no dropdown")


# Basic info
page_type = 'Dropdown'
sourcepage = 'https://www.biketours.com/'
Class_attribute = 'class'
dropdown_input = 'search-input'
select_current_dropdown_attribute_value = 'angucomplete-row ng-scope angucomplete-selected-row'
# Sleep timer
length_of_sleep = 3


# Currently working

# sourcepage = 'https://www.biketours.com/'
# number_of_colums = 2
# dropdown_parent_element = '// *[ @ id = "home-search-dropdown"] / div[2] / div[1] / div / div['
# dropdown_child_element = 'li'

# https://www.classic-car-tours.com/
# 0
# //*[@id="1273917352"]/ul/li[2]/ul
# li
# sourcepage = "https://www.biketours.com/"
# requires_click = "Yes"
# dropdown_input = "search-input"
# number_of_colums = 2
# dropdown_parent_element =  '// *[ @ id = "home-search-dropdown"] / div[2] / div[1] / div / div['
# dropdown_child_element = 'li'


# input fields
sourcepage = input("what site would you like to scrape?")
requires_click = input("Does the search bar require a click:")
dropdown_input = input("If yes to previous question add Path:")
number_of_colums = int(input("How many drop down columns:"))
dropdown_parent_element = input("dropdown parent path (X.Path):") #'// *[ @ id = "home-search-dropdown"] / div[2] / div[1] / div / div['
dropdown_child_element = input("dropdown children path (CSS SELECTOR):") # 'li'

g = UniScrape( sourcepage, page_type, dropdown_parent_element, dropdown_child_element, dropdown_input, number_of_colums,requires_click)

g.selenuim_dynamic_dropdown(sourcepage, page_type, dropdown_parent_element, dropdown_child_element, dropdown_input, number_of_colums,requires_click)

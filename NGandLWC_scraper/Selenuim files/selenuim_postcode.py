
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class UniScrape():

    def __init__(self, source, page_type, dropdown_parent_element, dropdown_child_element, dropdown_input
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

    # *********************** Please Read ************* The goal of this particular dropdown search is to type in a
    # postcode, find the parent Div and count out how many child divs there are matching a particular parameter(You
    # define) Once this is found it will be used in a loop as the max count. This can be refactored to take in a list
    # which would be much more practical if it is looking for categories.

    # If there is no search nput at all and it is one drop down menu we can just loop throughout the amount of divs (Easy
    # pecccccy) (Will make a if else)

    def selenuim_dynamic_dropdown(self, source, page_type, dropdown_parent_element, dropdown_child_element, dropdown_input):
        page_type = input("What type is this page?")
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # Download google chrome driver (Needed for Selenuim)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(f'{source}')

        time.sleep(length_of_sleep)
        # Needs to be a input of "Dropdown" to run
        if page_type == page_type:

            postcode_input = driver.find_element(By.XPATH, f'{dropdown_input}')

            # Loop through increments of 5 for the postcodes.
            for postcode in range(5, 65, 5):
                # print(postcode)
                parent_div = driver.find_element(By.XPATH, f'{dropdown_parent_element}')
                # 2 seconds or will not catch
                time.sleep(length_of_sleep)
                postcode_input.send_keys(postcode)
                # 2 seconds or will not catch
                time.sleep(length_of_sleep)
                count_of_divs = len(parent_div.find_elements(By.CLASS_NAME, f'{dropdown_child_element}'))
                # print(count_of_divs)

                # Loop through all the elements in a dropdown
                for dropdowns in range(1, count_of_divs + 1):
                    # Testing
                    # for dropdowns in range(2, 5, 1):

                    postcode_input.send_keys(postcode)

                    time.sleep(length_of_sleep)
                    print(dropdowns, 'out of', count_of_divs, 'results in postcode search: ', postcode)

                    try:
                        # *** This will cause issues for other sites will fix this later ***
                        dropdown_increments = driver.find_element(By.XPATH,
                                                                  f'{dropdown_parent_element}/div[{dropdowns}]')
                        # *** This will cause issues for other sites will fix this later ***
                        # Assign the text of the current postcode to a name
                        names_of_postcodes = driver.find_element(By.XPATH,
                                                                 f'{dropdown_parent_element}/div[{dropdowns}]/div[1]').text

                        # print(dropdown_increments)
                        print('Postcode: ', names_of_postcodes)

                        # Setting the attribute and attribute name so the current dropdown option is selected
                        driver.execute_script(
                            f"arguments[0].setAttribute('class',"
                            f" '{select_current_dropdown_attribute_value}')",
                            dropdown_increments)
                        # driver.execute_script(
                        #     "arguments[0].setAttribute('class', 'angucomplete-row ng-scope angucomplete-selected-row')",
                        #     dropdown_increments)

                    except:
                        print('no dropdown or element found')
                    time.sleep(length_of_sleep)
                    try:
                        # Click current dropdown
                        dropdown_increments.click()
                    except:
                        print('There is no element to click')
                    time.sleep(length_of_sleep)
                    postcode_input.clear()
            else:
                print("There is no dropdown")


# Basic info
page_type = 'Dropdown'
sourcepage = 'https://pga.org.au/find-a-pga-pro/'
# Attributes
# Xpath = 'By.XPATH'
# Class_name = 'By.CLASS_NAME'
Class_attribute = 'class'
# ID = 'ID'
# Needed for drop down functionality
dropdown_input = '//*[@id="members_value"]'
dropdown_parent_element = '//*[@id="members_dropdown"]'
dropdown_child_element = "angucomplete-row"
select_current_dropdown_attribute_value = 'angucomplete-row ng-scope angucomplete-selected-row'
# Sleep timer
length_of_sleep = 3

g = UniScrape( sourcepage, page_type, dropdown_parent_element, dropdown_child_element, dropdown_input)

g.selenuim_dynamic_dropdown(sourcepage, page_type, dropdown_parent_element,
                            dropdown_child_element, dropdown_input)

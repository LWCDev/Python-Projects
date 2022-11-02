from selenium import webdriver
from time import sleep
import os
import csv

class GetURLs:

    def __init__(self):
        pass


    def user_agent(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'
        proxy_ip = "localhost"
        proxy_port = int('24005')
        options = webdriver.FirefoxOptions()
        # options.add_argument('-headless')
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        profile.set_preference('permissions.default.image', 2)
        # profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy_ip)
        profile.set_preference("network.proxy.http_port", proxy_port)
        # profile.set_preference("network.proxy.ssl",proxy_ip)
        # profile.set_preference("network.proxy.ssl_port",proxy_port)
        driver = webdriver.Firefox(executable_path='C:/Users/jack.baxter/AppData/Local/Programs/Python/Python39/geckodriver', firefox_profile=profile,
                                   options=options, service_log_path=os.devnull)
        return driver

    def get_redirect_urls_list(self):
        with open('redirects/vanakkamredirects.csv', 'r') as csv_file:
            lines = csv_file.readlines()

        redirect_urls = []
        for line in lines[1:]:
                url = line.strip("\n")
                redirect_urls.append(url)

        return redirect_urls

    def get_actual_url(self, driver, redirect_url):
        try:
            driver.get(redirect_url)
            sleep(10)
            found_url = driver.current_url
            found_domain = found_url.replace('http://', "")
            found_domain = found_domain.replace('https://', "")
            found_domain = found_domain.replace('www.', "")
            split_string = found_domain.split('/')
            found_domain = split_string[0]
            new_split_string = found_domain.split('?')
            found_domain = new_split_string[0]
        except:
            found_domain = ""
        print(found_domain)

        result = {'URL': found_domain}

        return result


if __name__ == '__main__':
    redirect_urls = GetURLs().get_redirect_urls_list()
    driver = GetURLs().user_agent()

    with open('urls/vanakkamurls.csv', 'a', newline='', encoding="utf-8-sig") as input_file:
        headers = ['URL']
        writer = csv.DictWriter(input_file, fieldnames=headers, dialect='excel')
        writer.writeheader()

    for redirect_url in redirect_urls:
        result = GetURLs().get_actual_url(driver=driver, redirect_url=redirect_url)
        
        with open('urls/vanakkamurls.csv', 'a', newline='', encoding="utf-8-sig") as input_file:
            headers = ['URL']
            writer = csv.DictWriter(input_file, fieldnames=headers, dialect='excel')
            writer.writerow(result)
            
driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import os, time, datetime


# webdriver 
url = 'https://www.all-senmonka.jp/search/chiba/'
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get(url)


# next_button function
def next_button():
    is_found = True

    while is_found:
        try:
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '#search_next > a').click()
        except:
            is_found = False
# call the function
next_button()


# empty list to store the office names
office_list = []

# the list of members
member_list = driver.find_element(By.ID, 'search_results')

for member in member_list.find_elements(By.CLASS_NAME, 'result_block'):
    h3_title = member.find_element(By.CSS_SELECTOR, 'h3').text
    office_list.append(h3_title)

driver.close()

print(len(office_list))

### create function to save h3_title to csv here ###
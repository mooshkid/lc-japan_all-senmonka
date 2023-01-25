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


### create the next button function here ###





# the list of members
member_list = driver.find_element(By.ID, 'search_results')

for member in member_list.find_elements(By.CLASS_NAME, 'result_block'):
    h3_title = member.find_element(By.CSS_SELECTOR, 'h3').text
    print(h3_title)



### create function to save h3_title to csv here ###
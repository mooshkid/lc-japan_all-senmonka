from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, time, datetime


# webdriver 
url = 'https://www.all-senmonka.jp/search/chiba/'
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get(url)

## 1 ##
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


## 2 ##
# empty list to store the office names
office_list = []
print('Creating list of all office names...')

# the list of members
member_list = driver.find_element(By.ID, 'search_results')

for member in member_list.find_elements(By.CLASS_NAME, 'result_block'):
    h3_title = member.find_element(By.CSS_SELECTOR, 'h3').text
    office_list.append(h3_title)

driver.close()

print(str(len(office_list)) + ' Offices Found' + '\n')


## 3 ##
# search office names in google 
for query in office_list[:3]:

    # set the number of search results
    results = 1
    url = (f"https://www.google.com/search?q={query}&num={results}")
    response = requests.get(url)

    # parse the response's HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # the title div
    title = soup.select_one('div.kCrYT > a')
    text = title.text
    link = title['href']

    print(text)
    print(link.replace('/url?q=', '').split("&sa=U")[0])
    print('\n')



### create function to save h3_title to csv here ###
## 4 ##    
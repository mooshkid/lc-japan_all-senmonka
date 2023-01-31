from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


prefecture = 'iwate'

# webdriver 
url = 'https://www.all-senmonka.jp/search/{}/'.format(prefecture)
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get(url)


## Functions ##
# next_button function
def next_button():
    is_found = True
    print('Clicking next...')

    while is_found:
        try:
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '#search_next > a').click()
        except:
            is_found = False

# scrape_emails function
def scrape_emails(i, prefecture):
    retries = 3
    retries_left = retries
    while retries_left:
        try:
            page = requests.get(i, timeout=5, allow_redirects=False)
            break
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
            retries_left -= 1
            if retries_left == 0:
                print(f"Could not retrieve the page after {retries} tries.")
                return

    soup = BeautifulSoup(page.content, 'html.parser')
    emails = []
    for link in soup.find_all('a'):
        email = link.get('href')
        if email:
            match = re.search(r'[\w\.-]+@[\w\.-]+', email)
            if match:
                emails.append(match.group(0))

    print(emails)

    df = pd.DataFrame(emails, columns=["Email"])
    df.to_csv(prefecture + '.csv', mode='a', index=False, header=False)



### Main Script ###

## Variables ##
# empty list to store urls
url_list = []
# set the number of search results
results = 1
# counter
counter = 0


## 1 ##
# call the function
next_button()


## 2 ## - Create List of All Offices
# empty list to store the office names
office_list = []
print('Creating list of all office names...')

# the list of members
member_list = driver.find_element(By.ID, 'search_results')

for member in member_list.find_elements(By.CLASS_NAME, 'result_block'):
    office_name = member.find_element(By.CSS_SELECTOR, 'h3').text
    office_list.append(office_name)

driver.close()

office_count = str(len(office_list))
print(office_count + ' Offices Found' + '\n')


## 3 ## - Begin searching Google
for query in office_list:

    counter += 1

    url = (f"https://www.google.com/search?q={query}&num={results}")
    response = requests.get(url)

    # parse the response's HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # the title div
    title = soup.select_one('div.kCrYT > a')
    
    # incase there are no search results
    if title is not None:
        text = title.text
        link = title['href'].replace('/url?q=', '').split("&sa=U")[0]
        url_list.append(link)

        print('Starting(' + str(counter) + '/' + office_count + ')...')
        print(text)
        print(link)
        # call the function with arguments
        scrape_emails(link, prefecture)

        print("---------------")
        
    else:
        continue

print('Done')
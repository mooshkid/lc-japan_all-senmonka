from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from collections import deque
import re
import pandas as pd
import os, time, datetime


prefecture = 'chiba'

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
def scrape_emails():
    i = link
    unscraped = deque([i])

    scraped = set()

    emails = set()

    while len(unscraped):
        url = unscraped.popleft()
        scraped.add(url)

        parts = urlsplit(url)

        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
            path = url[:url.rfind('/')+1]
        else:
            path = url

        print("Crawling URL %s" % url)
        try:
            response = requests.get(url, timeout=5, allow_redirects=False)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            continue

        ### CHOOSE THE BEST REGEX HERE ###
        new_emails = set(re.findall(
            # r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            # r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text, re.I))
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,}\b', response.text, re.I))
        emails.update(new_emails)

        print(emails)

        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all("a"):
            if "href" in anchor.attrs:
                link = anchor.attrs["href"]
            else:
                link = ''

                if link.startswith('/'):
                    link = base_url + link

                elif not link.startswith('http'):
                    link = path + link

                if not link.endswith(".gz"):
                    if not link in unscraped and not link in scraped:
                        unscraped.append(link)

    print("---------------")
    

    df = pd.DataFrame(emails, columns=["Email"])
    df.to_csv(prefecture + '.csv', mode='a', index=False, header=False)




### Main Script ###
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
        # call the function 
        scrape_emails()
        
    else:
        continue

print('Done')
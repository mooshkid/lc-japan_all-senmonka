import requests
import re
from bs4 import BeautifulSoup

url = "https://lcom-energy.jp/service/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

emails = []
for link in soup.find_all('a'):
    email = link.get('href')
    if email:
        match = re.search(r'[\w\.-]+@[\w\.-]+', email)
        if match:
            emails.append(match.group(0))

print(emails)
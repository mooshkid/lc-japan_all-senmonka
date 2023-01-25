import requests
from bs4 import BeautifulSoup

query_list = ['elephant', 'strawberries']
results = 3


for query in query_list:

    # send a GET request to Google with the query
    url = (f"https://www.google.com/search?q={query}&num={results}")
    response = requests.get(url)

    # parse the response's HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # the title div
    title = soup.select('div.kCrYT > a')
    for i in title:
        text = i.text
        link = i['href'].replace('/url?q=', '').split("&sa=U")[0]

        print(text)
        print(link)
        print('\n')
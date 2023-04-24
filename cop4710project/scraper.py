import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
url = 'https://store.steampowered.com/search/?filter=topsellers&start=0&count=105'


response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, features='html.parser')

info = soup.find_all('div', {'class': 'responsive_search_name_combined'})

for item in info:


    name = item.find('span', {'class': 'title'}).text
    date = item.find('div', {'class': 'col search_released responsive_secondrow'}).text
    price_element = item.find('div', {'class': 'col search_price responsive_secondrow'}) # Store the element in a variable
    price = price_element.text.strip() if price_element else 'Price not available' # Add a conditional check here
    print(name)
    print(date)
    print(price)
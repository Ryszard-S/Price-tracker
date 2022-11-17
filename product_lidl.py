import requests
from dotenv import load_dotenv
import django
import os
from bs4 import BeautifulSoup

load_dotenv()

django.setup()


def _get_name(name):
    name = name.split(" ")
    _brand: str = ""
    _title: str = ""
    for i in name:
        if i.isupper():
            _brand += i + " "
        else:
            _title += i + " "
    return _brand.strip(), _title.strip()


req = requests.get('https://www.lidl.pl/c/najlepsze-okazje/a10009219')
soup = BeautifulSoup(req.text, 'html.parser')
product_divs = soup.find_all('div', 'AProductGridBox')
for product in product_divs:
    product_id = product['section-item-id']
    canonical_url = product['canonicalurl']
    brand, full_title = _get_name(product['fulltitle'])
    print("product_id: ", product_id, "full_title: ", full_title, "canonical_url: ", canonical_url, "brand: ", brand)

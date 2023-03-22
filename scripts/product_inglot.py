import requests
from dotenv import load_dotenv
import django
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

load_dotenv()

django.setup()
from prices.models import *

shop_id = Shop.objects.get(name='INGLOT')
category_id = Category.objects.get(shop_id=shop_id)
brand_id = ProductBrand.objects.get(shop_id=shop_id)
print(shop_id)


def add_inglot_products():
    req = requests.get('https://inglot.pl/107-makijaz?resultsPerPage=500&order=product.price.asc')
    soup = BeautifulSoup(req.text, 'html.parser')
    articles = soup.find_all("article")

    for article in articles:

        product_id = int(article['data-id-product'])
        product_name = article.find('h2', 'product-title').get_text().strip()

        try:
            product = Product.objects.get(shop_product_id=product_id, shop_id=shop_id)
        except ObjectDoesNotExist:
            photo_url: str = article.find('img')['src'].lstrip('https:')
            product = Product.objects.create(shop_product_id=product_id, product_name=product_name,
                                             shop_id=shop_id, photo_url=photo_url,
                                             category_id=category_id, brand_id=brand_id)
        except MultipleObjectsReturned:
            print(product_id, 'MULTIPLE')
            continue

        if product_price := article.find('span', 'price'):
            product_price = product_price.get_text().strip().replace(',', '.').replace(u'\xa0', '').replace("zł", '')

        if product_price_promo := article.find('span', 'regular-price'):
            product_price_promo = product_price_promo.get_text().strip().replace(',', '.').replace(u'\xa0', '').replace(
                "zł", '')
            product_price, product_price_promo = product_price_promo, product_price

        Price.objects.create(product_id=product, price=product_price, price_promo=product_price_promo)

        print(("product_id: ", product_id,
               "product_name: ", product_name,
               "product_price: ", product_price,
               "product_price_promo: ", product_price_promo),
              sep='\n')


def update_photos():
    req = requests.get('https://inglot.pl/107-makijaz?resultsPerPage=500&order=product.price.asc')
    soup = BeautifulSoup(req.text, 'html.parser')
    articles = soup.find_all("article")

    for article in articles:
        product_id = int(article['data-id-product'])
        product_name = article.find('h2', 'product-title').get_text().strip()
        photo_url: str = article.find('img')['src'].lstrip('https:')
        try:
            product = Product.objects.get(shop_product_id=product_id, shop_id=shop_id)
            product.photo_url = photo_url
            product.save()
        except MultipleObjectsReturned:
            print(product_id, 'MULTIPLE')
        except ObjectDoesNotExist:
            print(product_id, 'DO NOT EXIST')
        # print(product_id, product_name, photo_url)


if __name__ == '__main__':
    update_photos()
    # add_inglot_products()

import json
from random import randint
from time import sleep
import logging

from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from dotenv import load_dotenv

load_dotenv()

from django.conf import settings
import os
import django
from pathlib import Path
import dj_database_url
import requests

django.setup()

# print(dj_database_url.parse(os.environ.get( 'DATABASE_URL')))
# settings.configure(dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600))
#
#
from prices.models import *

shop = Shop.objects.get(name='CARREFOUR')
user_agent = os.environ.get('User-Agent')

X_SESSION = requests.get("https://www.carrefour.pl/", headers={"User-Agent": user_agent}).cookies['SESSION']
print(X_SESSION)

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s\t%(levelname)s\t%(message)s')


def get_categories():
    req = requests.get("https://www.carrefour.pl/", headers={"User-Agent": user_agent})
    soup = BeautifulSoup(req.text, 'html.parser')
    link = soup.find_all('a', 'MuiButtonBase-root jss135 gtm-cat')
    arr = []
    for i in link:
        x = i['href']
        print(x)
        print(type(x))
        y = x.lstrip('/')
        arr.append(y)

    with open('cat_carrefour.txt', 'w') as f:
        for i in arr:
            f.write(i + '\n')


def add_carrefour_products():
    req = requests.get(
        'https://www.carrefour.pl/web/catalog?available=true&page=0',
        headers={"X-Session": X_SESSION, "User-Agent": user_agent})
    jar = req.cookies
    print(req, jar)
    # if get_page_end.status_code == 200:
    #     page_end = get_page_end.json()['totalPages']
    # else:
    #     page_end = 0
    # print(page_end)
    # pages = range(0, page_end)

    categories = Category.objects.filter(shop_id=shop)
    for category in categories:
        print(category.category_name)

        req = requests.get(
            f'https://www.carrefour.pl/web/catalog?available=true&categorySlugs={category.category_name}&resolveBrands=true&page=0',
            headers={"X-Session": X_SESSION, "User-Agent": user_agent})

        if req.status_code == 200:
            page_end = req.json()['totalPages']
        else:
            page_end = 0
        print(page_end)
        pages = range(0, page_end)

        for page in pages:
            time = randint(1, 2)
            print('sleep: ', time)
            sleep(time)

            req = requests.get(
                f'https://www.carrefour.pl/web/catalog?available=true&categorySlugs={category.category_name}&resolveBrands=true&page={page}',
                headers={"X-Session": X_SESSION, "User-Agent": user_agent}, cookies=jar)

            print('page: ', page, 'status code: ', req.status_code)
            items = req.json()['content']
            print(len(items))

            for item in items:

                brand_name = item.get('brandName', "Carrefour")
                product_name = item.get('name')
                product_id = item.get('product').get('id')
                ean = [item.get('product').get('code', None)]
                photo_name = item.get('defaultImage').get('name')
                photo_url = 'https://www.carrefour.pl/images/product/180x180/' + photo_name

                # try:
                #     category_id = item['defaultCategoryId']
                #     category = Category.objects.get(shop_category_id=category_id, shop_id=shop)
                # except ObjectDoesNotExist:
                #     category_name = item['defaultCategoryName']
                #     category = Category.objects.create(shop_category_id=category_id, category_name=category_name,
                #                                        shop_id=shop)

                brand_id, brand_created = ProductBrand.objects.get_or_create(shop_id=shop, brand_name=brand_name)

                print('brand created: ', brand_created, brand_id)
                try:
                    product = Product.objects.get(shop_product_id=product_id, shop_id=shop)
                except ObjectDoesNotExist:
                    product = Product(shop_product_id=product_id, product_name=product_name, shop_id=shop,
                                      category_id=category, brand_id=brand_id, ean=ean, photo_url=photo_url)
                    product.save()
                except MultipleObjectsReturned:
                    logging.warning(f'MULTIPLE product_id: {product_id}')

                promo = item['actualSku']['promotion']
                if promo:
                    price = item.get('actualSku').get('amount').get('actualOldPrice')
                    price_promo = item.get('actualSku').get('amount').get('actualGrossPrice')
                else:
                    price = item.get('actualSku').get('amount').get('actualGrossPrice')
                    price_promo = None

                print("price: ", price, "Promo price: ", price_promo)

                Price.objects.create(product_id=product, price=price, price_promo=price_promo)


if __name__ == '__main__':
    # Product.objects.all().delete()
    # Price.objects.all().delete()
    # add_rossmann_products()
    # print('end')
    # r = requests.get("https://www.carrefour.pl/").cookies['SESSION']
    # print(r)
    # page_endd = requests.get(
    #     'https://www.carrefour.pl/web/catalog?available=true&page=0', headers={"X-Session": X_SESSION}).json()[
    #     'totalPages']

    # get_categories()
    add_carrefour_products()

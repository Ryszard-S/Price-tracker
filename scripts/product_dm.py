from time import sleep
import logging

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from dotenv import load_dotenv

load_dotenv()

import django
import requests

django.setup()

from prices.models import *

shop = Shop.objects.get(name='DM')

logging.basicConfig(filename='../app.log', level=logging.DEBUG, format='%(asctime)s\t%(levelname)s\t%(message)s')


def add_dm_products():
    categories = Category.objects.filter(shop_id=shop)
    cat = {
        "Makijaż": '010000',
        "Pielęgnacja i perfumy": '020000',
        "Włosy": "110000",
        "Mężczyzna": '021400',
        "Zdrowie": '030000',
        "Odżywianie": '040000',
        "Dzieci i niemowlęta": '050000',
        "Gospodarstwo domowe": '060000',
        "Zwierzęta": '070000',
    }
    for category in categories:
        print(category.category_name)
        cat_id = cat.get(category.category_name)

        req = requests.get(
            f'https://product-search.services.dmtech.com/pl/search/crawl?allCategories.id={cat_id}&sort=editorial_relevance&type=search-static&pageSize=100&currentPage=0')

        if req.status_code == 200:
            page_end = req.json()['totalPages']
        else:
            page_end = 0
        print(page_end)
        pages = range(0, page_end)

        for page in pages:
            req = requests.get(
                f'https://product-search.services.dmtech.com/pl/search/crawl?allCategories.id={cat_id}&sort=editorial_relevance&type=search-static&pageSize=100&currentPage={page}')
            print('headers: ', req.headers)

            print('page: ', page, 'status code: ', req.status_code)
            if req.status_code == 429:
                for i in range(0, 60):

                    if i % 5 == 0:
                        print('sleep: ', i)
                    sleep(1)

                req = requests.get(
                    f'https://product-search.services.dmtech.com/pl/search/crawl?allCategories.id={cat_id}&sort=editorial_relevance&type=search-static&pageSize=100&currentPage={page}')
                print('after sleep page: ', page, 'status code: ', req.status_code)
            items = req.json()['products']

            for item in items:

                brand_name = item.get('brandName', 'DM')
                product_name = item.get('title')
                product_id = item.get('dan')
                ean = [item.get('gtin')]
                photo_name = item.get('imageUrlTemplates')[0]
                photo_url = photo_name.replace("{transformations}", "f_auto,q_auto,c_fit,h_270,w_260").lstrip('https:')

                brand_id, brand_created = ProductBrand.objects.get_or_create(shop_id=shop, brand_name=brand_name)

                try:
                    product = Product.objects.get(shop_product_id=product_id, shop_id=shop)
                except ObjectDoesNotExist:
                    product = Product(shop_product_id=product_id, product_name=product_name, shop_id=shop,
                                      category_id=category, brand_id=brand_id, ean=ean, photo_url=photo_url)
                    product.save()
                except MultipleObjectsReturned:
                    logging.warning(f'MULTIPLE product_id: {product_id}')

                promo = item.get('selloutPriceLocalized', None)
                if promo:
                    price = promo.rstrip(' zł').replace(',', '.')
                    price_promo = item.get('price').get('value')
                else:
                    price = item.get('price').get('value')
                    price_promo = None

                print("price: ", price, "Promo price: ", price_promo)

                Price.objects.create(product_id=product, price=price, price_promo=price_promo)


if __name__ == '__main__':
    add_dm_products()

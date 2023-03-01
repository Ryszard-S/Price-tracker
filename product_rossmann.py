import json

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

shop = Shop.objects.get(name='ROSSMANN')


def add_rossmann_brands():
    req = requests.get('https://www.rossmann.pl/additionals/api/brands')
    brands = req.json()
    keys_in_brands = brands['data'].keys()

    only_brands = []

    for x in keys_in_brands:
        w = brands['data'][x]['brands']
        for y in w:
            only_brands.append({'name': y['name'], 'id': y['id']})

    sorted_brands_by_id = sorted(only_brands, key=lambda k: k['id'])

    for brand in sorted_brands_by_id:
        ProductBrand.objects.create(shop_id=shop, shop_product_brand_id=brand['id'], brand_name=brand['name'])


def add_rossmann_categories():
    # with open('response_categories.json', 'r', encoding="utf-8") as f:
    #     categories_json = json.load(f)

    # categories_row = categories_json['data']
    req = requests.get('https://www.rossmann.pl/products/api/Categories')
    categories_json = req.json()
    for i in categories_json['data']:
        for j in i['children']:
            for k in j['children']:
                Category.objects.create(shop_category_id=k['id'], category_name=k['name'], shop_id=shop)


def add_rossmann_products():
    page_end = requests.get(
        'https://www.rossmann.pl/marketing/api/Catalog?Page=1&PageSize=100&SortOrder=priceAsc').json()['data'][
        'totalPages']

    print(page_end, page_end + 1)
    pages = range(1, page_end + 1)
    for page in pages:
        req = requests.get(f'https://www.rossmann.pl/marketing/api/Catalog?Page={page}&PageSize=100&SortOrder=priceAsc')
        items = req.json()['data']['items']
        print(page, req.status_code)

        for item in items:
            i = item['product']
            print(i)

            category = i['category'].split('-')[-1]
            print(category)

            product_name = i['caption'] + " " + i.get('name', '')
            shop_product_id = i['id']
            # product_name = i['name']
            shop_id = shop
            try:
                category_id = Category.objects.get(category_name=category, shop_id=shop)
            except:
                category_id = None

            try:
                brand_id = ProductBrand.objects.get(shop_id=shop, shop_product_brand_id=i['brandId'])
            except:
                brand_id = ProductBrand.objects.create(shop_id=shop, shop_product_brand_id=i['brandId'],
                                                       brand_name=i['brand'])

            try:
                product = Product.objects.get(shop_product_id=shop_product_id, product_name=product_name,
                                              shop_id=shop_id, category_id=category_id, brand_id=brand_id)
            except:
                product = Product.objects.create(shop_product_id=shop_product_id, product_name=product_name,
                                                 shop_id=shop_id, category_id=category_id, brand_id=brand_id)

            price = i.get('price')
            old_price = i.get('oldPrice', None)
            price_promo = None
            if old_price:
                price, price_promo = old_price, price

            print("price: ", price, "Promo price: ", price_promo)

            Price.objects.create(product_id=product, price=price, price_promo=price_promo)


if __name__ == '__main__':
    # Product.objects.all().delete()
    # Price.objects.all().delete()
    add_rossmann_products()
    print('end')

import logging

import requests
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from dotenv import load_dotenv
import django
import os

load_dotenv()

django.setup()
from prices.models import *

logging.basicConfig(filename='app_xkom.log', level=logging.DEBUG, format='%(asctime)s\t%(levelname)s\t%(message)s')

shop = Shop.objects.get(name='X-KOM')

print(shop)
X_API_Key = os.environ.get('X-API-Key')
User_Agent = os.environ.get('User-Agent')

headers = {
    'X-API-Key': X_API_Key,
    'User-Agent': User_Agent
}


def get_categories():
    req = requests.get(
        'https://mobileapi.x-kom.pl/api/v1/xkom/categories?groupIds=2,4,7,5,6,8,64,12&expand=ChildCategories',
        headers=headers)

    print('Status: ', req.status_code)

    response = req.json()

    for i in response:
        obj, created = Category.objects.get_or_create(shop_id=shop, category_name=i['NameSingular'],
                                                      shop_category_id=i['Id'])
        if not created:
            print(obj, 'duplicated')

        # children_categories = i.get('ChildCategories', None)
        # if children_categories:
        #     for j in children_categories:
        #         obj, created = Category.objects.get_or_create(shop_id=shop, category_name=j['NameSingular'],
        #                                                       shop_category_id=j['Id'])
        #         if not created:
        #             print(obj)
        # else:
        #     obj, created = Category.objects.get_or_create(shop_id=shop, category_name=i['NameSingular'],
        #                                                   shop_category_id=i['Id'])
        #     if not created:
        #         print(obj, 'from else')


def add_products():
    categories = Category.objects.filter(shop_id=shop)
    for category in categories:
        cat = category.shop_category_id
        req = requests.get(
            f'https://mobileapi.x-kom.pl/api/v1/xkom/products?criteria.categoryIds={cat}&pagination.currentPage=1&pagination.pageSize=90',
            headers=headers)
        print(req.status_code)
        req = req.json()
        pages = req['TotalPages']
        for i in range(1, pages + 1):
            req1 = requests.get(
                f'https://mobileapi.x-kom.pl/api/v1/xkom/products?criteria.categoryIds={cat}&pagination.currentPage={i}&pagination.pageSize=90',
                headers=headers)
            print('status req1 ', req1.status_code)
            req1 = req1.json().get('Items')
            for item in req1:
                brand_name = item.get('Producer').get('Name', 'brak nazwy')
                brand_id, created = ProductBrand.objects.get_or_create(shop_id=shop,
                                                                       brand_name=brand_name,
                                                                       shop_product_brand_id=int(
                                                                           item.get('Producer').get('Id')))

                shop_product_id = int(item.get('Id'))
                product_name = item.get('Name')

                try:
                    product = Product.objects.get(shop_id=shop, shop_product_id=shop_product_id)
                except ObjectDoesNotExist:
                    photo_url: str = item.get('MainPhoto').get('ThumbnailUrl', None)
                    if photo_url:
                        photo_url = photo_url.lstrip('https:')

                    product = Product(shop_product_id=shop_product_id,
                                      product_name=product_name,
                                      shop_id=shop,
                                      category_id=category,
                                      brand_id=brand_id,
                                      photo_url=photo_url)
                    product.save()
                except MultipleObjectsReturned:
                    print('MULTIPLE: ', shop_product_id)
                    logging.warning(f'MULTIPLE shop product id: {shop_product_id}')
                    continue
                except AttributeError:
                    print('ATTRIBUTE ERROR: ', shop_product_id)
                    logging.info(f'ATTRIBUTE ERROR shop product id: {shop_product_id}')
                    continue
                price = item['Price']
                old_price = item.get('OldPrice')
                price_promo = None
                if old_price:
                    price, price_promo = old_price, price

                Price.objects.create(product_id=product, price=price, price_promo=price_promo)


def update_images():
    categories = Category.objects.filter(shop_id=shop)
    for category in categories:
        cat = category.shop_category_id
        req = requests.get(
            f'https://mobileapi.x-kom.pl/api/v1/xkom/products?criteria.categoryIds={cat}&pagination.currentPage=1&pagination.pageSize=90',
            headers=headers)
        print(req.status_code)
        req = req.json()
        pages = req['TotalPages']
        for i in range(1, pages + 1):
            req1 = requests.get(
                f'https://mobileapi.x-kom.pl/api/v1/xkom/products?criteria.categoryIds={cat}&pagination.currentPage={i}&pagination.pageSize=90',
                headers=headers)
            print('status req1 ', req1.status_code, req1.url)
            req1 = req1.json().get('Items')
            for item in req1:
                brand_name = item.get('Producer').get('Name', 'brak nazwy')
                brand_id, created = ProductBrand.objects.get_or_create(shop_id=shop,
                                                                       brand_name=brand_name,
                                                                       shop_product_brand_id=int(
                                                                           item.get('Producer').get(
                                                                               'Id')))

                shop_product_id = int(item.get('Id'))
                product_name = item.get('Name')

                try:
                    product = Product.objects.get(shop_id=shop, shop_product_id=shop_product_id)
                    photo_url: str = item.get('MainPhoto').get('ThumbnailUrl', None)
                    if photo_url:
                        photo_url = photo_url.lstrip('https:')
                    product.photo_url = photo_url
                    product.save()
                    print(photo_url)
                except ObjectDoesNotExist:
                    print('DOES NOT EXIST', shop_product_id)
                except MultipleObjectsReturned:
                    print('MULTIPLE: ', shop_product_id)
                    continue
                except AttributeError:
                    print('ATTRIBUTE ERROR: ', shop_product_id)
                    continue


if __name__ == '__main__':
    # add_products()
    update_images()

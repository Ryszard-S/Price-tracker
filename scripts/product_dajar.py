import logging
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from dotenv import load_dotenv

load_dotenv()

import os
import django
import requests
from math import ceil

django.setup()

from prices.models import *

shop = Shop.objects.get(name='DAJAR')
user_agent = os.environ.get('User-Agent')
headers = {"User-Agent": user_agent}

logging.basicConfig(filename='../app_dajar.log', level=logging.DEBUG, format='%(asctime)s\t%(levelname)s\t%(message)s')

url = "https://dajar.pl/searchengine/pl/V1/products\
?searchCriteria[filter_groups][0][filters][0][field]=category_id\
&searchCriteria[filter_groups][0][filters][0][value]={category_id}\
&searchCriteria[filter_groups][0][filters][0][condition_type]=eq\
&searchCriteria[pageSize]={page_size}\
&searchCriteria[filter_groups][2][filters][0][field]=type_id\
&searchCriteria[filter_groups][2][filters][0][value]=simple\
&searchCriteria[filter_groups][3][filters][0][field]=visibility\
&searchCriteria[filter_groups][3][filters][0][value]=2,4\
&searchCriteria[filter_groups][3][filters][0][condition_type]=in\
&searchCriteria[sortOrders][4][direction]=desc\
&searchCriteria[sortOrders][4][field]=position\
&searchCriteria[sortOrders][5][direction]=desc\
&searchCriteria[sortOrders][5][field]=id\
&searchCriteria[currentPage]={current_page}"


def get_producer(array: []):
    """
    search for producer in array of dict
    """
    for i in array:
        if i.get('attribute_code') == 'producer':
            return i
    return None


def add_dajar_products():
    categories = Category.objects.filter(shop_id=shop)
    for category in categories:
        print(category.shop_category_id)

        req = requests.get(url.format(category_id=category.shop_category_id, page_size=1, current_page=1),
                           headers=headers)

        if req.status_code == 200:
            page_end = ceil(req.json()['total_count'] / 100) + 1
        else:
            page_end = 0
        print("page end: ", page_end, "status code: ", req.status_code)

        for page in range(1, page_end):

            req = requests.get(url.format(category_id=category.shop_category_id, page_size=100, current_page=page),
                               headers=headers)

            print('page: ', page, 'status code: ', req.status_code)
            items = req.json()['items']

            for item in items:

                try:
                    atr = get_producer(item.get("custom_attributes"))
                    brand_id = atr.get('value')
                    brand_name = atr.get('name')
                    brand = ProductBrand.objects.get(shop_product_brand_id=brand_id, shop_id=shop)
                except ObjectDoesNotExist:
                    brand = ProductBrand.objects.create(shop_product_brand_id=brand_id, shop_id=shop,
                                                        brand_name=brand_name)
                except MultipleObjectsReturned:
                    logging.warning(f"brand duplicated: {brand_id}")
                    continue
                except AttributeError:
                    logging.warning(f"Attribute Error brand: {product_id}")
                    continue

                try:
                    product_id = item.get('id')
                    product = Product.objects.get(shop_product_id=product_id, shop_id=shop)
                except ObjectDoesNotExist:
                    product_name = item.get('name')
                    extension_attributes = item.get('extension_attributes')
                    print("extension_attributes: ", extension_attributes)
                    ean = [extension_attributes.get('ean', None)]
                    photo_name = extension_attributes.get("image_dimensions")[0] \
                        .get('product_page_image_small').get('src')
                    photo_url = '//dajarmedia.dajarmedia.com/cdn-cgi/image/width=420,quality=70,format=auto' + photo_name
                    product = Product(shop_product_id=product_id, product_name=product_name, shop_id=shop,
                                      category_id=category, brand_id=brand, ean=ean, photo_url=photo_url)
                    product.save()
                except MultipleObjectsReturned:
                    logging.warning(f'MULTIPLE product_id: {product_id}')
                    continue
                except AttributeError:
                    logging.warning(f"Attribute Error product: {product_id}")
                    continue

                price = item.get('price')
                final_price = item.get('final_price')
                if final_price < price:
                    price_promo = final_price
                else:
                    price_promo = None

                Price.objects.create(product_id=product, price=price, price_promo=price_promo)


if __name__ == '__main__':
    add_dajar_products()

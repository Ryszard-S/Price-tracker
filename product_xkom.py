import requests
from dotenv import load_dotenv
import django
import os

load_dotenv()

django.setup()
from prices.models import *

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
    categories = Category.objects.filter(shop_id=shop, id__gt=989)
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
                print(item)

                if brand_name := item.get('Producer').get('Name', 'brak nazwy'):
                    brand_name = brand_name
                else:
                    brand_name = 'brak nazwy'

                brand_id, created = ProductBrand.objects.get_or_create(shop_id=shop,
                                                                       brand_name=brand_name,
                                                                       shop_product_brand_id=int(
                                                                           item.get('Producer').get('Id')))

                # print(item)
                print(type(item))
                print(type(int(item['Id'])))
                print(brand_id)
                shop_product_id = int(item.get('Id'))
                product_name = item.get('Name')
                product, created = Product.objects.get_or_create(shop_product_id=shop_product_id,
                                                                 product_name=product_name,
                                                                 shop_id=shop,
                                                                 category_id=category,
                                                                 brand_id=brand_id)

                price = item['Price']
                old_price = item.get('OldPrice')
                price_promo = None
                if old_price:
                    price, price_promo = old_price, price

                Price.objects.create(product_id=product, price=price, price_promo=price_promo)


if __name__ == '__main__':
    add_products()

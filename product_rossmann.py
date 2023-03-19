from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from dotenv import load_dotenv

load_dotenv()
import requests
import django

django.setup()
import logging
from prices.models import *

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s\t%(levelname)s\t%(message)s')
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
    req = requests.get('https://www.rossmann.pl/products/api/Categories')
    categories_json = req.json()
    for i in categories_json['data']:
        for j in i['children']:
            for k in j['children']:
                Category.objects.create(shop_category_id=k['id'], category_name=k['name'], shop_id=shop)


def update_rossmann_products():
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
            item = item['product']
            shop_product_id = item['id']
            ean = item.get('eanNumber', None)
            photo_url = item.get('pictures', None)[0].get('medium', None)
            print(ean, photo_url)
            if not ean or not photo_url:
                logging.info(f'shop product id: {shop_product_id}\tean: {ean}\turl: {photo_url}')

            try:
                product = Product.objects.get(shop_product_id=shop_product_id, shop_id=shop)
                product.ean = ean
                product.photo_url = photo_url
                product.save()
            except ObjectDoesNotExist:
                logging.warning(f'shop product id: {shop_product_id} does not exist in db')
            except MultipleObjectsReturned:
                logging.warning(f'MULTIPLE shop product id: {shop_product_id}')


def reduce_prices_for_same_products():
    remove_id = set()
    with open('todelete.txt', 'r') as f:
        x = f.readlines()
        for i in x:
            z = int(i.rstrip('\n'))
            remove_id.add(z)

    for item_id in sorted(remove_id):
        print(item_id)
        products = list(Product.objects.filter(shop_product_id=item_id, shop_id=shop))
        last_product = products[-1]
        for item in products[:-1]:
            print(item.id)
            prices = Price.objects.filter(product_id=item.id)
            for price in prices:
                price.product_id = last_product
                price.save()
            item.delete()
        print('next')


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

            product_name = i['caption'] + " " + i.get('name', '')
            shop_product_id = i['id']
            ean = i.get('eanNumber', None)
            photo_url = i.get('pictures', None)[0].get('medium', None)

            try:
                product = Product.objects.get(shop_product_id=shop_product_id, shop_id=shop_id)
            except ObjectDoesNotExist:
                product = Product.objects.create(shop_product_id=shop_product_id, product_name=product_name,
                                                 shop_id=shop_id, category_id=category_id, brand_id=brand_id, ean=ean,
                                                 photo_url=photo_url)
                logging.info(f'Product Created {shop_product_id}')
            except MultipleObjectsReturned:
                logging.warning(f'MULTIPLE shop product id: {shop_product_id}')

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
    # update_rossmann_products()
    # reduce_prices_for_same_products()
    print('end')

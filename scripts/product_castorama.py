from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from dotenv import load_dotenv

load_dotenv()
import requests
import django

django.setup()
import logging
from prices.models import *

logging.basicConfig(filename='../app_castorama.log', level=logging.DEBUG,
                    format='%(asctime)s\t%(levelname)s\t%(message)s')
shop = Shop.objects.get(name='CASTORAMA')

CATEGORY_URL = "https://www.castorama.pl/api/rest/headless/public/categories/list\
?searchCriteria[filterGroups][0][filters][0][conditionType]=like\
&searchCriteria[filterGroups][0][filters][0][field]=path\
&searchCriteria[filterGroups][0][filters][0][value]=1/2/1574/{main_category}/%\
&searchCriteria[filterGroups][1][filters][0][conditionType]=lteq\
&searchCriteria[filterGroups][1][filters][0][field]=level\
&searchCriteria[filterGroups][1][filters][0][value]=5"

SPECIFIC_CATEGORY_URL = "https://www.castorama.pl/api/rest/headless/public/categories/products\
?searchCriteria[currentPage]={current_page}\
&searchCriteria[filterGroups][0][filters][0][conditionType]=eq\
&searchCriteria[filterGroups][0][filters][0][field]=category\
&searchCriteria[filterGroups][0][filters][0][value]={category_id}\
&searchCriteria[pageSize]=47\
&searchCriteria[sortOrders][0][direction]=desc\
&searchCriteria[sortOrders][0][field]=promoted&storeId=default"

PRODUCTS_URL = "https://www.castorama.pl/bold_all/data/getProductPriceStockByStore/\
?isAjax=true\
&store=1\
&typeBlock=recommended\
&needData={ids}"


def add_categories():
    main_categories = {
        "budowa": 1839,
        'instalacja': 1840,
        'wykonczenie': 1841,
        'urzadzanie': 4355,
        'ogrod': 1843,
        'narzedzia-i-artykuly': 1844
    }
    for main_category in main_categories.values():
        req = requests.get(CATEGORY_URL.format(main_category=main_category))
        print(req.status_code)
        request = req.json()
        for category in request:
            try:
                Category.objects.get(shop_category_id=category['id'], shop_id=shop)
            except ObjectDoesNotExist:
                Category.objects.create(shop_category_id=category['id'], shop_id=shop, category_name=category['name'])
            except MultipleObjectsReturned:
                logging.warning(f"Multiple objects: {category['id']}")
                continue


def add_products():
    categories = Category.objects.filter(shop_id=shop)
    PER_PAGE = 47
    for category in categories:
        print(category.shop_category_id)
        req = requests.get(SPECIFIC_CATEGORY_URL.format(current_page=1, category_id=category.shop_category_id))
        print(req.status_code)
        request = req.json()
        page_end = int(request['all']) // PER_PAGE
        if page_end % PER_PAGE != 0: page_end += 1

        for page in range(1, page_end + 1):
            req = requests.get(SPECIFIC_CATEGORY_URL.format(current_page=page, category_id=category.shop_category_id))
            print(req.status_code)
            request = req.json()
            items = request['items']
            array_ids = [str(i.get("entity_id")) for i in items]
            ids = ','.join(array_ids)
            req1 = requests.get(PRODUCTS_URL.format(ids=ids)).json()
            products: dict = req1.get('products')
            for product_id in array_ids:
                try:
                    product: dict = products.get(product_id, None)

                    brand_name = product.get('attrData', {"brand": "Castorama"}).get('brand', 'Castorama')
                    brand, created = ProductBrand.objects.get_or_create(brand_name=brand_name, shop_id=shop)

                    product_name = product.get('name')
                    photo_url: str = product.get('image')
                    photo_url = photo_url.lstrip('https:')

                    prod = Product.objects.get(shop_product_id=product_id, shop_id=shop)
                except ObjectDoesNotExist:
                    prod = Product.objects.create(shop_product_id=product_id, shop_id=shop, product_name=product_name,
                                                  category_id=category, brand_id=brand, photo_url=photo_url)
                except MultipleObjectsReturned:
                    logging.warning(f"MULTIPLE: shop_product_id: {product_id}")
                    continue
                except AttributeError:
                    logging.warning(f"Attr Err: product_id: {product_id} product(dict): {product}")
                    continue

                price = product.get('price')
                if price_promo := product.get('was_price'):
                    price, price_promo = price_promo, price

                price_obj = Price(product_id=prod, price=price, price_promo=price_promo)
                price_obj.save()


if __name__ == "__main__":
    add_products()

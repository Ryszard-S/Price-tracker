import requests
from dotenv import load_dotenv
import django
from bs4 import BeautifulSoup

load_dotenv()

django.setup()
from prices.models import *

shop_id = Shop.objects.get(name='INGLOT')
category_id = Category.objects.get(shop_id=shop_id)
brand_id = ProductBrand.objects.get(shop_id=shop_id)
print(shop_id)

req = requests.get('https://inglot.pl/107-makijaz?resultsPerPage=500&order=product.price.asc')
soup = BeautifulSoup(req.text, 'html.parser')
articles = soup.find_all("article")

for article in articles:

    product_id = int(article['data-id-product'])
    product_name = article.find('h2', 'product-title').get_text().strip()

    product, created = Product.objects.get_or_create(shop_product_id=product_id, product_name=product_name,
                                                     shop_id=shop_id,
                                                     category_id=category_id, brand_id=brand_id)

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

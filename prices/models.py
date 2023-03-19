from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    shop_category_id = models.IntegerField(null=True, blank=True)  # id which is given by shop api
    category_name = models.CharField(max_length=100)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name


class ProductBrand(models.Model):
    shop_product_brand_id = models.CharField(max_length=30, null=True, blank=True)  # id which is given by shop api
    brand_name = models.CharField(max_length=100)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    shop_product_id = models.CharField(max_length=30, null=True, blank=True)  # id which is given by shop api
    product_name = models.CharField(max_length=300)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    brand_id = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    ean = ArrayField(models.CharField(max_length=13), blank=True, null=True)
    photo_url = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.product_name


class Price(models.Model):
    class Meta:
        ordering = ['date', 'id']

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    price_promo = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product_id.product_name + " " + str(self.price) + " " + str(self.date)

from django.db import models


# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    shop_category_id = models.IntegerField()  # id which is given by shop api
    category_name = models.CharField(max_length=100)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name


class ProductBrand(models.Model):
    shop_product_brand_id = models.IntegerField()  # id which is given by shop api
    brand_name = models.CharField(max_length=100)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    shop_product_id = models.IntegerField()  # id which is given by shop api
    product_name = models.CharField(max_length=300)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    brand_id = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Price(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    price_promo = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.product_id.product_name + " " + str(self.price) + " " + str(self.date)

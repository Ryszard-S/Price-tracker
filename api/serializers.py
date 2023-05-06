from rest_framework import serializers
from prices.models import Shop, Category, ProductBrand, Product, Price


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class ProductWithoutPricesSerializer(serializers.ModelSerializer):
    shop_id = serializers.StringRelatedField(many=False)
    category_id = serializers.StringRelatedField(many=False)
    brand_id = serializers.StringRelatedField(many=False)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(ProductWithoutPricesSerializer):
    prices = PriceSerializer(many=True)

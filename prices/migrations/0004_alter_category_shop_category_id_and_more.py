# Generated by Django 4.1.7 on 2023-03-01 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0003_remove_product_name_alter_price_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='shop_category_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='shop_product_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='shop_product_brand_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
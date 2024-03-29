# Generated by Django 4.1.7 on 2023-03-16 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0006_alter_price_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['date', 'id']},
        ),
        migrations.AlterField(
            model_name='product',
            name='shop_product_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='shop_product_brand_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

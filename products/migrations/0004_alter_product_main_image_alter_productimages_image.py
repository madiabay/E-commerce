# Generated by Django 5.0.1 on 2024-03-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/%Y/%m/%d/', verbose_name='Main Image'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product-images/%Y/%m/%d/', verbose_name='Image'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-29 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerproduct',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
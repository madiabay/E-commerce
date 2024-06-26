# Generated by Django 5.0.1 on 2024-03-14 08:08

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=14)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('amount_currency', models.CharField(choices=[('KZT', 'Kzt'), ('USD', 'Usd'), ('RUB', 'Rub')], max_length=3)),
                ('status', models.CharField(choices=[('New', 'New'), ('Pending', 'Pending'), ('Paid', 'Paid'), ('Expired', 'Expired'), ('Refund', 'Refund'), ('Refund_Partially', 'Refund Partially')], default='New', max_length=20)),
                ('number', models.CharField(db_index=True, max_length=10, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('amount_currency', models.CharField(choices=[('KZT', 'Kzt'), ('USD', 'Usd'), ('RUB', 'Rub')], max_length=3)),
                ('transaction_type', models.CharField(choices=[('OK', 'Ok'), ('Refund', 'Refund')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order')),
            ],
        ),
    ]

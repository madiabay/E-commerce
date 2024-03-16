import uuid
import random

from django.db import models
from payments import choices as bill_status_choices
from seller_products import choices as seller_product_choices


class Bill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.SET_NULL,
        null=True,
    )
    total = models.DecimalField(max_digits=14, decimal_places=2)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    amount_currency = models.CharField(
        max_length=3,
        choices=seller_product_choices.CurrencyChoices.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=bill_status_choices.BillStatusChoices.choices,
        default=bill_status_choices.BillStatusChoices.New,
    )
    number = models.CharField(max_length=10, unique=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_number(cls):
        number = ''.join(random.choices('0123456789', k=10))

        if cls.objects.filter(number=number).exists():
            return cls.generate_number()

        return number


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    bill = models.ForeignKey(to=Bill, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    amount_currency = models.CharField(
        max_length=3,
        choices=seller_product_choices.CurrencyChoices.choices,
    )
    transaction_type = models.CharField(max_length=20, choices=bill_status_choices.TransactionType.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

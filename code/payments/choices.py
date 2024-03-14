from django.db import models


class BillStatusChoices(models.TextChoices):
    New = 'New'
    Pending = 'Pending'
    Paid = 'Paid'
    Expired = 'Expired'
    Refund = 'Refund'
    Refund_Partially = 'Refund_Partially'


class TransactionType(models.TextChoices):
    OK = 'OK'
    Refund = 'Refund'

from django.db import models


class OrderStatusChoices(models.TextChoices):
    new = 'new'
    process_in_progress = 'process_in_progress'
    cancel = 'cancel'
    paid = 'paid'

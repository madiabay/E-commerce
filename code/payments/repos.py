import uuid
from typing import Protocol

from django.db import transaction

from . import models, choices as payments_choices


class BillReposInterface(Protocol):

    @staticmethod
    def pay_bill(bill_id: uuid.UUID): ...


class BillReposV1:

    @staticmethod
    def pay_bill(bill_id: uuid.UUID):
        with transaction.atomic():
            bill = models.Bill.objects.get(id=bill_id)
            bill.status = payments_choices.BillStatusChoices.Paid
            models.Transaction.objects.create(
                order=bill.order,
                amount=bill.amount,
                amount_currency=bill.amount_currency,
                transaction_type=payments_choices.TransactionType.OK,
            )

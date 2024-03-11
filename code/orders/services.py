from typing import Protocol, OrderedDict
from django.db.models import QuerySet
from . import models, repos


class OrderServicesInterface(Protocol):

    def create_order(self, data: OrderedDict) -> models.Order: ...

    def get_orders(self) -> QuerySet[models.Order]: ...


class OrderServicesV1:
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    def create_order(self, data: OrderedDict) -> models.Order:
        return self.order_repos.create_order(data=data)

    def get_orders(self) -> QuerySet[models.Order]:
        return self.order_repos.get_orders()
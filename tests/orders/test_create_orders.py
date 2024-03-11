from collections import OrderedDict

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.test.client import Client
from rest_framework import status

from seller_products import models, choices
from orders import repos


@pytest.mark.django_db
class OrderReposTest:
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    def test_create_user(self):
        customer = get_user_model().objects.get(phone_number='+77076461874')
        seller_product = models.SellerProduct.objects.get()
        data = {
            'customer': customer,
            'order_items': [
                {'seller_product': seller_product}
            ],
        }

        order_repos: repos.OrderReposInterface = repos.OrderReposV1()
        order = order_repos.create_order(data=OrderedDict(data))

        assert order.order_items.count() == len(data['order_items'])

        total = order.order_items.aggregate(total=Sum('amount'))['total']

        assert total == sum([i['seller_product'].amount for i in data['order_items']])

        assert all([i.amount_currency == choices.CurrencyChoices.KZT for i in order.order_items.all()])


@pytest.mark.django_db
class OrderViewsTest:
    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    def test_view_order(self, client: Client):
        customer = get_user_model().objects.get(phone_number='+77076461874')
        data = {
            'order_items': [
                {'seller_product': 1}
            ]
        }
        client.force_login(user=customer)
        response = client.post('/api/v1/orders', data=data)

        assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY

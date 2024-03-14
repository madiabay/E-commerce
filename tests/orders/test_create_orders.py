from collections import OrderedDict

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import status

from seller_products import models
from orders import repos
from payments import models as payments_models, choices as payments_choices
import helpers


@pytest.mark.django_db
class OrderReposTest:
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    @pytest.mark.parametrize('user_id, seller_product_ides', (
        ('4322d2d8-e6df-49b1-882b-1fb79a8fbb70', (1,)),
        ('4322d2d8-e6df-49b1-882b-1fb79a8fbb70', (1, 2))
    ))
    def test_create_order(self, user_id, seller_product_ides):
        customer = get_user_model().objects.get(id=user_id)
        seller_products = models.SellerProduct.objects.filter(id__in=seller_product_ides)
        data = {
            'customer': customer,
            'order_items': [
                {'seller_product': seller_product} for seller_product in seller_products
            ],
        }

        order_repos: repos.OrderReposInterface = repos.OrderReposV1()
        order = order_repos.create_order(data=OrderedDict(data))

        assert order.order_items.count() == len(data['order_items'])

        total = order.order_items.aggregate(total=Sum('amount'))['total']

        assert total == sum([i['seller_product'].amount for i in data['order_items']])

        bill = payments_models.Bill.objects.get(order=order)

        assert bill.amount == bill.total == total
        assert bill.status == payments_choices.BillStatusChoices.New


@pytest.mark.django_db
class OrderViewsTest:
    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    @pytest.mark.parametrize('cases, user_id, status_code', (
        ('1', '4322d2d8-e6df-49b1-882b-1fb79a8fbb70', status.HTTP_201_CREATED),
        ('2', '4322d2d8-e6df-49b1-882b-1fb79a8fbb70', status.HTTP_201_CREATED),
        ('3', '4322d2d8-e6df-49b1-882b-1fb79a8fbb70', status.HTTP_400_BAD_REQUEST),
        ('4', '4322d2d8-e6df-49b1-882b-1fb79a8fbb70', status.HTTP_400_BAD_REQUEST),
        ('5', '4322d2d8-e6df-49b1-882b-1fb79a8fbb70', status.HTTP_400_BAD_REQUEST),
        ('1', '97407a89-2682-40de-943c-89320d3f50e4', status.HTTP_403_FORBIDDEN),
    ))
    def test_view_order(self, cases, user_id, status_code, api_client):
        user = get_user_model().objects.get(pk=user_id)
        data = helpers.load_json_data(path=f'orders/create_order/{cases}')
        response = api_client.post(
            '/api/v1/orders/',
            format='json',
            data=data,
            HTTP_AUTHORIZATION=helpers.access_token(user=user),
        )

        assert response.status_code == status_code

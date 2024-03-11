# from decimal import Decimal
# from collections import OrderedDict
#
# from django.contrib.auth import get_user_model
# from django.db.models import Sum
# from django.test import TestCase
# from products.models import Product
# from seller_products.models import SellerProduct
# from seller_products.choices import CurrencyChoices
# from users.choices import UserType
# from orders.repos import OrderReposInterface, OrderReposV1
#
#
# class OrderTestCase(TestCase):
#
#     def setUp(self) -> None:
#         customer = get_user_model().objects.create_user(
#             email='customer@gmail.com',
#             phone_number='+77082698956',
#         )
#         customer.user_type = UserType.Customer
#         customer.save()
#
#         seller = get_user_model().objects.create_user(
#             email='seller@gmail.com',
#             phone_number='+77082698955',
#         )
#         seller.user_type = UserType.Seller
#         seller.save()
#
#         product = Product.objects.create(
#             title='product',
#             body='some info',
#             data={'data': 'data'},
#         )
#         seller_product = SellerProduct.objects.create(
#             product=product,
#             seller=seller,
#             amount=Decimal(10000),
#             amount_currency=CurrencyChoices.KZT,
#         )
#
#     def test_create_order(self):
#         customer = get_user_model().objects.get(phone_number='+77082698955')
#         seller_product = SellerProduct.objects.get()
#         data = {
#             'customer': customer,
#             'order_items': [
#                 {'seller_product': seller_product}
#             ],
#         }
#
#         order_repos: OrderReposInterface = OrderReposV1()
#         order = order_repos.create_order(data=OrderedDict(data))
#
#         self.assertEqual(order.order_items.count(), len(data['order_items']))
#
#         total = order.order_items.aggregate(total=Sum('amount'))['total']
#
#         self.assertEqual(
#             total,
#             sum([i['seller_product'].amount for i in data['order_items']])
#         )
#
#         self.assertTrue(
#             all([i.amount_currency == CurrencyChoices.KZT for i in order.order_items.all()])
#         )

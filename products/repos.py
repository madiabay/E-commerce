from typing import Protocol
from django.db.models import QuerySet, Min, Q
from . import models


class ProductReposInterface(Protocol):
    @staticmethod
    def get_products() -> QuerySet[models.Product]: ...


class ProductReposV1:
    @staticmethod
    def get_products() -> QuerySet[models.Product]:
        return models.Product.objects.annotate(
            min_amount=Min(
                'seller_products__amount',
                filter=Q(seller_products__is_active=True)
            )
        )


class ProductImageReposInterface(Protocol):
    @staticmethod
    def get_products_images() -> QuerySet[models.Product]: ...


class ProductImageReposV1:
    @staticmethod
    def get_products_images() -> QuerySet[models.Product]:
        return models.ProductImages.objects.all()

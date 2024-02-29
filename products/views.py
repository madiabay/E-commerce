from django.db.models import Min, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from . import models, serializers, permissions
from utils import mixins


class ProductImageViewSet(ModelViewSet):
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImages.objects.all()


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer
    }
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.annotate(
        min_amount=Min('seller_products__amount', filter=Q(seller_products__is_active=True))
    )
    # permission_classes = IsAuthenticated,

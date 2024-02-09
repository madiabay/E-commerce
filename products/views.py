from rest_framework.viewsets import ModelViewSet

from . import models, serializers
from utils import mixins


class ProductImageViewSet(ModelViewSet):
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImages.objects.all()


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer
    }
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

from rest_framework.viewsets import ModelViewSet

from . import serializers, permissions, services
from utils import mixins


class ProductImageViewSet(ModelViewSet):
    product_image_services: services.ProductImageServicesInterface = services.ProductImageServicesV1()
    queryset = product_image_services.get_products_images()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = permissions.IsAdminOrReadOnly,


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    product_services: services.ProductServicesInterface = services.ProductServicesV1()
    queryset = product_services.get_products()
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer
    }
    serializer_class = serializers.ProductSerializer
    permission_classes = permissions.IsAdminOrReadOnly,

    def list(self, request, *args, **kwargs):
        print(request.api.post('https://www.example.org/'))
        return super().list(request, *args, **kwargs)

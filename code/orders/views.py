from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, serializers, services, permissions
from utils import mixins


class OrderItemViewSet(ModelViewSet):
    serializer_class = serializers.OrderItemSerializer
    queryset = models.OrderItem.objects.all()
    permission_classes = IsAuthenticated,


class OrderViewSet(
        mixins.ActionSerializerMixin,
        mixins.ActionPermissionMixin,
        ModelViewSet):
    order_services: services.OrderServicesInterface = services.OrderServicesV1()

    ACTION_SERIALIZERS = {
        'create': serializers.CreateOrderSerializer
    }
    ACTION_PERMISSIONS = {
        'create': (permissions.IsCustomer(),),
    }
    serializer_class = serializers.OrderSerializer
    queryset = order_services.get_orders()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.order_services.create_order(data=serializer.validated_data)
        data = serializers.OrderSerializer(order).data
        return Response(data, status=status.HTTP_201_CREATED)

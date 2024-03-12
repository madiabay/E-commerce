from rest_framework import serializers

from . import models
from users import choices as user_choices


class _CreateOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = 'seller_product',


class CreateOrderSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = _CreateOrderItemSerializer(write_only=True, many=True, min_length=1)

    class Meta:
        model = models.Order
        fields = 'customer', 'order_items',

    def validate(self, attrs):
        user = self.context['request'].user
        if user.user_type != user_choices.UserType.Customer:
            raise serializers.ValidationError("Only customers can create orders.")
        return attrs


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'

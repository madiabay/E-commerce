from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import signals
from django.dispatch import receiver
from . import models


# User = get_user_model()
#
#
# @receiver(signals.post_save, sender=models.Order)
# def send_email_to_customers(sender, instance: models.Order, created: bool, **kwargs):
#     if not created:
#         customer = User.objects.get(id=instance.customer_id)
#
#         send_mail(
#             "Order Status",
#             f"NOW Your order status is {instance.status}",
#             settings.EMAIL_HOST_USER,
#             [customer.email],
#             fail_silently=False,
#         )

@receiver(signals.post_save, sender=models.Order)
def send_order_notification(sender, instance: models.Order, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(instance.id),
        {
            'type': 'send_notification',
            'status': instance.status,
        }
    )

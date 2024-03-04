from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail
from django.conf import settings
from . import models
from users import choices as user_choices

User = get_user_model()


@receiver(signals.post_save, sender=models.Product)
def send_email_to_sellers(sender, instance: models.Product, created: bool, **kwargs):
    if created:
        sellers = User.objects.filter(user_type=user_choices.UserType.Seller)
        seller_emails = [s.email for s in sellers]
        message = (
            f"new product: {instance.title}",
            f"information: {instance.body}",
            settings.EMAIL_HOST_USER,
            seller_emails,
        )
        send_mass_mail(datatuple=(message,))


# signals have these events:
# signals.post_save, signals.post_delete
# signals.pre_save, signals.pre_delete and etc

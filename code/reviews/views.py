from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.mixins import PermissionRequiredMixin
from . import models, serializers


class ReviewViewSet(ModelViewSet, PermissionRequiredMixin):
    permission_required = 'review.view_review',

    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.filter(parent_review__isnull=True).prefetch_related('reviews')

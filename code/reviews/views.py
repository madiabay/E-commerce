from rest_framework.viewsets import ModelViewSet
from . import models, serializers


class ReviewViewSet(ModelViewSet):

    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.filter(parent_review__isnull=True).prefetch_related('reviews')

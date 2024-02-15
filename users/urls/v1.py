from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('users/create/', views.UserViewSet.as_view({'post': 'create_user'})),
    # path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/', views.UserViewSet.as_view({'post': 'create_token'}), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import (
    UserViewSet,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    PaymentListCreateAPIView,
    PaymentRetrieveUpdateDestroyAPIView,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path("profile/", UserListCreateAPIView.as_view(), name="user_list_create"),
    path(
        "profile/<int:pk>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user_detail",
    ),
    path("payment/", PaymentListCreateAPIView.as_view(), name="payment_detail"),
    path(
        "payment/<int:pk>/",
        PaymentRetrieveUpdateDestroyAPIView.as_view(),
        name="payment_detail",
    ),
] + router.urls

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ("paid_course", "paid_lesson", "payment_date")


class UserCreateAPIView(CreateAPIView):
    """Контроллер для регистрации пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(ListAPIView):
    """Эндпоинт просмотра оплаты"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_fields = ("date_payment",)


class PaymentCreateAPIView(CreateAPIView):
    """Эндпоинт создания оплаты"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        stripe_product_id = create_stripe_product(payment)
        payment.amount = payment.amount
        price = create_stripe_price(
            stripe_product_id=stripe_product_id, amount=payment.amount
        )
        session_id, payment_link = create_stripe_session(price=price)
        payment.stripe_session_id = session_id
        payment.stripe_payment_url = payment_link
        payment.save()

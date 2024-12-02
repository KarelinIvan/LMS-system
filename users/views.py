import stripe
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.services import create_stripe_price, create_stripe_sessions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ("payment_date",)
    ordering_fields = ("paid_course", "paid_lesson")


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.amount)
        session_id, payment_link = create_stripe_sessions(price)
        payment.stripe_session_id = session_id
        payment.stripe_payment_url = payment_link
        payment.save()


class PaymentStatusAPIView(APIView):
    """Эндпоинт для получения статуса платежа по ID сессии Stripe"""

    def get(self, request, session_id):
        session = stripe.checkout.Session.retrieve(session_id)
        payment_status = session.get('payment_status', 'unknown')

        return JsonResponse({
            'session_id': session.id,
            'payment_status': payment_status
        })


class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class UserCreateAPIView(CreateAPIView):
    """Контроллер для регистрации пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

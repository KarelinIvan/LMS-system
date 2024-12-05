from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}
# Create your models here.


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Почта", help_text="уакжите e-mail")
    phone = models.CharField(max_length=35, verbose_name="номер телефона", help_text="укажите номер телефона",
                             **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="город", help_text="укажите город")
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="Аватар", help_text="загружите фото", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
        ('stripe', 'Stripe'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments", **NULLABLE)
    payment_date = models.DateTimeField(auto_now_add=True, **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Оплаченный курс", **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name="Оплаченный урок", **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")
    stripe_session_id = models.CharField(max_length=255, **NULLABLE, verbose_name="ID сессии Stripe")
    stripe_payment_url = models.URLField(max_length=500, **NULLABLE, verbose_name="Ссылка на оплату")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_date})"

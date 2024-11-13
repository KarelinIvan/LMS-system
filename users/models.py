from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="уакжите e-mail"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="номер телефона",
        help_text="укажите номер телефона",
    )
    city = models.CharField(
        max_length=50, verbose_name="город", help_text="укажите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="загружите фото",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

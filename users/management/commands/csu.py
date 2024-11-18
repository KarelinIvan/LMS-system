from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Кастомная команда для создания суперпользователя"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email="ivan.karelin.1993@mail.ru",
            first_name='Admin',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )

        user.set_password("Mt076954")
        user.save()

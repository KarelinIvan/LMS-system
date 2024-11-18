from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Понель пользователи  в админке"""
    list_display = ('email', 'id', 'phone')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Панель платежи в админке"""
    list_display = ('user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method')

from rest_framework import permissions

class IsModer(permissions.BasePermission):
    """Проверка принадлежности к группе модератор"""
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модератор').exists()

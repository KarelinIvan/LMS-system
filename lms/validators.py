from rest_framework.exceptions import ValidationError


def validate_links(value):
    """Запрещает пользователю размещать любые ссылки, кроме Youtube"""
    if "http" in value and "youtube.com" not in value:
        raise ValidationError("Материалы могут содержать ссылки только на youtube.com")

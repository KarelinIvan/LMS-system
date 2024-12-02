import stripe
from django.conf import settings

from forex_python.converter import CurrencyRates

stripe.api_key = settings.STRIPE_SECRET_KEY


def convert_rub_to_dollars(amount):
    """ Конвертирует рубли в доллары """

    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)


def create_stripe_price(amount):
    """ Создает цену в stripe """

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": "Payment"},
    )


def create_stripe_sessions(price):
    """ Создает сессию на оплату в stripe """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

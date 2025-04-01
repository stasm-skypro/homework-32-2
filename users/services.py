import stripe
from forex_python.converter import CurrencyRates
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(amount):
    """
    Конвертирует рубли в доллары
    :param amount: Сумма в рублях
    :return: Сумма в долларах
    """
    c = CurrencyRates()
    amount = c.convert("RUB", "USD", amount)
    return amount

def create_price(amount):
    """
    Создаёт цену
    :param amount: Цена оплаты
    :return: Объект цены stripe
    """
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,  # цена всегда в копейках
        recurring={"interval": "month"},
        product_data={"name": "Gold Plan"}
    )


def create_checkout_session(price_id):
    """
    Создаёт сессию оплаты
    :param price_id: ID цены
    :return: Объект сессии stripe
    """
    session = stripe.checkout.Session.create(
        line_items=[{
            "price": price_id,
            "quantity": 1,
        }],
        mode="subscription",
        success_url="http://localhost:8000/",
        cancel_url="http://localhost:8000/",
    )
    return session.get("id"), session.get("url")

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name, description):
    """Создает продукт в Stripe."""
    product = stripe.Product.create(name=name, description=description)
    return product.id


def create_stripe_price(amount, currency, product_id):
    """Создает цену для продукта в Stripe."""
    price = stripe.Price.create(
        unit_amount=int(amount * 100),  # Преобразование в центы
        currency=currency,
        product=product_id
    )
    return price.id


# def create_checkout_session(price_id, success_url, cancel_url):
#     """Создает сессию для оплаты в Stripe."""
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{'price': price_id, 'quantity': 1}],
#         mode='payment',
#         success_url=success_url,
#         cancel_url=cancel_url
#     )
#     return session

def create_checkout_session(price_id, success_url, cancel_url):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1
            }],
            mode='subscription',  # Или 'payment', в зависимости от сценария
            success_url=success_url,
            cancel_url=cancel_url
        )
        return session
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        raise e
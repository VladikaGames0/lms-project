import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(payment):
    paid_item = payment.course if payment.course else payment.lesson
    product = stripe.Product.create(
        name=paid_item.title,
        description=paid_item.description or f"Оплата за {paid_item.title}",
        metadata={
            'payment_id': str(payment.id),
            'user_id': str(payment.user.id),
            'item_type': 'course' if payment.course else 'lesson',
            'item_id': str(paid_item.id)
        }
    )
    return product.id


def create_stripe_price(product_id, amount):
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency='rub',
        billing_scheme='per_unit'
    )
    return price.id


def create_stripe_checkout_session(price_id, payment_id, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': price_id, 'quantity': 1}],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={'payment_id': str(payment_id)}
    )
    return session.id, session.url


def get_stripe_session_status(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            'status': session.status,
            'payment_status': session.payment_status,
            'customer_email': session.customer_details.email if session.customer_details else None
        }
    except stripe.error.StripeError as e:
        return {'error': str(e)}

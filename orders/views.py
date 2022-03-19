from django.shortcuts import render
from config.settings.base import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from lots.models import Lot

from .models import Cart, Order

import stripe


def cart_view(request):

    if len(Cart.objects.filter(user=request.user)) > 0:
        cart = Cart.objects.filter(user=request.user)[0]
    else:
        cart = Cart.objects.create(user=request.user)
        cart.save()

    cartless_won_lots = (
        Lot.objects.filter(winner=request.user).exclude(cart=cart).exclude(is_paid=True)
    )

    if cartless_won_lots:
        for lot in cartless_won_lots:
            lot.cart = cart
            lot.save()
            cart.save()

    return render(
        request, "my-cart.html", {"cart": cart, "lots": Lot.objects.filter(cart=cart)}
    )

# where we will redirect when order is complete
def order_complete(request):

    for lot in Lot.objects.filter(cart=Cart.objects.first(user=request.user)):
        # remove from user's cart
        lot.cart = None
        # mark it paid so it doesn't get added to cart again
        lot.is_paid = True
        lot.save()


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    
    my_cart = Cart.objects.filter(user=request.user)[0]
    this_order = Order.objects.create(user=request.user, items_value=my_cart.total_value)

    my_cart.lots().update(order=this_order)

    
    
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': f'Order #{this_order.pk}',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': f'{int(this_order.items_value * 100)}',
                    }
                ]
            )
            this_order.checkout_session_id = checkout_session['id']
            this_order.save()
            ### then we need to setup web hooks so strip can tell the order_db record if it was success or not
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
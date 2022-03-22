import json

import stripe
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from config.settings.base import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from lots.models import Lot

from .models import Cart, Order


def cart_view(request):

    if len(Cart.objects.filter(user=request.user)) > 0:
        cart = Cart.objects.filter(user=request.user)[0]
    else:
        cart = Cart.objects.create(user=request.user)
        cart.save()

    Lot.objects.filter(winner=request.user).exclude(cart=cart).exclude(
        is_paid=True
    ).update(cart=cart)

    cart.update_cart_value()

    return render(
        request, "my-cart.html", {"cart": cart, "lots": Lot.objects.filter(cart=cart)}
    )


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):

    my_cart = Cart.objects.filter(user=request.user)[0]
    this_order = Order.objects.create(
        user=request.user, items_value=my_cart.total_value
    )

    my_cart.lots().update(order=this_order)

    if request.method == "GET":
        domain_url = "http://localhost:8000/account/"
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
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "name": f"Order #{this_order.pk}",
                        "quantity": 1,
                        "currency": "usd",
                        "amount": f"{int(this_order.items_value * 100)}",
                    }
                ],
            )
            this_order.stripe_checkout_session_id = checkout_session["id"]
            this_order.save()
            # then we need to setup web hooks so strip can tell the order_db record if it was success or not
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


def checkout_success(request):
    # if checkout is intially success, we want to remove items from cart

    checkout_id = request.GET["session_id"] if request.GET["session_id"] else None

    order = Order.objects.get(stripe_checkout_session_id=checkout_id)

    Lot.objects.filter(order=order).update(cart=None, is_paid=True)

    return HttpResponse(f"Success for {checkout_id}")


def checkout_failure(request):
    return HttpResponse("Something went wrong")


# EXAMPLE ENDPOINT https://testdriven.io/blog/django-stripe-tutorial/
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = STRIPE_SECRET_KEY
    endpoint_secret = (
        "whsec_c92b8c238da9616cc17dda806b6b7b6ddb8b3b0dfe246229a5e8358c7ef95f0b"
    )
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    checkout_session_id = event["data"]["object"]["id"]
    order = Order.objects.get(stripe_checkout_session_id=checkout_session_id)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        order.paid = True
        order.stripe_session_data = json.loads(payload.decode("UTF-8"))
        order.save()

    if event["type"] == "checkout.session.async_payment_failed":
        # to do: make a notification for user that this payment actually failed
        Lot.objects.filter(order=order).update(is_paid=False)
        order.paid = False
        order.stripe_session_data = json.loads(payload.decode("UTF-8"))
        order.save()
        pass

    return HttpResponse(status=200)


def completed_orders_list_view(request):
    # a list of paid orders
    pass


def completed_orders_detail_view(request):
    # the lots inside the paid order, maybe shipping info, etc
    pass


def my_bids(request):
    pass


def my_watchlist(request):
    pass

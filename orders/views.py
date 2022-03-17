from django.shortcuts import render

from lots.models import Lot

from .models import Cart


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

    return render(
        request, "my-cart.html", {"cart": cart, "lots": Lot.objects.filter(cart=cart)}
    )


def order_complete(request):

    for lot in Lot.objects.filter(cart=Cart.objects.first(user=request.user)):
        # remove from user's cart
        lot.cart = None
        # mark it paid so it doesn't get added to cart again
        lot.is_paid = True
        lot.save()

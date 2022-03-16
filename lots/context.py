from .models import Auction


# https://betterprogramming.pub/django-quick-tips-context-processors-da74f887f1fc
def get_auctions(request):
    return {"auctions": Auction.objects.all()}

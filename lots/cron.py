from .models import Lot


def end_of_auction():
    all_lots = Lot.objects.all()
    number = 0
    for lot in all_lots:
        number += lot.end_auction()
    return f"This endpoint altered {number} lots"

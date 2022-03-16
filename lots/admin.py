from django.contrib import admin

from .models import Auction, Lot, LotImage


# Register your models here.
class LotAdmin(admin.ModelAdmin):
    ordering = ["auction"]
    search_fields = ["sku", "name", "description"]


class LotImageAdmin(admin.ModelAdmin):
    ordering = ["file_name"]
    search_fields = ["file_name"]


admin.site.register(Lot, LotAdmin)
admin.site.register(LotImage, LotImageAdmin)
admin.site.register(Auction)

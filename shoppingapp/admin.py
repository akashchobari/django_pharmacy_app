from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([CategoryModel,CartModel])

@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("user","all_items","total_price","discount","final_price","delivery_date")
    def get_ordering(self, request):
        return ['id']
    def all_items(self, obj):
        return [item[0] for item in obj.items]
    def total_price(self,obj):
        return sum(item[1] for item in obj.items)
    def final_price(self,obj):
        return sum(item[1] for item in obj.items) - int(obj.discount)
    
@admin.register(ItemModel)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ("name","price")

@admin.register(PromoCodeModel)
class PromoModelAdmin(admin.ModelAdmin):
    list_display = ("promo","discount")
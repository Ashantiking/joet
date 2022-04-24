from django.contrib import admin
from .models import Order, OrderProduct, Product, BillingAddress, Payment, Category, Section, Sizes


class SizesAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Section),
admin.site.register(Category),
admin.site.register(Product),
admin.site.register(OrderProduct),
admin.site.register(Order),
admin.site.register(BillingAddress),
admin.site.register(Payment),
admin.site.register(Sizes, SizesAdmin),

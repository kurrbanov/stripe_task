from django.contrib import admin

from stripe_app.models import Item, Order, OrderItem, Discount, PromoCode


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('uuid',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('percent_off', 'duration', 'duration_in_months')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'coupon')

from django.contrib import admin

from api.models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    # inlines allows you to attach a related object
    model = OrderItem


# register the order model with the admin
class OrderAdmin(admin.ModelAdmin):
    # ability to add orders and items dynamically on the admin page
    inlines = [
        OrderItemInline,
    ]


admin.site.register(
    Order,  # model class
    OrderAdmin,  # admin class
)

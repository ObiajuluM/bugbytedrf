from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # define the model it's going to serialize
        model = Product
        # tuple with all the fields it's going to convert to serialize (json)
        fields = (
            "id",
            "name",
            # "description",
            "price",
            "stock",
        )

    # field level validation function
    # validate_<field_name>
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0",
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    #
    product_name = serializers.CharField(
        # where to fetch data from during serialization
        source="product.name",  # return the name value from the product
    )
    product_price = serializers.DecimalField(
        # where to fetch data from during serialization
        source="product.price",
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "quantity",
            # "order",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        # can only be read. GET requeste
        read_only=True,
    )

    # this is a serializer only field, i didn't define it in the model
    # serializer method field that allows you to call functions on a field in a serializer
    total_price = serializers.SerializerMethodField(
        # optional
        method_name="total",
    )

    # function that is called on the total_price serializer field - get_<field_name>(self, model: Order)
    def total(self, obj: Order):
        # return the queryset of all order items
        order_items = obj.items.all()

        # return the sum of items subtotal
        return sum(order_item.item_subtotal or 0 for order_item in order_items)

    # # function that is called on the total_price serializer field - get_<field_name>(self, model: Order)
    # def get_total(self, obj: Order):
    #     # return the queryset of all order items
    #     order_items = obj.items.all()

    #     # return the sum of items subtotal
    #     return sum(order_item.item_subtotal or 0 for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            "order_id",
            "created_at",
            "user",
            "status",
            "items",
            "total_price",
        )

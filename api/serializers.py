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
            "description",
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

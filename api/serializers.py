from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # define the model it's going to serialize
        model = Product
        # tuple with all the fields it's going to convert to json
        fields = ()
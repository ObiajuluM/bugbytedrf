from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view


# function based views
@api_view(["GET"])
def product_list(request: Request):
    # queryset
    products = Product.objects.all()
    # serializer
    serializer = ProductSerializer(
        products,
        # to return a list of items
        many=True,
    )
    # return a json response containing the serialized data
    return Response(
        serializer.data,
    )


@api_view(["GET"])
def product_detail(request: Request, pk: int):
    # queryset to get object with primary key or 404
    product = get_object_or_404(Product, pk=pk)
    # serializer
    serializer = ProductSerializer(product)
    # return a json response containing the serialized data
    return Response(serializer.data)

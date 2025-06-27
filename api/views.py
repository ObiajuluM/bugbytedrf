from django.shortcuts import get_object_or_404
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer
from api.models import Order, Product, User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.exclude(stock__gt=0)
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # use the product id as the look up reference instead of pk
    lookup_url_kwarg = "product_id"


class OrderListApiView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related(
        # "items",
        "items__product",
    )  # prefetch_related, prefetches the related items, speeding up the query
    # serializer
    serializer_class = OrderSerializer


class UserOrderListApiView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related(
        # "items",
        "items__product",
    )  # prefetch_related, prefetches the related items, speeding up the query
    # serializer
    serializer_class = OrderSerializer

    # function to return the queryset based on the user
    def get_queryset(self):
        user = self.request.user
        qs =  super().get_queryset()
        return qs.filter(user=user)


# function based views
# @api_view(["GET"])
# def product_list(request: Request):
#     # queryset
#     products = Product.objects.all()
#     # serializer
#     serializer = ProductSerializer(
#         products,
#         # to return a list of items
#         many=True,
#     )
#     # return a json response containing the serialized data
#     return Response(
#         serializer.data,
#     )


# @api_view(["GET"])
# def product_detail(request: Request, pk: int):
#     # queryset to get object with primary key or 404
#     product = get_object_or_404(Product, pk=pk)
#     # serializer
#     serializer = ProductSerializer(product)
#     # return a json response containing the serialized data
#     return Response(serializer.data)


# @api_view(["GET"])
# def order_list(request: Request):
#     # queryset
#     orders = Order.objects.prefetch_related(
#         # "items",
#         "items__product",
#     )  # prefetch_related, prefetches the related items, speeding up the query
#     # serializer
#     serializer = OrderSerializer(
#         orders,
#         # to return a list of items
#         many=True,
#     )
#     # return a json response containing the serialized data
#     return Response(
#         serializer.data,
#     )


@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer(
        {
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"],
        }
    )
    return Response(serializer.data)

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(
        # store images to product directory
        upload_to="products/",
        blank=True,
        null=True,
    )

    # property to check if item is in stock
    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Order(models.Model):

    # possible order status choices
    class StatusChoices(models.TextChoices):
        PENDING = "pending"
        CONFIRMED = "confirmed"
        CANCELLED = "cancelled"

    order_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    user = models.ForeignKey(
        User,
        # if the user is deleted, delete all the orders
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        # Set on Creation Only
        # not updateable and not editable
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=10,
        # associates the StatusChoices with this status field
        choices=StatusChoices.choices,
        # set the default order state to pending
        default=StatusChoices.PENDING,
    )
    # products in the order
    products = models.ManyToManyField(
        Product,
        related_name="orders",
        # uses the order item class as a hidden table to set more information for the product
        through="OrderItem",
    )

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


# links order to product
class OrderItem(models.Model):
    # link order item to order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    # link order item to product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    # quantiity of the given product for this order
    quantity = models.PositiveIntegerField()

    # product.price * quantity
    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} X {self.product.name} in order {self.order.order_id}"

from django.test import TestCase
from django.urls import reverse
from api.models import Order, User
from rest_framework import status

# Create your tests here.


class UserOrderTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(
            username="user1",
            password="test",
        )
        user2 = User.objects.create_user(
            username="user2",
            password="test",
        )
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username="user1")
        # accesses the client from the `testcase` to authenticate with the user
        self.client.force_login(user=user)
        # reverse the endpoint `user-orders`, it returns the url and then makes a get request
        response = self.client.get(
            reverse("user-orders"),
        )

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()

        self.assertTrue(
            all(order["user"] == user.id for order in orders),
        )
        # print(orders)

    def test_user_order_list_unauthenticated(self):
        # reverse the endpoint `user-orders`, it returns the url and then makes a get request
        response = self.client.get(reverse("user-orders"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

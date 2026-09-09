import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory


class TestOrderViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)

        self.category = CategoryFactory(title="Technology")
        self.product = ProductFactory(
            category=[self.category], title="Laptop", price=999.99
        )
        self.other_product = ProductFactory(title="Mouse", price=99.90)

        self.order = OrderFactory(user=self.user, product=(self.product,))
        self.other_order = OrderFactory(
            user=self.other_user, product=(self.other_product,)
        )

    def authenticate(self, token=None):
        token = token or self.token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_order_requires_authentication(self):
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_orders(self):
        self.authenticate()
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["product"][0]["title"],
            self.product.title,
        )

    def test_user_cannot_retrieve_another_users_order(self):
        self.authenticate()
        response = self.client.get(
            reverse(
                "order-detail",
                kwargs={"version": "v1", "pk": self.other_order.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_order_uses_authenticated_user(self):
        self.authenticate()
        product = ProductFactory(title="Keyboard", price=80.00)
        data = json.dumps({"product_ids": [product.id]})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_order = Order.objects.exclude(
            id__in=[self.order.id, self.other_order.id]
        ).get()
        self.assertEqual(created_order.user, self.user)
        self.assertTrue(created_order.product.filter(id=product.id).exists())
        self.assertEqual(response.data["user"], self.user.id)

    def test_other_user_receives_only_their_orders(self):
        self.authenticate(self.other_token)
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["product"][0]["title"],
            self.other_product.title,
        )

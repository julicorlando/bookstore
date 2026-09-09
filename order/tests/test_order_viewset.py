from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.models import Order
from product.models import Category, Product


class TestOrderViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="julio",
            password="test12345",
        )
        self.category = Category.objects.create(
            title="Books",
            slug="books",
            description="Books category",
        )
        self.product = Product.objects.create(
            title="Django for APIs",
            description="Django REST Framework book",
            price=Decimal("99.90"),
        )
        self.product.category.add(self.category)
        self.order = Order.objects.create(user=self.user)
        self.order.product.add(self.product)

    def test_list_orders(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = response.data["results"][0]
        self.assertEqual(order["product"][0]["title"], "Django for APIs")
        self.assertEqual(order["product"][0]["category"][0]["title"], "Books")
        self.assertEqual(float(order["total"]), 99.90)

    def test_retrieve_order(self):
        url = reverse(
            "order-detail",
            kwargs={"version": "v1", "pk": self.order.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["product"][0]["title"], "Django for APIs")

    def test_create_order(self):
        second_product = Product.objects.create(
            title="Python Book",
            description="Python book",
            price=Decimal("49.90"),
        )
        data = {
            "user": self.user.id,
            "product_ids": [second_product.id],
        }
        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Order.objects.exclude(pk=self.order.pk).get(user=self.user)
        self.assertTrue(created.product.filter(pk=second_product.pk).exists())

    def test_delete_order(self):
        url = reverse(
            "order-detail",
            kwargs={"version": "v1", "pk": self.order.pk},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())

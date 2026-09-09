from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.models import Order
from product.models import Product


class TestOrderPagination(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="pagination-user",
            password="test-password",
        )
        self.product = Product.objects.create(
            title="Pagination Product",
            description="Product used in pagination tests",
            price="20.00",
        )

        for _ in range(12):
            order = Order.objects.create(user=self.user)
            order.product.add(self.product)

    def test_order_default_page_size_is_five(self):
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 5)

    def test_order_page_size_can_be_ten(self):
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"}),
            {"page_size": 10},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

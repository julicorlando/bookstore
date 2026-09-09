from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Category, Product


class TestProductViewSet(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Technology",
            slug="technology",
            description="Technology category",
        )
        self.product = Product.objects.create(
            title="Mouse",
            description="Wireless mouse",
            price=Decimal("50.00"),
        )
        self.product.category.add(self.category)

    def test_list_products(self):
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product = response.data["results"][0]
        self.assertEqual(product["title"], "Mouse")
        self.assertEqual(product["category"][0]["title"], "Technology")

    def test_retrieve_product(self):
        url = reverse(
            "product-detail",
            kwargs={"version": "v1", "pk": self.product.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Mouse")
        self.assertEqual(response.data["category"][0]["slug"], "technology")

    def test_create_product(self):
        data = {
            "title": "Keyboard",
            "description": "Mechanical keyboard",
            "price": "80.00",
            "active": True,
            "categories_ids": [self.category.id],
        }
        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Product.objects.get(title="Keyboard")
        self.assertEqual(created.price, Decimal("80.00"))
        self.assertTrue(created.category.filter(pk=self.category.pk).exists())

    def test_delete_product(self):
        url = reverse(
            "product-detail",
            kwargs={"version": "v1", "pk": self.product.pk},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Category, Product


class TestProductAndCategoryPagination(APITestCase):
    def setUp(self):
        for index in range(12):
            Category.objects.create(
                title=f"Category {index}",
                slug=f"category-{index}",
                description=f"Description {index}",
            )
            Product.objects.create(
                title=f"Product {index}",
                description=f"Description {index}",
                price="10.00",
            )

    def test_product_default_page_size_is_five(self):
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    def test_product_page_size_can_be_ten(self):
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"}),
            {"page_size": 10},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    def test_product_page_size_is_limited_to_ten(self):
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"}),
            {"page_size": 50},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    def test_category_uses_same_pagination(self):
        response = self.client.get(
            reverse("category-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 5)

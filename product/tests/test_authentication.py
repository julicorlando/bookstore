from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.factories import ProductFactory


class TestProductAuthentication(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = ProductFactory(title="Public product", price=25.00)

    def test_product_list_is_public(self):
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

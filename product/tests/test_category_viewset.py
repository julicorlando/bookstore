from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Category


class TestCategoryViewSet(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Books",
            slug="books",
            description="Books category",
        )

    def test_list_categories(self):
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["title"], "Books")

    def test_retrieve_category(self):
        url = reverse(
            "category-detail",
            kwargs={"version": "v1", "pk": self.category.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], "books")

    def test_create_category(self):
        data = {
            "title": "Technology",
            "slug": "technology",
            "description": "Technology category",
            "active": True,
        }
        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(slug="technology").exists())

    def test_delete_category(self):
        url = reverse(
            "category-detail",
            kwargs={"version": "v1", "pk": self.category.pk},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())

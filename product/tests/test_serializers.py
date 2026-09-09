from decimal import Decimal

from django.test import TestCase

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer


class CategorySerializerTestCase(TestCase):
    def test_accepts_valid_data_and_creates_category(self):
        payload = {
            "title": "Tecnologia",
            "slug": "tecnologia",
            "description": "Livros sobre tecnologia",
            "active": True,
        }

        serializer = CategorySerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()
        self.assertEqual(category.slug, "tecnologia")
        self.assertTrue(category.active)

    def test_validates_required_fields(self):
        serializer = CategorySerializer(data={"title": "Sem dados obrigatorios"})

        self.assertFalse(serializer.is_valid())
        self.assertIn("slug", serializer.errors)
        self.assertIn("description", serializer.errors)

    def test_rejects_duplicate_slug(self):
        Category.objects.create(
            title="Tecnologia",
            slug="tecnologia",
            description="Categoria existente",
        )
        serializer = CategorySerializer(
            data={
                "title": "Outra categoria",
                "slug": "tecnologia",
                "description": "Slug duplicado",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("slug", serializer.errors)

    def test_returns_expected_fields(self):
        category = Category.objects.create(
            title="Tecnologia",
            slug="tecnologia",
            description="Livros sobre tecnologia",
        )

        data = CategorySerializer(category).data

        self.assertEqual(
            set(data.keys()),
            {"id", "title", "slug", "description", "active"},
        )


class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Programacao",
            slug="programacao",
            description="Livros de programacao",
        )

    def test_accepts_valid_data_and_creates_product_with_category(self):
        payload = {
            "title": "Django para APIs",
            "description": "Livro sobre Django REST Framework",
            "price": "99.90",
            "active": True,
            "categories_ids": [self.category.id],
        }

        serializer = ProductSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.title, "Django para APIs")
        self.assertEqual(product.price, Decimal("99.90"))
        self.assertEqual(list(product.category.all()), [self.category])

    def test_validates_required_fields(self):
        serializer = ProductSerializer(
            data={"categories_ids": [self.category.id]}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("description", serializer.errors)
        self.assertIn("price", serializer.errors)

    def test_category_is_nested_in_product_representation(self):
        product = Product.objects.create(
            title="Python",
            description="Livro de Python",
            price=Decimal("59.90"),
        )
        product.category.add(self.category)

        data = ProductSerializer(product).data

        self.assertEqual(data["category"][0]["id"], self.category.id)
        self.assertEqual(data["category"][0]["slug"], "programacao")
        self.assertNotIn("categories_ids", data)
        self.assertEqual(
            set(data.keys()),
            {
                "id",
                "title",
                "description",
                "price",
                "active",
                "category",
            },
        )

    def test_product_can_be_created_without_category(self):
        serializer = ProductSerializer(
            data={
                "title": "Produto sem categoria",
                "description": "Relacionamento opcional no modelo",
                "price": "10.00",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.category.count(), 0)

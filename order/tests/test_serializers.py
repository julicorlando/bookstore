from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from order.models import Order
from order.serializers import OrderSerializer
from product.models import Category, Product


class OrderSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="julio",
            password="senha-segura",
        )
        self.category = Category.objects.create(
            title="Backend",
            slug="backend",
            description="Livros de backend",
        )
        self.product = Product.objects.create(
            title="Django REST Framework",
            description="Livro de APIs",
            price=Decimal("80.00"),
        )
        self.product.category.add(self.category)

    def test_accepts_valid_data_and_creates_order(self):
        serializer = OrderSerializer(
            data={
                "user": self.user.id,
                "product_ids": [self.product.id],
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.user, self.user)
        self.assertEqual(list(order.product.all()), [self.product])

    def test_user_is_required(self):
        serializer = OrderSerializer(
            data={"product_ids": [self.product.id]}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_product_ids_is_required(self):
        serializer = OrderSerializer(data={"user": self.user.id})

        self.assertFalse(serializer.is_valid())
        self.assertIn("product_ids", serializer.errors)

    def test_rejects_invalid_product_id(self):
        serializer = OrderSerializer(
            data={"user": self.user.id, "product_ids": [999999]}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("product_ids", serializer.errors)

    def test_returns_expected_fields_relationship_and_total(self):
        order = Order.objects.create(user=self.user)
        order.product.add(self.product)

        data = OrderSerializer(order).data

        self.assertEqual(
            set(data.keys()),
            {"id", "product", "total", "user"},
        )
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(data["product"][0]["title"], self.product.title)
        self.assertEqual(
            data["product"][0]["category"][0]["slug"],
            self.category.slug,
        )
        self.assertEqual(float(data["total"]), 80.0)

from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True
    )
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        return sum(product.price for product in instance.product.all())

    class Meta:
        model = Order
        fields = ["product", "total", "user", "product_ids"]
        extra_kwargs = {
            "product": {"required": False},
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        product_data = validated_data.pop("product_ids")
        order = Order.objects.create(**validated_data)
        order.product.set(product_data)
        return order

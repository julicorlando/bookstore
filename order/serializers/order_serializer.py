from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        many=True,
    )
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        return sum(product.price for product in instance.product.all())

    class Meta:
        model = Order
        fields = ["id", "product", "total", "user", "product_ids"]

    def create(self, validated_data):
        products = validated_data.pop("product_ids")
        order = Order.objects.create(**validated_data)
        order.product.set(products)
        return order

    def update(self, instance, validated_data):
        products = validated_data.pop("product_ids", None)
        instance = super().update(instance, validated_data)

        if products is not None:
            instance.product.set(products)

        return instance

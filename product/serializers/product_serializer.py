from rest_framework import serializers

from product.models import Category, Product
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    categories_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        many=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "category",
            "categories_ids",
        ]

    def create(self, validated_data):
        categories = validated_data.pop("categories_ids", [])
        product = Product.objects.create(**validated_data)
        product.category.set(categories)
        return product

    def update(self, instance, validated_data):
        categories = validated_data.pop("categories_ids", None)
        instance = super().update(instance, validated_data)

        if categories is not None:
            instance.category.set(categories)

        return instance

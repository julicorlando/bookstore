from rest_framework.viewsets import ModelViewSet

from bookstore.pagination import BookstorePagination
from product.models import Category
from product.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = BookstorePagination

    def get_queryset(self):
        return Category.objects.all().order_by("-id")

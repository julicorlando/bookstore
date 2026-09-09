from rest_framework.viewsets import ModelViewSet

from product.models import Product
from product.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related("category").all().order_by("-id")

from rest_framework.viewsets import ModelViewSet

from bookstore.pagination import BookstorePagination
from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = BookstorePagination
    queryset = Order.objects.all().order_by("-id")

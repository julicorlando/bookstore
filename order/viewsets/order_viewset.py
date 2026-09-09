from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = (
        Order.objects.select_related("user")
        .prefetch_related("product__category")
        .all()
        .order_by("-id")
    )

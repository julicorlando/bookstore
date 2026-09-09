from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from bookstore.pagination import BookstorePagination
from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = BookstorePagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("product__category")
            .order_by("-id")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

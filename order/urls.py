from django.urls import include, path
from rest_framework import routers

from order.viewsets import OrderViewSet

router = routers.SimpleRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]

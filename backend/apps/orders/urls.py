from django.urls import path
from apps.orders.views import OrderDetailAPIView, OrderProcessAPIView, OrderHistoryAPIView

urlpatterns = [
    path('process/', OrderProcessAPIView.as_view(), name='process-order'),
    path('history/', OrderHistoryAPIView.as_view(), name='order-history'),
    path('<str:order_no>/', OrderDetailAPIView.as_view(), name='order-detail'),
]

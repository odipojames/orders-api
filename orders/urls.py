from django.urls import path
from .views import OrderListCreateView,OrderDetailView




urlpatterns = [
    path('orders/',OrderListCreateView.as_view(),name="create-list-order"),
    path('orders/<int:pk>/',OrderDetailView.as_view(),name="order-details"),
]

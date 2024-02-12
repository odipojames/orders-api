from django.urls import path
from .views import CustomerListCreateView,CustomerDetailView


urlpatterns = [
      path("customers/", CustomerListCreateView.as_view(), name="create-list-customers"),
      path("customers/<int:pk>/", CustomerDetailView.as_view(), name="view-customer"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.CustomObtainAuthToken.as_view(), name='login'),
    path('protected/', views.protected_resource_view, name='protected_resource'),
]
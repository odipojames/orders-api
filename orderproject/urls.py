"""
URL configuration for orderproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from oidc_provider import urls as oidc_urls
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic.base import RedirectView


schema_view = get_schema_view(
    openapi.Info(
        title="orders API",
        default_version="v1",
        description=(
            "Savana Informatics Technical Challenge, Simple API built with Python, Django REST framework, and PostgreSQL DB"
        ),
        terms_of_service="https://www.odipojames12.com/policies/terms/",
        contact=openapi.Contact(email="odipojames12@mail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/auth/", include("authentication.urls")),
    path("api/v1/", include("customers.urls")),
    path("api/v1/", include("orders.urls")),
    path("api/v1/", schema_view.with_ui("swagger"), name="api-documentation"),
    path("api/v1/redoc/", schema_view.with_ui("redoc"), name="schema-redoc"),
    path("", RedirectView.as_view(url="api/v1/", permanent=False), name="api_documentation"),
    
]



# Cache settings
if settings.DEBUG:
    from django.views.decorators.cache import cache_page
    schema_view = cache_page(60 * 15)(schema_view)

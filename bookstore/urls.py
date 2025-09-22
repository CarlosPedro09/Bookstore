"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views.
"""

import debug_toolbar
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.http import HttpResponse

# View simples para a raiz
def home(request):
    return HttpResponse("Bookstore Django está funcionando!")

urlpatterns = [
    # Debug toolbar
    path("__debug__/", include(debug_toolbar.urls)),

    # Admin
    path("admin/", admin.site.urls),

    # Raiz para teste
    path("", home, name="home"),

    # Orders endpoints
    re_path(r"bookstore/(?P<version>(v1|v2))/", include("order.urls")),

    # Products endpoints
    re_path(r"bookstore/(?P<version>(v1|v2))/products/", include("product.urls")),

    # Token authentication
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]

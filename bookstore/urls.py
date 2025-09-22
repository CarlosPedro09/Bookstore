"""
bookstore URL Configuration

The `urlpatterns` list routes URLs to views.
"""

import debug_toolbar
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from bookstore import views

urlpatterns = [
    # Debug toolbar (só funciona com DEBUG=True)
    path("__debug__/", include(debug_toolbar.urls)),

    # Admin do Django
    path("admin/", admin.site.urls),

    # Endpoints de orders e products (separados para não conflitar)
    re_path(r"bookstore/(?P<version>(v1|v2))/orders/", include("order.urls")),
    re_path(r"bookstore/(?P<version>(v1|v2))/products/", include("product.urls")),

    # Autenticação via token
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),

    # Atualização do código via POST
    path("update_server/", views.update, name="update"),

    # Teste de template simples
    path("hello/", views.hello_world, name="hello_world"),
]


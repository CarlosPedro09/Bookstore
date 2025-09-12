import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        # Criando categoria e produto
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

        # Criando usuário e token
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_order(self):
        # Autenticação com token
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        # Autenticação com token
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": self.user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=self.user)
        self.assertEqual(created_order.user.id, self.user.id)

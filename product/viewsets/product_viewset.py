from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.serializers.product_serializer import ProductSerializer

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # permite GET público

    def get_queryset(self):
        return Product.objects.all().order_by("id")

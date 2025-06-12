from rest_framework.viewsets import ModelViewSet
from django_api.renderers import ViewRenderer
from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    renderer_classes = [ViewRenderer]
    http_method_names = ["get", "post", "patch", "delete"]
    
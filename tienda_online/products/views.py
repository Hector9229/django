from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import obtener_estrategia


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


@swagger_auto_schema(
    method='get',
    tags=['Productos'],
    operation_summary='Calcular el precio final de un producto',
    operation_description=(
        'Aplica el descuento según la categoría del producto. '
        'Requiere token JWT.'
    ),
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def precio_final(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    estrategia = obtener_estrategia(producto.category.name)
    precio_con_descuento = estrategia.calcular(float(producto.price))
    return Response(
        {
            'producto': producto.name,
            'precio_original': producto.price,
            'precio_final': round(precio_con_descuento, 2),
        }
    )

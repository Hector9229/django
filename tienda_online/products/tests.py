from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Product


class CategoryProductAPITestCase(APITestCase):
    """
    Pruebas unitarias para la API de Categorías y Productos.
    """

    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        Creamos un usuario y generamos su token JWT.
        """
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

        # Generar token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Autenticar todas las peticiones con el token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Crear una categoría de prueba (útil para varias pruebas)
        self.category = Category.objects.create(name='Electrónica')

        # Crear un producto de prueba
        self.product = Product.objects.create(
            name='Laptop',
            description='Laptop de 15 pulgadas',
            price='15000.00',
            category=self.category,
            is_active=True
        )

    # ==================== PRUEBAS DE CATEGORÍAS ====================

    def test_crear_categoria(self):
        """Prueba: Crear una categoría"""
        url = reverse('categories-list')  # /api/v1/categories/
        data = {'name': 'Ropa'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  # Ya había 1 + la nueva
        self.assertEqual(response.data['name'], 'Ropa')

    def test_listar_categorias(self):
        """Prueba: Listar categorías"""
        url = reverse('categories-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo la de setUp
        self.assertEqual(response.data[0]['name'], 'Electrónica')

    # ==================== PRUEBAS DE PRODUCTOS ====================

    def test_crear_producto(self):
        """Prueba: Crear un producto"""
        url = reverse('products-list')  # /api/v1/products/
        data = {
            'name': 'Mouse',
            'description': 'Mouse inalámbrico',
            'price': '350.00',
            'category': self.category.id,
            'is_active': True
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Mouse')

    def test_listar_productos(self):
        """Prueba: Listar productos"""
        url = reverse('products-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop')

    def test_actualizar_producto(self):
        """Prueba: Actualizar un producto"""
        url = reverse('products-detail', args=[self.product.id])  # /api/v1/products/1/
        data = {
            'name': 'Laptop Actualizada',
            'description': 'Laptop actualizada de 16 pulgadas',
            'price': '18000.00',
            'category': self.category.id,
            'is_active': True
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Actualizada')
        self.assertEqual(str(self.product.price), '18000.00')

    def test_eliminar_producto(self):
        """Prueba: Eliminar un producto"""
        url = reverse('products-detail', args=[self.product.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_precio_final_autenticado(self):
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)
 
 
    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)


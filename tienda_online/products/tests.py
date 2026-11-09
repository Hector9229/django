from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Product

User = get_user_model()


class CategoryProductAPITestCase(APITestCase):
    """Pruebas unitarias para la API de Categorías y Productos."""

    def setUp(self):
        """Crea un usuario, su token JWT y datos de prueba."""
        self.user = User.objects.create_user(
            email='test@tiendaonline.com',
            password='testpassword123',
            phone='5550001111',
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Autenticar todas las peticiones con el token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.category = Category.objects.create(name='Electrónica')
        self.product = Product.objects.create(
            name='Laptop',
            description='Laptop de 15 pulgadas',
            price='15000.00',
            category=self.category,
            is_active=True,
        )

    # ==================== PRUEBAS DE CATEGORÍAS ====================

    def test_crear_categoria(self):
        url = reverse('categories-list')
        response = self.client.post(url, {'name': 'Ropa'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Ropa')

    def test_listar_categorias(self):
        url = reverse('categories-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Electrónica')

    # ==================== PRUEBAS DE PRODUCTOS ====================

    def test_crear_producto(self):
        url = reverse('products-list')
        data = {
            'name': 'Mouse',
            'description': 'Mouse inalámbrico',
            'price': '350.00',
            'category': self.category.id,
            'is_active': True,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Mouse')

    def test_listar_productos(self):
        url = reverse('products-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop')

    def test_actualizar_producto(self):
        url = reverse('products-detail', args=[self.product.id])
        data = {
            'name': 'Laptop Actualizada',
            'description': 'Laptop actualizada de 16 pulgadas',
            'price': '18000.00',
            'category': self.category.id,
            'is_active': True,
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Actualizada')
        self.assertEqual(str(self.product.price), '18000.00')

    def test_eliminar_producto(self):
        url = reverse('products-detail', args=[self.product.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_precio_final_autenticado(self):
        response = self.client.get(
            f'/api/v1/products/{self.product.id}/precio-final/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(
            f'/api/v1/products/{self.product.id}/precio-final/'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserAPITestCase(APITestCase):
    """Pruebas del CRUD de usuarios, /auth/me y login con JWT."""

    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='AdminPassword123!',
            first_name='Admin',
            last_name='Test',
            phone='5551112222',
        )
        self.user = User.objects.create_user(
            email='user@test.com',
            password='UserPassword123!',
            first_name='Usuario',
            last_name='Prueba',
            phone='5553334444',
        )

        self.admin_token = str(RefreshToken.for_user(self.admin).access_token)
        self.user_token = str(RefreshToken.for_user(self.user).access_token)

    def _auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # ==================== LOGIN JWT ====================

    def test_login_con_email_devuelve_tokens(self):
        response = self.client.post(
            '/api/v1/auth/token/',
            {'email': 'user@test.com', 'password': 'UserPassword123!'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_con_password_incorrecta(self):
        response = self.client.post(
            '/api/v1/auth/token/',
            {'email': 'user@test.com', 'password': 'incorrecta'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ==================== DATOS PERSONALES ====================

    def test_auth_me_requiere_token(self):
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_me_devuelve_datos_sin_password(self):
        self._auth(self.user_token)
        response = self.client.get('/api/v1/auth/me/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user@test.com')
        self.assertEqual(response.data['phone'], '5553334444')
        self.assertNotIn('password', response.data)

    # ==================== CRUD DE USUARIOS ====================

    def test_listar_usuarios_no_expone_password(self):
        self._auth(self.admin_token)
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for item in response.data:
            self.assertNotIn('password', item)

    def test_crear_usuario_hashea_password_y_no_la_devuelve(self):
        self._auth(self.admin_token)
        response = self.client.post(
            '/api/v1/users/',
            {
                'email': 'nuevo@test.com',
                'password': 'NuevoPassword123!',
                'first_name': 'Nuevo',
                'last_name': 'Usuario',
                'phone': '5557778888',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        creado = User.objects.get(email='nuevo@test.com')
        self.assertNotEqual(creado.password, 'NuevoPassword123!')
        self.assertTrue(creado.check_password('NuevoPassword123!'))

    def test_actualizar_sin_password_no_cambia_password(self):
        self._auth(self.admin_token)
        hash_original = self.user.password
        url = reverse('users-detail', args=[self.user.id])

        response = self.client.patch(
            url,
            {'first_name': 'Nombre Actualizado', 'phone': '5559990000'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.password, hash_original)
        self.assertTrue(self.user.check_password('UserPassword123!'))
        self.assertEqual(self.user.first_name, 'Nombre Actualizado')
        self.assertEqual(self.user.phone, '5559990000')

    def test_actualizar_con_password_si_cambia_password(self):
        self._auth(self.admin_token)
        url = reverse('users-detail', args=[self.user.id])

        response = self.client.patch(
            url,
            {'password': 'PasswordNueva123!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('PasswordNueva123!'))
        self.assertFalse(self.user.check_password('UserPassword123!'))

    def test_usuario_no_admin_no_puede_listar_usuarios(self):
        self._auth(self.user_token)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

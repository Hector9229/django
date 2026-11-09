from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User
from .serializers import UserSerializer


class UserApiViewSet(viewsets.ModelViewSet):
    """CRUD de usuarios. Solo accesible para administradores.

    La creación y la actualización de la contraseña se delegan al
    ``UserSerializer``, que usa ``set_password`` para generar el hash.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'is_staff']


class UserView(APIView):
    """Devuelve los datos personales del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Autenticación'],
        operation_summary='Consultar mis datos personales',
        operation_description=(
            'Requiere el token JWT en el encabezado '
            '`Authorization: Bearer <access_token>`. '
            'La contraseña nunca se incluye en la respuesta.'
        ),
        responses={200: UserSerializer()},
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class EmailTokenObtainPairView(TokenObtainPairView):
    """Login con email y contraseña. Devuelve access y refresh token."""

    @swagger_auto_schema(
        tags=['Autenticación'],
        security=[],
        operation_summary='Iniciar sesión (obtener token JWT)',
        operation_description=(
            'Enviar el **email** y la **contraseña** del usuario. '
            'La respuesta incluye `access` (token de acceso) y `refresh`.'
        ),
        responses={
            200: openapi.Response(
                description='Tokens generados correctamente.',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class EmailTokenRefreshView(TokenRefreshView):
    """Renueva el token de acceso a partir del refresh token."""

    @swagger_auto_schema(
        tags=['Autenticación'],
        security=[],
        operation_summary='Renovar token de acceso',
        operation_description='Enviar el `refresh` para obtener un nuevo `access`.',
        responses={
            200: openapi.Response(
                description='Nuevo token de acceso generado.',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

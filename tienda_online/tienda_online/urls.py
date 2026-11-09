"""URL configuration for the tienda_online project."""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Tienda Online API',
        default_version='v1',
        description=(
            'API REST del proyecto **Tienda Online**.\n\n'
            'Incluye autenticación con JWT (email + contraseña), '
            'CRUD de usuarios, datos personales del usuario autenticado '
            'y CRUD de productos/categorías.'
        ),
        contact=openapi.Contact(email='hector@tiendaonline.local'),
        license=openapi.License(name='MIT'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
    path(
        'swagger<format>/',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]

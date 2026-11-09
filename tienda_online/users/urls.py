from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserApiViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', views.UserView.as_view(), name='auth-me'),
    path(
        'auth/token/',
        views.EmailTokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'auth/token/refresh/',
        views.EmailTokenRefreshView.as_view(),
        name='token_refresh',
    ),
]

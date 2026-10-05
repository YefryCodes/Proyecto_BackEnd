from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestauranteViewSet, MesaViewSet, ReservaViewSet

# Enrutador automático de DRF para endpoints RESTful
router = DefaultRouter()
router.register(r'restaurantes', RestauranteViewSet, basename='restaurante')
router.register(r'mesas', MesaViewSet, basename='mesa')
router.register(r'reservas', ReservaViewSet, basename='reserva')

urlpatterns = [
    path('', include(router.urls)),
]

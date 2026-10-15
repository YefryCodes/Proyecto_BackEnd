from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SucursalViewSet,
    MesaViewSet,
    ReservaViewSet,
    HistorialReservaViewSet
)

router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'mesas', MesaViewSet, basename='mesa')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'auditorias', HistorialReservaViewSet, basename='auditoria')

urlpatterns = [
    path('', include(router.urls)),
]

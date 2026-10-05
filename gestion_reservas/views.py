from django.shortcuts import render
from rest_framework import viewsets
from .models import Restaurante, Mesa, Reserva
from .serializers import RestauranteSerializer, MesaSerializer, ReservaSerializer

# --- Vista Web HTML de Bienvenida (Evaluación 1) ---
def home(request):
    restaurantes_activos = Restaurante.objects.filter(activo=True)
    total_restaurantes = restaurantes_activos.count()
    total_mesas = Mesa.objects.filter(activo=True).count()
    total_reservas = Reserva.objects.count()

    context = {
        'restaurantes': restaurantes_activos,
        'total_restaurantes': total_restaurantes,
        'total_mesas': total_mesas,
        'total_reservas': total_reservas,
    }
    return render(request, 'gestion_reservas/home.html', context)


# --- ViewSets de la API REST (Evaluación 2 - DRF ModelViewSet) ---
class RestauranteViewSet(viewsets.ModelViewSet):
    """
    Controlador CRUD para el recurso Restaurantes.
    Permite GET (lista/detalle), POST, PUT, PATCH y DELETE.
    """
    queryset = Restaurante.objects.all()
    serializer_class = RestauranteSerializer


class MesaViewSet(viewsets.ModelViewSet):
    """
    Controlador CRUD para el recurso Mesas.
    Permite GET (lista/detalle), POST, PUT, PATCH y DELETE.
    """
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    """
    Controlador CRUD para el recurso Reservas.
    Permite GET (lista/detalle), POST, PUT, PATCH y DELETE.
    """
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
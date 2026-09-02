from django.shortcuts import render
from .models import Restaurante, Mesa, Reserva

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
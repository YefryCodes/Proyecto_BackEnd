from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from datetime import date
from rest_framework import viewsets, permissions
from .models import Sucursal, Mesa, Reserva, HistorialReserva
from .serializers import (
    SucursalSerializer,
    MesaSerializer,
    ReservaSerializer,
    HistorialReservaSerializer
)

# 1. Vista Pública Principal
def bienvenida(request):
    """Landing page accesible para todo público."""
    return render(request, 'bienvenida.html')

# 2. FBV Protegida (Criterio 1.2): Panel Gerencial e Indicadores de Ocupación
@login_required
def dashboard_privado(request):
    """
    Vista protegida mediante @login_required.
    Calcula KPIs de gestión: ocupación actual, cancelaciones y registro de auditoría.
    """
    hoy = date.today()
    total_mesas = Mesa.objects.filter(activa=True).count()
    reservas_hoy = Reserva.objects.filter(fecha_reserva=hoy).exclude(estado='CANCELADA').count()
    reservas_confirmadas = Reserva.objects.filter(fecha_reserva=hoy, estado='CONFIRMADA').count()
    reservas_canceladas = Reserva.objects.filter(fecha_reserva=hoy, estado='CANCELADA').count()

    tasa_ocupacion = round((reservas_hoy / total_mesas * 100), 1) if total_mesas > 0 else 0

    ultimas_auditorias = HistorialReserva.objects.select_related(
        'reserva', 'usuario'
    ).order_by('-fecha_registro')[:6]

    contexto = {
        'usuario': request.user,
        'total_mesas': total_mesas,
        'reservas_hoy': reservas_hoy,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_canceladas': reservas_canceladas,
        'tasa_ocupacion': tasa_ocupacion,
        'ultimas_auditorias': ultimas_auditorias,
    }
    return render(request, 'dashboard.html', contexto)

# 3. CBV Protegida (Criterio 1.3): Gestión Operativa de Mesas
class GestionMesasPrivadaView(LoginRequiredMixin, ListView):
    """
    Vista basada en clases protegida mediante LoginRequiredMixin.
    Despliega el catálogo y estado físico de mesas en la cadena.
    """
    model = Mesa
    template_name = 'gestion_mesas.html'
    context_object_name = 'mesas'
    paginate_by = 12

    def get_queryset(self):
        return Mesa.objects.select_related('sucursal').order_by('sucursal', 'numero_mesa')

# 4. ViewSets RESTful (Criterios 2 y 3)
class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.select_related('sucursal').all()
    serializer_class = MesaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related('mesa', 'mesa__sucursal').all()
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        reserva = serializer.save()
        if self.request.user.is_authenticated:
            HistorialReserva.objects.create(
                reserva=reserva,
                usuario=self.request.user,
                estado_anterior='NUEVA',
                estado_nuevo=reserva.estado,
                motivo='Creación de reserva inicial en API'
            )

class HistorialReservaViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint de auditoría histórica de sólo lectura para administradores."""
    queryset = HistorialReserva.objects.select_related('reserva', 'usuario').all()
    serializer_class = HistorialReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

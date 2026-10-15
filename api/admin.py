from django.contrib import admin
from .models import Sucursal, Mesa, Reserva, HistorialReserva

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'telefono', 'capacidad_total', 'activo')
    search_fields = ('nombre', 'direccion')
    list_filter = ('activo',)


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sucursal', 'numero_mesa', 'capacidad', 'ubicacion', 'activa')
    list_filter = ('sucursal', 'ubicacion', 'activa')
    search_fields = ('numero_mesa', 'sucursal__nombre')


class HistorialInline(admin.TabularInline):
    model = HistorialReserva
    extra = 0
    readonly_fields = ('fecha_registro', 'usuario', 'estado_anterior', 'estado_nuevo', 'motivo')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'mesa', 'fecha_reserva', 'turno', 'cantidad_personas', 'estado')
    list_filter = ('estado', 'turno', 'fecha_reserva', 'mesa__sucursal')
    search_fields = ('cliente_nombre', 'cliente_email', 'cliente_telefono')
    inlines = [HistorialInline]


@admin.register(HistorialReserva)
class HistorialReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'usuario', 'estado_anterior', 'estado_nuevo', 'motivo', 'fecha_registro')
    list_filter = ('estado_nuevo', 'fecha_registro')
    search_fields = ('reserva__cliente_nombre', 'usuario__username', 'motivo')
    readonly_fields = ('fecha_registro',)

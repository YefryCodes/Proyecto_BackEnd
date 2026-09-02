from django.contrib import admin
from .models import Restaurante, Mesa, Reserva, HistorialReserva

@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'activo')
    search_fields = ('nombre', 'direccion')

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'restaurante', 'capacidad', 'activo')
    list_filter = ('restaurante', 'capacidad', 'activo')

class HistorialInline(admin.TabularInline):
    model = HistorialReserva
    extra = 0
    readonly_fields = ('estado_anterior', 'estado_nuevo', 'fecha_cambio', 'modificado_por')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'mesa', 'fecha_reserva', 'cantidad_personas', 'estado')
    list_filter = ('estado', 'fecha_reserva', 'mesa__restaurante')
    search_fields = ('cliente__username', 'mesa__restaurante__nombre')
    inlines = [HistorialInline]
# Register your models here.

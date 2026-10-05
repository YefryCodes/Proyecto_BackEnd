from rest_framework import serializers
from .models import Restaurante, Mesa, Reserva

class RestauranteSerializer(serializers.ModelSerializer):
    # Campo calculado para conocer el total de mesas asociadas
    total_mesas = serializers.IntegerField(source='mesas.count', read_only=True)

    class Meta:
        model = Restaurante
        fields = ['id', 'nombre', 'direccion', 'telefono', 'activo', 'total_mesas']


class MesaSerializer(serializers.ModelSerializer):
    # Permite visualizar el nombre del restaurante además del ID de la relación
    restaurante_nombre = serializers.ReadOnlyField(source='restaurante.nombre')

    class Meta:
        model = Mesa
        fields = ['id', 'restaurante', 'restaurante_nombre', 'numero', 'capacidad', 'activo']

    # Validación personalizada de capacidad de mesa
    def validate_capacidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La capacidad de la mesa debe ser un número entero mayor a 0.")
        return value


class ReservaSerializer(serializers.ModelSerializer):
    # Representación amigable de las claves foráneas
    cliente_username = serializers.ReadOnlyField(source='cliente.username')
    mesa_info = serializers.ReadOnlyField(source='mesa.__str__')

    class Meta:
        model = Reserva
        fields = [
            'id',
            'cliente',
            'cliente_username',
            'mesa',
            'mesa_info',
            'fecha_reserva',
            'duracion_estimada_minutos',
            'cantidad_personas',
            'estado',
            'creado_en'
        ]

    # Validaciones personalizadas requeridas por la rúbrica (métodos validate_*)
    def validate_duracion_estimada_minutos(self, value):
        if value < 15:
            raise serializers.ValidationError("La duración estimada de la reserva no puede ser inferior a 15 minutos.")
        return value

    def validate_cantidad_personas(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad de personas debe ser mayor a cero.")
        return value

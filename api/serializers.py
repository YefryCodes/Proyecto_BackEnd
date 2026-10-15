from rest_framework import serializers
from datetime import date
from .models import Sucursal, Mesa, Reserva, HistorialReserva

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'


class MesaSerializer(serializers.ModelSerializer):
    sucursal_nombre = serializers.ReadOnlyField(source='sucursal.nombre')

    class Meta:
        model = Mesa
        fields = ['id', 'sucursal', 'sucursal_nombre', 'numero_mesa', 'capacidad', 'ubicacion', 'activa']


class ReservaSerializer(serializers.ModelSerializer):
    mesa_info = serializers.ReadOnlyField(source='mesa.__str__')
    sucursal_nombre = serializers.ReadOnlyField(source='mesa.sucursal.nombre')

    class Meta:
        model = Reserva
        fields = [
            'id', 'mesa', 'mesa_info', 'sucursal_nombre', 'cliente_nombre',
            'cliente_email', 'cliente_telefono', 'fecha_reserva', 'turno',
            'cantidad_personas', 'estado', 'observaciones', 'fecha_creacion'
        ]

    def validate_fecha_reserva(self, value):
        if value < date.today():
            raise serializers.ValidationError("No es posible agendar reservas para fechas pasadas.")
        return value

    def validate(self, data):
        mesa = data.get('mesa', getattr(self.instance, 'mesa', None))
        personas = data.get('cantidad_personas', getattr(self.instance, 'cantidad_personas', 1))
        fecha = data.get('fecha_reserva', getattr(self.instance, 'fecha_reserva', None))
        turno = data.get('turno', getattr(self.instance, 'turno', None))
        estado = data.get('estado', getattr(self.instance, 'estado', 'PENDIENTE'))

        # Regla 1: Validar capacidad física de la mesa
        if mesa and personas > mesa.capacidad:
            raise serializers.ValidationError({
                "cantidad_personas": f"La mesa {mesa.numero_mesa} tiene una capacidad máxima de {mesa.capacidad} personas."
            })

        # Regla 2: Prevención de doble reserva / solapamiento
        if mesa and fecha and turno and estado not in ['CANCELADA', 'NO_SHOW']:
            solapadas = Reserva.objects.filter(
                mesa=mesa,
                fecha_reserva=fecha,
                turno=turno
            ).exclude(estado__in=['CANCELADA', 'NO_SHOW'])

            if self.instance:
                solapadas = solapadas.exclude(id=self.instance.id)

            if solapadas.exists():
                raise serializers.ValidationError({
                    "mesa": f"La mesa {mesa.numero_mesa} ya está reservada para la fecha {fecha} en el turno {turno}."
                })

        return data

    def update(self, instance, validated_data):
        estado_anterior = instance.estado
        estado_nuevo = validated_data.get('estado', estado_anterior)
        motivo = validated_data.pop('motivo_auditoria', 'Actualización mediante API REST')

        reserva = super().update(instance, validated_data)

        # Registro de auditoría si hubo alteración del estado
        if estado_anterior != estado_nuevo:
            request = self.context.get('request')
            usuario = request.user if request and request.user.is_authenticated else None
            if usuario:
                HistorialReserva.objects.create(
                    reserva=reserva,
                    usuario=usuario,
                    estado_anterior=estado_anterior,
                    estado_nuevo=estado_nuevo,
                    motivo=motivo
                )
        return reserva


class HistorialReservaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    cliente_nombre = serializers.ReadOnlyField(source='reserva.cliente_nombre')

    class Meta:
        model = HistorialReserva
        fields = [
            'id', 'reserva', 'cliente_nombre', 'usuario', 'usuario_nombre',
            'estado_anterior', 'estado_nuevo', 'motivo', 'fecha_registro'
        ]
        read_only_fields = ['fecha_registro']

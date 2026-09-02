from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='mesas')
    numero = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField(help_text="Número máximo de personas")
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('restaurante', 'numero')

    def __str__(self):
        return f"{self.restaurante.nombre} - Mesa {self.numero} (Capacidad: {self.capacidad})"

class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('EN_CURSO', 'En Curso / Sentados'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
        ('NO_SHOW', 'No asistió'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, related_name='reservas')
    fecha_reserva = models.DateTimeField()
    duracion_estimada_minutos = models.PositiveIntegerField(default=90)
    cantidad_personas = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    creado_en = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 1. Validación de fecha futura (solo al crear por primera vez)
        if not self.pk and self.fecha_reserva and self.fecha_reserva < timezone.now():
            raise ValidationError("No es posible programar reservas en fechas pasadas.")
            
        # 2. Validación de capacidad de mesa
        if self.mesa and self.cantidad_personas > self.mesa.capacidad:
            raise ValidationError(f"La mesa seleccionada solo soporta hasta {self.mesa.capacidad} personas.")

        # 3. Validación de no-solapamiento (misma mesa, mismo rango horario)
        if self.mesa and self.fecha_reserva:
            inicio = self.fecha_reserva
            fin = inicio + timedelta(minutes=self.duracion_estimada_minutos)
            
            # Buscar si otra reserva activa colisiona en este rango
            solapadas = Reserva.objects.filter(
                mesa=self.mesa,
                fecha_reserva__lt=fin,
                fecha_reserva__gte=inicio - timedelta(minutes=90)
            ).exclude(estado__in=['CANCELADA', 'NO_SHOW'])

            if self.pk:
                solapadas = solapadas.exclude(pk=self.pk)

            if solapadas.exists():
                raise ValidationError("Esta mesa ya tiene una reserva activa dentro de este horario.")

    def save(self, *args, **kwargs):
        # Si la reserva ya existía, revisar si cambió el estado para auditarlo
        if self.pk:
            anterior = Reserva.objects.get(pk=self.pk)
            if anterior.estado != self.estado:
                HistorialReserva.objects.create(
                    reserva=self,
                    estado_anterior=anterior.estado,
                    estado_nuevo=self.estado,
                    modificado_por=self.cliente,
                    comentario="Cambio de estado registrado automáticamente"
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente.username} en {self.mesa}"

class HistorialReserva(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='historial')
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    modificado_por = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cambio #{self.reserva.id}: {self.estado_anterior} -> {self.estado_nuevo}"
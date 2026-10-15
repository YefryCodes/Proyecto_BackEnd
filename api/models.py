from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    capacidad_total = models.PositiveIntegerField(default=50)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    UBICACION_CHOICES = [
        ('SALON', 'Salón Principal'),
        ('TERRAZA', 'Terraza al Aire Libre'),
        ('VIP', 'Zona VIP / Reservado'),
    ]

    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name='mesas')
    numero_mesa = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    ubicacion = models.CharField(max_length=15, choices=UBICACION_CHOICES, default='SALON')
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        unique_together = ('sucursal', 'numero_mesa')
        ordering = ['sucursal', 'numero_mesa']

    def __str__(self):
        return f"Mesa {self.numero_mesa} ({self.get_ubicacion_display()}) - {self.sucursal.nombre}"


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente de Confirmación'),
        ('CONFIRMADA', 'Confirmada'),
        ('COMPLETADA', 'Completada / Comensales Sentados'),
        ('CANCELADA', 'Cancelada'),
        ('NO_SHOW', 'No Presentado'),
    ]

    TURNO_CHOICES = [
        ('ALMUERZO_1', 'Almuerzo Turno 1 (12:30 - 14:30)'),
        ('ALMUERZO_2', 'Almuerzo Turno 2 (14:30 - 16:30)'),
        ('CENA_1', 'Cena Turno 1 (19:30 - 21:30)'),
        ('CENA_2', 'Cena Turno 2 (21:30 - 23:30)'),
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, related_name='reservas')
    cliente_nombre = models.CharField(max_length=120)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20)
    fecha_reserva = models.DateField()
    turno = models.CharField(max_length=15, choices=TURNO_CHOICES)
    cantidad_personas = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha_reserva', 'turno']

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente_nombre} ({self.fecha_reserva} [{self.turno}])"


class HistorialReserva(models.Model):
    """Auditoría y trazabilidad histórica de cambios de estado y operaciones."""
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='auditorias')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cambios_reserva')
    estado_anterior = models.CharField(max_length=15)
    estado_nuevo = models.CharField(max_length=15)
    motivo = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Historial de Reserva'
        verbose_name_plural = 'Historiales de Reservas'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"Cambio R#{self.reserva.id}: {self.estado_anterior} -> {self.estado_nuevo} por {self.usuario.username}"

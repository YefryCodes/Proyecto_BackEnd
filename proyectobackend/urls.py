from django.contrib import admin
from django.urls import path
from gestion_reservas.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Esta línea reemplaza el cohete por tu pantalla de inicio
]
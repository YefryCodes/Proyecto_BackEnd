from django.contrib import admin
from django.urls import path, include
from gestion_reservas.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('gestion_reservas.urls')),  # Conexión global de la API REST
]
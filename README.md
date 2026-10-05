# API REST de Gestión de Reservas - Cadena Gastronómica

Plataforma Backend desarrollada en **Python**, **Django** y **Django REST Framework (DRF)** orientada a la administración centralizada de disponibilidad de mesas, capacidad y gestión integral de reservas para restaurantes.

Este proyecto corresponde a la **Evaluación N.° 2 - Backend**, incorporando una arquitectura RESTful profesional, persistencia relacional con protección de integridad referencial, desacoplamiento seguro de credenciales mediante variables de entorno y soporte CRUD exhaustivo.

---

## 1. Requerimientos Técnicos

- **Lenguaje:** Python 3.10+
- **Framework Web:** Django 5.x / 6.x
- **API Framework:** Django REST Framework (DRF) 3.15+
- **Gestión de Entorno:** python-dotenv
- **Base de Datos:** MySQL / MariaDB (puerto 3306) o SQLite para desarrollo
- **Control de Versiones:** Git & GitHub

---

## 2. Configuración de Base de Datos y Variables de Entorno

### 2.1 Script de Inicialización de Base de Datos (MySQL)
En `scripts/01_init_db.sql` se encuentran las sentencias DDL y DCL para crear la base de datos, usuario y otorgar privilegios en MySQL:

```sql
CREATE DATABASE IF NOT EXISTS reservas_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'reservas_user'@'localhost' 
    IDENTIFIED BY 'Reservas123';

GRANT ALL PRIVILEGES ON reservas_db.* TO 'reservas_user'@'localhost';

FLUSH PRIVILEGES;
```

### 2.2 Variables de Entorno (.env)
El proyecto utiliza un archivo `.env` para desacoplar credenciales sensibles. Crea tu archivo local copiando la plantilla `.env.example`:

```powershell
cp .env.example .env
```

Contenido de `.env`:
```env
SECRET_KEY=django-insecure-reservas-cadena-gastronomica-key-2026
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Configuración Base de Datos (MySQL / SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

---

## 3. Instalación y Puesta en Marcha

Sigue estos pasos en tu terminal (PowerShell) para levantar el proyecto:

### 3.1 Entorno Virtual e Instalación de Dependencias
```powershell
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 3. Instalar librerías
pip install -r requirements.txt
```

### 3.2 Migraciones y Superusuario
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3.3 Ejecución del Servidor
```powershell
python manage.py runserver
```

---

## 4. Catálogo de Endpoints de la API REST

Interfaz navegable interactiva (DRF Browsable API): **`http://127.0.0.1:8000/api/`**

### 4.1 Restaurantes (`/api/restaurantes/`)
- `GET /api/restaurantes/` : Listar todos los restaurantes registrados.
- `POST /api/restaurantes/` : Crear un nuevo restaurante.
- `GET /api/restaurantes/{id}/` : Obtener detalle de un restaurante específico.
- `PUT /api/restaurantes/{id}/` : Actualización total de datos del restaurante.
- `PATCH /api/restaurantes/{id}/` : Actualización parcial de datos.
- `DELETE /api/restaurantes/{id}/` : Eliminar restaurante.

### 4.2 Mesas (`/api/mesas/`)
- `GET /api/mesas/` : Listar todas las mesas con detalle de capacidad y restaurante.
- `POST /api/mesas/` : Registrar nueva mesa (con validación de capacidad > 0).
- `GET /api/mesas/{id}/` : Consultar detalle de mesa.
- `PUT / PATCH /api/mesas/{id}/` : Modificar datos de mesa.
- `DELETE /api/mesas/{id}/` : Eliminar mesa (con protección referencial ante reservas asociadas).

### 4.3 Reservas (`/api/reservas/`)
- `GET /api/reservas/` : Listar todas las reservas realizadas.
- `POST /api/reservas/` : Crear nueva reserva (con validación de duración y cantidad de personas).
- `GET /api/reservas/{id}/` : Consultar detalle de reserva por ID.
- `PUT / PATCH /api/reservas/{id}/` : Modificar o actualizar estado de la reserva.
- `DELETE /api/reservas/{id}/` : Cancelar o eliminar reserva del sistema.

---

## 5. Accesos Adicionales

- **Panel de Administración Django:** `http://127.0.0.1:8000/admin/`
con el usuario y contra de createsuperuser creado anteriormente
- **Página de Inicio Web:** `http://127.0.0.1:8000/`

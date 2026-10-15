# Gestor de Reservas de Restaurantes y Disponibilidad de Mesas - Cadena Gastronómica

Plataforma Web y API RESTful desarrollada con **Python**, **Django**, **Django REST Framework (DRF)** y **MySQL**, orientada a la administración centralizada de disponibilidad de mesas, capacidad y gestión integral de reservas para una cadena gastronómica.

Este repositorio corresponde a la **Evaluación N.° 3 - Backend**, incorporando una arquitectura completamente desacoplada mediante `python-decouple`, capa canónica de autenticación, vistas protegidas por control de acceso (FBV y CBV), auditoría transaccional de estados y validaciones estrictas de reglas de negocio.

---

## 1. Requerimientos Técnicos

- **Lenguaje:** Python 3.10+
- **Framework Web:** Django 6.x
- **API REST Framework:** Django REST Framework (DRF) 3.18+
- **Desacoplamiento de Variables:** python-decouple 3.8+
- **Conector y Base de Datos:** MySQL / MariaDB (XAMPP o servidor local puerto 3306) con `mysqlclient`
- **Control de Versiones:** Git & GitHub

---

## 2. Aprovisionamiento de Base de Datos (Scripts SQL)

En la carpeta `scripts/` se encuentran las 3 sentencias DDL y DCL independientes para el aprovisionamiento de la base de datos MySQL:

1. `scripts/01_create_db.sql`: Creación de la base de datos `restaurante_reservas_db`.
2. `scripts/02_create_user.sql`: Creación del usuario de aplicación `restaurante_admin`.
3. `scripts/03_grant_privileges.sql`: Otorgamiento de privilegios exclusivos para `restaurante_admin`.

```sql
CREATE DATABASE IF NOT EXISTS restaurante_reservas_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'restaurante_admin'@'localhost' IDENTIFIED BY 'GastroSecure2026!';
GRANT ALL PRIVILEGES ON restaurante_reservas_db.* TO 'restaurante_admin'@'localhost';
FLUSH PRIVILEGES;
```

---

## 3. Variables de Entorno (`.env`)

El archivo `.env` se gestiona mediante `python-decouple`. Crea tu archivo local copiando la plantilla `.env.example`:

```powershell
cp .env.example .env
```

Contenido de `.env`:
```env
SECRET_KEY=django-insecure-gastro-reservas-audit-2026-prod-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,testserver

DB_ENGINE=django.db.backends.mysql
DB_NAME=restaurante_reservas_db
DB_USER=restaurante_admin
DB_PASSWORD=GastroSecure2026!
DB_HOST=localhost
DB_PORT=3306
```

---

## 4. Instalación y Puesta en Marcha

### 4.1 Entorno Virtual e Instalación de Dependencias
```powershell
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 3. Instalar librerías
pip install -r requirements.txt
```

### 4.2 Migraciones y Superusuario
```powershell
# Crear y aplicar migraciones en MySQL
python manage.py makemigrations api
python manage.py migrate

# Crear superusuario para acceso al panel y vistas protegidas
python manage.py createsuperuser
```

### 4.3 Ejecución del Servidor
```powershell
python manage.py runserver
```

---

## 5. Arquitectura de Navegación y Rutas del Sistema

### 5.1 Vistas Web y Control de Acceso
- **Landing Page Pública (`/`):** Portal de bienvenida para anfitriones y comensales.
- **Acceso / Formulario de Login (`/login/`):** Formulario canónico `auth_views.LoginView` con Tailwind CSS y protección CSRF.
- **Cierre de Sesión (`/logout/`):** Endpoint POST `auth_views.LogoutView` con redirección a la landing page.
- **Dashboard Analítico FBV (`/dashboard/`):** Vista protegida mediante `@login_required` que calcula KPIs en tiempo real (mesas habilitadas, reservas del día, tasa de ocupación estimada y cancelaciones) junto a la tabla de auditoría transaccional.
- **Catálogo de Mesas CBV (`/mesas/`):** Vista protegida mediante `LoginRequiredMixin` (`ListView`) con la disponibilidad física y zonas de mesas.
- **Panel de Administración (`/admin/`):** Gestión avanzada de modelos con inlines de auditoría.

### 5.2 Capa de API RESTful DRF (`/api/`)
Navegable de forma interactiva en **`http://127.0.0.1:8000/api/`**:
- `/api/sucursales/` : CRUD para gestión de locales y sucursales gastronómicas.
- `/api/mesas/` : CRUD para mesas, asignación de zonas (Salón, Terraza, VIP) y capacidad.
- `/api/reservas/` : CRUD de reservas con validación de capacidad, prevención de doble reserva y bloqueo de fechas pasadas.
- `/api/auditorias/` : Endpoint de solo lectura (`ReadOnlyModelViewSet`) protegido (`IsAuthenticated`) para trazabilidad de estados.

---

## 6. Reglas de Negocio Implementadas

1. **Control de Capacidad:** No se permite reservar una mesa si la cantidad de comensales excede su capacidad física.
2. **Prevención de Solapamiento:** Rechaza reservas simultáneas para la misma mesa, misma fecha y mismo turno (Almuerzo 1, Almuerzo 2, Cena 1, Cena 2), excluyendo reservas canceladas o no presentadas.
3. **Bloqueo Temporal:** No permite registrar reservas en fechas anteriores al día actual.
4. **Auditoría Transaccional:** Cada cambio de estado de reserva genera automáticamente un registro en `HistorialReserva` vinculando al operador responsable y motivo del cambio.

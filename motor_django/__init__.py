"""
Módulo de configuración central motor_django.
"""

# --- Bypass de compatibilidad MariaDB (XAMPP 10.4) para Django ---
try:
    from django.db.backends.base.base import BaseDatabaseWrapper
    BaseDatabaseWrapper.check_database_version_supported = lambda self: None

    from django.db.backends.mysql.features import DatabaseFeatures
    DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
except ImportError:
    pass
# ------------------------------------------------------------------

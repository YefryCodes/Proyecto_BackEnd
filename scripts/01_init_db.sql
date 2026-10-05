-- Script: 01_init_db.sql
-- Propósito: Creación de Base de Datos, Usuario y Asignación de Privilegios
-- Proyecto: API de Gestión de Reservas de Restaurantes

-- 1. Creación de la Base de Datos
CREATE DATABASE IF NOT EXISTS reservas_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 2. Creación de Usuario con clave segura
CREATE USER IF NOT EXISTS 'reservas_user'@'localhost' 
    IDENTIFIED BY 'Reservas123';

-- 3. Asignación de Privilegios sobre la base de datos
GRANT ALL PRIVILEGES ON reservas_db.* TO 'reservas_user'@'localhost';

-- 4. Aplicar cambios de privilegios
FLUSH PRIVILEGES;

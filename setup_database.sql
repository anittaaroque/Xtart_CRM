-- Script para crear la base de datos del E-Commerce XTART
-- Usuario: root
-- Password: admin

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS proyecto_1t CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE proyecto_1t;

-- Las tablas serán creadas automáticamente por Hibernate
-- debido a la configuración hibernate.hbm2ddl.auto=update

-- Verificar que la base de datos existe
SELECT 'Base de datos proyecto_1t creada exitosamente!' AS status;

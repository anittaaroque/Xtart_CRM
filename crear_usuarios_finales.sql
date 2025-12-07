-- Crear usuarios finales con hashes correctos
USE proyecto_1t;

-- Eliminar empleados existentes
DELETE FROM empleado;

-- Insertar ADMIN con password: cliente123 (mismo hash que funciona)
INSERT INTO empleado (nombre, apellidos, email, telefono, contraseña, rol, estado, estatus, fecha_contrato, intentos_login)
VALUES ('Admin', 'Sistema', 'admin@xtart.com', '666555444', '$2a$10$3v9Do/DCUip.65e9.l6sf.ARUPjz44LFj/T1CUp3GNatVpYrzFOV.', 'ADMIN', 'ACTIVO', 'A', CURDATE(), 0);

-- Insertar EMPLEADO con password: cliente123 (mismo hash que funciona)
INSERT INTO empleado (nombre, apellidos, email, telefono, contraseña, rol, estado, estatus, fecha_contrato, intentos_login)
VALUES ('Juan', 'Empleado', 'empleado@xtart.com', '666777888', '$2a$10$3v9Do/DCUip.65e9.l6sf.ARUPjz44LFj/T1CUp3GNatVpYrzFOV.', 'EMPLEADO', 'ACTIVO', 'A', CURDATE(), 0);

-- Verificar
SELECT 'Usuarios creados correctamente!' AS status;
SELECT id_empleado, nombre, email, rol FROM empleado;

-- Insertar datos de prueba para E-Commerce XTART
USE proyecto_1t;

-- Insertar empleado ADMIN
-- Email: admin@xtart.com
-- Password: admin123
SET @password_admin = '$2a$10$N9qo8uLOickgx2ZMRZoMye4QFfq6Q.h7HqW1vFWEYHsqNdYhxB8.q';
INSERT INTO empleado (nombre, apellidos, email, telefono, contraseña, rol, estado, estatus, fecha_contrato, intentos_login)
VALUES ('Administrador', 'Sistema', 'admin@xtart.com', '666555444', @password_admin, 'ADMIN', 'ACTIVO', 'A', CURDATE(), 0);

-- Insertar empleado regular
-- Email: empleado@xtart.com
-- Password: emp123
SET @password_emp = '$2a$10$8K1p/a0dL1LWPkBbzbEeYe8x7Yz2J3q4m5n6o7p8q9r0s1t2u3v4w';
INSERT INTO empleado (nombre, apellidos, email, telefono, contraseña, rol, estado, estatus, fecha_contrato, intentos_login)
VALUES ('Juan', 'Empleado', 'empleado@xtart.com', '666777888', @password_emp, 'EMPLEADO', 'ACTIVO', 'A', CURDATE(), 0);

-- Insertar cliente de prueba
-- Email: cliente@test.com
-- Password: cliente123
SET @password_cliente = '$2a$10$rO0H3XhQBYe8x7Yz2J3q4m5n6o7p8q9r0s1t2u3v4w5x6y7z8A9B';
INSERT INTO cliente (nombre, apellidos, email, contraseña, direccion, pais, estado, fecha_alta, intentos_login, rol_cliente)
VALUES ('María', 'Cliente Test', 'cliente@test.com', @password_cliente, 'Calle Principal 123', 'España', 'ACTIVO', NOW(), 0, 'CLIENTE');

-- Mostrar resumen
SELECT 'Datos insertados correctamente!' AS status;
SELECT COUNT(*) as total_empleados FROM empleado;
SELECT COUNT(*) as total_clientes FROM cliente;

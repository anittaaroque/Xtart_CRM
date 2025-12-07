# Configuración de la API
API_BASE_URL = "http://localhost:8080/proyecto/api"

# Endpoints
ENDPOINTS = {
    "login_cliente": f"{API_BASE_URL}/clientes/login",
    "registro_cliente": f"{API_BASE_URL}/clientes/registro",
    "logout_cliente": f"{API_BASE_URL}/clientes/logout",
    "login_empleado": f"{API_BASE_URL}/empleados/login",
    "logout_empleado": f"{API_BASE_URL}/empleados/logout",
    "productos": f"{API_BASE_URL}/productos",
    "producto_detalle": f"{API_BASE_URL}/productos",
    "carrito_agregar": f"{API_BASE_URL}/carrito/agregar",
    "carrito_ver": f"{API_BASE_URL}/carrito",
    "carrito_eliminar": f"{API_BASE_URL}/carrito",
    "facturas": f"{API_BASE_URL}/facturas",
    "facturas_cliente": f"{API_BASE_URL}/facturas/cliente",
    "clientes": f"{API_BASE_URL}/clientes",
    "empleados": f"{API_BASE_URL}/empleados",
    "proveedores": f"{API_BASE_URL}/proveedores",
}

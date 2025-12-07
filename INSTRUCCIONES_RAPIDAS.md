# Instrucciones Rápidas - E-Commerce XTART

## Problema Actual: Base de datos no existe

### Solución:

1. **Crear la base de datos MySQL**

   Opción A - Usando el script:
   ```bash
   crear_base_datos.bat
   ```

   Opción B - MySQL Workbench:
   - Abrir MySQL Workbench
   - Conectar con usuario: `root`, password: `admin`
   - Ejecutar: `CREATE DATABASE proyecto_1t;`

   Opción C - Línea de comandos:
   ```bash
   mysql -u root -padmin -e "CREATE DATABASE proyecto_1t;"
   ```

2. **Reiniciar Tomcat** (para que reconozca la nueva BD)
   - Detener el servidor Tomcat
   - Iniciar nuevamente

3. **Probar la conexión**
   ```bash
   python test_api.py
   ```

4. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

## Configuración Actual

- **API URL**: `http://localhost:8080/proyecto/api`
- **Base de datos**: `proyecto_1t`
- **Usuario DB**: `root`
- **Password DB**: `admin`
- **Puerto MySQL**: `3306`
- **Puerto Tomcat**: `8080`

## Verificar que todo funciona

1. MySQL está corriendo en puerto 3306
2. Tomcat está corriendo en puerto 8080
3. Base de datos `proyecto_1t` existe
4. Aplicación desplegada en contexto `/proyecto`

## Credenciales de Prueba

Una vez que la BD esté creada, Hibernate creará las tablas automáticamente.
Deberás insertar datos de prueba (clientes, empleados, productos) manualmente o desde la aplicación.

## Contacto

Si persisten los problemas, verifica:
- Los logs de Tomcat en: `Proyecto_1T/Proyecto_1T/proyecto/target/`
- El servicio MySQL está activo
- Las credenciales son correctas

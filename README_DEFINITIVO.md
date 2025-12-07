# Proyecto Full Stack - Sistema de Gestión CRM y E-Commerce

## Descripción General

Este proyecto es una aplicación Full Stack que integra un sistema de gestión de relaciones con clientes (CRM) y una plataforma de e-commerce. La aplicación está compuesta por:

- **Backend**: Aplicación Java EE con Jakarta EE, JPA/Hibernate y API REST
- **Frontend**: Interfaz gráfica desarrollada con Tkinter (Python)
- **Base de datos**: MySQL

## Arquitectura del Sistema

### Backend (Java)

El backend está desarrollado siguiendo una arquitectura en capas:

```
┌──────────────────────────┐
│   REST Resources (JAX-RS) │  ← Capa de presentación
├──────────────────────────┤
│      Services            │  ← Lógica de negocio
├──────────────────────────┤
│    Repositories          │  ← Acceso a datos
├──────────────────────────┤
│    Entities (JPA)        │  ← Modelo de datos
└──────────────────────────┘
```

**Tecnologías principales**:
- Jakarta EE 10
- Hibernate 6.2.7 (JPA)
- Jersey 3.1.3 (JAX-RS)
- Jackson 2.15.2 (JSON)
- MySQL Connector 8.0.33
- Weld 5.1.2 (CDI)
- jBCrypt (seguridad de contraseñas)

### Frontend (Python/Tkinter)

Interfaz gráfica de escritorio desarrollada en Python con Tkinter siguiendo principios de usabilidad y diseño coherente.

**Características**:
- Diseño moderno con tema oscuro
- Navegación por pestañas
- Componentes reutilizables
- Comunicación HTTP con el backend

## Requisitos Previos

### Backend (Java)

- **Java**: JDK 21 o superior
- **Maven**: 3.8 o superior
- **Servidor de aplicaciones**: Apache Tomcat 10.1 o WildFly 27+
- **Base de datos**: MySQL 8.0+

### Frontend (Python)

- **Python**: 3.10 o superior
- **Librerías**:
  - tkinter (incluida en Python)
  - requests
  - Pillow (opcional para imágenes)

## Instalación y Configuración

### Paso 1: Configurar la Base de Datos

1. Instalar MySQL Server 8.0+

2. Crear la base de datos:

```bash
cd c:\Users\migue\Desktop\Proyecto_1T\Proyecto_AINHOA\Proyecto_AINHOA\Proyecto_AINHOA
mysql -u root -p < setup_database.sql
```

O manualmente:

```sql
CREATE DATABASE proyecto_1t CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Configurar el usuario de MySQL:

```sql
CREATE USER 'proyecto_user'@'localhost' IDENTIFIED BY 'proyecto_pass';
GRANT ALL PRIVILEGES ON proyecto_1t.* TO 'proyecto_user'@'localhost';
FLUSH PRIVILEGES;
```

4. Verificar la configuración en `persistence.xml`:

```xml
<!-- Archivo: Proyecto_1T/proyecto/src/main/resources/META-INF/persistence.xml -->
<property name="jakarta.persistence.jdbc.url" value="jdbc:mysql://localhost:3306/proyecto_1t"/>
<property name="jakarta.persistence.jdbc.user" value="root"/>
<property name="jakarta.persistence.jdbc.password" value="tu_password"/>
```

### Paso 2: Compilar y Desplegar el Backend

#### Opción A: Usando Maven y Tomcat

1. Navegar al directorio del proyecto Java:

```bash
cd Proyecto_1T\Proyecto_1T\proyecto
```

2. Compilar el proyecto:

```bash
mvn clean install
```

3. El archivo WAR generado estará en:

```
target/proyecto-1.0-SNAPSHOT.war
```

4. Copiar el WAR al directorio de Tomcat:

```bash
copy target\proyecto-1.0-SNAPSHOT.war C:\ruta\a\tomcat\webapps\
```

5. Iniciar Tomcat:

```bash
C:\ruta\a\tomcat\bin\startup.bat
```

6. Verificar que la aplicación esté corriendo:

```
http://localhost:8080/proyecto/api/productos
```

#### Opción B: Usando Maven con Tomcat Embedded

```bash
mvn tomcat7:run
```

### Paso 3: Configurar y Ejecutar el Frontend

1. Navegar al directorio del frontend:

```bash
cd c:\Users\migue\Desktop\Proyecto_1T\Proyecto_AINHOA\Proyecto_AINHOA\Proyecto_AINHOA
```

2. Instalar las dependencias de Python:

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install requests
```

3. Verificar la configuración del backend en `config.py`:

```python
API_BASE_URL = "http://localhost:8080/proyecto/api"
```

4. Ejecutar la aplicación:

```bash
python main.py
```

## Estructura del Proyecto

### Backend (Java)

```
Proyecto_1T/proyecto/
├── src/main/java/org/proyecto/backend/
│   ├── config/              # Configuración (Jackson, etc.)
│   ├── controller/          # Servlets tradicionales
│   ├── dto/                 # Data Transfer Objects
│   ├── entity/              # Entidades JPA
│   ├── filter/              # Filtros HTTP
│   ├── repository/          # Capa de acceso a datos
│   │   ├── impl/           # Implementaciones de repositorios
│   ├── rest/               # REST Resources (JAX-RS)
│   │   ├── request/       # Request DTOs
│   │   └── resource/      # Endpoints REST
│   ├── service/            # Capa de lógica de negocio
│   │   └── impl/          # Implementaciones de servicios
│   ├── threads/            # Concurrencia y paralelismo
│   │   └── executorManager/
│   └── util/               # Utilidades (JpaUtil, etc.)
├── src/main/resources/
│   └── META-INF/
│       └── persistence.xml # Configuración JPA
└── pom.xml                 # Dependencias Maven
```

### Frontend (Python)

```
Proyecto_AINHOA/
├── main.py                 # Aplicación principal Tkinter
├── api_client.py          # Cliente HTTP para comunicación con backend
├── config.py              # Configuración de endpoints
├── requirements.txt       # Dependencias Python
└── *.sql                  # Scripts de base de datos
```

## Endpoints de la API REST

### Autenticación

```
POST   /api/clientes/login           - Login de cliente
POST   /api/clientes/registro        - Registro de cliente
POST   /api/clientes/logout          - Cerrar sesión
POST   /api/empleados/login          - Login de empleado
POST   /api/empleados/logout         - Cerrar sesión empleado
```

### Productos

```
GET    /api/productos                - Listar todos los productos
GET    /api/productos/{id}           - Obtener producto por ID
POST   /api/productos                - Crear producto
PUT    /api/productos                - Actualizar producto
DELETE /api/productos/{id}           - Eliminar producto
```

### Carrito

```
POST   /api/carrito/agregar          - Agregar producto al carrito
GET    /api/carrito/{clienteId}      - Ver carrito del cliente
DELETE /api/carrito/{clienteId}/{productoId} - Eliminar del carrito
```

### Facturas

```
POST   /api/facturas                 - Crear factura
GET    /api/facturas                 - Listar todas las facturas
GET    /api/facturas/{id}            - Obtener factura por ID
GET    /api/facturas/cliente/{id}    - Facturas de un cliente
PUT    /api/facturas                 - Actualizar factura
DELETE /api/facturas/{id}            - Eliminar factura
```

### Proveedores

```
GET    /api/proveedores              - Listar proveedores
GET    /api/proveedores/{id}         - Obtener por ID
POST   /api/proveedores              - Crear proveedor
PUT    /api/proveedores              - Actualizar proveedor
DELETE /api/proveedores/{id}         - Eliminar proveedor
GET    /api/proveedores/nombre/{nombre} - Buscar por nombre
GET    /api/proveedores/pais/{pais}  - Listar por país
```

### Clientes

```
GET    /api/clientes                 - Listar clientes
GET    /api/clientes/{id}            - Obtener cliente por ID
POST   /api/clientes                 - Crear cliente
```

### Empleados

```
GET    /api/empleados                - Listar empleados
POST   /api/empleados                - Crear empleado
```

## Funcionalidades Principales

### Para Clientes (E-Commerce)

- Navegación de productos por catálogo
- Visualización de detalles de productos
- Agregar productos al carrito
- Modificar cantidades en el carrito
- Finalizar compra y generar factura
- Ver historial de compras (Mis Facturas)
- Gestión de perfil

### Para Empleados (CRM)

- Gestión completa de clientes (CRUD)
- Gestión de productos (CRUD)
- Gestión de proveedores (CRUD)
- Gestión de facturas (CRUD)
- Visualización de todas las facturas del sistema
- Creación de empleados
- Dashboard con estadísticas

## Características Técnicas Destacadas

### Acceso a Datos

- **JPA/Hibernate**: Mapeo objeto-relacional
- **Repository Pattern**: Abstracción de acceso a datos
- **Transacciones**: Manejo explícito de transacciones
- **Optional**: Manejo seguro de valores nulos

### Servicios y Procesos (Concurrencia)

- **ExecutorService**: Pool de hilos para tareas asíncronas
- **Hilos múltiples**: Implementados con Runnable, Lambda y clases anónimas
- **Sincronización**: Control de race conditions con `synchronized`
- **Control de versiones**: `@Version` en entidades para evitar lost updates
- **Tareas asíncronas**:
  - Envío de emails
  - Generación de logs
  - Generación de informes

### API REST

- **JAX-RS (Jersey)**: Framework para API REST
- **JSON**: Formato de intercambio de datos
- **Jackson**: Serialización/deserialización JSON
- **CDI**: Inyección de dependencias
- **Filtros**: Validación y procesamiento de peticiones

### Interfaz de Usuario

- **Tema oscuro**: Diseño moderno y profesional
- **Componentes reutilizables**: Cards, formularios, tablas
- **Validación de formularios**: En tiempo real
- **Navegación por pestañas**: Organización clara
- **Feedback al usuario**: Mensajes de éxito/error

## Credenciales de Prueba

### Clientes

```
Email: cliente1@test.com
Password: password123
```

### Empleados

```
Email: empleado1@empresa.com
Password: admin123
```

## Solución de Problemas

### Error: "No se puede conectar a la base de datos"

**Solución**:
1. Verificar que MySQL esté corriendo
2. Comprobar credenciales en `persistence.xml`
3. Verificar que la base de datos `proyecto_1t` exista

### Error: "404 Not Found al acceder a la API"

**Solución**:
1. Verificar que Tomcat esté corriendo
2. Comprobar que el WAR esté desplegado correctamente
3. Verificar la URL: `http://localhost:8080/proyecto/api/`

### Error: "Module 'tkinter' not found"

**Solución**:
En Windows, tkinter viene incluido con Python. Si falta:
```bash
python -m pip install tk
```

### Error en el frontend: "Connection refused"

**Solución**:
1. Verificar que el backend esté corriendo
2. Comprobar la URL en `config.py`
3. Verificar firewall/antivirus

## Ejecución Rápida

### 1. Iniciar MySQL

```bash
# Windows
net start MySQL80

# Linux/Mac
sudo service mysql start
```

### 2. Iniciar Backend

```bash
cd Proyecto_1T\Proyecto_1T\proyecto
mvn clean install
# Copiar WAR a Tomcat y iniciar
```

### 3. Iniciar Frontend

```bash
cd c:\Users\migue\Desktop\Proyecto_1T\Proyecto_AINHOA\Proyecto_AINHOA\Proyecto_AINHOA
python main.py
```

## Estructura de la Base de Datos

### Entidades Principales

- **cliente**: Usuarios del e-commerce
- **empleado**: Usuarios del CRM
- **producto**: Catálogo de productos
- **proveedor**: Proveedores de productos
- **categoria**: Categorías de productos
- **factura**: Facturas de compra
- **detalle_factura**: Líneas de las facturas
- **carrito_detalle**: Carrito de compras temporal

### Relaciones

```
cliente (1) ←→ (N) factura
producto (N) ←→ (1) proveedor
producto (N) ←→ (1) categoria
factura (1) ←→ (N) detalle_factura
producto (1) ←→ (N) detalle_factura
cliente (1) ←→ (1) carrito_detalle
```

## Autores

Proyecto desarrollado para las asignaturas:
- Acceso a Datos
- Programación de Servicios y Procesos
- Desarrollo de Interfaces

## Licencia

Este proyecto es de carácter educativo.

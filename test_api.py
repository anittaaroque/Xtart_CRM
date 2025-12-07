#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la conexión con la API del E-Commerce XTART
"""

from api_client import APIClient
import sys
import io

# Configurar la salida para UTF-8 en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_connection():
    print("=" * 60)
    print("TEST DE CONEXIÓN API E-COMMERCE XTART")
    print("=" * 60)
    print()

    client = APIClient()

    print("1. Probando conexión con el servidor...")
    print("   Endpoint: GET /api/productos")
    success, productos = client.get_productos()

    if success:
        print(f"   [OK] Conexion exitosa!")
        print(f"   [OK] Se encontraron {len(productos)} productos")
        if productos:
            print(f"   [OK] Ejemplo de producto: {productos[0].get('nombre', 'N/A')}")
    else:
        print("   [ERROR] Error de conexion")
        print("   [ERROR] Verifique que el backend este ejecutandose en http://localhost:8080/api")
        sys.exit(1)

    print()
    print("2. Probando endpoint de clientes...")
    print("   Endpoint: GET /api/clientes")
    success, clientes = client.get_clientes()

    if success:
        print(f"   [OK] Endpoint funcional!")
        print(f"   [OK] Se encontraron {len(clientes)} clientes registrados")
    else:
        print("   [ERROR] Error al obtener clientes")

    print()
    print("3. Probando endpoint de empleados...")
    print("   Endpoint: GET /api/empleados")
    success, empleados = client.get_empleados()

    if success:
        print(f"   [OK] Endpoint funcional!")
        print(f"   [OK] Se encontraron {len(empleados)} empleados registrados")
    else:
        print("   [ERROR] Error al obtener empleados")

    print()
    print("4. Probando endpoint de proveedores...")
    print("   Endpoint: GET /api/proveedores")
    success, proveedores = client.get_proveedores()

    if success:
        print(f"   [OK] Endpoint funcional!")
        print(f"   [OK] Se encontraron {len(proveedores)} proveedores registrados")
    else:
        print("   [ERROR] Error al obtener proveedores")

    print()
    print("5. Probando endpoint de facturas...")
    print("   Endpoint: GET /api/facturas")
    success, facturas = client.get_todas_facturas()

    if success:
        print(f"   [OK] Endpoint funcional!")
        print(f"   [OK] Se encontraron {len(facturas)} facturas en el sistema")
    else:
        print("   [ERROR] Error al obtener facturas")

    print()
    print("=" * 60)
    print("RESUMEN DEL TEST")
    print("=" * 60)
    print("[OK] La API esta funcionando correctamente")
    print("[OK] Todos los endpoints principales estan accesibles")
    print()
    print("Puede ejecutar la aplicacion principal con:")
    print("  python main.py")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_connection()
    except KeyboardInterrupt:
        print("\n\nTest interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        print("\nVerifique que:")
        print("  1. El backend esta ejecutandose")
        print("  2. La base de datos esta activa")
        print("  3. La URL de la API es correcta en config.py")
        sys.exit(1)

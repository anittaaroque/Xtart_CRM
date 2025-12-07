#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el login y ver los errores detallados
"""

from api_client import APIClient
import sys

def test_logins():
    client = APIClient()

    print("=" * 60)
    print("TEST DE LOGIN - DIAGNÓSTICO DETALLADO")
    print("=" * 60)
    print()

    # Test 1: Login de cliente
    print("1. Probando login de CLIENTE:")
    print("   Email: cliente@test.com")
    print("   Password: cliente123")
    success, data = client.login_cliente("cliente@test.com", "cliente123")
    print(f"   Resultado: {'EXITOSO' if success else 'FALLIDO'}")
    print(f"   Respuesta: {data}")
    print()

    # Test 2: Login de empleado
    print("2. Probando login de EMPLEADO:")
    print("   Email: empleado@xtart.com")
    print("   Password: emp123")
    success, data = client.login_empleado("empleado@xtart.com", "emp123")
    print(f"   Resultado: {'EXITOSO' if success else 'FALLIDO'}")
    print(f"   Respuesta: {data}")
    print()

    # Test 3: Login de admin
    print("3. Probando login de ADMIN:")
    print("   Email: admin@xtart.com")
    print("   Password: admin123")
    success, data = client.login_empleado("admin@xtart.com", "admin123")
    print(f"   Resultado: {'EXITOSO' if success else 'FALLIDO'}")
    print(f"   Respuesta: {data}")
    print()

    # Test 4: Ver empleados
    print("4. Verificando que existan empleados:")
    success, empleados = client.get_empleados()
    if success:
        print(f"   [OK] Se encontraron {len(empleados)} empleados")
        for emp in empleados:
            print(f"   - {emp.get('email')} (Rol: {emp.get('rol')})")
    else:
        print(f"   [ERROR] No se pudieron obtener empleados")
    print()

    # Test 5: Ver clientes
    print("5. Verificando que existan clientes:")
    success, clientes = client.get_clientes()
    if success:
        print(f"   [OK] Se encontraron {len(clientes)} clientes")
        for cli in clientes:
            print(f"   - {cli.get('email')} (Estado: {cli.get('estado')})")
    else:
        print(f"   [ERROR] No se pudieron obtener clientes")

    print()
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_logins()
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()

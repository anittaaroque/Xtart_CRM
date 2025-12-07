#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear usuarios usando la API (hashea correctamente las contraseñas)
"""

from api_client import APIClient
import sys

def crear_usuarios():
    client = APIClient()

    print("=" * 60)
    print("CREANDO USUARIOS DE PRUEBA VIA API")
    print("=" * 60)
    print()

    # Registrar cliente de prueba
    print("1. Registrando cliente de prueba...")
    success, msg = client.registro_cliente(
        nombre="Test",
        apellidos="Cliente",
        email="testcliente@xtart.com",
        direccion="Calle Test 123",
        pais="Spain",
        password="cliente123"
    )
    if success:
        print("   [OK] Cliente registrado: testcliente@xtart.com / cliente123")
    else:
        print(f"   [INFO] {msg}")
    print()

    # Verificar login del cliente
    print("2. Probando login del cliente...")
    success, data = client.login_cliente("testcliente@xtart.com", "cliente123")
    if success:
        print("   [OK] Login exitoso!")
        print(f"   Rol: {data.get('rol')}")
    else:
        print(f"   [ERROR] Login fallido: {data}")
    print()

    print("=" * 60)
    print("USUARIOS DISPONIBLES:")
    print("=" * 60)
    print()
    print("CLIENTE:")
    print("  Email:    testcliente@xtart.com")
    print("  Password: cliente123")
    print()
    print("NOTA: Los empleados deben ser insertados directamente")
    print("      en la base de datos o desde el backend")
    print("=" * 60)

if __name__ == "__main__":
    try:
        crear_usuarios()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

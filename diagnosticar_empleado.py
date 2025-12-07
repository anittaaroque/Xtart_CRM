#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnosticar por qué no funciona el login de empleados
"""

from api_client import APIClient
import requests

print("=" * 60)
print("DIAGNÓSTICO DE LOGIN DE EMPLEADO")
print("=" * 60)
print()

# Pedir email y password del empleado que acabas de crear
email = input("Email del empleado que creaste: ")
password = input("Password del empleado: ")

print()
print("1. Verificando que el empleado existe en la BD...")
client = APIClient()
success, empleados = client.get_empleados()
if success:
    empleado_encontrado = None
    for emp in empleados:
        if emp.get('email') == email:
            empleado_encontrado = emp
            break

    if empleado_encontrado:
        print(f"   [OK] Empleado encontrado en BD")
        print(f"   - ID: {empleado_encontrado.get('idEmpleado')}")
        print(f"   - Nombre: {empleado_encontrado.get('nombre')}")
        print(f"   - Rol: {empleado_encontrado.get('rol')}")
        print(f"   - Estado: {empleado_encontrado.get('estado')}")
    else:
        print(f"   [ERROR] Empleado con email {email} NO encontrado")
        print("\n   Empleados disponibles:")
        for emp in empleados:
            print(f"   - {emp.get('email')} ({emp.get('rol')})")
else:
    print("   [ERROR] No se pudieron obtener empleados")

print()
print("2. Probando login con la API...")
success, data = client.login_empleado(email, password)
if success:
    print(f"   [OK] Login EXITOSO!")
    print(f"   Respuesta: {data}")
else:
    print(f"   [ERROR] Login FALLIDO")
    print(f"   Respuesta: {data[:200] if isinstance(data, str) else data}")

print()
print("3. Probando con curl directo...")
import subprocess
result = subprocess.run([
    'curl', '-s', '-X', 'POST',
    'http://localhost:8080/proyecto/api/empleados/login',
    '-H', 'Content-Type: application/json',
    '-d', f'{{"email":"{email}","password":"{password}"}}'
], capture_output=True, text=True)
print(f"   Respuesta del servidor:")
print(f"   {result.stdout[:300]}")

print()
print("=" * 60)

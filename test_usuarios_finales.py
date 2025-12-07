#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from api_client import APIClient

client = APIClient()

print("=" * 60)
print("TEST FINAL - TODOS LOS USUARIOS")
print("=" * 60)
print()

# Test ADMIN
print("1. ADMIN:")
print("   Email: admin@xtart.com")
print("   Password: cliente123")
success, data = client.login_empleado("admin@xtart.com", "cliente123")
print(f"   Resultado: {'[OK] EXITOSO' if success else '[ERROR] FALLIDO'}")
if not success:
    print(f"   Error: {data[:100]}")
print()

# Test EMPLEADO
print("2. EMPLEADO:")
print("   Email: empleado@xtart.com")
print("   Password: cliente123")
success, data = client.login_empleado("empleado@xtart.com", "cliente123")
print(f"   Resultado: {'[OK] EXITOSO' if success else '[ERROR] FALLIDO'}")
if not success:
    print(f"   Error: {data[:100]}")
print()

# Test CLIENTE
print("3. CLIENTE:")
print("   Email: testcliente@xtart.com")
print("   Password: cliente123")
success, data = client.login_cliente("testcliente@xtart.com", "cliente123")
print(f"   Resultado: {'[OK] EXITOSO' if success else '[ERROR] FALLIDO'}")
if not success:
    print(f"   Error: {data[:100]}")
print()

print("=" * 60)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from api_client import APIClient

client = APIClient()

print("=" * 60)
print("PROBANDO USUARIO QUE FUNCIONA")
print("=" * 60)
print()

print("Login como CLIENTE:")
print("Email: testcliente@xtart.com")
print("Password: cliente123")
success, data = client.login_cliente("testcliente@xtart.com", "cliente123")
print(f"Resultado: {'EXITOSO' if success else 'FALLIDO'}")
if success:
    print(f"Rol: {data}")
    print("\n[OK] Este usuario FUNCIONA!")
else:
    print(f"Error: {data}")

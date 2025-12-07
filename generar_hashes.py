#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generar hashes bcrypt correctos para las contraseñas
"""

import requests

# Usar el endpoint de registro para generar hashes válidos
def obtener_hash(password):
    """Registra un usuario temporal para obtener el hash correcto"""
    import random
    import string

    # Email temporal aleatorio
    random_email = ''.join(random.choices(string.ascii_lowercase, k=10)) + "@temp.com"

    url = "http://localhost:8080/proyecto/api/clientes/registro"
    data = {
        "nombre": "Temp",
        "apellidos": "User",
        "email": random_email,
        "direccion": "Temp",
        "pais": "Spain",
        "password": password
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('contraseña')
    return None

print("Generando hashes correctos...")
print()

hash_admin = obtener_hash("admin123")
print(f"Hash para 'admin123': {hash_admin}")

hash_emp = obtener_hash("emp123")
print(f"Hash para 'emp123': {hash_emp}")

hash_cliente = obtener_hash("cliente123")
print(f"Hash para 'cliente123': {hash_cliente}")

print()
print("Ahora actualizando la base de datos...")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para actualizar main.py con las nuevas funcionalidades
"""

def update_main_py():
    # Leer el archivo original
    with open('main.py.backup', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # 1. Eliminar botones de registro del login (líneas 181-208)
        if i >= 180 and '# Enlace de registro' in line:
            # Saltar hasta encontrar '# Bind Enter key'
            while i < len(lines) and '# Bind Enter key' not in lines[i]:
                i += 1
            # No agregar las líneas que saltamos
            continue

        new_lines.append(line)
        i += 1

    # Escribir el archivo actualizado
    with open('main.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print("Archivo actualizado exitosamente")

if __name__ == "__main__":
    update_main_py()

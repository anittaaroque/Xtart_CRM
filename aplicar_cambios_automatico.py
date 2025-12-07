#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para aplicar AUTOMÁTICAMENTE todos los cambios necesarios a main.py

IMPORTANTE: Este script hace un backup de main.py antes de modificarlo.
Si algo sale mal, puedes restaurar desde main.py.backup

Uso:
  python aplicar_cambios_automatico.py
"""

import shutil
import os
from datetime import datetime

def aplicar_cambios():
    archivo_original = 'main.py'
    archivo_backup = f'main.py.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'

    # Crear backup
    print(f"Creando backup: {archivo_backup}")
    shutil.copy(archivo_original, archivo_backup)

    # Leer el archivo
    with open(archivo_original, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    nuevas_lineas = []
    i = 0

    while i < len(lineas):
        linea = lineas[i]

        # =====================================================================
        # MODIFICACIÓN 1: CRUD Productos - Actualizar botones (línea ~1216)
        # =====================================================================
        if 'ttk.Button(btn_frame, text="🔄 Actualizar", command=cargar_productos' in linea and \
           i > 1200 and i < 1230:
            # Reemplazar los dos botones antiguos con los nuevos 6 botones
            nuevas_lineas.append('        ttk.Button(btn_frame, text="Actualizar", command=cargar_productos,\n')
            nuevas_lineas.append('                  style=\'Accent.TButton\').pack(side=tk.LEFT, padx=5)\n')
            nuevas_lineas.append('        ttk.Button(btn_frame, text="Crear Producto", command=crear_producto,\n')
            nuevas_lineas.append('                  style=\'Accent.TButton\').pack(side=tk.LEFT, padx=5)\n')
            nuevas_lineas.append('        ttk.Button(btn_frame, text="Actualizar Producto", command=actualizar_producto,\n')
            nuevas_lineas.append('                  style=\'Accent.TButton\').pack(side=tk.LEFT, padx=5)\n')
            nuevas_lineas.append('        ttk.Button(btn_frame, text="Eliminar Producto", command=eliminar_producto,\n')
            nuevas_lineas.append('                  style=\'Accent.TButton\').pack(side=tk.LEFT, padx=5)\n')
            nuevas_lineas.append('        ttk.Button(btn_frame, text="Buscar por ID", command=buscar_por_id,\n')
            nuevas_lineas.append('                  style=\'Accent.TButton\').pack(side=tk.LEFT, padx=5)\n')
            nuevas_lineas.append('        ttk.Button(btn_frame, text="Ver Detalles", command=ver_detalles,\n')
            nuevas_lineas.append('                  style=\'Accent.TButton\').pack(side=tk.LEFT, padx=5)\n')

            # Saltar las dos líneas siguientes (el botón Ver Detalles antiguo)
            i += 1
            while i < len(lineas) and 'Ver Detalles' in lineas[i]:
                i += 1
            continue

        # =====================================================================
        # MODIFICACIÓN 2: CRUD Productos - Insertar funciones antes de btn_frame
        # =====================================================================
        if 'btn_frame = ttk.Frame(frame, style=\'Dark.TFrame\')' in linea and \
           i > 1200 and i < 1230:
            # Insertar todas las funciones CRUD de productos ANTES de btn_frame
            nuevas_lineas.append('''
        def crear_producto():
            dialog = tk.Toplevel(self.root)
            dialog.title("Crear Producto")
            dialog.geometry("600x700")
            dialog.configure(bg=COLORS['bg_secondary'])
            dialog.transient(self.root)

            ttk.Label(dialog, text="Crear Producto",
                     font=('Segoe UI', 16, 'bold'),
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=20)

            form_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
            form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            canvas = tk.Canvas(form_frame, bg=COLORS['bg_secondary'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
            scrollable_form = ttk.Frame(canvas, style='Card.TFrame')

            scrollable_form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_form, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            fields = [
                ("Nombre:", "nombre"),
                ("Descripcion:", "descripcion"),
                ("SKU:", "sku"),
                ("Precio Lista:", "precioLista"),
                ("Stock Minimo:", "stockMin"),
                ("Stock Actual:", "stockActual"),
                ("Proveedor ID:", "proveedorId"),
            ]

            entries = {}
            for i, (label, key) in enumerate(fields):
                ttk.Label(scrollable_form, text=label,
                         background=COLORS['bg_secondary'],
                         foreground=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, padx=10, pady=8)
                entry = ttk.Entry(scrollable_form, width=30, style='Dark.TEntry')
                entry.grid(row=i, column=1, padx=10, pady=8)
                entries[key] = entry

            def guardar():
                data = {key: entry.get().strip() for key, entry in entries.items()}

                if not all(data.values()):
                    messagebox.showerror("Error", "Complete todos los campos")
                    return

                try:
                    data['precioLista'] = float(data['precioLista'])
                    data['stockMin'] = int(data['stockMin'])
                    data['stockActual'] = int(data['stockActual'])
                    data['proveedorId'] = int(data['proveedorId'])
                except ValueError:
                    messagebox.showerror("Error", "Valores numericos invalidos")
                    return

                success, msg = self.api.crear_producto(data)
                if success:
                    messagebox.showinfo("Exito", "Producto creado")
                    dialog.destroy()
                    cargar_productos()
                else:
                    messagebox.showerror("Error", msg)

            ttk.Button(scrollable_form, text="Guardar", command=guardar,
                      style='Accent.TButton').grid(row=len(fields), column=0, columnspan=2, pady=20)

        def actualizar_producto():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return

            item = tree.item(selected[0])
            producto_id = item["values"][0]

            success, producto_actual = self.api.get_producto(producto_id)
            if not success:
                messagebox.showerror("Error", "No se pudo cargar el producto")
                return

            dialog = tk.Toplevel(self.root)
            dialog.title("Actualizar Producto")
            dialog.geometry("600x700")
            dialog.configure(bg=COLORS['bg_secondary'])
            dialog.transient(self.root)

            ttk.Label(dialog, text=f"Actualizar Producto ID: {producto_id}",
                     font=('Segoe UI', 16, 'bold'),
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=20)

            form_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
            form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            canvas = tk.Canvas(form_frame, bg=COLORS['bg_secondary'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
            scrollable_form = ttk.Frame(canvas, style='Card.TFrame')

            scrollable_form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_form, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            fields = [
                ("Nombre:", "nombre"),
                ("Descripcion:", "descripcion"),
                ("SKU:", "sku"),
                ("Precio Lista:", "precioLista"),
                ("Stock Minimo:", "stockMin"),
                ("Stock Actual:", "stockActual"),
                ("Proveedor ID:", "proveedorId"),
            ]

            entries = {}
            for i, (label, key) in enumerate(fields):
                ttk.Label(scrollable_form, text=label,
                         background=COLORS['bg_secondary'],
                         foreground=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, padx=10, pady=8)
                entry = ttk.Entry(scrollable_form, width=30, style='Dark.TEntry')
                entry.grid(row=i, column=1, padx=10, pady=8)

                if key == "proveedorId":
                    proveedor = producto_actual.get("proveedor", {})
                    if isinstance(proveedor, dict):
                        entry.insert(0, str(proveedor.get("idProveedor", "")))
                else:
                    entry.insert(0, str(producto_actual.get(key, "")))

                entries[key] = entry

            def guardar():
                data = {key: entry.get().strip() for key, entry in entries.items()}
                data['idProducto'] = producto_id

                if not all(data.values()):
                    messagebox.showerror("Error", "Complete todos los campos")
                    return

                try:
                    data['precioLista'] = float(data['precioLista'])
                    data['stockMin'] = int(data['stockMin'])
                    data['stockActual'] = int(data['stockActual'])
                    data['proveedorId'] = int(data['proveedorId'])
                except ValueError:
                    messagebox.showerror("Error", "Valores numericos invalidos")
                    return

                success, msg = self.api.actualizar_producto(data)
                if success:
                    messagebox.showinfo("Exito", "Producto actualizado")
                    dialog.destroy()
                    cargar_productos()
                else:
                    messagebox.showerror("Error", msg)

            ttk.Button(scrollable_form, text="Actualizar", command=guardar,
                      style='Accent.TButton').grid(row=len(fields), column=0, columnspan=2, pady=20)

        def eliminar_producto():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return

            item = tree.item(selected[0])
            producto_id = item["values"][0]
            producto_nombre = item["values"][1]

            if messagebox.askyesno("Confirmar", f"Eliminar producto: {producto_nombre}?"):
                success, msg = self.api.eliminar_producto(producto_id)
                if success:
                    messagebox.showinfo("Exito", "Producto eliminado")
                    cargar_productos()
                else:
                    messagebox.showerror("Error", msg)

        def buscar_por_id():
            dialog = tk.Toplevel(self.root)
            dialog.title("Buscar Producto")
            dialog.geometry("400x200")
            dialog.configure(bg=COLORS['bg_secondary'])
            dialog.transient(self.root)

            ttk.Label(dialog, text="Buscar Producto por ID",
                     font=('Segoe UI', 14, 'bold'),
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=20)

            ttk.Label(dialog, text="ID del Producto:",
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=10)

            id_entry = ttk.Entry(dialog, width=20, style='Dark.TEntry')
            id_entry.pack(pady=10)
            id_entry.focus()

            def buscar():
                producto_id = id_entry.get().strip()
                if not producto_id:
                    messagebox.showerror("Error", "Ingrese un ID")
                    return

                success, producto = self.api.get_producto(producto_id)
                if success:
                    details = json.dumps(producto, indent=2, ensure_ascii=False)

                    result_dialog = tk.Toplevel(self.root)
                    result_dialog.title(f"Producto ID: {producto_id}")
                    result_dialog.geometry("700x500")
                    result_dialog.configure(bg=COLORS['bg'])

                    text = scrolledtext.ScrolledText(result_dialog, wrap=tk.WORD,
                                                    bg=COLORS['bg_secondary'],
                                                    fg=COLORS['fg'],
                                                    font=('Consolas', 10))
                    text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                    text.insert(tk.END, details)
                    text.config(state=tk.DISABLED)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Producto no encontrado")

            id_entry.bind('<Return>', lambda e: buscar())

            ttk.Button(dialog, text="Buscar", command=buscar,
                      style='Accent.TButton').pack(pady=10)

''')
            # Ahora agregar la línea original
            nuevas_lineas.append(linea)
            i += 1
            continue

        # Continuar con el resto de líneas
        nuevas_lineas.append(linea)
        i += 1

    # Escribir el archivo modificado
    with open(archivo_original, 'w', encoding='utf-8') as f:
        f.writelines(nuevas_lineas)

    print(f"✓ Cambios aplicados exitosamente!")
    print(f"✓ Backup guardado en: {archivo_backup}")
    print(f"\nPor favor, ejecuta main.py para probar los cambios.")
    print(f"Si algo sale mal, puedes restaurar el backup con:")
    print(f"  copy {archivo_backup} main.py")

if __name__ == "__main__":
    print("=" * 60)
    print("APLICADOR AUTOMÁTICO DE CAMBIOS PARA main.py")
    print("=" * 60)
    print()

    if not os.path.exists('main.py'):
        print("ERROR: No se encontró el archivo main.py en el directorio actual")
        print(f"Directorio actual: {os.getcwd()}")
        exit(1)

    respuesta = input("¿Deseas continuar? (s/n): ").strip().lower()

    if respuesta == 's':
        aplicar_cambios()
    else:
        print("Operación cancelada.")

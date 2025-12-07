#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este script genera un nuevo main.py con TODAS las funcionalidades requeridas
"""

def generar_main_completo():
    # Leer el archivo actual
    with open('main.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nueva lista de líneas con modificaciones
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # =========================================================================
        # MODIFICACIÓN 1: CRUD de Productos en CRM (después de ver_detalles)
        # Buscar la sección de botones en setup_crm_productos_tab
        # =========================================================================
        if 'def setup_crm_productos_tab(self, parent):' in line:
            # Copiar todo hasta llegar a btn_frame
            new_lines.append(line)
            i += 1

            # Copiar hasta encontrar la línea de btn_frame
            while i < len(lines):
                new_lines.append(lines[i])

                # Cuando encontramos ver_detalles, agregamos las nuevas funciones después
                if 'def ver_detalles():' in lines[i]:
                    # Copiar toda la función ver_detalles
                    indent_count = 1
                    i += 1
                    while i < len(lines) and indent_count > 0:
                        new_lines.append(lines[i])
                        if lines[i].strip().startswith('def ') and lines[i][0] != ' ':
                            break
                        if lines[i].strip().startswith('def ') and '        def ' in lines[i]:
                            indent_count += 1
                        if 'btn_frame = ttk.Frame(frame' in lines[i]:
                            break
                        i += 1

                    # Insertar las nuevas funciones CRUD antes de btn_frame
                    new_lines.append('''
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
                    break

                i += 1

            continue

        new_lines.append(line)
        i += 1

    # Escribir el nuevo archivo
    with open('main_modificado.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print("Archivo main_modificado.py generado exitosamente!")
    print("Por favor, revíselo antes de reemplazar main.py")

if __name__ == "__main__":
    generar_main_completo()

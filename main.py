import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from api_client import APIClient
import json

# Colores del tema oscuro profesional
COLORS = {
    'bg': '#1e1e1e',
    'bg_secondary': '#2d2d2d',
    'bg_tertiary': '#3d3d3d',
    'fg': '#ffffff',
    'fg_secondary': '#b0b0b0',
    'accent': '#007acc',
    'accent_hover': '#005a9e',
    'success': '#4caf50',
    'error': '#f44336',
    'warning': '#ff9800',
    'border': '#404040'
}

class ECommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce XTART")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['bg'])

        self.api = APIClient()
        self.current_user = None
        self.current_cliente_id = None
        self.user_type = None

        self.setup_styles()
        self.show_login_page()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Frame styles
        style.configure('Dark.TFrame', background=COLORS['bg'])
        style.configure('Card.TFrame', background=COLORS['bg_secondary'], borderwidth=1, relief='solid')

        # Label styles
        style.configure('Dark.TLabel', background=COLORS['bg'], foreground=COLORS['fg'], font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=COLORS['bg'], foreground=COLORS['fg'], font=('Segoe UI', 28, 'bold'))
        style.configure('Subtitle.TLabel', background=COLORS['bg'], foreground=COLORS['fg_secondary'], font=('Segoe UI', 12))
        style.configure('Header.TLabel', background=COLORS['bg_secondary'], foreground=COLORS['fg'], font=('Segoe UI', 16, 'bold'))

        # Button styles
        style.configure('Accent.TButton',
                       background=COLORS['accent'],
                       foreground=COLORS['fg'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        style.map('Accent.TButton',
                 background=[('active', COLORS['accent_hover'])],
                 foreground=[('active', COLORS['fg'])])

        # Entry style
        style.configure('Dark.TEntry',
                       fieldbackground=COLORS['bg_tertiary'],
                       foreground=COLORS['fg'],
                       borderwidth=1,
                       insertcolor=COLORS['fg'])

        # Notebook style
        style.configure('Dark.TNotebook', background=COLORS['bg'], borderwidth=0)
        style.configure('Dark.TNotebook.Tab',
                       background=COLORS['bg_secondary'],
                       foreground=COLORS['fg'],
                       padding=[20, 10],
                       borderwidth=0)
        style.map('Dark.TNotebook.Tab',
                 background=[('selected', COLORS['accent'])],
                 foreground=[('selected', COLORS['fg'])])

        # Treeview style
        style.configure('Dark.Treeview',
                       background=COLORS['bg_secondary'],
                       foreground=COLORS['fg'],
                       fieldbackground=COLORS['bg_secondary'],
                       borderwidth=0)
        style.configure('Dark.Treeview.Heading',
                       background=COLORS['bg_tertiary'],
                       foreground=COLORS['fg'],
                       borderwidth=1)
        style.map('Dark.Treeview',
                 background=[('selected', COLORS['accent'])],
                 foreground=[('selected', COLORS['fg'])])

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_page(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Logo/Title
        ttk.Label(main_frame, text="XTART", style='Title.TLabel').pack(pady=(0, 10))
        ttk.Label(main_frame, text="E-Commerce Platform", style='Subtitle.TLabel').pack(pady=(0, 40))

        # Login Card
        card = ttk.Frame(main_frame, style='Card.TFrame', padding=40)
        card.pack()

        ttk.Label(card, text="Iniciar Sesión",
                 font=('Segoe UI', 18, 'bold'),
                 background=COLORS['bg_secondary'],
                 foreground=COLORS['fg']).grid(row=0, column=0, columnspan=2, pady=(0, 30))

        ttk.Label(card, text="Email:",
                 background=COLORS['bg_secondary'],
                 foreground=COLORS['fg']).grid(row=1, column=0, sticky=tk.W, pady=10)
        email_entry = ttk.Entry(card, width=35, style='Dark.TEntry')
        email_entry.grid(row=1, column=1, pady=10, padx=(10, 0))

        ttk.Label(card, text="Contraseña:",
                 background=COLORS['bg_secondary'],
                 foreground=COLORS['fg']).grid(row=2, column=0, sticky=tk.W, pady=10)
        password_entry = ttk.Entry(card, show="●", width=35, style='Dark.TEntry')
        password_entry.grid(row=2, column=1, pady=10, padx=(10, 0))

        def login():
            email = email_entry.get().strip()
            password = password_entry.get()

            if not email or not password:
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            # Intentar login como cliente
            success_cliente, data_cliente = self.api.login_cliente(email, password)
            if success_cliente:
                self.current_user = data_cliente
                self.user_type = "CLIENTE"

                # Obtener ID del cliente
                success, clientes = self.api.get_clientes()
                if success:
                    for cliente in clientes:
                        if cliente.get("email") == email:
                            self.current_cliente_id = cliente.get("idCliente")
                            break

                messagebox.showinfo("Bienvenido", f"Acceso concedido como Cliente")
                self.show_cliente_interface()
                return

            # Intentar login como empleado
            success_empleado, data_empleado = self.api.login_empleado(email, password)
            if success_empleado:
                self.current_user = data_empleado
                self.user_type = "EMPLEADO"
                messagebox.showinfo("Bienvenido", f"Acceso concedido como Empleado")
                self.show_empleado_interface()
                return

            # Si ninguno funcionó
            messagebox.showerror("Error", "Credenciales incorrectas")

        def go_to_register():
            self.show_registro_page()

        def go_to_register_empleado():
            self.show_registro_empleado_page()

        # Botones
        btn_frame = ttk.Frame(card, style='Card.TFrame')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(30, 10))

        login_btn = ttk.Button(btn_frame, text="Iniciar Sesión", command=login,
                              style='Accent.TButton', width=20)
        login_btn.pack(pady=5)


        # Bind Enter key
        password_entry.bind('<Return>', lambda _: login())
        email_entry.focus()

    def show_registro_page(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(main_frame, text="Crear Cuenta", style='Title.TLabel').pack(pady=(0, 30))

        card = ttk.Frame(main_frame, style='Card.TFrame', padding=40)
        card.pack()

        fields = [
            ("Nombre:", "nombre"),
            ("Apellidos:", "apellidos"),
            ("Email:", "email"),
            ("Dirección:", "direccion"),
            ("País:", "pais"),
            ("Contraseña:", "password"),
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(card, text=label, background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            entry = ttk.Entry(card, width=35, style='Dark.TEntry',
                            show="●" if key == "password" else "")
            entry.grid(row=i, column=1, pady=8)
            entries[key] = entry

        def registrar():
            data = {key: entry.get().strip() for key, entry in entries.items()}

            if not all(data.values()):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            success, msg = self.api.registro_cliente(**data)
            if success:
                messagebox.showinfo("Éxito", "Cuenta creada exitosamente")
                self.show_login_page()
            else:
                messagebox.showerror("Error", f"Error en registro: {msg}")

        btn_frame = ttk.Frame(card, style='Card.TFrame')
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=(20, 0))

        ttk.Button(btn_frame, text="Crear Cuenta", command=registrar,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Volver", command=self.show_login_page,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)

    def show_registro_cliente_modal(self, callback=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Cliente")
        dialog.geometry("500x600")
        dialog.configure(bg=COLORS['bg_secondary'])
        
        ttk.Label(dialog, text="Registrar Cliente", 
                 font=('Segoe UI', 16, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['fg']).pack(pady=20)
        
        form_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
        form_frame.pack(padx=20, pady=10)
        
        fields = [
            ("Nombre:", "nombre"),
            ("Apellidos:", "apellidos"),
            ("Email:", "email"),
            ("Dirección:", "direccion"),
            ("País:", "pais"),
            ("Contraseña:", "password")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(form_frame, text=label, bg=COLORS['bg_secondary'], fg=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame, width=30, style='Dark.TEntry')
            if key == "password":
                entry.config(show="*")
            entry.grid(row=i, column=1, pady=5)
            entries[key] = entry
            
        def guardar():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            if not all(data.values()):
                messagebox.showerror("Error", "Complete todos los campos")
                return
                
            success, msg = self.api.registro_cliente(
                data['nombre'], data['apellidos'], data['email'], 
                data['direccion'], data['pais'], data['password']
            )
            
            if success:
                messagebox.showinfo("Exito", "Cliente registrado")
                dialog.destroy()
                if callback:
                    callback()
            else:
                messagebox.showerror("Error", msg)
        
        ttk.Button(form_frame, text="Registrar", command=guardar, style='Accent.TButton').grid(row=len(fields), column=0, columnspan=2, pady=20)

    def show_registro_empleado_page(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(main_frame, text="Crear Empleado [TEMPORAL]",
                 font=('Segoe UI', 20, 'bold'),
                 background=COLORS['bg'],
                 foreground=COLORS['warning']).pack(pady=(0, 30))

        card = ttk.Frame(main_frame, style='Card.TFrame', padding=40)
        card.pack()

        fields = [
            ("Nombre:", "nombre"),
            ("Apellidos:", "apellidos"),
            ("Email:", "email"),
            ("Teléfono:", "telefono"),
            ("Contraseña:", "password"),
            ("Rol (ADMIN/EMPLEADO):", "rol"),
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(card, text=label, background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            entry = ttk.Entry(card, width=35, style='Dark.TEntry',
                            show="●" if key == "password" else "")
            entry.grid(row=i, column=1, pady=8)
            entries[key] = entry

            # Valor por defecto para rol
            if key == "rol":
                entry.insert(0, "EMPLEADO")

        def registrar_empleado():
            data = {key: entry.get().strip() for key, entry in entries.items()}

            if not all(data.values()):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            # Validar rol
            if data['rol'].upper() not in ['ADMIN', 'EMPLEADO']:
                messagebox.showerror("Error", "Rol debe ser ADMIN o EMPLEADO")
                return

            # Primero crear un cliente temporal para obtener el hash correcto
            import random
            import string
            temp_email = ''.join(random.choices(string.ascii_lowercase, k=10)) + "@temp.com"

            try:
                import requests
                response = requests.post("http://localhost:8080/proyecto/api/clientes/registro", json={
                    "nombre": "Temp",
                    "apellidos": "User",
                    "email": temp_email,
                    "direccion": "Temp",
                    "pais": "Spain",
                    "password": data['password']
                })

                if response.status_code == 200:
                    temp_user = response.json()
                    password_hash = temp_user.get('contraseña')

                    # Ahora insertar el empleado con el hash correcto
                    import subprocess
                    sql_command = f"""
                    INSERT INTO empleado (nombre, apellidos, email, telefono, contraseña, rol, estado, estatus, fecha_contrato, intentos_login)
                    VALUES ('{data['nombre']}', '{data['apellidos']}', '{data['email']}', '{data['telefono']}', '{password_hash}', '{data['rol'].upper()}', 'ACTIVO', 'A', CURDATE(), 0);
                    """

                    result = subprocess.run([
                        "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe",
                        "-u", "root", "-padmin", "proyecto_1t",
                        "-e", sql_command
                    ], capture_output=True, text=True)

                    if result.returncode == 0:
                        # Eliminar el cliente temporal
                        subprocess.run([
                            "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe",
                            "-u", "root", "-padmin", "proyecto_1t",
                            "-e", f"DELETE FROM cliente WHERE email = '{temp_email}';"
                        ], capture_output=True, text=True)

                        messagebox.showinfo("Éxito", f"Empleado {data['rol']} creado exitosamente!\n\nEmail: {data['email']}\nPassword: {data['password']}")
                        self.show_login_page()
                    else:
                        messagebox.showerror("Error", f"Error al crear empleado en BD: {result.stderr}")
                else:
                    messagebox.showerror("Error", "No se pudo generar el hash de contraseña")

            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

        btn_frame = ttk.Frame(card, style='Card.TFrame')
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=(20, 0))

        ttk.Button(btn_frame, text="Crear Empleado", command=registrar_empleado,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Volver", command=self.show_login_page,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)

    def show_cliente_interface(self):
        self.clear_window()

        # Top bar
        top_bar = ttk.Frame(self.root, style='Dark.TFrame', padding=15)
        top_bar.pack(fill=tk.X)

        ttk.Label(top_bar, text="XTART E-Commerce",
                 font=('Segoe UI', 18, 'bold'),
                 background=COLORS['bg'],
                 foreground=COLORS['accent']).pack(side=tk.LEFT)

        logout_btn = ttk.Button(top_bar, text="Cerrar Sesión",
                               command=self.logout_cliente,
                               style='Accent.TButton')
        logout_btn.pack(side=tk.RIGHT)

        # Notebook
        notebook = ttk.Notebook(self.root, style='Dark.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        productos_tab = ttk.Frame(notebook, style='Dark.TFrame')
        carrito_tab = ttk.Frame(notebook, style='Dark.TFrame')
        facturas_tab = ttk.Frame(notebook, style='Dark.TFrame')

        notebook.add(productos_tab, text="🛍️ Productos")
        notebook.add(carrito_tab, text="🛒 Mi Carrito")
        notebook.add(facturas_tab, text="📄 Mis Facturas")

        self.setup_productos_tab(productos_tab)
        self.setup_carrito_tab(carrito_tab)
        self.setup_facturas_tab(facturas_tab)

    def setup_productos_tab(self, parent):
        main_container = ttk.Frame(parent, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header con buscador
        header = ttk.Frame(main_container, style='Dark.TFrame', padding=20)
        header.pack(fill=tk.X)

        ttk.Label(header, text="🛍️ Tienda Online",
                 font=('Segoe UI', 20, 'bold'),
                 background=COLORS['bg'],
                 foreground=COLORS['fg']).pack(side=tk.LEFT)

        # Canvas con scrollbar para los productos
        canvas_frame = ttk.Frame(main_container, style='Dark.TFrame')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(canvas_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind scroll del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        def crear_producto_card(container, producto, row, col):
            """Crea una card de producto estilo web"""
            card = tk.Frame(container, bg=COLORS['bg_secondary'],
                           relief='raised', borderwidth=2)
            card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')

            # Imagen placeholder
            img_frame = tk.Frame(card, bg=COLORS['bg_tertiary'], height=150)
            img_frame.pack(fill=tk.X, padx=10, pady=10)

            img_label = tk.Label(img_frame, text="📦",
                                font=('Segoe UI', 48),
                                bg=COLORS['bg_tertiary'],
                                fg=COLORS['fg_secondary'])
            img_label.pack(expand=True)

            # Info del producto
            info_frame = tk.Frame(card, bg=COLORS['bg_secondary'])
            info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

            # Nombre
            nombre = tk.Label(info_frame,
                            text=producto.get('nombre', 'Producto')[:30],
                            font=('Segoe UI', 12, 'bold'),
                            bg=COLORS['bg_secondary'],
                            fg=COLORS['fg'],
                            wraplength=200)
            nombre.pack(anchor='w', pady=(0, 5))

            # Descripción
            desc = tk.Label(info_frame,
                           text=producto.get('descripcion', '')[:60] + '...',
                           font=('Segoe UI', 9),
                           bg=COLORS['bg_secondary'],
                           fg=COLORS['fg_secondary'],
                           wraplength=200,
                           justify='left')
            desc.pack(anchor='w', pady=(0, 10))

            # Precio y stock
            precio_frame = tk.Frame(info_frame, bg=COLORS['bg_secondary'])
            precio_frame.pack(fill=tk.X, pady=(0, 10))

            precio = tk.Label(precio_frame,
                            text=f"${producto.get('precioLista', 0):.2f}",
                            font=('Segoe UI', 16, 'bold'),
                            bg=COLORS['bg_secondary'],
                            fg=COLORS['success'])
            precio.pack(side=tk.LEFT)

            stock = tk.Label(precio_frame,
                           text=f"Stock: {producto.get('stockActual', 0)}",
                           font=('Segoe UI', 9),
                           bg=COLORS['bg_secondary'],
                           fg=COLORS['fg_secondary'])
            stock.pack(side=tk.RIGHT)

            # Botón agregar al carrito
            def agregar():
                dialog = tk.Toplevel(self.root)
                dialog.title("Agregar al Carrito")
                dialog.geometry("400x250")
                dialog.configure(bg=COLORS['bg_secondary'])
                dialog.transient(self.root)
                dialog.grab_set()

                # Centrar dialog
                dialog.update_idletasks()
                x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
                y = (dialog.winfo_screenheight() // 2) - (250 // 2)
                dialog.geometry(f'400x250+{x}+{y}')

                tk.Label(dialog,
                        text=producto.get('nombre', 'Producto'),
                        font=('Segoe UI', 14, 'bold'),
                        bg=COLORS['bg_secondary'],
                        fg=COLORS['fg']).pack(pady=20)

                tk.Label(dialog,
                        text="Cantidad:",
                        font=('Segoe UI', 11),
                        bg=COLORS['bg_secondary'],
                        fg=COLORS['fg']).pack(pady=10)

                cantidad_entry = ttk.Entry(dialog, style='Dark.TEntry',
                                         font=('Segoe UI', 12),
                                         width=10,
                                         justify='center')
                cantidad_entry.pack(pady=10)
                cantidad_entry.insert(0, "1")
                cantidad_entry.focus()

                def confirmar():
                    try:
                        cantidad = int(cantidad_entry.get())
                        if cantidad <= 0:
                            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                            return

                        if cantidad > producto.get('stockActual', 0):
                            messagebox.showerror("Error", "No hay suficiente stock")
                            return

                        if self.current_cliente_id:
                            success, msg = self.api.agregar_al_carrito(
                                self.current_cliente_id,
                                producto.get('idProducto'),
                                cantidad)
                            if success:
                                messagebox.showinfo("¡Agregado!",
                                                  f"✓ {producto.get('nombre')} agregado al carrito")
                                dialog.destroy()
                            else:
                                messagebox.showerror("Error", msg)
                        else:
                            messagebox.showerror("Error", "No se pudo identificar el cliente")
                    except ValueError:
                        messagebox.showerror("Error", "Cantidad inválida")

                cantidad_entry.bind('<Return>', lambda e: confirmar())

                btn_frame = tk.Frame(dialog, bg=COLORS['bg_secondary'])
                btn_frame.pack(pady=20)

                ttk.Button(btn_frame, text="Agregar al Carrito",
                          command=confirmar,
                          style='Accent.TButton').pack(side=tk.LEFT, padx=5)
                ttk.Button(btn_frame, text="Cancelar",
                          command=dialog.destroy,
                          style='Accent.TButton').pack(side=tk.LEFT, padx=5)

            btn = tk.Button(card,
                          text="🛒 Agregar al Carrito",
                          command=agregar,
                          bg=COLORS['accent'],
                          fg=COLORS['fg'],
                          font=('Segoe UI', 10, 'bold'),
                          relief='flat',
                          cursor='hand2',
                          activebackground=COLORS['accent_hover'],
                          activeforeground=COLORS['fg'],
                          padx=20,
                          pady=10)
            btn.pack(fill=tk.X, padx=10, pady=(0, 10))

        def cargar_productos():
            # Limpiar productos existentes
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            success, productos = self.api.get_productos()
            if success and productos:
                # Configurar grid
                cols = 3  # 3 productos por fila
                for i in range(cols):
                    scrollable_frame.columnconfigure(i, weight=1, minsize=280)

                # Crear cards
                for idx, prod in enumerate(productos):
                    row = idx // cols
                    col = idx % cols
                    crear_producto_card(scrollable_frame, prod, row, col)
            else:
                tk.Label(scrollable_frame,
                        text="No hay productos disponibles",
                        font=('Segoe UI', 14),
                        bg=COLORS['bg'],
                        fg=COLORS['fg_secondary']).pack(pady=50)

        # Botón actualizar en la parte inferior
        bottom_bar = ttk.Frame(main_container, style='Dark.TFrame', padding=10)
        bottom_bar.pack(fill=tk.X)

        ttk.Button(bottom_bar, text="🔄 Actualizar Productos",
                  command=cargar_productos,
                  style='Accent.TButton').pack()

        cargar_productos()

    def show_registro_cliente_modal(self, callback=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Cliente")
        dialog.geometry("500x700")
        dialog.configure(bg=COLORS['bg'])
        dialog.transient(self.root)

        ttk.Label(dialog, text="Registro de Cliente",
                 font=('Segoe UI', 16, 'bold'),
                 background=COLORS['bg'],
                 foreground=COLORS['fg']).pack(pady=20)

        form_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        fields = [
            ("Nombre:", "nombre"),
            ("Apellidos:", "apellidos"),
            ("Email:", "email"),
            ("Contraseña:", "password", True),
            ("Dirección:", "direccion"),
            ("País:", "pais")
        ]

        entries = {}
        for i, field in enumerate(fields):
            label_text = field[0]
            key = field[1]
            is_password = len(field) > 2 and field[2]

            ttk.Label(form_frame, text=label_text,
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, padx=10, pady=8)
            
            entry = ttk.Entry(form_frame, width=30, style='Dark.TEntry', show="*" if is_password else "")
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries[key] = entry

        def registrar():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            
            if not all(data.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            # Validar email simple
            if "@" not in data['email']:
                messagebox.showerror("Error", "Email inválido")
                return

            success, msg = self.api.registro_cliente(data)
            if success:
                messagebox.showinfo("Éxito", "Cliente registrado correctamente")
                dialog.destroy()
                if callback:
                    callback()
            else:
                messagebox.showerror("Error", msg)

        ttk.Button(form_frame, text="Registrar", command=registrar,
                  style='Accent.TButton').grid(row=len(fields), column=0, columnspan=2, pady=20)

    def setup_carrito_tab(self, parent):
        main_container = ttk.Frame(parent, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Frame(main_container, style='Dark.TFrame', padding=20)
        header.pack(fill=tk.X)

        ttk.Label(header, text="🛒 Mi Carrito de Compras",
                 font=('Segoe UI', 20, 'bold'),
                 background=COLORS['bg'],
                 foreground=COLORS['fg']).pack(side=tk.LEFT)

        # Canvas con scrollbar
        canvas_frame = ttk.Frame(main_container, style='Dark.TFrame')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(canvas_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind scroll del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        def crear_item_card(container, item, cargar_callback):
            """Crea una card para un item del carrito"""
            card = tk.Frame(container, bg=COLORS['bg_secondary'],
                           relief='raised', borderwidth=2)
            card.pack(fill=tk.X, padx=10, pady=10)

            # Layout horizontal
            content_frame = tk.Frame(card, bg=COLORS['bg_secondary'])
            content_frame.pack(fill=tk.X, padx=15, pady=15)

            # Imagen placeholder (izquierda)
            img_frame = tk.Frame(content_frame, bg=COLORS['bg_tertiary'],
                               width=80, height=80)
            img_frame.pack(side=tk.LEFT, padx=(0, 15))
            img_frame.pack_propagate(False)

            img_label = tk.Label(img_frame, text="📦",
                               font=('Segoe UI', 32),
                               bg=COLORS['bg_tertiary'],
                               fg=COLORS['fg_secondary'])
            img_label.pack(expand=True)

            # Info del producto (centro)
            info_frame = tk.Frame(content_frame, bg=COLORS['bg_secondary'])
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            producto = item.get("producto", {})
            nombre = tk.Label(info_frame,
                            text=producto.get('nombre', 'Producto'),
                            font=('Segoe UI', 14, 'bold'),
                            bg=COLORS['bg_secondary'],
                            fg=COLORS['fg'],
                            anchor='w')
            nombre.pack(fill=tk.X)

            cantidad_label = tk.Label(info_frame,
                                    text=f"Cantidad: {item.get('cantidad', 0)}",
                                    font=('Segoe UI', 10),
                                    bg=COLORS['bg_secondary'],
                                    fg=COLORS['fg_secondary'],
                                    anchor='w')
            cantidad_label.pack(fill=tk.X, pady=(5, 0))

            precio_unit_label = tk.Label(info_frame,
                                        text=f"Precio unitario: ${item.get('precioUnitario', 0):.2f}",
                                        font=('Segoe UI', 10),
                                        bg=COLORS['bg_secondary'],
                                        fg=COLORS['fg_secondary'],
                                        anchor='w')
            precio_unit_label.pack(fill=tk.X, pady=(2, 0))

            # Precio y botón (derecha)
            right_frame = tk.Frame(content_frame, bg=COLORS['bg_secondary'])
            right_frame.pack(side=tk.RIGHT, padx=(15, 0))

            total_item = item.get("total", 0)
            precio_label = tk.Label(right_frame,
                                   text=f"${total_item:.2f}",
                                   font=('Segoe UI', 18, 'bold'),
                                   bg=COLORS['bg_secondary'],
                                   fg=COLORS['success'])
            precio_label.pack(pady=(0, 10))

            def eliminar():
                producto_id = producto.get("idProducto")
                if messagebox.askyesno("Confirmar",
                                      f"¿Eliminar {producto.get('nombre', 'este producto')} del carrito?"):
                    success, msg = self.api.eliminar_del_carrito(
                        self.current_cliente_id, producto_id)
                    if success:
                        messagebox.showinfo("Éxito", "Producto eliminado")
                        cargar_callback()
                    else:
                        messagebox.showerror("Error", msg)

            btn_eliminar = tk.Button(right_frame,
                                    text="🗑️ Eliminar",
                                    command=eliminar,
                                    bg=COLORS['error'],
                                    fg=COLORS['fg'],
                                    font=('Segoe UI', 9, 'bold'),
                                    relief='flat',
                                    cursor='hand2',
                                    activebackground='#c62828',
                                    activeforeground=COLORS['fg'],
                                    padx=15,
                                    pady=8)
            btn_eliminar.pack()

        def cargar_carrito():
            # Limpiar items existentes
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            if not self.current_cliente_id:
                messagebox.showerror("Error", "No se pudo identificar el cliente")
                return

            success, carrito = self.api.ver_carrito(self.current_cliente_id)

            if success and carrito:
                total = 0
                for item in carrito:
                    crear_item_card(scrollable_frame, item, cargar_carrito)
                    total += item.get("total", 0)

                # Card de resumen
                resumen_card = tk.Frame(scrollable_frame, bg=COLORS['accent'],
                                      relief='raised', borderwidth=3)
                resumen_card.pack(fill=tk.X, padx=10, pady=20)

                resumen_content = tk.Frame(resumen_card, bg=COLORS['accent'])
                resumen_content.pack(fill=tk.X, padx=20, pady=20)

                tk.Label(resumen_content,
                        text="TOTAL A PAGAR",
                        font=('Segoe UI', 14, 'bold'),
                        bg=COLORS['accent'],
                        fg=COLORS['fg']).pack()

                tk.Label(resumen_content,
                        text=f"${total:.2f}",
                        font=('Segoe UI', 28, 'bold'),
                        bg=COLORS['accent'],
                        fg=COLORS['fg']).pack(pady=(5, 15))

                def generar_factura():
                    if not self.current_cliente_id:
                        messagebox.showerror("Error", "No se pudo identificar el cliente")
                        return

                    carrito_map = {}
                    total_factura = 0
                    for item in carrito:
                        producto_id = str(item.get("producto", {}).get("idProducto", ""))
                        cantidad = item.get("cantidad", 0)
                        carrito_map[producto_id] = cantidad
                        total_factura += item.get("total", 0)

                    success, msg = self.api.crear_factura(self.current_cliente_id,
                                                         carrito_map, total_factura)
                    if success:
                        messagebox.showinfo("¡Compra Exitosa!",
                                          "✓ Factura generada correctamente\n\nRevisa tus facturas en la pestaña 'Mis Facturas'")
                        # Limpiar UI del carrito
                        for widget in scrollable_frame.winfo_children():
                            widget.destroy()
                        # Mostrar mensaje de vacío
                        empty_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
                        empty_frame.pack(fill=tk.BOTH, expand=True, pady=100)
                        tk.Label(empty_frame, text="Tu carrito está vacío", font=('Segoe UI', 18, 'bold'), bg=COLORS['bg'], fg=COLORS['fg']).pack(pady=(20, 10))
                        # Actualizar total
                        # lbl_total.config(text="$0.00") # lbl_total is not defined here, we just cleared the frame so it's fine.
                        cargar_carrito() # Reload to show empty state cleanly
                    else:
                        messagebox.showerror("Error", msg)

                btn_factura = tk.Button(resumen_content,
                                       text="💳 PROCEDER AL PAGO",
                                       command=generar_factura,
                                       bg=COLORS['success'],
                                       fg=COLORS['fg'],
                                       font=('Segoe UI', 12, 'bold'),
                                       relief='flat',
                                       cursor='hand2',
                                       activebackground='#2e7d32',
                                       activeforeground=COLORS['fg'],
                                       padx=30,
                                       pady=15)
                btn_factura.pack()

            else:
                # Carrito vacío
                empty_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
                empty_frame.pack(fill=tk.BOTH, expand=True, pady=100)

                tk.Label(empty_frame,
                        text="🛒",
                        font=('Segoe UI', 64),
                        bg=COLORS['bg'],
                        fg=COLORS['fg_secondary']).pack()

                tk.Label(empty_frame,
                        text="Tu carrito está vacío",
                        font=('Segoe UI', 18, 'bold'),
                        bg=COLORS['bg'],
                        fg=COLORS['fg']).pack(pady=(20, 10))

                tk.Label(empty_frame,
                        text="¡Agrega productos desde la tienda!",
                        font=('Segoe UI', 12),
                        bg=COLORS['bg'],
                        fg=COLORS['fg_secondary']).pack()

        # Botón actualizar en la parte inferior
        bottom_bar = ttk.Frame(main_container, style='Dark.TFrame', padding=10)
        bottom_bar.pack(fill=tk.X)

        ttk.Button(bottom_bar, text="🔄 Actualizar Carrito",
                  command=cargar_carrito,
                  style='Accent.TButton').pack()

        cargar_carrito()

    def setup_facturas_tab(self, parent):
        main_container = ttk.Frame(parent, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Frame(main_container, style='Dark.TFrame', padding=20)
        header.pack(fill=tk.X)

        ttk.Label(header, text="📄 Mis Facturas",
                 font=('Segoe UI', 20, 'bold'),
                 background=COLORS['bg'],
                 foreground=COLORS['fg']).pack(side=tk.LEFT)

        # Canvas con scrollbar
        canvas_frame = ttk.Frame(main_container, style='Dark.TFrame')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(canvas_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind scroll del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        def crear_factura_card(container, factura):
            """Crea una card de factura estilo recibo"""
            card = tk.Frame(container, bg=COLORS['bg_secondary'],
                           relief='raised', borderwidth=2)
            card.pack(fill=tk.X, padx=10, pady=15)

            # Header de la factura
            header_frame = tk.Frame(card, bg=COLORS['accent'])
            header_frame.pack(fill=tk.X)

            header_content = tk.Frame(header_frame, bg=COLORS['accent'])
            header_content.pack(fill=tk.X, padx=20, pady=15)

            tk.Label(header_content,
                    text="🧾 FACTURA",
                    font=('Segoe UI', 12, 'bold'),
                    bg=COLORS['accent'],
                    fg=COLORS['fg']).pack(side=tk.LEFT)

            tk.Label(header_content,
                    text=f"#{factura.get('idFactura', 'N/A')}",
                    font=('Segoe UI', 12, 'bold'),
                    bg=COLORS['accent'],
                    fg=COLORS['fg']).pack(side=tk.RIGHT)

            # Contenido de la factura
            content_frame = tk.Frame(card, bg=COLORS['bg_secondary'])
            content_frame.pack(fill=tk.X, padx=20, pady=20)

            # Fecha
            fecha_frame = tk.Frame(content_frame, bg=COLORS['bg_secondary'])
            fecha_frame.pack(fill=tk.X, pady=(0, 15))

            tk.Label(fecha_frame,
                    text="📅 Fecha:",
                    font=('Segoe UI', 10, 'bold'),
                    bg=COLORS['bg_secondary'],
                    fg=COLORS['fg_secondary']).pack(side=tk.LEFT)

            fecha_str = factura.get("fecha", "")[:19]
            tk.Label(fecha_frame,
                    text=fecha_str,
                    font=('Segoe UI', 10),
                    bg=COLORS['bg_secondary'],
                    fg=COLORS['fg']).pack(side=tk.LEFT, padx=(10, 0))

            # Separador
            separator = tk.Frame(content_frame, bg=COLORS['bg_tertiary'], height=1)
            separator.pack(fill=tk.X, pady=15)

            # Detalles de productos
            detalles = factura.get("detalles", [])
            if detalles:
                tk.Label(content_frame,
                        text="Artículos:",
                        font=('Segoe UI', 10, 'bold'),
                        bg=COLORS['bg_secondary'],
                        fg=COLORS['fg']).pack(anchor='w', pady=(0, 10))

                for detalle in detalles:
                    item_frame = tk.Frame(content_frame, bg=COLORS['bg_tertiary'])
                    item_frame.pack(fill=tk.X, pady=2)

                    producto = detalle.get("producto", {})
                    cantidad = detalle.get("cantidad", 0)
                    precio = detalle.get("precioUnitario", 0)

                    # Nombre y cantidad
                    left_frame = tk.Frame(item_frame, bg=COLORS['bg_tertiary'])
                    left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)

                    tk.Label(left_frame,
                            text=f"• {producto.get('nombre', 'Producto')}",
                            font=('Segoe UI', 9),
                            bg=COLORS['bg_tertiary'],
                            fg=COLORS['fg'],
                            anchor='w').pack(side=tk.LEFT)

                    tk.Label(left_frame,
                            text=f"(x{cantidad})",
                            font=('Segoe UI', 9),
                            bg=COLORS['bg_tertiary'],
                            fg=COLORS['fg_secondary'],
                            anchor='w').pack(side=tk.LEFT, padx=(5, 0))

                    # Precio
                    tk.Label(item_frame,
                            text=f"${precio * cantidad:.2f}",
                            font=('Segoe UI', 9, 'bold'),
                            bg=COLORS['bg_tertiary'],
                            fg=COLORS['fg'],
                            anchor='e').pack(side=tk.RIGHT, padx=10)

            # Footer con total
            footer_frame = tk.Frame(card, bg=COLORS['success'])
            footer_frame.pack(fill=tk.X)

            footer_content = tk.Frame(footer_frame, bg=COLORS['success'])
            footer_content.pack(fill=tk.X, padx=20, pady=15)

            tk.Label(footer_content,
                    text="TOTAL PAGADO",
                    font=('Segoe UI', 11, 'bold'),
                    bg=COLORS['success'],
                    fg=COLORS['fg']).pack(side=tk.LEFT)

            tk.Label(footer_content,
                    text=f"${factura.get('total', 0):.2f}",
                    font=('Segoe UI', 18, 'bold'),
                    bg=COLORS['success'],
                    fg=COLORS['fg']).pack(side=tk.RIGHT)

        def cargar_facturas():
            # Limpiar facturas existentes
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            if not self.current_cliente_id:
                messagebox.showerror("Error", "No se pudo identificar el cliente")
                return

            success, facturas = self.api.get_facturas_cliente(self.current_cliente_id)

            if success and facturas:
                # Ordenar por fecha (más reciente primero)
                facturas_ordenadas = sorted(facturas,
                                           key=lambda f: f.get("fecha", ""),
                                           reverse=True)

                for factura in facturas_ordenadas:
                    crear_factura_card(scrollable_frame, factura)

            else:
                # Sin facturas
                empty_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
                empty_frame.pack(fill=tk.BOTH, expand=True, pady=100)

                tk.Label(empty_frame,
                        text="📄",
                        font=('Segoe UI', 64),
                        bg=COLORS['bg'],
                        fg=COLORS['fg_secondary']).pack()

                tk.Label(empty_frame,
                        text="No tienes facturas aún",
                        font=('Segoe UI', 18, 'bold'),
                        bg=COLORS['bg'],
                        fg=COLORS['fg']).pack(pady=(20, 10))

                tk.Label(empty_frame,
                        text="Tus compras aparecerán aquí",
                        font=('Segoe UI', 12),
                        bg=COLORS['bg'],
                        fg=COLORS['fg_secondary']).pack()

        # Botón actualizar en la parte inferior
        bottom_bar = ttk.Frame(main_container, style='Dark.TFrame', padding=10)
        bottom_bar.pack(fill=tk.X)

        ttk.Button(bottom_bar, text="🔄 Actualizar Facturas",
                  command=cargar_facturas,
                  style='Accent.TButton').pack()

        cargar_facturas()

    def show_empleado_interface(self):
        
        self.clear_window()

        # Top bar
        top_bar = ttk.Frame(self.root, style='Dark.TFrame', padding=15)
        top_bar.pack(fill=tk.X)

        ttk.Label(top_bar, text="XTART CRM",
                 font=('Segoe UI', 18, 'bold'),
                 background=COLORS['bg'],
                 foreground=COLORS['warning']).pack(side=tk.LEFT)

        ttk.Label(top_bar, text="Panel de Administración",
                 font=('Segoe UI', 10),
                 background=COLORS['bg'],
                 foreground=COLORS['fg_secondary']).pack(side=tk.LEFT, padx=(15, 0))

        logout_btn = ttk.Button(top_bar, text="Cerrar Sesión",
                               command=self.logout_empleado,
                               style='Accent.TButton')
        logout_btn.pack(side=tk.RIGHT)

        # Notebook
        notebook = ttk.Notebook(self.root, style='Dark.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        empleados_tab = ttk.Frame(notebook, style='Dark.TFrame')
        clientes_tab = ttk.Frame(notebook, style='Dark.TFrame')
        productos_tab = ttk.Frame(notebook, style='Dark.TFrame')
        facturas_tab = ttk.Frame(notebook, style='Dark.TFrame')
        proveedores_tab = ttk.Frame(notebook, style='Dark.TFrame')
        
        notebook.add(empleados_tab, text="Empleados")
        notebook.add(clientes_tab, text="Clientes")
        notebook.add(productos_tab, text="Productos")
        notebook.add(facturas_tab, text="Facturas")
        notebook.add(proveedores_tab, text="Proveedores")


        self.setup_crm_clientes_tab(clientes_tab)
        self.setup_crm_productos_tab(productos_tab)
        self.setup_crm_facturas_tab(facturas_tab)
        self.setup_crm_proveedores_tab(proveedores_tab)
        self.setup_crm_empleados_tab(empleados_tab)

    def show_registro_cliente_modal(self, callback=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Cliente")
        dialog.geometry("500x700")
        dialog.configure(bg=COLORS['bg'])
        dialog.transient(self.root)

        ttk.Label(dialog, text="Registro de Cliente",
                 font=('Segoe UI', 16, 'bold'),
                 background=COLORS['bg'],
                 foreground=COLORS['fg']).pack(pady=20)

        form_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        fields = [
            ("Nombre:", "nombre"),
            ("Apellidos:", "apellidos"),
            ("Email:", "email"),
            ("Contraseña:", "password", True),
            ("Dirección:", "direccion"),
            ("País:", "pais")
        ]

        entries = {}
        for i, field in enumerate(fields):
            label_text = field[0]
            key = field[1]
            is_password = len(field) > 2 and field[2]

            ttk.Label(form_frame, text=label_text,
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, padx=10, pady=8)
            
            entry = ttk.Entry(form_frame, width=30, style='Dark.TEntry', show="*" if is_password else "")
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries[key] = entry

        def registrar():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            
            if not all(data.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            # Validar email simple
            if "@" not in data['email']:
                messagebox.showerror("Error", "Email inválido")
                return

            success, msg = self.api.registro_cliente(**data)
            if success:
                messagebox.showinfo("Éxito", "Cliente registrado correctamente")
                dialog.destroy()
                if callback:
                    callback()
            else:
                messagebox.showerror("Error", msg)

        ttk.Button(form_frame, text="Registrar", command=registrar,
                  style='Accent.TButton').grid(row=len(fields), column=0, columnspan=2, pady=20)

    def setup_crm_clientes_tab(self, parent):
        frame = ttk.Frame(parent, style='Dark.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Gestión de Clientes", style='Header.TLabel').pack(pady=(0, 20))

        tree_frame = ttk.Frame(frame, style='Dark.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Nombre", "Apellidos", "Email", "Dirección", "País", "Estado", "Fecha Alta")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, style='Dark.Treeview')
        scrollbar.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)

        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_clientes():
            for item in tree.get_children():
                tree.delete(item)

            success, clientes = self.api.get_clientes()
            if success:
                for cliente in clientes:
                    tree.insert("", tk.END, values=(
                        cliente.get("idCliente", ""),
                        cliente.get("nombre", ""),
                        cliente.get("apellidos", ""),
                        cliente.get("email", ""),
                        cliente.get("direccion", ""),
                        cliente.get("pais", ""),
                        cliente.get("estado", ""),
                        cliente.get("fechaAlta", "")[:10] if cliente.get("fechaAlta") else ""
                    ))

        def ver_detalles():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un cliente")
                return

            item = tree.item(selected[0])
            cliente_id = item["values"][0]

            success, cliente = self.api.get_cliente(cliente_id)
            if success:
                details = f"""
ID: {cliente.get('idCliente')}
Nombre: {cliente.get('nombre')} {cliente.get('apellidos')}
Email: {cliente.get('email')}
Dirección: {cliente.get('direccion')}
País: {cliente.get('pais')}
Estado: {cliente.get('estado')}
Rol: {cliente.get('rolCliente')}
Fecha Alta: {cliente.get('fechaAlta')}
Intentos Login: {cliente.get('intentosLogin')}
                """
                messagebox.showinfo("Detalles del Cliente", details)
            else:
                messagebox.showerror("Error", "No se pudo cargar el cliente")

        def nuevo_cliente():
            self.show_registro_cliente_modal(callback=cargar_clientes)

        def eliminar_cliente():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un cliente")
                return

            item = tree.item(selected[0])
            cliente_id = item["values"][0]

            if messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
                success, msg = self.api.eliminar_cliente(cliente_id)
                if success:
                    messagebox.showinfo("Éxito", "Cliente eliminado")
                    cargar_clientes()
                else:
                    messagebox.showerror("Error", msg)

        def buscar_por_id():
            dialog = tk.Toplevel(self.root)
            dialog.title("Buscar Cliente por ID")
            dialog.geometry("400x200")
            dialog.configure(bg=COLORS['bg_secondary'])

            ttk.Label(dialog, text="Buscar Cliente por ID",
                     font=('Segoe UI', 14, 'bold'),
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=20)

            ttk.Label(dialog, text="ID del Cliente:",
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack()

            id_entry = ttk.Entry(dialog, width=30, style='Dark.TEntry')
            id_entry.pack(pady=10)

            def buscar():
                cliente_id = id_entry.get().strip()
                if not cliente_id:
                    messagebox.showerror("Error", "Ingrese un ID")
                    return

                success, cliente = self.api.get_cliente(cliente_id)
                if success and cliente:
                    details = f"""ID: {cliente.get('idCliente')}
Nombre: {cliente.get('nombre')} {cliente.get('apellidos')}
Email: {cliente.get('email')}
Dirección: {cliente.get('direccion')}
País: {cliente.get('pais')}
Estado: {cliente.get('estado')}"""
                    messagebox.showinfo("Cliente Encontrado", details)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Cliente no encontrado")

            ttk.Button(dialog, text="Buscar", command=buscar,
                      style='Accent.TButton').pack(pady=10)

        def actualizar_cliente():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un cliente")
                return

            item = tree.item(selected[0])
            cliente_id = item["values"][0]

            success, cliente = self.api.get_cliente(cliente_id)
            if not success:
                messagebox.showerror("Error", "No se pudo cargar el cliente")
                return

            dialog = tk.Toplevel(self.root)
            dialog.title("Actualizar Cliente")
            dialog.geometry("500x600")
            dialog.configure(bg=COLORS['bg_secondary'])
            dialog.transient(self.root)

            ttk.Label(dialog, text=f"Actualizar Cliente ID: {cliente_id}",
                     font=('Segoe UI', 16, 'bold'),
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=20)

            form_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
            form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            fields = [
                ("Nombre:", "nombre"),
                ("Apellidos:", "apellidos"),
                ("Email:", "email"),
                ("Dirección:", "direccion"),
                ("País:", "pais")
            ]

            entries = {}
            for i, (label, key) in enumerate(fields):
                ttk.Label(form_frame, text=label,
                         background=COLORS['bg_secondary'],
                         foreground=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, padx=10, pady=8)
                entry = ttk.Entry(form_frame, width=30, style='Dark.TEntry')
                entry.grid(row=i, column=1, padx=10, pady=8)
                entry.insert(0, str(cliente.get(key, "")))
                entries[key] = entry

            def guardar():
                data = {key: entry.get().strip() for key, entry in entries.items()}

                # Validar campos editables
                if not all(data.values()):
                    messagebox.showerror("Error", "Complete todos los campos")
                    return

                data['idCliente'] = cliente_id
                data['contraseña'] = cliente.get('contraseña', '')
                data['rolCliente'] = cliente.get('rolCliente') or 'REGISTRADO'
                data['estado'] = cliente.get('estado') or 'ACTIVO'

                success, msg = self.api.actualizar_cliente(data)
                if success:
                    messagebox.showinfo("Exito", "Cliente actualizado")
                    dialog.destroy()
                    cargar_clientes()
                else:
                    messagebox.showerror("Error", msg)

            ttk.Button(form_frame, text="Guardar Cambios", command=guardar,
                      style='Accent.TButton').grid(row=len(fields), column=0, columnspan=2, pady=20)

        btn_frame = ttk.Frame(frame, style='Dark.TFrame')
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Actualizar Lista", command=cargar_clientes,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ver Detalles", command=ver_detalles,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Nuevo Cliente", command=nuevo_cliente,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar", command=actualizar_cliente,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=eliminar_cliente,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Buscar por ID", command=buscar_por_id,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)

        cargar_clientes()

    def setup_crm_productos_tab(self, parent):
        frame = ttk.Frame(parent, style='Dark.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Gestión de Productos", style='Header.TLabel').pack(pady=(0, 20))

        tree_frame = ttk.Frame(frame, style='Dark.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Nombre", "Descripción", "SKU", "Precio", "Stock Min", "Stock Actual")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, style='Dark.Treeview')
        scrollbar.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)

        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_productos():
            for item in tree.get_children():
                tree.delete(item)

            success, productos = self.api.get_productos()
            if success:
                for prod in productos:
                    tree.insert("", tk.END, values=(
                        prod.get("idProducto", ""),
                        prod.get("nombre", ""),
                        prod.get("descripcion", "")[:50],
                        prod.get("sku", ""),
                        f"${prod.get('precioLista', 0):.2f}",
                        prod.get("stockMin", 0),
                        prod.get("stockActual", 0)
                    ))

        def ver_detalles():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
                return

            item = tree.item(selected[0])
            producto_id = item["values"][0]

            success, producto = self.api.get_producto(producto_id)
            if success:
                details = json.dumps(producto, indent=2, ensure_ascii=False)

                dialog = tk.Toplevel(self.root)
                dialog.title("Detalles del Producto")
                dialog.geometry("700x500")
                dialog.configure(bg=COLORS['bg'])

                text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD,
                                                bg=COLORS['bg_secondary'],
                                                fg=COLORS['fg'],
                                                font=('Consolas', 10))
                text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                text.insert(tk.END, details)
                text.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", "No se pudo cargar el producto")

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
                    proveedor_id = int(data['proveedorId'])

                    producto_data = {
                        'nombre': data['nombre'],
                        'descripcion': data['descripcion'],
                        'sku': data['sku'],
                        'precioLista': float(data['precioLista']),
                        'stockMin': int(data['stockMin']),
                        'stockActual': int(data['stockActual']),
                        'idProveedor': proveedor_id,
                        'idCategoria': 1 # Default category or add field
                    }
                except ValueError:
                    messagebox.showerror("Error", "Valores numericos invalidos")
                    return

                success, msg = self.api.crear_producto(producto_data)
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

                if not all(data.values()):
                    messagebox.showerror("Error", "Complete todos los campos")
                    return

                try:
                    proveedor_id = int(data['proveedorId'])

                    producto_data = {
                        'idProducto': producto_id,
                        'nombre': data['nombre'],
                        'descripcion': data['descripcion'],
                        'sku': data['sku'],
                        'precioLista': float(data['precioLista']),
                        'stockMin': int(data['stockMin']),
                        'stockActual': int(data['stockActual']),
                        'idProveedor': proveedor_id,
                        'idCategoria': 1 # Default
                    }
                except ValueError:
                    messagebox.showerror("Error", "Valores numericos invalidos")
                    return

                success, msg = self.api.actualizar_producto(producto_data)
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

        btn_frame = ttk.Frame(frame, style='Dark.TFrame')
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Actualizar Lista", command=cargar_productos,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Crear Producto", command=crear_producto,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        # Wait, I need to make sure crear_producto is defined. It was in the snippet 1374+ in Step 286. 
        # But I don't see it in the current view. I will assume it's there or I need to add it.
        # Actually, let's just add the buttons for what I see: actualizar_producto, eliminar_producto, buscar_por_id.
        # And I should probably check if crear_producto is defined.
        # In Step 286 diff, crear_producto WAS defined.
        # So I will add the button.
        
        ttk.Button(btn_frame, text="Actualizar Producto", command=actualizar_producto,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Producto", command=eliminar_producto,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Buscar por ID", command=buscar_por_id,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)

        cargar_productos()

    def setup_crm_facturas_tab(self, parent):
        frame = ttk.Frame(parent, style='Dark.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Gestión de Facturas", style='Header.TLabel').pack(pady=(0, 20))

        tree_frame = ttk.Frame(frame, style='Dark.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Cliente ID", "Fecha", "Total")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, style='Dark.Treeview')
        scrollbar.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=250)

        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_facturas():
            for item in tree.get_children():
                tree.delete(item)

            success, facturas = self.api.get_todas_facturas()
            if success:
                for factura in facturas:
                    cliente_id = ""
                    if isinstance(factura.get("cliente"), dict):
                        cliente_id = factura.get("cliente", {}).get("idCliente", "")
                    tree.insert("", tk.END, values=(
                        factura.get("idFactura", ""),
                        cliente_id,
                        factura.get("fecha", "")[:19],
                        f"${factura.get('total', 0):.2f}"
                    ))

        def ver_detalles():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione una factura")
                return

            item = tree.item(selected[0])
            factura_id = item["values"][0]

            success, factura = self.api.get_factura(factura_id)
            if success:
                details = json.dumps(factura, indent=2, ensure_ascii=False)
                
                dialog = tk.Toplevel(self.root)
                dialog.title(f"Detalles Factura #{factura_id}")
                dialog.geometry("600x500")
                dialog.configure(bg=COLORS['bg'])
                
                text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, bg=COLORS['bg_secondary'], fg=COLORS['fg'], font=('Consolas', 10))
                text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                text.insert(tk.END, details)
                text.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", "No se pudo cargar la factura")

        # Buttons moved to end of function to avoid UnboundLocalError

        cargar_facturas()
        def eliminar_factura():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione una factura")
                return

            item = tree.item(selected[0])
            factura_id = item["values"][0]

            if messagebox.askyesno("Confirmar", f"Eliminar factura ID: {factura_id}?"):
                success, msg = self.api.eliminar_factura(factura_id)
                if success:
                    messagebox.showinfo("Exito", "Factura eliminada")
                    cargar_facturas()
                else:
                    messagebox.showerror("Error", msg)

        def buscar_por_id():
            dialog = tk.Toplevel(self.root)
            dialog.title("Buscar Factura")
            dialog.geometry("400x200")
            dialog.configure(bg=COLORS['bg_secondary'])
            dialog.transient(self.root)

            ttk.Label(dialog, text="Buscar Factura por ID",
                     font=('Segoe UI', 14, 'bold'),
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=20)

            ttk.Label(dialog, text="ID de la Factura:",
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=10)

            id_entry = ttk.Entry(dialog, width=20, style='Dark.TEntry')
            id_entry.pack(pady=10)
            id_entry.focus()

            def buscar():
                factura_id = id_entry.get().strip()
                if not factura_id:
                    messagebox.showerror("Error", "Ingrese un ID")
                    return

                success, factura = self.api.get_factura(factura_id)
                if success:
                    details = json.dumps(factura, indent=2, ensure_ascii=False)

                    result_dialog = tk.Toplevel(self.root)
                    result_dialog.title(f"Factura ID: {factura_id}")
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
                    messagebox.showerror("Error", "Factura no encontrada")

            id_entry.bind('<Return>', lambda e: buscar())

            ttk.Button(dialog, text="Buscar", command=buscar,
                      style='Accent.TButton').pack(pady=10)

        btn_frame = ttk.Frame(frame, style='Dark.TFrame')
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Actualizar Lista", command=cargar_facturas,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ver Detalles", command=ver_detalles,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Factura", command=eliminar_factura,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Buscar por ID", command=buscar_por_id,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)

        cargar_facturas()

    def setup_crm_empleados_tab(self, parent):
        frame = ttk.Frame(parent, style='Dark.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Gestion de Empleados", style='Header.TLabel').pack(pady=(0, 20))

        tree_frame = ttk.Frame(frame, style='Dark.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Nombre", "Apellidos", "Email", "Telefono", "Rol", "Estado")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, style='Dark.Treeview')
        scrollbar.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)

        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_empleados():
            for item in tree.get_children():
                tree.delete(item)

            success, empleados = self.api.get_empleados()
            print(f"DEBUG: get_empleados success={success}, count={len(empleados) if empleados else 0}")
            if success:
                if not empleados:
                    print("DEBUG: Lista de empleados vacía")
                for emp in empleados:
                    print(f"DEBUG: Empleado: {emp}")
                    tree.insert("", tk.END, values=(
                        emp.get("idEmpleado", ""),
                        emp.get("nombre", ""),
                        emp.get("apellidos", ""),
                        emp.get("email", ""),
                        emp.get("telefono", ""),
                        emp.get("rol", ""),
                        emp.get("estado", "")
                    ))

        def nuevo_empleado():
            dialog = tk.Toplevel(self.root)
            dialog.title("Crear Empleado")
            dialog.geometry("500x500")
            dialog.configure(bg=COLORS['bg_secondary'])

            title_frame = ttk.Frame(dialog, style='Dark.TFrame')
            title_frame.pack(fill=tk.X, pady=(20, 10))

            ttk.Label(title_frame, text="Crear Nuevo Empleado",
                     style='Header.TLabel').pack()

            form_frame = ttk.Frame(dialog, style='Dark.TFrame')
            form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

            fields = [
                ("Nombre:", "nombre"),
                ("Apellidos:", "apellidos"),
                ("Email:", "email"),
                ("Teléfono:", "telefono"),
                ("Contraseña:", "password", True),
                ("Rol (ADMIN/EMPLEADO):", "rol"),
            ]

            entries = {}
            for i, field_info in enumerate(fields):
                label = field_info[0]
                key = field_info[1]
                is_password = field_info[2] if len(field_info) > 2 else False

                tk.Label(form_frame, text=label, bg=COLORS['bg_secondary'], fg=COLORS['fg']).grid(
                    row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))
                entry = ttk.Entry(form_frame, width=30, style='Dark.TEntry',
                                show="●" if is_password else "")
                entry.grid(row=i, column=1, pady=8)
                entries[key] = entry

                if key == "rol":
                    entry.insert(0, "EMPLEADO")

            def guardar():
                data = {key: entry.get().strip() for key, entry in entries.items()}

                if not all(data.values()):
                    messagebox.showerror("Error", "Complete todos los campos")
                    return

                if data['rol'].upper() not in ['ADMIN', 'EMPLEADO']:
                    messagebox.showerror("Error", "Rol debe ser ADMIN o EMPLEADO")
                    return

                success, msg = self.api.registro_empleado(
                    nombre=data['nombre'],
                    apellidos=data['apellidos'],
                    email=data['email'],
                    telefono=data['telefono'],
                    password=data['password'],
                    rol=data['rol'].upper()
                )

                if success:
                    messagebox.showinfo("Exito", f"Empleado creado exitosamente")
                    dialog.destroy()
                    cargar_empleados()
                else:
                    messagebox.showerror("Error", f"Error al crear empleado: {msg}")

            btn_frame = ttk.Frame(dialog, style='Dark.TFrame')
            btn_frame.pack(pady=20)

            ttk.Button(btn_frame, text="Crear", command=guardar,
                      style='Accent.TButton').pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy,
                      style='Accent.TButton').pack(side=tk.LEFT, padx=5)

        def actualizar_empleado():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un empleado")
                return

            item = tree.item(selected[0])
            empleado_id = item["values"][0]

            success, empleado = self.api.get_empleado(empleado_id)
            if not success:
                messagebox.showerror("Error", "No se pudo cargar el empleado")
                return

            dialog = tk.Toplevel(self.root)
            dialog.title("Actualizar Empleado")
            dialog.geometry("500x400")
            dialog.configure(bg=COLORS['bg_secondary'])

            ttk.Label(dialog, text=f"Actualizar Empleado ID: {empleado_id}",
                     font=('Segoe UI', 14, 'bold'), background=COLORS['bg_secondary'], foreground=COLORS['fg']).pack(pady=20)

            form_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
            form_frame.pack(padx=20, pady=10)

            fields = [
                ("Nombre:", "nombre"),
                ("Apellidos:", "apellidos"),
                ("Email:", "email"),
                ("Telefono:", "telefono")
            ]

            entries = {}
            for i, (label, key) in enumerate(fields):
                tk.Label(form_frame, text=label, bg=COLORS['bg_secondary'], fg=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
                entry = ttk.Entry(form_frame, width=30, style='Dark.TEntry')
                entry.insert(0, str(empleado.get(key, "")))
                entry.grid(row=i, column=1, pady=5, padx=5)
                entries[key] = entry

            def guardar():
                for key, entry in entries.items():
                    empleado[key] = entry.get().strip()

                if not all([empleado.get(k) for k in ['nombre', 'apellidos', 'email', 'telefono']]):
                    messagebox.showerror("Error", "Complete todos los campos")
                    return

                success, msg = self.api.actualizar_empleado(empleado)
                if success:
                    messagebox.showinfo("Exito", "Empleado actualizado")
                    dialog.destroy()
                    cargar_empleados()
                else:
                    messagebox.showerror("Error", msg)

            ttk.Button(form_frame, text="Guardar", command=guardar, style='Accent.TButton').grid(row=len(fields), column=0, columnspan=2, pady=20)

        def eliminar_empleado():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un empleado")
                return

            item = tree.item(selected[0])
            empleado_id = item["values"][0]
            nombre = item["values"][1]

            if messagebox.askyesno("Confirmar", f"¿Eliminar empleado {nombre}?"):
                success, msg = self.api.eliminar_empleado(empleado_id)
                if success:
                    messagebox.showinfo("Exito", "Empleado eliminado")
                    cargar_empleados()
                else:
                    messagebox.showerror("Error", msg)

        btn_frame = ttk.Frame(frame, style='Dark.TFrame')
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Actualizar Lista", command=cargar_empleados,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Nuevo Empleado", command=nuevo_empleado,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar Empleado", command=actualizar_empleado,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Empleado", command=eliminar_empleado,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)

        cargar_empleados()

    def setup_crm_proveedores_tab(self, parent):
        frame = ttk.Frame(parent, style='Dark.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Gestión de Proveedores", style='Header.TLabel').pack(pady=(0, 20))

        tree_frame = ttk.Frame(frame, style='Dark.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Nombre", "Contacto", "Email", "Teléfono", "País")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                           yscrollcommand=scrollbar.set, style='Dark.Treeview')
        scrollbar.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)

        tree.pack(fill=tk.BOTH, expand=True)

        def cargar_proveedores():
            for item in tree.get_children():
                tree.delete(item)

            success, proveedores = self.api.get_proveedores()
            print(f"DEBUG: get_proveedores success={success}, count={len(proveedores) if proveedores else 0}")
            if success and proveedores:
                for prov in proveedores:
                    print(f"DEBUG: Proveedor: {prov}")
                    tree.insert("", tk.END, values=(
                        prov.get("idProveedor", ""),
                        prov.get("nombre", ""),
                        prov.get("contacto", ""),
                        prov.get("email", ""),
                        prov.get("telefono", ""),
                        prov.get("pais", "")
                    ))
            else:
                # Si no hay proveedores o error
                pass # Treeview se queda vacío, pero podríamos mostrar un mensaje
                # Por ahora dejamos vacío pero aseguramos que no falle

        def crear_proveedor():
            dialog = tk.Toplevel(self.root)
            dialog.title("Nuevo Proveedor")
            dialog.geometry("500x450")
            dialog.configure(bg=COLORS['bg_secondary'])

            ttk.Label(dialog, text="Nuevo Proveedor",
                     font=('Segoe UI', 16, 'bold'),
                     background=COLORS['bg_secondary'],
                     foreground=COLORS['fg']).pack(pady=20)

            form_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
            form_frame.pack(padx=20, pady=10)

            fields = [
                ("Nombre:", "nombre"),
                ("Contacto:", "contacto"),
                ("Email:", "email"),
                ("Teléfono:", "telefono"),
                ("País:", "pais"),
            ]

            entries = {}
            for i, (label, key) in enumerate(fields):
                ttk.Label(form_frame, text=label,
                         background=COLORS['bg_secondary'],
                         foreground=COLORS['fg']).grid(row=i, column=0, sticky=tk.W, padx=10, pady=8)
                entry = ttk.Entry(form_frame, width=30, style='Dark.TEntry')
                entry.grid(row=i, column=1, padx=10, pady=8)
                entries[key] = entry

            def guardar():
                data = {key: entry.get().strip() for key, entry in entries.items()}

                if not all(data.values()):
                    messagebox.showerror("Error", "Complete todos los campos")
                    return

                success, msg = self.api.crear_proveedor(data)
                if success:
                    messagebox.showinfo("Éxito", "Proveedor creado")
                    dialog.destroy()
                    cargar_proveedores()
                else:
                    messagebox.showerror("Error", msg)

            ttk.Button(form_frame, text="Guardar", command=guardar,
                      style='Accent.TButton').grid(row=len(fields), column=0, columnspan=2, pady=20)

        def eliminar_proveedor():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un proveedor")
                return

            item = tree.item(selected[0])
            proveedor_id = item["values"][0]

            if messagebox.askyesno("Confirmar", "¿Eliminar este proveedor?"):
                success, msg = self.api.eliminar_proveedor(proveedor_id)
                if success:
                    messagebox.showinfo("Éxito", "Proveedor eliminado")
                    cargar_proveedores()
                else:
                    messagebox.showerror("Error", msg)

        btn_frame = ttk.Frame(frame, style='Dark.TFrame')
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Actualizar", command=cargar_proveedores,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Nuevo", command=crear_proveedor,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=eliminar_proveedor,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)

        cargar_proveedores()

    def logout_cliente(self):
        if messagebox.askyesno("Confirmar", "¿Cerrar sesión?"):
            self.api.logout_cliente()
            self.current_user = None
            self.current_cliente_id = None
            self.user_type = None
            self.show_login_page()

    def logout_empleado(self):
        if messagebox.askyesno("Confirmar", "¿Cerrar sesión?"):
            self.api.logout_empleado()
            self.current_user = None
            self.user_type = None
            self.show_login_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = ECommerceApp(root)
    root.mainloop()

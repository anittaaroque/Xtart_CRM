import requests
from config import ENDPOINTS

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.user_id = None
        self.user_role = None

    def login_cliente(self, email, password):
        try:
            response = self.session.post(ENDPOINTS["login_cliente"], json={
                "email": email,
                "password": password
            })
            if response.status_code == 200:
                data = response.json()
                self.user_role = data.get("rol")
                return True, data
            else:
                return False, response.text
        except Exception as e:
            return False, str(e)

    def registro_cliente(self, nombre, apellidos, email, direccion, pais, password):
        try:
            response = self.session.post(ENDPOINTS["registro_cliente"], json={
                "nombre": nombre,
                "apellidos": apellidos,
                "email": email,
                "direccion": direccion,
                "pais": pais,
                "password": password
            })
            if response.status_code == 200 or response.status_code == 201:
                return True, "Cliente registrado exitosamente"
            else:
                return False, response.text
        except Exception as e:
            return False, str(e)

    def login_empleado(self, email, password):
        try:
            response = self.session.post(ENDPOINTS["login_empleado"], json={
                "email": email,
                "password": password
            })
            if response.status_code == 200:
                data = response.json()
                self.user_role = data.get("rol")
                return True, data
            else:
                return False, response.text
        except Exception as e:
            return False, str(e)

    def logout_cliente(self):
        try:
            response = self.session.post(ENDPOINTS["logout_cliente"])
            self.user_id = None
            self.user_role = None
            return response.status_code == 200
        except:
            return False

    def logout_empleado(self):
        try:
            response = self.session.post(ENDPOINTS["logout_empleado"])
            self.user_id = None
            self.user_role = None
            return response.status_code == 200
        except:
            return False

    def get_productos(self):
        try:
            response = self.session.get(ENDPOINTS["productos"])
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, []
        except Exception as e:
            return False, []

    def get_producto(self, producto_id):
        try:
            response = self.session.get(f"{ENDPOINTS['producto_detalle']}/{producto_id}")
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, None
        except Exception as e:
            return False, None

    def agregar_al_carrito(self, cliente_id, producto_id, cantidad):
        try:
            response = self.session.post(ENDPOINTS["carrito_agregar"], json={
                "clienteId": cliente_id,
                "productoId": producto_id,
                "cantidad": cantidad
            })
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)

    def ver_carrito(self, cliente_id):
        try:
            response = self.session.get(f"{ENDPOINTS['carrito_ver']}/{cliente_id}")
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, []
        except Exception as e:
            return False, []

    def eliminar_del_carrito(self, cliente_id, producto_id):
        try:
            response = self.session.delete(f"{ENDPOINTS['carrito_eliminar']}/{cliente_id}/{producto_id}")
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)

    def crear_factura(self, cliente_id, carrito, total):
        try:
            response = self.session.post(ENDPOINTS["facturas"], json={
                "clienteId": cliente_id,
                "carrito": carrito,
                "total": total
            })
            return response.status_code == 200 or response.status_code == 201, response.text
        except Exception as e:
            return False, str(e)

    def get_facturas_cliente(self, cliente_id):
        try:
            response = self.session.get(f"{ENDPOINTS['facturas_cliente']}/{cliente_id}")
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, []
        except Exception as e:
            return False, []

    def get_clientes(self):
        try:
            response = self.session.get(ENDPOINTS["clientes"])
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, []
        except Exception as e:
            return False, []

    def get_cliente(self, cliente_id):
        try:
            response = self.session.get(f"{ENDPOINTS['clientes']}/{cliente_id}")
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, None
        except Exception as e:
            return False, None

    def get_empleados(self):
        try:
            response = self.session.get(ENDPOINTS["empleados"])
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, []
        except Exception as e:
            return False, []

    def get_proveedores(self):
        try:
            response = self.session.get(ENDPOINTS["proveedores"])
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, []
        except Exception as e:
            return False, []

    def crear_proveedor(self, data):
        try:
            response = self.session.post(ENDPOINTS["proveedores"], json=data)
            return response.status_code == 200 or response.status_code == 201, response.text
        except Exception as e:
            return False, str(e)

    def actualizar_proveedor(self, data):
        try:
            response = self.session.put(ENDPOINTS["proveedores"], json=data)
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)

    def eliminar_proveedor(self, proveedor_id):
        try:
            response = self.session.delete(f"{ENDPOINTS['proveedores']}/{proveedor_id}")
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)

    def get_todas_facturas(self):
        try:
            response = self.session.get(ENDPOINTS["facturas"])
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, []
        except Exception as e:
            return False, []

    def crear_producto(self, data):
        try:
            response = self.session.post(ENDPOINTS["productos"], json=data)
            return response.status_code == 200 or response.status_code == 201, response.text
        except Exception as e:
            return False, str(e)

    def actualizar_producto(self, data):
        try:
            response = self.session.put(ENDPOINTS["productos"], json=data)
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)

    def eliminar_producto(self, producto_id):
        try:
            response = self.session.delete(f"{ENDPOINTS['productos']}/{producto_id}")
            return response.status_code == 200 or response.status_code == 204, response.text
        except Exception as e:
            return False, str(e)

    def actualizar_factura(self, data):
        try:
            response = self.session.put(ENDPOINTS["facturas"], json=data)
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)

    def eliminar_factura(self, factura_id):
        try:
            response = self.session.delete(f"{ENDPOINTS['facturas']}/{factura_id}")
            return response.status_code == 200 or response.status_code == 204, response.text
        except Exception as e:
            return False, str(e)

    def get_factura(self, factura_id):
        try:
            response = self.session.get(f"{ENDPOINTS['facturas']}/{factura_id}")
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, None
        except Exception as e:
            return False, None

    def registro_empleado(self, nombre, apellidos, email, telefono, password, rol="EMPLEADO"):
        try:
            response = self.session.post(ENDPOINTS["empleados"], json={
                "nombre": nombre,
                "apellidos": apellidos,
                "email": email,
                "telefono": telefono,
                "contraseña": password,
                "rol": rol,
                "estatus": "A"
            })
            if response.status_code == 200 or response.status_code == 201:
                return True, "Empleado registrado exitosamente"
            else:
                return False, response.text
        except Exception as e:
            return False, str(e)

    def eliminar_cliente(self, cliente_id):
        try:
            response = self.session.delete(f"{ENDPOINTS['clientes']}/{cliente_id}")
            return response.status_code == 200 or response.status_code == 204, response.text
        except Exception as e:
            return False, str(e)

    def get_empleado(self, empleado_id):
        try:
            response = self.session.get(f"{ENDPOINTS['empleados']}/{empleado_id}")
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, None
        except Exception as e:
            return False, None

    def actualizar_empleado(self, data):
        try:
            response = self.session.put(ENDPOINTS["empleados"], json=data)
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)

    def eliminar_empleado(self, empleado_id):
        try:
            response = self.session.delete(f"{ENDPOINTS['empleados']}/{empleado_id}")
            return response.status_code == 200 or response.status_code == 204, response.text
        except Exception as e:
            return False, str(e)

    def actualizar_cliente(self, data):
        try:
            response = self.session.put(ENDPOINTS["clientes"], json=data)
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)

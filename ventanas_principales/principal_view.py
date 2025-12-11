import tkinter as tk
from vistas.cliente_view import ventana_cliente
from vistas.proveedor_view import ventana_proveedor
from vistas.colegio_view import ventana_colegio
from vistas.producto_view import ventana_producto
from vistas.pedido_view import ventana_pedido
from vistas.cambiar_estado_view import ventana_cambiar_estado
from vistas.factura_view import ventana_factura, ventana_facturar_pedido
from vistas.informes_view import ventana_informes
from vistas.materia_prima_view import ventana_materia_prima
from vistas.incluye_view import ventana_incluye
from vistas.usuario_view import ventana_crear_usuario  # NUEVA VENTANA


def ventana_principal(nombre_usuario, id_rol):
    principal = tk.Toplevel()
    principal.title("Ventana Principal")
    principal.geometry("420x600")

    saludo = tk.Label(principal, text=f"Bienvenido, {nombre_usuario}", font=("Arial", 12))
    saludo.pack(pady=20)

    # =============================================================
    # BOTONES COMUNES PARA TODOS LOS ROLES
    # =============================================================
    tk.Button(principal, text="Cliente", command=ventana_cliente).pack(pady=10)
    tk.Button(principal, text="Pedido", command=ventana_pedido).pack(pady=10)
    tk.Button(principal, text="Incluir Producto en Pedido", command=ventana_incluye).pack(pady=10)
    tk.Button(principal, text="Cambiar Estado Pedido", command=ventana_cambiar_estado).pack(pady=10)
    tk.Button(principal, text="Facturar Pedido", command=ventana_facturar_pedido).pack(pady=10)
    tk.Button(principal, text="Ver Facturas", command=ventana_factura).pack(pady=10)

    # =============================================================
    # SI ES ADMINISTRADOR (ID_ROL = 1) MUESTRA TODO
    # =============================================================
    if id_rol == 1:
        tk.Label(principal, text="Opciones de Administrador", fg="blue", font=("Arial", 11)).pack(pady=10)

        tk.Button(principal, text="Proveedor", command=ventana_proveedor).pack(pady=6)
        tk.Button(principal, text="Materia Prima", command=ventana_materia_prima).pack(pady=6)
        tk.Button(principal, text="Inventario Producto Terminado", command=ventana_producto).pack(pady=6)
        tk.Button(principal, text="Colegio", command=ventana_colegio).pack(pady=6)
        tk.Button(principal, text="Informes del Sistema", command=ventana_informes).pack(pady=6)
        tk.Button(principal, text="Crear Usuario", command=ventana_crear_usuario).pack(pady=6)

    # =============================================================
    # ROL 2 = VENDEDOR (solo ve opciones básicas)
    # =============================================================
    else:
        tk.Label(principal, text="Rol: Vendedor (acceso limitado)", fg="red", font=("Arial", 11)).pack(pady=10)

    tk.Button(principal, text="Salir", command=principal.destroy).pack(pady=20)

import tkinter as tk

from vistas.cliente_view import ventana_cliente
from vistas.proveedor_view import ventana_proveedor
from vistas.colegio_view import ventana_colegio
from vistas.producto_view import ventana_producto
from vistas.pedido_view import ventana_pedido
from vistas.cambiar_estado_view import ventana_cambiar_estado
from vistas.factura_view import ventana_factura, ventana_facturar_pedido
from vistas.informes_view import ventana_informes
#from factura_view import ventana_factura, ventana_facturar_pedido

#from vistas.factura_view import ventana_factura_auto  # si la usas así
# Si falta alguna función me dices y la enlazo.


def ventana_principal(nombre_usuario):
    principal = tk.Toplevel()
    principal.title("Ventana Principal")
    principal.geometry("400x500")

    saludo = tk.Label(principal, text=f"Bienvenido, {nombre_usuario}", font=("Arial", 12))
    saludo.pack(pady=20)

    tk.Button(principal, text="Cliente", command=ventana_cliente).pack(pady=10)
    tk.Button(principal, text="Proveedor", command=ventana_proveedor).pack(pady=10)
    tk.Button(principal, text="Colegio", command=ventana_colegio).pack(pady=10)
    tk.Button(principal, text="Inventario Producto Terminado", command=ventana_producto).pack(pady=10)
    tk.Button(principal, text="Pedido", command=ventana_pedido).pack(pady=10)
    tk.Button(principal, text="Cambiar Estado Pedido", command=ventana_cambiar_estado).pack(pady=10)
    #tk.Button(principal, text="Factura", command=ventana_factura).pack(pady=10)
    tk.Button(principal, text="Facturar Pedido", command=ventana_facturar_pedido).pack(pady=10)
    tk.Button(principal, text="Ver Facturas", command=ventana_factura).pack(pady=10)
    tk.Button(principal, text="Informes", command=ventana_informes).pack(pady=10)



    tk.Button(principal, text="Salir", command=principal.destroy).pack(pady=10)
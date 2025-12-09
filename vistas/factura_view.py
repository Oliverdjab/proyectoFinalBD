import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd
from controladora import generar_factura, descontar_inventario

def ventana_factura():
    win = tk.Toplevel()
    win.title("Facturas registradas")
    win.geometry("500x400")

    text = tk.Text(win, width=70, height=20)
    text.pack()

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT f.num_factura, p.fecha_entrega, f.total, f.num_pedido
            FROM factura f
            JOIN pedido p ON p.num_pedido = f.num_pedido
            ORDER BY f.num_factura
        """)
        filas = cursor.fetchall()

        text.insert(tk.END, "Factura | Fecha Entrega | Total | Pedido\n")
        text.insert(tk.END, "-------------------------------------------------------------\n")

        for fila in filas:
            linea = f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]}\n"
            text.insert(tk.END, linea)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)


# ===========================================================
#  FACTURAR AUTOMÁTICAMENTE UN PEDIDO
# ===========================================================
def ventana_facturar_pedido():
    win = tk.Toplevel()
    win.title("Facturar Pedido")
    win.geometry("300x250")

    tk.Label(win, text="Número de Pedido:").pack()
    entry_pedido = tk.Entry(win)
    entry_pedido.pack()

    def facturar():
        num_ped = entry_pedido.get().strip()

        if num_ped == "":
            messagebox.showwarning("Aviso", "Debes ingresar el número de pedido.")
            return

        # Generar factura (el num_factura se autogenera en la BD)
        creado = generar_factura(num_ped)

        if not creado:
            return

        # Descontar inventario
        descontar_inventario(num_ped)

        # Cambiar estado a entregado
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("UPDATE pedido SET estado='Entregado' WHERE num_pedido=%s", (num_ped,))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("OK", "Factura generada y pedido entregado.")

    tk.Button(win, text="Generar Factura", command=facturar).pack(pady=10)
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=5)

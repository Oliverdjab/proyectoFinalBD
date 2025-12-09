import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd

def ventana_incluye():
    win = tk.Toplevel()
    win.title("Incluir Producto en Pedido")
    win.geometry("320x350")

    # CAMPOS
    tk.Label(win, text="Número de Pedido:").pack()
    entry_pedido = tk.Entry(win)
    entry_pedido.pack()

    tk.Label(win, text="Código del Producto:").pack()
    entry_producto = tk.Entry(win)
    entry_producto.pack()

    tk.Label(win, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(win)
    entry_cantidad.pack()

    # GUARDAR
    def guardar_incluye():
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO incluye(num_pedido, cod_producto, cantidad)
                VALUES (%s, %s, %s)
            """, (entry_pedido.get(), entry_producto.get(), entry_cantidad.get()))

            conn.commit()
            messagebox.showinfo("Éxito", "Producto incluido correctamente en el pedido.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Guardar", command=guardar_incluye).pack(pady=5)

    # VER REGISTROS
    def ver_incluye():
        win_ver = tk.Toplevel()
        win_ver.title("Registros INCLUYE")
        win_ver.geometry("380x300")

        text = tk.Text(win_ver, width=50, height=15)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM incluye")
            filas = cursor.fetchall()

            text.insert(tk.END, "Pedido | Producto | Cantidad\n")
            text.insert(tk.END, "------------------------------\n")

            for fila in filas:
                linea = f"{fila[0]} | {fila[1]} | {fila[2]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack()

    tk.Button(win, text="Ver registros", command=ver_incluye).pack(pady=5)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

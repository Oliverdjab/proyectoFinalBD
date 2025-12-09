import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd

def ventana_informes():
    win = tk.Toplevel()
    win.title("Mostrar Informes")
    win.geometry("320x350")

    # CAMPOS
    tk.Label(win, text="prueba:").pack()
    entry_pedido = tk.Entry(win)
    entry_pedido.pack()

     # ESTE VER REGISTROS ES DE PRUEBA. ESTE NO ES EL QUE DEBERIA MOSTRARSE EN LA VENTANA INFORMES
     #ES SOLO PARA QUE TENGAS UNA IDEA DE COMO MOSTRAR LOS REGISTROS EN UNA VENTANA NUEVA


     ## DE AQUI PARA ABAJO ES SOLO DE PRUEBA, OJOOO
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
# DE AQUI PARA ARRIBA ES SOLO DE PRUEBA

    
# el comando de boton esta igualado a la funcion que tiene la ventana donde estan los registros
    tk.Button(win, text="Ver registros", command=ver_incluye).pack(pady=5)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

   
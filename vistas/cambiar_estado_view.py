import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd

def ventana_cambiar_estado():
    win = tk.Toplevel()
    win.title("Cambiar Estado del Pedido")
    win.geometry("320x250")

    tk.Label(win, text="Número de Pedido:").pack()
    entry_num = tk.Entry(win)
    entry_num.pack()

    tk.Label(win, text="Nuevo Estado:").pack()
    entry_estado = tk.Entry(win)
    entry_estado.pack()

    # ACTUALIZAR ESTADO
    def cambiar_estado():
        if entry_num.get() == "" or entry_estado.get() == "":
            messagebox.showwarning("Aviso", "Debes llenar ambos campos.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE pedido
                SET estado=%s
                WHERE num_pedido=%s
            """, (entry_estado.get(), entry_num.get()))

            conn.commit()
            messagebox.showinfo("Éxito", "Estado del pedido actualizado.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Cambiar estado", command=cambiar_estado).pack(pady=10)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=5)

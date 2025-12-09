import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd

def ventana_cliente():
    win = tk.Toplevel()
    win.title("Cliente - CRUD")
    win.geometry("300x300")

    # CAMPOS
    tk.Label(win, text="ID Cliente (para actualizar/eliminar):").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    tk.Label(win, text="Nombre:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Teléfono:").pack()
    entry_telefono = tk.Entry(win)
    entry_telefono.pack()

    # INSERTAR
    def guardar_cliente():

        if entry_nombre.get() == "" or entry_telefono.get() == "":
            messagebox.showwarning("Aviso", "Nombre y Teléfono son obligatorios.")
            return
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO cliente(nombre, telefono)
                VALUES (%s, %s)
            """, (entry_nombre.get(), entry_telefono.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()
    tk.Button(win, text="Guardar", command=guardar_cliente).pack(pady=5)

    # ACTUALIZAR
    def actualizar_cliente():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID.")
            return
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE cliente
                SET nombre=%s, telefono=%s
                WHERE id_cliente=%s
            """, (entry_nombre.get(), entry_telefono.get(), entry_id.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()
    tk.Button(win, text="Actualizar", command=actualizar_cliente).pack(pady=5)

    # ELIMINAR
    def eliminar_cliente():
        id_c = entry_id.get()
        if id_c == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID.")
            return
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_c,))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()
    tk.Button(win, text="Eliminar", command=eliminar_cliente).pack(pady=5)

    # VER REGISTROS
    def ver_registros_cliente():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Cliente")
        win_ver.geometry("350x300")

        text = tk.Text(win_ver, width=45, height=15)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM cliente")
            filas = cursor.fetchall()

            text.insert(tk.END, "ID | Nombre | Teléfono\n")
            text.insert(tk.END, "-----------------------------\n")

            for f in filas:
                linea = f"{f[0]} | {f[1]} | {f[2]}\n"
                text.insert(tk.END, linea)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_registros_cliente).pack(pady=5)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

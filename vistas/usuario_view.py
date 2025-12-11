import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd


def ventana_crear_usuario():
    win = tk.Toplevel()
    win.title("Crear Usuario")
    win.geometry("300x300")

    tk.Label(win, text="Nombre de Usuario:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Contraseña:").pack()
    entry_contra = tk.Entry(win, show="*")
    entry_contra.pack()

    tk.Label(win, text="Rol (1 = Admin, 2 = Vendedor):").pack()
    entry_rol = tk.Entry(win)
    entry_rol.pack()

    def guardar():
        nombre = entry_nombre.get().strip()
        contra = entry_contra.get().strip()
        rol = entry_rol.get().strip()

        if nombre == "" or contra == "" or rol == "":
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuario(nombre_usuario, contrasena, id_rol)
                VALUES (%s, %s, %s)
            """, (nombre, contra, rol))

            conn.commit()
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Crear Usuario", command=guardar).pack(pady=10)
    tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)

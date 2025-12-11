import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd
from ventanas_principales.principal_view import ventana_principal

def iniciar_sesion(entry_usuario, entry_contra):
    nombre = entry_usuario.get()
    clave = entry_contra.get()

    conn = conectar_bd()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT contrasena FROM usuario WHERE nombre_usuario = %s",
            (nombre,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            messagebox.showwarning("Aviso", "El usuario no existe.")
        else:
            contrasena_correcta = resultado[0]
            if clave == contrasena_correcta:
                messagebox.showinfo("Bienvenido", "Inicio de sesión exitoso.")
                ventana_principal(nombre)
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()


def crear_login():
    ventana = tk.Tk()
    ventana.title("Login")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Usuario:").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    tk.Label(ventana, text="Contraseña:").pack()
    entry_contra = tk.Entry(ventana, show="*")
    entry_contra.pack()

    tk.Button(
        ventana, text="Iniciar Sesión",
        command=lambda: iniciar_sesion(entry_usuario, entry_contra)
    ).pack(pady=10)

    ventana.mainloop()
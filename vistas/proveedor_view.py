import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd
from vistas.materia_prima_view import ventana_materia_prima

def ventana_proveedor():
    win = tk.Toplevel()
    win.title("Proveedor - CRUD")
    win.geometry("300x380")

    # CAMPOS
    tk.Label(win, text="NIT (Solo para actualizar o eliminar):").pack()
    entry_nit = tk.Entry(win)
    entry_nit.pack()

    tk.Label(win, text="Nombre:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Dirección:").pack()
    entry_direccion = tk.Entry(win)
    entry_direccion.pack()

    tk.Label(win, text="Teléfono:").pack()
    entry_telefono = tk.Entry(win)
    entry_telefono.pack()

    tk.Label(win, text="Nombre Contacto:").pack()
    entry_contacto = tk.Entry(win)
    entry_contacto.pack()

    # ---------------------------------
    # 1️⃣ INSERTAR PROVEEDOR
    # ---------------------------------
    def guardar_proveedor():
        nombre = entry_nombre.get().strip()
        telefono = entry_telefono.get().strip()

        # Validación obligatoria
        if nombre == "" or telefono == "":
            messagebox.showwarning("Aviso", "Nombre y Teléfono son obligatorios.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO proveedor(nombre_p, direccion, telefono, nom_contacto)
                VALUES (%s, %s, %s, %s)
            """, (
                entry_nombre.get(),
                entry_direccion.get(),
                entry_telefono.get(),
                entry_contacto.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Proveedor guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Guardar", command=guardar_proveedor).pack(pady=5)

    # ---------------------------------
    # 2️⃣ ACTUALIZAR PROVEEDOR
    # ---------------------------------
    def actualizar_proveedor():
        if entry_nit.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el NIT.")
            return

        nombre = entry_nombre.get().strip()
        telefono = entry_telefono.get().strip()

        if nombre == "" or telefono == "":
            messagebox.showwarning("Aviso", "Nombre y Teléfono no pueden estar vacíos.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE proveedor 
                SET nombre_p = %s,
                    direccion = %s,
                    telefono = %s,
                    nom_contacto = %s
                WHERE nit = %s
            """, (
                entry_nombre.get(),
                entry_direccion.get(),
                entry_telefono.get(),
                entry_contacto.get(),
                entry_nit.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_proveedor).pack(pady=5)

    # ---------------------------------
    # 3️⃣ ELIMINAR PROVEEDOR
    # ---------------------------------
    def eliminar_proveedor():
        nit = entry_nit.get()
        if nit == "":
            messagebox.showwarning("Aviso", "Debes escribir el NIT.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM proveedor WHERE nit = %s", (nit,))
            conn.commit()
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_proveedor).pack(pady=5)

    # ------------------------------
    # 4️⃣ VER REGISTROS PROVEEDOR
    # ------------------------------
    def ver_registros_proveedor():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Proveedor")
        win_ver.geometry("450x300")

        text = tk.Text(win_ver, width=60, height=15)
        text.pack()

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM proveedor")
            filas = cursor.fetchall()

            text.insert(tk.END, "NIT | Nombre | Dirección | Teléfono | Contacto\n")
            text.insert(tk.END, "----------------------------------------------------------\n")

            for f in filas:
                text.insert(tk.END, f"{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_registros_proveedor).pack(pady=5)

    # ------------------------------
    # 5️⃣ BOTÓN MATERIA PRIMA (RESTAURADO)
    # ------------------------------
    tk.Button(win, text="Materia Prima", command=ventana_materia_prima).pack(pady=5)

    # ---------------------------------
    # 6️⃣ VOLVER
    # ---------------------------------
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

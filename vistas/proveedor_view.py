import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd
from vistas.materia_prima_view import ventana_materia_prima

print(">>> CARGANDO proveedor_view.py DESDE:", __file__)

def ventana_proveedor():
    win = tk.Toplevel()
    win.title("Proveedor - CRUD")
    win.geometry("300x380")

    # CAMPOS
    tk.Label(win, text="NIT:").pack()
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
    print("USANDO EL ARCHIVO CORRECTO DE PROVEEDOR")
    def guardar_proveedor():
        nit = entry_nit.get().strip()
        nombre = entry_nombre.get().strip()
        telefono = entry_telefono.get().strip()

        # Validación obligatoria
        if nit == "":
            messagebox.showwarning("Aviso", "El NIT es obligatorio.")
            return

        if not nit.isdigit():
            messagebox.showwarning("Aviso", "El NIT debe ser un número.")
            return

        if nombre == "":
            messagebox.showwarning("Aviso", "El nombre es obligatorio.")
            return

        if telefono == "":
            messagebox.showwarning("Aviso", "El teléfono es obligatorio.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO proveedor (nit, nombre_p, direccion, telefono, nom_contacto)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                nit,
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
        nit = entry_nit.get().strip()

        if nit == "":
            messagebox.showwarning("Aviso", "Debes escribir el NIT.")
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
                nit
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
    # 5️⃣ MATERIA PRIMA
    # ------------------------------
    tk.Button(win, text="Materia Prima", command=ventana_materia_prima).pack(pady=5)

    # ---------------------------------
    # 6️⃣ VOLVER
    # ---------------------------------
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)
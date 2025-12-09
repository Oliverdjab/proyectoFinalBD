# vistas/materia_prima_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from conexion import conectar_bd
from vistas.utiliza_view import ventana_utiliza

def ventana_materia_prima():
    win = tk.Toplevel()
    win.title("Inventario de Materias Primas - CRUD")
    win.geometry("350x650")

    # ---- CAMPOS ----
    tk.Label(win, text="Código materia (PK):").pack()
    entry_cod = tk.Entry(win)
    entry_cod.pack()

    tk.Label(win, text="Tipo:").pack()
    combo_tipo = ttk.Combobox(win, state="readonly")
    combo_tipo['values'] = ["telas", "hilos", "botones", "cierres", "agujas", "tijeras", "cinta metrica"]
    combo_tipo.pack()

    tk.Label(win, text="Descripción:").pack()
    entry_desc = tk.Entry(win)
    entry_desc.pack()

    tk.Label(win, text="Cantidad:").pack()
    entry_cant = tk.Entry(win)
    entry_cant.pack()

    tk.Label(win, text="Unidad de medida:").pack()
    combo_unidad = ttk.Combobox(win, state="readonly")
    combo_unidad['values'] = ["Kilogramos", "Metros", "Unidades", "Tubos"]
    combo_unidad.pack()

    # ----- SELECT PROVEEDORES -----
    tk.Label(win, text="Proveedor:").pack()

    combo_proveedor = ttk.Combobox(win, state="readonly")
    combo_proveedor.pack()

    # Cargar proveedores desde PostgreSQL
    conn = conectar_bd()
    lista_ids = []   # lista interna para almacenar ID reales
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT nit, nombre_p FROM proveedor ORDER BY nombre_p")
            datos = cursor.fetchall()

            lista_nombres = []

            for fila in datos:
                lista_ids.append(fila[0])   # ID real
                lista_nombres.append(fila[1])  # Nombre visible

            combo_proveedor['values'] = lista_nombres

        except Exception as e:
            messagebox.showerror("Error al cargar proveedores", str(e))
        finally:
            cursor.close()
            conn.close()

    # Función para obtener el ID del proveedor seleccionado
    def obtener_id_proveedor():
        index = combo_proveedor.current()
        if index == -1:
            return None
        return lista_ids[index]

    # =====================================================
    # 1️⃣ INSERTAR MATERIA PRIMA
    # =====================================================
    def guardar_mp():
        if combo_tipo.get().strip() == "" or entry_desc.get().strip() == "" or entry_cant.get().strip() == "" or combo_unidad.get().strip() == "" or obtener_id_proveedor() is None:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios.")
            return
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO materia_prima(tipo, description,
                                          cantidad, unidad_medida, nit)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                combo_tipo.get(),
                entry_desc.get(),
                entry_cant.get(),
                combo_unidad.get(),
                obtener_id_proveedor()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Materia prima guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Guardar", command=guardar_mp).pack(pady=5)

    # =====================================================
    # 2️⃣ ACTUALIZAR
    # =====================================================
    def actualizar_mp():
        if entry_cod.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el código.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE materia_prima
                SET tipo=%s, description=%s, cantidad=%s,
                    unidad_medida=%s, nit=%s
                WHERE cod_materia=%s
            """, (
                combo_tipo.get(),
                entry_desc.get(),
                entry_cant.get(),
                combo_unidad.get(),
                obtener_id_proveedor(),
                entry_cod.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Materia prima actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error: ", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_mp).pack(pady=5)

    # =====================================================
    # 3️⃣ ELIMINAR
    # =====================================================
    def eliminar_mp():
        if entry_cod.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el código.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM materia_prima WHERE cod_materia=%s",
                           (entry_cod.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Materia prima eliminada.")
        except Exception as e:
            messagebox.showerror("Error: ", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_mp).pack(pady=5)

    # =====================================================
    # 4️⃣ VER REGISTROS
    # =====================================================
    def ver_mp():
        win_ver = tk.Toplevel()
        win_ver.title("Registros Materias Primas")
        win_ver.geometry("700x400")

        text = tk.Text(win_ver, width=90, height=20)
        text.pack()

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM materia_prima")
            filas = cursor.fetchall()

            text.insert(tk.END, "COD | Tipo | Descripción | Cantidad | Unidad | NIT\n")
            text.insert(tk.END, "---------------------------------------------------------------------\n")

            for f in filas:
                linea = f"{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error: ", str(e))
        finally:
            cursor.close()
            conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack()

    # Botón Utiliza (vuelve a la ventana que asocia materia prima con piezas)
    btn_utiliza = tk.Button(win, text="Utiliza", command=ventana_utiliza)
    btn_utiliza.pack(pady=10)

    tk.Button(win, text="Ver registros", command=ver_mp).pack(pady=5)

    # =====================================================
    # 5️⃣ VOLVER
    # =====================================================
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

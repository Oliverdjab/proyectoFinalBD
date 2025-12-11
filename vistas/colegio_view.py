import tkinter as tk
from tkinter import messagebox, ttk
from conexion import conectar_bd

# ===================================================================
#   VENTANA PRINCIPAL DE COLEGIOS
# ===================================================================
def ventana_colegio():
    win = tk.Toplevel()
    win.title("Colegio - CRUD")
    win.geometry("300x350")

    tk.Label(win, text="ID Colegio (para actualizar/eliminar):").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    tk.Label(win, text="Nombre:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Dirección:").pack()
    entry_direccion = tk.Entry(win)
    entry_direccion.pack()

    tk.Label(win, text="Teléfono:").pack()
    entry_telefono = tk.Entry(win)
    entry_telefono.pack()

    # --------------------- GUARDAR ---------------------
    def guardar_colegio():
        if entry_nombre.get() == "" or entry_direccion.get() == "" or entry_telefono.get() == "":
            messagebox.showwarning("Aviso", "Nombre, Dirección y Teléfono son obligatorios.")
            return
        conn = conectar_bd()

        if conn is None: return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO colegio(nombre_c, direccion, telefono)
                VALUES (%s, %s, %s)
            """, (entry_nombre.get(), entry_direccion.get(), entry_telefono.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Colegio guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Guardar", command=guardar_colegio).pack(pady=5)

    # --------------------- ACTUALIZAR ---------------------
    def actualizar_colegio():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID.")
            return
        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE colegio
                SET nombre_c=%s, direccion=%s, telefono=%s
                WHERE id_colegio=%s
            """, (entry_nombre.get(), entry_direccion.get(), entry_telefono.get(), entry_id.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Colegio actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_colegio).pack(pady=5)

    # --------------------- ELIMINAR ---------------------
    def eliminar_colegio():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM colegio WHERE id_colegio=%s", (entry_id.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Colegio eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_colegio).pack(pady=5)

    # --------------------- VER REGISTROS ---------------------
    def ver_registros_colegio():
        win_ver = tk.Toplevel()
        win_ver.title("Registros Colegio")
        win_ver.geometry("400x300")

        text = tk.Text(win_ver, width=50, height=15)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM colegio")
            filas = cursor.fetchall()

            text.insert(tk.END, "ID | Nombre | Dirección | Teléfono\n")
            text.insert(tk.END, "-------------------------------------------\n")
            for fila in filas:
                text.insert(tk.END, f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_registros_colegio).pack(pady=5)

    # ---------------- BOTÓN UNIFORMES ---------------------
    tk.Button(win, text="Uniformes por Colegio", command=ventana_uniforme).pack(pady=5)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)


# ============================================================================
#                   VENTANA DE UNIFORMES 
# ============================================================================

def ventana_uniforme():
    win = tk.Toplevel()
    win.title("Uniformes por Colegio - CRUD")
    win.geometry("350x650")

    # ----- CAMPOS -----
    tk.Label(win, text="ID pieza (Solo para actualizar o eliminar):").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    tk.Label(win, text="Tipo de uniforme:").pack()
    combo_tipo = ttk.Combobox(win, state="readonly")
    combo_tipo['values'] = [
        "Camisa de Diario", "Camibuso de Ed.Fisica",
        "Pantalón de Diario", "Sudadera",
        "Pantaloneta", "Jardinera"
    ]
    combo_tipo.pack()

    tk.Label(win, text="Color:").pack()
    entry_color = tk.Entry(win)
    entry_color.pack()

    tk.Label(win, text="Tipo de tela:").pack()
    combo_tela = ttk.Combobox(win, state="readonly")
    combo_tela['values'] = ["Algodón", "Poliéster", "Mezcla", "Lana"]
    combo_tela.pack()

    tk.Label(win, text="Lleva bordado (True/False):").pack()
    combo_bordado = ttk.Combobox(win, state="readonly")
    combo_bordado['values'] = ["True", "False"]
    combo_bordado.pack()

    tk.Label(win, text="Lugar del bordado:").pack()
    combo_lugar = ttk.Combobox(win, state="readonly")
    combo_lugar['values'] = ["True", "False"]
    combo_lugar.pack()


    tk.Label(win, text="Tipo de estampado:").pack()
    combo_estampa = ttk.Combobox(win, state="readonly")
    combo_estampa['values'] = ["Sublimación", "Transfer digital", "Serigrafía"]
    combo_estampa.pack()


    tk.Label(win, text="Borde de mangas:").pack()
    combo_mangas = ttk.Combobox(win, state="readonly")
    combo_mangas['values'] = ["Manga normal", "Manga con ribete", "Manga sin borde", "Manga dobladillo sencillo"]
    combo_mangas.pack()
 

    tk.Label(win, text="Borde de cuello:").pack()
    combo_cuello = ttk.Combobox(win, state="readonly")
    combo_cuello['values'] = ["Cuello redondo", "Cuello en V", "Cuello polo", "Cuello con ribete"]
    combo_cuello.pack()

    # ----- SELECT COLEGIOS -----
    tk.Label(win, text="Colegio:").pack()

    combo_colegio = ttk.Combobox(win, state="readonly")
    combo_colegio.pack()

    conn = conectar_bd()
    lista_ids = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_colegio, nombre_c FROM colegio ORDER BY nombre_c")
            datos = cursor.fetchall()

            lista_nombres = []
            for fila in datos:
                lista_ids.append(fila[0])
                lista_nombres.append(fila[1])

            combo_colegio['values'] = lista_nombres

        except Exception as e:
            messagebox.showerror("Error al cargar colegios", str(e))
        finally:
            cursor.close(); conn.close()

    def obtener_id_colegio():
        index = combo_colegio.current()
        if index == -1:
            return None
        return lista_ids[index]

    # 1️⃣ INSERTAR
    def guardar_uniforme():
        conn = conectar_bd()
        if conn is None: return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO pieza_uni(tipo_pieza, color, tipo_tela,
                                      lleva_bordado, lugar_bordado,
                                      tipo_estampa, borde_mangas, borde_cuello,
                                      id_colegio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                combo_tipo.get(),
                entry_color.get(),
                combo_tela.get(),
                combo_bordado.get(),
                combo_lugar.get(),
                combo_estampa.get(),
                combo_mangas.get(),
                combo_cuello.get(),
                obtener_id_colegio()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Uniforme guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Guardar", command=guardar_uniforme).pack(pady=5)

    # 2️⃣ ACTUALIZAR
    def actualizar_uniforme():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID.")
            return

        conn = conectar_bd()
        if conn is None: return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE pieza_uni
                SET tipo_pieza=%s, color=%s, tipo_tela=%s,
                    lleva_bordado=%s, lugar_bordado=%s,
                    tipo_estampa=%s, borde_mangas=%s, borde_cuello=%s,
                    id_colegio=%s
                WHERE id_pieza=%s
            """, (
                combo_tipo.get(),
                entry_color.get(),
                combo_tela.get(),
                combo_bordado.get(),
                combo_lugar.get(),
                combo_estampa.get(),
                combo_mangas.get(),
                combo_cuello.get(),
                obtener_id_colegio(),
                entry_id.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Uniforme actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_uniforme).pack(pady=5)

    # 3️⃣ ELIMINAR
    def eliminar_uniforme():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir un ID.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM pieza_uni WHERE id_pieza=%s", (entry_id.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Uniforme eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_uniforme).pack(pady=5)

    # 4️⃣ VER REGISTROS
    def ver_uniformes():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Uniformes")
        win_ver.geometry("700x400")

        text = tk.Text(win_ver, width=90, height=20)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM pieza_uni")
            filas = cursor.fetchall()

            text.insert(tk.END, "ID | Tipo | Color | Tela | Bordado | Lugar | Estampa | Mangas | Cuello | Colegio\n")
            text.insert(tk.END, "-------------------------------------------------------------------------------------------------\n")

            for f in filas:
                text.insert(tk.END, f"{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]} | {f[6]} | {f[7]} | {f[8]} | {f[9]}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_uniformes).pack(pady=5)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)
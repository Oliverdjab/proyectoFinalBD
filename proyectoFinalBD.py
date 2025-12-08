import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2


# -----------------------------------------------------
# FUNCIÓN: Conectar a PostgreSQL
# -----------------------------------------------------
def conectar_bd():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="proyecto final",
            user="postgres",
            password="oliverarboleda18*"
        )
        return conn
    except:
        messagebox.showerror("Error", "No se pudo conectar a PostgreSQL.")
        return None


# =====================================================
#  VENTANAS PARA INSERTAR DATOS EN TABLAS
# =====================================================

# ----------------------
# 1. Ventana COLEGIO
# ----------------------
def ventana_colegio():
    win = tk.Toplevel()
    win.title("Colegio - CRUD")
    win.geometry("300x320")

    # LABELS E INPUTS
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

    # ------------------------------
    # 1️⃣ GUARDAR (INSERT)
    # ------------------------------
    def guardar_colegio():
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO colegio(nombre_c, direccion, telefono) VALUES (%s, %s, %s)",
                (nombre, direccion, telefono)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Colegio guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Guardar", command=guardar_colegio).pack(pady=5)

    # ------------------------------
    # 2️⃣ ACTUALIZAR (UPDATE)
    # ------------------------------
    def actualizar_colegio():
        id_c = entry_id.get()
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()

        if id_c == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID del colegio.")
            return

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE colegio SET nombre_c=%s, direccion=%s, telefono=%s WHERE id_colegio=%s",
                (nombre, direccion, telefono, id_c)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Colegio actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_colegio).pack(pady=5)

    # ------------------------------
    # 3️⃣ ELIMINAR (DELETE)
    # ------------------------------
    def eliminar_colegio():
        id_c = entry_id.get()

        if id_c == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID para eliminar.")
            return

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM colegio WHERE id_colegio = %s", (id_c,))
            conn.commit()
            messagebox.showinfo("Éxito", "Colegio eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_colegio).pack(pady=5)

    # ------------------------------
    # 4️⃣ VOLVER
    # ------------------------------
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

        # ------------------------------
    # 4️⃣ VER REGISTROS (SELECT *)
    # ------------------------------
    def ver_registros_colegio():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Colegio")
        win_ver.geometry("400x300")

        text = tk.Text(win_ver, width=50, height=15)
        text.pack()

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM colegio")
            filas = cursor.fetchall()

            text.insert(tk.END, "ID | Nombre | Dirección | Teléfono\n")
            text.insert(tk.END, "-------------------------------------------\n")

            for fila in filas:
                linea = f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_registros_colegio).pack(pady=5)

    tk.Button(win, text="Uniformes por Colegio", command=ventana_uniforme).pack(pady=5)


# ----------------------
# 2. Ventana PROVEEDOR
# ----------------------
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

    tk.Label(win, text="NIT o documento:").pack()
    entry_documento = tk.Entry(win)
    entry_documento.pack()

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
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO proveedor(nit, nombre_p, direccion, telefono, nom_contacto)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                entry_documento.get(),
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
            cursor.close(); conn.close()

    tk.Button(win, text="Guardar", command=guardar_proveedor).pack(pady=5)

    # ---------------------------------
    # 2️⃣ ACTUALIZAR PROVEEDOR
    # ---------------------------------
    def actualizar_proveedor():
        if entry_nit.get() == "":
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
                entry_nit.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

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
            cursor.close(); conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_proveedor).pack(pady=5)

        # ------------------------------
    # VER REGISTROS PROVEEDOR
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
                linea = f"{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_registros_proveedor).pack(pady=5)

    tk.Button(win, text="Materia Prima", command=ventana_materia_prima).pack(pady=5)

    # ---------------------------------
    # BOTÓN VOLVER
    # ---------------------------------
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)


# ----------------------
# 3. Ventana CLIENTE
# ----------------------
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

    # -------------------------------
    # 1️⃣ INSERTAR CLIENTE
    # -------------------------------
    def guardar_cliente():
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO cliente(nombre, telefono)
                VALUES (%s, %s)
            """, (
                entry_nombre.get(),
                entry_telefono.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Guardar", command=guardar_cliente).pack(pady=5)

    # -------------------------------
    # 2️⃣ ACTUALIZAR CLIENTE
    # -------------------------------
    def actualizar_cliente():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE cliente
                SET nombre = %s, telefono = %s
                WHERE id_cliente = %s
            """, (
                entry_nombre.get(),
                entry_telefono.get(),
                entry_id.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_cliente).pack(pady=5)

    # -------------------------------
    # 3️⃣ ELIMINAR CLIENTE
    # -------------------------------
    def eliminar_cliente():
        id_c = entry_id.get()
        if id_c == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_c,))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_cliente).pack(pady=5)

        # ------------------------------
    # VER REGISTROS CLIENTE
    # ------------------------------
    def ver_registros_cliente():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Cliente")
        win_ver.geometry("350x300")

        text = tk.Text(win_ver, width=45, height=15)
        text.pack()

        conn = conectar_bd()
        if conn is None:
            return
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


    # -------------------------------
    # BOTÓN VOLVER
    # -------------------------------
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

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
    combo_tipo['values'] = ["Camisa de Diario", "Camibuso de Ed.Fisica", "Pantalón de Diario", "Sudadera", "Pantaloneta", "Jardinera"]
    combo_tipo.pack()


    tk.Label(win, text="Color:").pack()
    entry_color = tk.Entry(win)
    entry_color.pack()

    tk.Label(win, text="Tipo de tela:").pack()
    entry_tela = tk.Entry(win)
    entry_tela.pack()

    tk.Label(win, text="Lleva bordado (True/False):").pack()
    combo_bordado = ttk.Combobox(win, state="readonly")
    combo_bordado['values'] = ["True", "False"]
    combo_bordado.pack()

    tk.Label(win, text="Lugar del bordado:").pack()
    entry_lugar = tk.Entry(win)
    entry_lugar.pack()

    tk.Label(win, text="Tipo de estampado:").pack()
    entry_estampa = tk.Entry(win)
    entry_estampa.pack()

    tk.Label(win, text="Borde de mangas:").pack()
    entry_mangas = tk.Entry(win)
    entry_mangas.pack()

    tk.Label(win, text="Borde de cuello:").pack()
    entry_cuello = tk.Entry(win)
    entry_cuello.pack()

    # ----- SELECT COLEGIOS -----
    tk.Label(win, text="Colegio:").pack()

    combo_colegio = ttk.Combobox(win, state="readonly")
    combo_colegio.pack()

    # Cargar colegios desde PostgreSQL
    conn = conectar_bd()
    lista_ids = []   # lista interna para almacenar ID reales
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_colegio, nombre_c FROM colegio ORDER BY nombre_c")
            datos = cursor.fetchall()

            lista_nombres = []

            for fila in datos:
                lista_ids.append(fila[0])   # ID real
                lista_nombres.append(fila[1])  # Nombre visible

            combo_colegio['values'] = lista_nombres

        except Exception as e:
            messagebox.showerror("Error al cargar colegios", str(e))
        finally:
            cursor.close()
            conn.close()

    # Función para obtener el ID del colegio seleccionado
    def obtener_id_colegio():
        index = combo_colegio.current()
        if index == -1:
            return None
        return lista_ids[index]


    # =====================================================
    # 1️⃣ INSERTAR UNIFORME
    # =====================================================
    def guardar_uniforme():
        conn = conectar_bd()
        if conn is None:
            return

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
                entry_tela.get(),
                combo_bordado.get(),  
                entry_lugar.get(),
                entry_estampa.get(),
                entry_mangas.get(),
                entry_cuello.get(),
                obtener_id_colegio()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Uniforme guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Guardar", command=guardar_uniforme).pack(pady=5)

    # =====================================================
    # 2️⃣ ACTUALIZAR
    # =====================================================
    def actualizar_uniforme():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el ID.")
            return

        conn = conectar_bd()
        if conn is None:
            return

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
                #entry_tipo.get(),
                entry_color.get(),
                entry_tela.get(),
                #entry_bordado.get(),
                entry_lugar.get(),
                entry_estampa.get(),
                entry_mangas.get(),
                entry_cuello.get(),
                #entry_colegio.get(),
                entry_id.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Uniforme actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_uniforme).pack(pady=5)

    # =====================================================
    # 3️⃣ ELIMINAR
    # =====================================================
    def eliminar_uniforme():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir un ID.")
            return

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM pieza_uni WHERE id_pieza = %s",
                           (entry_id.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Uniforme eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_uniforme).pack(pady=5)

    # =====================================================
    # 4️⃣ VER REGISTROS
    # =====================================================
    def ver_uniformes():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Uniformes")
        win_ver.geometry("700x400")

        text = tk.Text(win_ver, width=90, height=20)
        text.pack()

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM pieza_uni")
            filas = cursor.fetchall()

            text.insert(tk.END, "ID | Tipo | Color | Tela | Bordado | Lugar | Estampa | Mangas | Cuello | Colegio\n")
            text.insert(tk.END, "-------------------------------------------------------------------------------------------------\n")

            for f in filas:
                linea = f"{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]} | {f[6]} | {f[7]} | {f[8]} | {f[9]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_uniformes).pack(pady=5)

    # =====================================================
    # 5️⃣ VOLVER
    # =====================================================
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

def generar_factura(num_factura, num_pedido):
    conn = conectar_bd()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Calcular el total según los productos incluidos
        cursor.execute("""
            SELECT SUM(pt.precio * i.cantidad)
            FROM incluye i
            JOIN producto_terminado pt ON i.cod_producto = pt.cod_producto
            WHERE i.num_pedido = %s
        """, (num_pedido,))
        total = cursor.fetchone()[0]

        if total is None:
            messagebox.showwarning("Sin productos", "El pedido no tiene productos asociados.")
            return False

        # Insertar factura
        cursor.execute("""
            INSERT INTO factura(num_factura, fecha, total, num_pedido)
            VALUES (%s, NOW(), %s, %s)
        """, (num_factura, total, num_pedido))

        conn.commit()
        messagebox.showinfo("Factura creada", f"Factura generada correctamente.\nTotal: {total}")
        return True

    except Exception as e:
        messagebox.showerror("Error al generar factura", str(e))
        return False

    finally:
        cursor.close()
        conn.close()

def descontar_inventario(num_pedido):
    conn = conectar_bd()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Obtener todos los productos de este pedido
        cursor.execute("""
            SELECT cod_producto, cantidad
            FROM incluye
            WHERE num_pedido = %s
        """, (num_pedido,))
        filas = cursor.fetchall()

        if not filas:
            messagebox.showwarning("Aviso", "Este pedido no tiene productos en INCLUYE.")
            return False

        # Recorrer cada producto y descontar stock
        for cod_producto, cantidad in filas:
            cursor.execute("""
                UPDATE producto_terminado
                SET existe_cantidad = existe_cantidad - %s
                WHERE cod_producto = %s
            """, (cantidad, cod_producto))

            # Opción: cambiar estado del producto a "disponible"
            cursor.execute("""
                UPDATE producto_terminado
                SET estado_p = 'disponible'
                WHERE cod_producto = %s
            """, (cod_producto,))

        conn.commit()
        messagebox.showinfo("Inventario actualizado", "El inventario fue descontado correctamente.")
        return True

    except Exception as e:
        messagebox.showerror("Error al descontar inventario", str(e))
        return False

    finally:
        cursor.close()
        conn.close()


def ventana_pedido():
    win = tk.Toplevel()
    win.title("Pedidos - CRUD")
    win.geometry("350x600")

    # ---- CAMPOS ----
    tk.Label(win, text="Número de pedido (PK):").pack()
    entry_num = tk.Entry(win)
    entry_num.pack()

    tk.Label(win, text="Fecha encargo (YYYY-MM-DD):").pack()
    entry_fencargo = tk.Entry(win)
    entry_fencargo.pack()

    tk.Label(win, text="Fecha entrega (YYYY-MM-DD):").pack()
    entry_fentrega = tk.Entry(win)
    entry_fentrega.pack()

    tk.Label(win, text="Detalles de medidas:").pack()
    entry_detalles = tk.Entry(win)
    entry_detalles.pack()

    tk.Label(win, text="Abono:").pack()
    entry_abono = tk.Entry(win)
    entry_abono.pack()

    tk.Label(win, text="Estado:").pack()
    entry_estado = tk.Entry(win)
    entry_estado.pack()

    tk.Label(win, text="ID Cliente:").pack()
    entry_cliente = tk.Entry(win)
    entry_cliente.pack()

    # =====================================================
    # 1️⃣ INSERTAR PEDIDO
    # =====================================================
    def guardar_pedido():
        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO pedido(num_pedido, fecha_encargo, fecha_entrega,
                                   detalles_medidas, abono, estado, id_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                entry_num.get(),
                entry_fencargo.get(),
                entry_fentrega.get(),
                entry_detalles.get(),
                entry_abono.get(),
                entry_estado.get(),
                entry_cliente.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Pedido guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Guardar", command=guardar_pedido).pack(pady=5)

    # =====================================================
    # 2️⃣ ACTUALIZAR PEDIDO
    # =====================================================
    def actualizar_pedido():
        if entry_num.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el número de pedido.")
            return

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE pedido
                SET fecha_encargo=%s, fecha_entrega=%s, detalles_medidas=%s,
                    abono=%s, estado=%s, id_cliente=%s
                WHERE num_pedido=%s
            """, (
                entry_fencargo.get(),
                entry_fentrega.get(),
                entry_detalles.get(),
                entry_abono.get(),
                entry_estado.get(),
                entry_cliente.get(),
                entry_num.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Pedido actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_pedido).pack(pady=5)

    # =====================================================
    # 3️⃣ ELIMINAR PEDIDO
    # =====================================================
    def eliminar_pedido():
        if entry_num.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el número de pedido.")
            return

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM pedido WHERE num_pedido=%s",
                           (entry_num.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_pedido).pack(pady=5)

    # =====================================================
    # 4️⃣ VER REGISTROS
    # =====================================================
    def ver_pedidos():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Pedidos")
        win_ver.geometry("700x400")

        text = tk.Text(win_ver, width=90, height=20)
        text.pack()

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM pedido")
            filas = cursor.fetchall()

            text.insert(tk.END, "N° | Encargo | Entrega | Detalles | Abono | Estado | Cliente\n")
            text.insert(tk.END, "-----------------------------------------------------------------------\n")

            for f in filas:
                linea = f"{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]} | {f[6]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_pedidos).pack(pady=5)


        # =====================================================
    # 5️⃣ CAMBIAR ESTADO DEL PEDIDO (NUEVO)
    # =====================================================
    def cambiar_estado():
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE pedido SET estado=%s WHERE num_pedido=%s",
                           (entry_estado.get(), entry_num.get()))
            conn.commit()
            messagebox.showinfo("OK", "Estado actualizado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Cambiar Estado", command=cambiar_estado).pack(pady=5)

    # =====================================================
    # 6️⃣ AÑADIR PRODUCTOS (INCLUYE)
    # =====================================================
    tk.Button(win, text="Agregar productos (INCLUYE)",
              command=ventana_incluye).pack(pady=10)

    # =====================================================
    # 7️⃣ FACTURAR + DESCONTAR INVENTARIO + ENTREGAR
    # =====================================================
    tk.Label(win, text="Número de factura:").pack()
    entry_factura = tk.Entry(win)
    entry_factura.pack()

    def facturar_y_entregar():
        num_fact = entry_factura.get()
        num_pedido = entry_num.get()

        if num_fact == "" or num_pedido == "":
            messagebox.showwarning("Aviso", "Debes llenar pedido y factura.")
            return

        generar_factura(num_fact, num_pedido)
        descontar_inventario(num_pedido)

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("UPDATE pedido SET estado='Entregado' WHERE num_pedido=%s",
                       (num_pedido,))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("OK", "Pedido entregado y factura generada.")

    tk.Button(win, text="Facturar y Entregar",
            command=facturar_y_entregar, bg="green", fg="white").pack(pady=15)

    # =====================================================
    # 5️⃣ VOLVER
    # =====================================================
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

def ventana_factura():
    win = tk.Toplevel()
    win.title("Factura - CRUD")
    win.geometry("350x500")

    # ---- CAMPOS ----
    tk.Label(win, text="Número de factura (PK):").pack()
    entry_num = tk.Entry(win)
    entry_num.pack()

    tk.Label(win, text="Fecha De entrega (YYYY-MM-DD):").pack()
    entry_fecha = tk.Entry(win)
    entry_fecha.pack()

    tk.Label(win, text="Total:").pack()
    entry_total = tk.Entry(win)
    entry_total.pack()

    tk.Label(win, text="Número de pedido (FK):").pack()
    entry_pedido = tk.Entry(win)
    entry_pedido.pack()

    # =====================================================
    # 1️⃣ INSERTAR FACTURA
    # =====================================================
    def guardar_factura():
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO factura(num_factura, fecha, total, num_pedido)
                VALUES (%s, %s, %s, %s)
            """, (
                entry_num.get(),
                entry_fecha.get(),
                entry_total.get(),
                entry_pedido.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Factura guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Guardar", command=guardar_factura).pack(pady=5)

    # =====================================================
    # 2️⃣ ACTUALIZAR FACTURA
    # =====================================================
    def actualizar_factura():
        if entry_num.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el número de factura.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE factura
                SET fecha=%s, total=%s, num_pedido=%s
                WHERE num_factura=%s
            """, (
                entry_fecha.get(),
                entry_total.get(),
                entry_pedido.get(),
                entry_num.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Factura actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_factura).pack(pady=5)

    # =====================================================
    # 3️⃣ ELIMINAR FACTURA
    # =====================================================
    def eliminar_factura():
        if entry_num.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el número de factura.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM factura WHERE num_factura=%s",
                           (entry_num.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Factura eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_factura).pack(pady=5)

    # =====================================================
    # 4️⃣ VER REGISTROS
    # =====================================================
    def ver_facturas():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Facturas")
        win_ver.geometry("700x400")

        text = tk.Text(win_ver, width=90, height=20)
        text.pack()

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM factura")
            filas = cursor.fetchall()

            text.insert(tk.END, "N° Factura | Fecha | Total | N° Pedido\n")
            text.insert(tk.END, "-----------------------------------------------\n")

            for f in filas:
                linea = f"{f[0]} | {f[1]} | {f[2]} | {f[3]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_facturas).pack(pady=5)

    # =====================================================
    # 5️⃣ VOLVER
    # =====================================================
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

def ventana_materia_prima():
    win = tk.Toplevel()
    win.title("Inventario de Materias Primas - CRUD")
    win.geometry("350x650")

    # ---- CAMPOS ----
    tk.Label(win, text="Código materia (PK):").pack()
    entry_cod = tk.Entry(win)
    entry_cod.pack()

    tk.Label(win, text="Tipo:").pack()
    entry_tipo = tk.Entry(win)
    entry_tipo.pack()

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

    # Función para obtener el ID del colegio seleccionado
    def obtener_id_proveedor():
        index = combo_proveedor.current()
        if index == -1:
            return None
        return lista_ids[index]

    # =====================================================
    # 1️⃣ INSERTAR MATERIA PRIMA
    # =====================================================
    def guardar_mp():
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO materia_prima(tipo, description,
                                          cantidad, unidad_medida, nit)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                entry_tipo.get(),
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
                entry_tipo.get(),
                entry_desc.get(),
                entry_cant.get(),
                #entry_unidad.get(),
                #entry_nit.get(),
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

    tk.Button(win, text="Ver registros", command=ver_mp).pack(pady=5)

    # =====================================================
    # 5️⃣ VOLVER
    # =====================================================
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)



def ventana_producto():
    win = tk.Toplevel()
    win.title("Inventario de Producto Terminado - CRUD")
    win.geometry("350x650")

    # ---- CAMPOS ----
    tk.Label(win, text="Código producto (PK):").pack()
    entry_cod = tk.Entry(win)
    entry_cod.pack()

    tk.Label(win, text="Descripción:").pack()
    entry_desc = tk.Entry(win)
    entry_desc.pack()

    tk.Label(win, text="Talla:").pack()
    entry_talla = tk.Entry(win)
    entry_talla.pack()

    tk.Label(win, text="Sexo:").pack()
    entry_sexo = tk.Entry(win)
    entry_sexo.pack()

    tk.Label(win, text="Precio:").pack()
    entry_precio = tk.Entry(win)
    entry_precio.pack()

    tk.Label(win, text="Cantidad existente:").pack()
    entry_cant = tk.Entry(win)
    entry_cant.pack()

    tk.Label(win, text="Estado del producto:").pack()
    entry_estado = tk.Entry(win)
    entry_estado.pack()

    tk.Label(win, text="ID de la pieza (FK):").pack()
    entry_pieza = tk.Entry(win)
    entry_pieza.pack()

    # =====================================================
    # 1️⃣ INSERTAR PRODUCTO
    # =====================================================
    def guardar_producto():
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO producto_terminado(cod_producto, descripcion, talla,
                                               sexo, precio, existe_cantidad,
                                               estado_p, id_pieza)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                entry_cod.get(),
                entry_desc.get(),
                entry_talla.get(),
                entry_sexo.get(),
                entry_precio.get(),
                entry_cant.get(),
                entry_estado.get(),
                entry_pieza.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Guardar", command=guardar_producto).pack(pady=5)

    # =====================================================
    # 2️⃣ ACTUALIZAR PRODUCTO
    # =====================================================
    def actualizar_producto():
        if entry_cod.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el código del producto.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE producto_terminado
                SET descripcion=%s, talla=%s, sexo=%s,
                    precio=%s, existe_cantidad=%s,
                    estado_p=%s, id_pieza=%s
                WHERE cod_producto=%s
            """, (
                entry_desc.get(),
                entry_talla.get(),
                entry_sexo.get(),
                entry_precio.get(),
                entry_cant.get(),
                entry_estado.get(),
                entry_pieza.get(),
                entry_cod.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_producto).pack(pady=5)

    # =====================================================
    # 3️⃣ ELIMINAR PRODUCTO
    # =====================================================
    def eliminar_producto():
        if entry_cod.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el código del producto.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM producto_terminado WHERE cod_producto=%s",
                           (entry_cod.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto eliminado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_producto).pack(pady=5)

    # =====================================================
    # 4️⃣ VER REGISTROS
    # =====================================================
    def ver_productos():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Productos Terminados")
        win_ver.geometry("750x400")

        text = tk.Text(win_ver, width=95, height=20)
        text.pack()

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM producto_terminado")
            filas = cursor.fetchall()

            text.insert(tk.END, "COD | Desc | Talla | Sexo | Precio | Cant | Estado | ID Pieza\n")
            text.insert(tk.END, "------------------------------------------------------------------------------\n")

            for f in filas:
                linea = f"{f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]} | {f[6]} | {f[7]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_productos).pack(pady=5)

    # =====================================================
    # 5️⃣ VOLVER
    # =====================================================
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)



def ventana_incluye():
    inc = tk.Toplevel()
    inc.title("Agregar Productos a Pedido (INCLUYE)")
    inc.geometry("400x350")

    tk.Label(inc, text="Asignar Producto a Pedido", font=("Arial", 13)).pack(pady=10)

    # NUM_PEDIDO
    tk.Label(inc, text="Número del Pedido:").pack()
    entry_num_pedido = tk.Entry(inc)
    entry_num_pedido.pack()

    # COD_PRODUCTO
    tk.Label(inc, text="Código del Producto:").pack()
    entry_cod_producto = tk.Entry(inc)
    entry_cod_producto.pack()

    # CANTIDAD
    tk.Label(inc, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(inc)
    entry_cantidad.pack()

    # -------------------------------
    # Función INSERT a la tabla INCLUYE
    # -------------------------------
    def guardar_incluye():
        num = entry_num_pedido.get()
        prod = entry_cod_producto.get()
        cant = entry_cantidad.get()

        if num == "" or prod == "" or cant == "":
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        # Actualizar estado del producto
        cursor.execute(
            "UPDATE producto_terminado SET estado_p = 'encargado' WHERE cod_producto = %s",
            (prod,)
        )
        conn.commit()


        try:
            cursor.execute(
                "INSERT INTO incluye (num_pedido, cod_producto, cantidad) VALUES (%s, %s, %s)",
                (num, prod, cant)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado al pedido.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    # Botón guardar
    tk.Button(inc, text="Guardar", command=guardar_incluye).pack(pady=10)

    # -------------------------------
    # Función para VER registros
    # -------------------------------
    def ver_incluye():
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM incluye")
            datos = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            cursor.close()
            conn.close()
            return

        cursor.close()
        conn.close()

        # Crear ventana para mostrar datos
        vista = tk.Toplevel()
        vista.title("Registros de INCLUYE")
        vista.geometry("400x300")

        tk.Label(vista, text="Registros en la tabla INCLUYE", font=("Arial", 12)).pack(pady=10)

        texto = tk.Text(vista, width=45, height=10)
        texto.pack()

        for fila in datos:
            texto.insert(tk.END, f"Pedido: {fila[0]} | Producto: {fila[1]} | Cantidad: {fila[2]}\n")

        tk.Button(vista, text="Cerrar", command=vista.destroy).pack(pady=10)

    # Botón ver registros
    tk.Button(inc, text="Ver Registros", command=ver_incluye).pack(pady=5)

    # Botón volver
    tk.Button(inc, text="Volver", command=inc.destroy).pack(pady=15)

def ventana_utiliza():
    util = tk.Toplevel()
    util.title("Asociar Materia Prima a Uniforme (UTILIZA)")
    util.geometry("400x320")

    tk.Label(util, text="Asignar Materia Prima a Pieza de Uniforme", font=("Arial", 12)).pack(pady=10)

    # ID_PIEZA
    tk.Label(util, text="ID de la Pieza (Uniforme):").pack()
    entry_id_pieza = tk.Entry(util)
    entry_id_pieza.pack()

    # COD_MATERIA
    tk.Label(util, text="Código Materia Prima:").pack()
    entry_cod_materia = tk.Entry(util)
    entry_cod_materia.pack()

    # INSERT (guardar)
    def guardar_utiliza():
        id_pz = entry_id_pieza.get()
        mat = entry_cod_materia.get()

        if id_pz == "" or mat == "":
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO utiliza (id_pieza, cod_materia) VALUES (%s, %s)",
                (id_pz, mat)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Materia prima asociada a la pieza.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(util, text="Guardar", command=guardar_utiliza).pack(pady=10)

    # VER registros
    def ver_utiliza():
        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM utiliza")
            datos = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            cursor.close()
            conn.close()
            return

        cursor.close()
        conn.close()

        # Ventana para mostrar resultados
        vista = tk.Toplevel()
        vista.title("Registros UTILIZA")
        vista.geometry("380x300")

        tk.Label(vista, text="Relaciones UTILIZA (Pieza - Materia)", font=("Arial", 12)).pack(pady=10)

        text = tk.Text(vista, width=45, height=10)
        text.pack()

        for fila in datos:
            text.insert(tk.END, f"Pieza: {fila[0]}  |  Materia: {fila[1]} \n")

        tk.Button(vista, text="Cerrar", command=vista.destroy).pack(pady=10)

    tk.Button(util, text="Ver Registros", command=ver_utiliza).pack(pady=5)

    # VOLVER
    tk.Button(util, text="Volver", command=util.destroy).pack(pady=15)

def ventana_cambiar_estado():
    v = tk.Toplevel()
    v.title("Cambiar Estado del Pedido")
    v.geometry("350x250")

    tk.Label(v, text="Cambiar Estado", font=("Arial", 13)).pack(pady=10)

    tk.Label(v, text="Número de Pedido:").pack()
    entry_num = tk.Entry(v)
    entry_num.pack()

    tk.Label(v, text="Nuevo Estado:").pack()
    entry_estado = tk.Entry(v)
    entry_estado.pack()

    def cambiar_estado():
        num = entry_num.get()
        est = entry_estado.get()

        if num == "" or est == "":
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE pedido SET estado = %s WHERE num_pedido = %s",
                (est, num)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Estado actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(v, text="Actualizar Estado", command=cambiar_estado).pack(pady=15)
    tk.Button(v, text="Volver", command=v.destroy).pack()

def ventana_factura_auto():
    f = tk.Toplevel()
    f.title("Crear Factura")
    f.geometry("350x300")

    tk.Label(f, text="Crear Factura", font=("Arial", 13)).pack(pady=10)

    tk.Label(f, text="Número de Factura:").pack()
    entry_num_factura = tk.Entry(f)
    entry_num_factura.pack()

    tk.Label(f, text="Número de Pedido:").pack()
    entry_num_pedido = tk.Entry(f)
    entry_num_pedido.pack()

    def crear_factura():
        num_fact = entry_num_factura.get()
        num_pedido = entry_num_pedido.get()

        if num_fact == "" or num_pedido == "":
            messagebox.showwarning("Campos vacíos", "Todos los campos son necesarios.")
            return

        conn = conectar_bd()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            # 1 — Obtener total del pedido
            cursor.execute("""
                SELECT SUM(pt.precio * i.cantidad)
                FROM incluye i
                JOIN producto_terminado pt ON i.cod_producto = pt.cod_producto
                WHERE i.num_pedido = %s
            """, (num_pedido,))

            total = cursor.fetchone()[0]

            if total is None:
                messagebox.showwarning("Sin productos",
                    "Este pedido no tiene productos asociados.")
                return

            # 2 — Insertar factura
            cursor.execute(
                "INSERT INTO factura (num_factura, fecha, total, num_pedido) VALUES (%s, NOW(), %s, %s)",
                (num_fact, total, num_pedido)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Factura creada.\nTotal: ${total}")

            # 3 — Descontar del inventario los productos entregados
            cursor.execute("""
                SELECT cod_producto, cantidad 
                FROM incluye
                WHERE num_pedido = %s
            """, (num_pedido,))
            productos = cursor.fetchall()

            for cod, cant in productos:
                cursor.execute("""
                    UPDATE producto_terminado
                    SET existe_cantidad = existe_cantidad - %s,
                        estado_p = 'disponible'
                    WHERE cod_producto = %s
                """, (cant, cod))

            # 4 — Cambiar el estado del pedido a ENTREGADO
            cursor.execute("""
                UPDATE pedido 
                SET estado = 'Entregado'
                WHERE num_pedido = %s
            """, (num_pedido,))


            

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            cursor.close()
            conn.close()

    tk.Button(f, text="Crear Factura", command=crear_factura).pack(pady=15)
    tk.Button(f, text="Volver", command=f.destroy).pack()


# =====================================================
# VENTANA PRINCIPAL
# =====================================================
def ventana_principal(nombre_usuario):
    principal = tk.Toplevel()
    principal.title("Ventana Principal")
    principal.geometry("400x500")

    saludo = tk.Label(principal, text=f"Bienvenido, {nombre_usuario}", font=("Arial", 12))
    saludo.pack(pady=20)

    btn_cliente = tk.Button(principal, text="Cliente", command=ventana_cliente)
    btn_cliente.pack(pady=10)

    btn_proovedor = tk.Button(principal, text="Proveedor", command=ventana_proveedor)
    btn_proovedor.pack(pady=10)

    btn_colegio = tk.Button(principal, text="Colegio", command=ventana_colegio)
    btn_colegio.pack(pady=10)

    btn_producto = tk.Button(principal, text="Inventario Producto Terminado", command=ventana_producto)
    btn_producto.pack(pady=10)
    
    btn_pedido = tk.Button(principal, text="Pedido", command=ventana_pedido)
    btn_pedido.pack(pady=10)

    btn_estado = tk.Button(principal, text="Cambiar Estado Pedido", command=ventana_cambiar_estado)
    btn_estado.pack(pady=10)

    btn_factura = tk.Button(principal, text="Factura", command=ventana_factura)
    btn_factura.pack(pady=10)

    

    btn_utiliza = tk.Button(principal, text="Utiliza", command=ventana_utiliza)
    btn_utiliza.pack(pady=10)


    

    btn_incluye = tk.Button(principal, text="Incluye", command=ventana_incluye)
    btn_incluye.pack(pady=10)

    

    btn_facturar = tk.Button(principal, text="Facturar Pedido", command=ventana_factura_auto)
    btn_facturar.pack(pady=10)

    btn_inf = tk.Button(principal, text="Informes")
    btn_inf.pack(pady=10)

    btn_salir = tk.Button(principal, text="Salir", command=principal.destroy)
    btn_salir.pack(pady=10)


# =====================================================
# LOGIN
# =====================================================
def iniciar_sesion():
    nombre = entry_usuario.get()
    clave = entry_contra.get()

    conn = conectar_bd()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT contraseña FROM usuario WHERE nombre_usuario = %s",
            (nombre,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            messagebox.showwarning("Aviso", "El usuario no existe.")
        else:
            contraseña_correcta = resultado[0]

            if clave == contraseña_correcta:
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
    global entry_usuario, entry_contra

    ventana = tk.Tk()
    ventana.title("Login")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Usuario:").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    tk.Label(ventana, text="Contraseña:").pack()
    entry_contra = tk.Entry(ventana, show="*")
    entry_contra.pack()

    tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    crear_login()
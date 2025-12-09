import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd
from controladora import generar_factura, descontar_inventario

def ventana_pedido():
    win = tk.Toplevel()
    win.title("Pedido - CRUD")
    win.geometry("420x620")

    # =====================================================
    # NUM PEDIDO: SOLO PARA ACTUALIZAR / ELIMINAR
    # =====================================================
    tk.Label(win, text="Número de Pedido (para actualizar o eliminar):").pack()
    entry_num = tk.Entry(win)
    entry_num.pack()

    # =====================================================
    # CAMPOS REALES DE LA TABLA
    # =====================================================
    tk.Label(win, text="Fecha Encargo (YYYY-MM-DD):").pack()
    entry_fecha_enc = tk.Entry(win)
    entry_fecha_enc.pack()

    tk.Label(win, text="Fecha Entrega (YYYY-MM-DD):").pack()
    entry_fecha_ent = tk.Entry(win)
    entry_fecha_ent.pack()

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
    # 1️⃣ GUARDAR
    # =====================================================
    def guardar_pedido():

        if entry_fecha_enc.get().strip() == "" or entry_estado.get().strip() == "" or entry_cliente.get().strip() == "":
            messagebox.showwarning("Aviso", "Fecha encargo, estado e ID cliente son obligatorios.")
            return

        if not entry_cliente.get().isdigit():
            messagebox.showwarning("Aviso", "ID Cliente debe ser un número.")
            return

        abono = entry_abono.get().strip()
        if abono == "":
            abono = None

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO pedido(fecha_encargo, fecha_entrega,
                                   detalles_medidas, abono, estado, id_cliente)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                entry_fecha_enc.get(),
                entry_fecha_ent.get(),
                entry_detalles.get(),
                abono,
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
    # 2️⃣ ACTUALIZAR
    # =====================================================
    def actualizar_pedido():
        if entry_num.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el número de pedido.")
            return

        abono = entry_abono.get().strip()
        if abono == "":
            abono = None

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE pedido
                SET fecha_encargo=%s, fecha_entrega=%s,
                    detalles_medidas=%s, abono=%s,
                    estado=%s, id_cliente=%s
                WHERE num_pedido=%s
            """, (
                entry_fecha_enc.get(),
                entry_fecha_ent.get(),
                entry_detalles.get(),
                abono,
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
    # 3️⃣ ELIMINAR
    # =====================================================
    def eliminar_pedido():
        if entry_num.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el número del pedido.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM pedido WHERE num_pedido=%s", (entry_num.get(),))
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
        win_ver.title("Registros Pedido")
        win_ver.geometry("800x400")

        text = tk.Text(win_ver, width=110, height=20)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM pedido ORDER BY num_pedido")
            filas = cursor.fetchall()

            text.insert(tk.END, "N° | Encargo | Entrega | Detalles | Abono | Estado | Cliente\n")
            text.insert(tk.END, "----------------------------------------------------------------------------------------------\n")

            for fila in filas:
                linea = f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} | {fila[4]} | {fila[5]} | {fila[6]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_pedidos).pack(pady=10)


    # =====================================================
    # 5️⃣ FACTURAR + ENTREGAR
    #    (YA NO HAY CAMPOS EXTRAS AQUÍ)
    # =====================================================
        # =====================================================
    # 5️⃣ FACTURAR Y ENTREGAR (usa el mismo num_pedido)
    # =====================================================

    tk.Label(win, text="Número de factura:").pack()
    entry_factura = tk.Entry(win)
    entry_factura.pack()

    def facturar_y_entregar():
        num_pedido = entry_num.get().strip()
        num_factura = entry_factura.get().strip()

        if num_pedido == "" or num_factura == "":
            messagebox.showwarning("Aviso", "Debes escribir el número de pedido y la factura.")
            return

        # 1. Generar factura
        ok = generar_factura(num_factura, num_pedido)
        if not ok:
            return  # generar_factura ya muestra el error

        # 2. Descontar inventario
        descontar_inventario(num_pedido)

        # 3. Cambiar estado del pedido a ENTREGADO
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pedido
            SET estado = 'Entregado'
            WHERE num_pedido = %s
        """, (num_pedido,))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("OK", "Factura generada y pedido marcado como ENTREGADO.")

    tk.Button(win, text="Facturar y Entregar",
              bg="green", fg="white",
              command=facturar_y_entregar).pack(pady=15)



    # =====================================================
    # 6️⃣ VER FACTURAS
    # =====================================================
    def ver_facturas():
        win_ver = tk.Toplevel()
        win_ver.title("Facturas")
        win_ver.geometry("700x400")

        text = tk.Text(win_ver, width=90, height=20)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM factura")
            filas = cursor.fetchall()

            text.insert(tk.END, "Factura | Fecha | Total | Pedido\n")
            text.insert(tk.END, "---------------------------------------\n")

            for f in filas:
                text.insert(tk.END, f"{f[0]} | {f[1]} | {f[2]} | {f[3]}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver Facturas", command=ver_facturas).pack(pady=5)


    # =====================================================
    # 7️⃣ VOLVER
    # =====================================================
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

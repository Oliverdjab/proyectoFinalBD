import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd
from vistas.incluye_view import ventana_incluye
from vistas.utiliza_view import ventana_utiliza

def ventana_producto():
    win = tk.Toplevel()
    win.title("Inventario Producto Terminado")
    win.geometry("350x580")

    # CAMPOS
    tk.Label(win, text="Código Producto (solo para actualizar/eliminar):").pack()
    entry_codigo = tk.Entry(win)
    entry_codigo.pack()

    tk.Label(win, text="Descripción:").pack()
    entry_descripcion = tk.Entry(win)
    entry_descripcion.pack()

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
    entry_existencia = tk.Entry(win)
    entry_existencia.pack()

    tk.Label(win, text="Estado:").pack()
    entry_estado = tk.Entry(win)
    entry_estado.pack()

    tk.Label(win, text="ID pieza (uniforme):").pack()
    entry_idpieza = tk.Entry(win)
    entry_idpieza.pack()

    # =========================================================
    # GUARDAR PRODUCTO
    # =========================================================
    def guardar_producto():
        # Validar que no estén vacíos
        if entry_descripcion.get() == "" or entry_talla.get() == "" or entry_sexo.get() == "" \
        or entry_precio.get() == "" or entry_existencia.get() == "" or entry_estado.get() == "" \
        or entry_idpieza.get() == "":
            messagebox.showwarning("Aviso", "Todos los campos excepto código son obligatorios.")
            return

        try:
            precio = float(entry_precio.get())
            existencia = int(entry_existencia.get())
            id_pieza = int(entry_idpieza.get())
        except:
            messagebox.showerror("Error", "Precio, existencia e ID pieza deben ser numéricos.")
            return

        conn = conectar_bd()
        if conn is None: return
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO producto_terminado(descripcion, talla, sexo, precio, existe_cantidad, estado_p, id_pieza)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                entry_descripcion.get(),
                entry_talla.get(),
                entry_sexo.get(),
                precio,
                existencia,
                entry_estado.get(),
                id_pieza
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Guardar", command=guardar_producto).pack(pady=5)

    # =========================================================
    # ACTUALIZAR PRODUCTO
    # =========================================================
    def actualizar_producto():
        if entry_codigo.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el código para actualizar.")
            return
        
        try:
            precio = float(entry_precio.get())
            existencia = int(entry_existencia.get())
            id_pieza = int(entry_idpieza.get())
        except:
            messagebox.showerror("Error", "Precio, existencia e ID pieza deben ser numéricos.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE producto_terminado
                SET descripcion=%s, talla=%s, sexo=%s, precio=%s,
                    existe_cantidad=%s, estado_p=%s, id_pieza=%s
                WHERE cod_producto=%s
            """, (
                entry_descripcion.get(), entry_talla.get(), entry_sexo.get(),
                precio, existencia, entry_estado.get(), id_pieza,
                entry_codigo.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_producto).pack(pady=5)

    # =========================================================
    # ELIMINAR PRODUCTO
    # =========================================================
    def eliminar_producto():
        if entry_codigo.get() == "":
            messagebox.showwarning("Aviso", "Debes escribir el código para eliminar.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM producto_terminado WHERE cod_producto=%s", (entry_codigo.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_producto).pack(pady=5)

    # =========================================================
    # VER REGISTROS
    # =========================================================
    def ver_productos():
        win_ver = tk.Toplevel()
        win_ver.title("Registros Producto Terminado")
        win_ver.geometry("450x400")

        text = tk.Text(win_ver, width=60, height=20)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM producto_terminado")
            filas = cursor.fetchall()

            text.insert(tk.END, "Cod | Desc | Talla | Sexo | Precio | Exist | Estado | Pieza\n")
            text.insert(tk.END, "---------------------------------------------------------------\n")

            for fila in filas:
                linea = f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} | {fila[4]} | {fila[5]} | {fila[6]} | {fila[7]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack()

    tk.Button(win, text="Ver registros", command=ver_productos).pack(pady=5)

    # BOTONES A INCLUYE Y UTILIZA
    tk.Button(win, text="Incluir Productos a Pedido", command=ventana_incluye).pack(pady=5)
    tk.Button(win, text="Utilizar Materia Prima", command=ventana_utiliza).pack(pady=5)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd

def ventana_uniforme():
    win = tk.Toplevel()
    win.title("Uniformes por Colegio - CRUD")
    win.geometry("350x650")

    # CAMPOS
    tk.Label(win, text="ID pieza (Solo para actualizar o eliminar):").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()

    tk.Label(win, text="Tipo de pieza:").pack()
    entry_tipo = tk.Entry(win)
    entry_tipo.pack()

    tk.Label(win, text="Talla:").pack()
    entry_talla = tk.Entry(win)
    entry_talla.pack()

    tk.Label(win, text="Color:").pack()
    entry_color = tk.Entry(win)
    entry_color.pack()

    tk.Label(win, text="Valor unitario:").pack()
    entry_valor = tk.Entry(win)
    entry_valor.pack()

    tk.Label(win, text="ID Colegio:").pack()
    entry_id_colegio = tk.Entry(win)
    entry_id_colegio.pack()

    # GUARDAR
    def guardar_uniforme():
        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO uniforme(tipo_pieza, talla, color, valor_u, id_colegio)
                VALUES (%s, %s, %s, %s, %s)
            """, (entry_tipo.get(), entry_talla.get(), entry_color.get(),
                  entry_valor.get(), entry_id_colegio.get()))

            conn.commit()
            messagebox.showinfo("Éxito", "Pieza de uniforme guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Guardar", command=guardar_uniforme).pack(pady=5)

    # ACTUALIZAR
    def actualizar_uniforme():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes ingresar el ID de la pieza.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE uniforme
                SET tipo_pieza=%s, talla=%s, color=%s, valor_u=%s, id_colegio=%s
                WHERE id_pieza=%s
            """, (entry_tipo.get(), entry_talla.get(), entry_color.get(),
                  entry_valor.get(), entry_id_colegio.get(), entry_id.get()))
            conn.commit()

            messagebox.showinfo("Éxito", "Pieza de uniforme actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Actualizar", command=actualizar_uniforme).pack(pady=5)

    # ELIMINAR
    def eliminar_uniforme():
        if entry_id.get() == "":
            messagebox.showwarning("Aviso", "Debes ingresar el ID de la pieza.")
            return

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM uniforme WHERE id_pieza=%s", (entry_id.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Pieza eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

    tk.Button(win, text="Eliminar", command=eliminar_uniforme).pack(pady=5)

    # VER REGISTROS
    def ver_registros_uniforme():
        win_ver = tk.Toplevel()
        win_ver.title("Registros de Uniformes")
        win_ver.geometry("400x400")

        text = tk.Text(win_ver, width=50, height=20)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM uniforme")
            filas = cursor.fetchall()

            text.insert(tk.END, "ID | Tipo | Talla | Color | Valor | Colegio\n")
            text.insert(tk.END, "---------------------------------------------------\n")

            for fila in filas:
                linea = f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} | {fila[4]} | {fila[5]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close(); conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_registros_uniforme).pack(pady=5)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

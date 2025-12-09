import tkinter as tk
from tkinter import messagebox
from conexion import conectar_bd

def ventana_utiliza():
    win = tk.Toplevel()
    win.title("Utilizar Materia Prima")
    win.geometry("350x330")

    # CAMPOS
    tk.Label(win, text="ID pieza (uniforme):").pack()
    entry_pieza = tk.Entry(win)
    entry_pieza.pack()

    tk.Label(win, text="Código de materia prima:").pack()
    entry_materia = tk.Entry(win)
    entry_materia.pack()

    # GUARDAR RELACIÓN UTILIZA
    def guardar_utiliza():
        if entry_pieza.get() == "" or entry_materia.get() == "":
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios.")
            return

        try:
            id_pieza = int(entry_pieza.get())
            cod_materia = int(entry_materia.get())
        except:
            messagebox.showerror("Error", "Los datos deben ser numéricos.")
            return

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO utiliza(id_pieza, cod_materia)
                VALUES (%s, %s)
            """, (id_pieza, cod_materia))

            conn.commit()
            messagebox.showinfo("Éxito", "Relación guardada correctamente.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Guardar", command=guardar_utiliza).pack(pady=5)

    # VER REGISTROS
    def ver_utiliza():
        win_ver = tk.Toplevel()
        win_ver.title("Registros UTILIZA")
        win_ver.geometry("450x300")

        text = tk.Text(win_ver, width=60, height=15)
        text.pack()

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM utiliza")
            filas = cursor.fetchall()

            text.insert(tk.END, "ID Pieza | Cod. Materia\n")
            text.insert(tk.END, "-------------------------------\n")

            for fila in filas:
                linea = f"{fila[0]} | {fila[1]}\n"
                text.insert(tk.END, linea)

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            cursor.close()
            conn.close()

        tk.Button(win_ver, text="Volver", command=win_ver.destroy).pack(pady=5)

    tk.Button(win, text="Ver registros", command=ver_utiliza).pack(pady=5)

    tk.Button(win, text="Volver", command=win.destroy).pack(pady=10)

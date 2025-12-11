import psycopg2
from tkinter import messagebox

def conectar_bd():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="proyecto_final",
            user="postgres",
            password="admin"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a PostgreSQL.\n{e}")
        return None
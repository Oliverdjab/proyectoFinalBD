import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar_bd


def ventana_informes():
    win = tk.Toplevel()
    win.title("Informes del Sistema")
    win.geometry("350x400")

    tk.Label(win, text="Seleccione un informe:", font=("Arial", 12)).pack(pady=10)

    tk.Button(
        win,
        text="Productos Pendientes por Entregar",
        command=informe_productos_pendientes
    ).pack(pady=10)
    
    tk.Button(
        win,
        text="Productos por Cliente (No entregados)",
        command=informe_por_cliente
    ).pack(pady=10)

    tk.Button(
        win,
        text="Existencias Reales de Productos",
        command=informe_existencias_reales
    ).pack(pady=10)

    tk.Button(
        win,
        text="Listado de Colegios",
        command=informe_listado_colegios
    ).pack(pady=10)

    tk.Button(
        win,
        text="Uniformes por Colegio",
        command=informe_uniformes_por_colegio
    ).pack(pady=10)

    tk.Button(
        win,
        text="Total Vendido por Colegio",
        command=informe_total_vendido_por_colegio
    ).pack(pady=10)

    tk.Button(
        win,
        text="Total General de Ventas",
        command=informe_total_general_ventas
    ).pack(pady=10)

    tk.Button(
        win,
        text="Top 10 Productos Más Vendidos",
        command=informe_productos_mas_vendidos
    ).pack(pady=10)

    tk.Button(
        win,
        text="Top 10 Clientes con Mayor Compra",
        command=informe_clientes_top
    ).pack(pady=10)

    tk.Button(
        win,
        text="Materias Primas Más Utilizadas",
        command=informe_materias_primas_usadas
    ).pack(pady=10)










#=========================================================================
    tk.Button(win, text="Volver", command=win.destroy).pack(pady=20)


# ============================
#   INFORME 1 (TREEVIEW)
# ============================
def informe_productos_pendientes():
    win_inf = tk.Toplevel()
    win_inf.title("Productos pendientes por entregar")
    win_inf.geometry("900x450")

    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("pedido", "cliente", "producto", "cantidad", "fecha", "estado"),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")

    tabla.pack(fill="both", expand=True)

    tabla.heading("pedido", text="Pedido")
    tabla.heading("cliente", text="Cliente")
    tabla.heading("producto", text="Producto")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("fecha", text="Fecha Encargo")
    tabla.heading("estado", text="Estado")

    tabla.column("pedido", width=100)
    tabla.column("cliente", width=150)
    tabla.column("producto", width=200)
    tabla.column("cantidad", width=80)
    tabla.column("fecha", width=120)
    tabla.column("estado", width=120)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                p.num_pedido,
                c.nombre AS cliente,
                pt.descripcion AS producto,
                i.cantidad,
                p.fecha_encargo,
                p.estado
            FROM pedido p
            JOIN cliente c ON p.id_cliente = c.id_cliente
            JOIN incluye i ON p.num_pedido = i.num_pedido
            JOIN producto_terminado pt ON pt.cod_producto = i.cod_producto
            WHERE p.estado <> 'Entregado'
            ORDER BY p.fecha_encargo;
        """)

        filas = cursor.fetchall()
        for fila in filas:
            tabla.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_por_cliente():
    win_inf = tk.Toplevel()
    win_inf.title("Productos por Cliente (no entregados)")
    win_inf.geometry("900x450")

    # FRAME DE LA TABLA
    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    # SCROLLBARS
    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("cliente", "pedido", "producto", "cantidad", "fecha", "estado"),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)

    # ENCABEZADOS
    tabla.heading("cliente", text="Cliente")
    tabla.heading("pedido", text="N° Pedido")
    tabla.heading("producto", text="Producto")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("fecha", text="Fecha Encargo")
    tabla.heading("estado", text="Estado")

    # TAMAÑO COLUMNAS
    tabla.column("cliente", width=150)
    tabla.column("pedido", width=100)
    tabla.column("producto", width=200)
    tabla.column("cantidad", width=80)
    tabla.column("fecha", width=120)
    tabla.column("estado", width=120)

    # CONEXIÓN BD
    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                c.nombre AS cliente,
                p.num_pedido,
                pt.descripcion AS producto,
                i.cantidad,
                p.fecha_encargo,
                p.estado
            FROM cliente c
            JOIN pedido p ON c.id_cliente = p.id_cliente
            JOIN incluye i ON p.num_pedido = i.num_pedido
            JOIN producto_terminado pt ON pt.cod_producto = i.cod_producto
            WHERE p.estado <> 'Entregado'
            ORDER BY cliente, p.num_pedido;
        """)

        filas = cursor.fetchall()

        for fila in filas:
            tabla.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_existencias_reales():
    win_inf = tk.Toplevel()
    win_inf.title("Existencias reales de productos")
    win_inf.geometry("900x450")

    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("codigo", "descripcion", "exist_total", "encargado", "exist_real"),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)

    # ENCABEZADOS
    tabla.heading("codigo", text="Código")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("exist_total", text="Existencia Total")
    tabla.heading("encargado", text="Cantidad Encargada")
    tabla.heading("exist_real", text="Existencia Real")

    # TAMAÑO COLUMNAS
    tabla.column("codigo", width=100)
    tabla.column("descripcion", width=200)
    tabla.column("exist_total", width=120)
    tabla.column("encargado", width=120)
    tabla.column("exist_real", width=120)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                pt.cod_producto,
                pt.descripcion,
                pt.existe_cantidad AS existencia_total,
                COALESCE(SUM(i.cantidad), 0) AS cantidad_encargada,
                pt.existe_cantidad - COALESCE(SUM(i.cantidad), 0) AS existencia_real
            FROM producto_terminado pt
            LEFT JOIN incluye i ON pt.cod_producto = i.cod_producto
            LEFT JOIN pedido p ON p.num_pedido = i.num_pedido AND p.estado <> 'Entregado'
            GROUP BY pt.cod_producto, pt.descripcion, pt.existe_cantidad
            ORDER BY pt.cod_producto;
        """)

        filas = cursor.fetchall()

        for fila in filas:
            tabla.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_listado_colegios():
    win_inf = tk.Toplevel()
    win_inf.title("Listado de Colegios")
    win_inf.geometry("700x400")

    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("id", "nombre", "direccion", "telefono"),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)

    # ENCABEZADOS
    tabla.heading("id", text="ID Colegio")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("direccion", text="Dirección")
    tabla.heading("telefono", text="Teléfono")

    # TAMAÑO COLUMNAS
    tabla.column("id", width=100)
    tabla.column("nombre", width=200)
    tabla.column("direccion", width=250)
    tabla.column("telefono", width=120)

    # -------------------------------
    #       CONSULTA SQL OFICIAL
    # -------------------------------
    # SELECT id_colegio, nombre_c, direccion, telefono
    # FROM colegio
    # ORDER BY nombre_c;
    # -------------------------------

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id_colegio, nombre_c, direccion, telefono
            FROM colegio
            ORDER BY nombre_c;
        """)

        filas = cursor.fetchall()

        for fila in filas:
            tabla.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_uniformes_por_colegio():
    win_inf = tk.Toplevel()
    win_inf.title("Uniformes por Colegio")
    win_inf.geometry("950x500")

    # ----- Cargar colegios en combobox -----
    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_colegio, nombre_c FROM colegio ORDER BY nombre_c;")
        colegios = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    finally:
        cursor.close()
        conn.close()

    # Diccionario para mapear nombre → id
    mapa_colegios = {nombre: cid for cid, nombre in colegios}

    tk.Label(win_inf, text="Seleccione un colegio:", font=("Arial", 12)).pack(pady=10)

    combo = ttk.Combobox(win_inf, values=list(mapa_colegios.keys()), state="readonly", width=50)
    combo.pack(pady=5)

    # ----- Tabla de resultados -----
    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True, pady=20)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("id", "pieza", "color", "tela", "bordado", "lugar", "estampa", "mangas", "cuello"),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)

    # Encabezados
    columnas = [
        ("id", "ID Pieza"),
        ("pieza", "Tipo Pieza"),
        ("color", "Color"),
        ("tela", "Tipo Tela"),
        ("bordado", "Lleva Bordado"),
        ("lugar", "Lugar Bordado"),
        ("estampa", "Tipo Estampa"),
        ("mangas", "Borde Mangas"),
        ("cuello", "Borde Cuello")
    ]

    for code, text in columnas:
        tabla.heading(code, text=text)
        tabla.column(code, width=120)

    # ----- Consulta al seleccionar colegio -----
    def consultar():
        colegio_sel = combo.get()
        if not colegio_sel:
            messagebox.showwarning("Advertencia", "Seleccione un colegio.")
            return

        id_colegio = mapa_colegios[colegio_sel]

        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT 
                    id_pieza, tipo_pieza, color, tipo_tela, lleva_bordado,
                    lugar_bordado, tipo_estampa, borde_mangas, borde_cuello
                FROM pieza_uni
                WHERE id_colegio = %s;
            """, (id_colegio,))

            filas = cursor.fetchall()

            # Limpiar tabla antes de insertar nuevos
            for item in tabla.get_children():
                tabla.delete(item)

            for fila in filas:
                tabla.insert("", tk.END, values=fila)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win_inf, text="Consultar", command=consultar).pack(pady=10)

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_total_vendido_por_colegio():
    win_inf = tk.Toplevel()
    win_inf.title("Total Vendido por Colegio")
    win_inf.geometry("700x400")

    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("colegio", "total"),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tabla.pack(fill="both", expand=True)

    tabla.heading("colegio", text="Colegio")
    tabla.heading("total", text="Total Vendido")

    tabla.column("colegio", width=250)
    tabla.column("total", width=150)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                c.nombre_c AS colegio,
                SUM(i.cantidad * pt.precio) AS total_vendido
            FROM colegio c
            JOIN pieza_uni pu ON pu.id_colegio = c.id_colegio
            JOIN producto_terminado pt ON pt.id_pieza = pu.id_pieza
            JOIN incluye i ON i.cod_producto = pt.cod_producto
            JOIN pedido p ON p.num_pedido = i.num_pedido
            JOIN factura f ON f.num_pedido = p.num_pedido
            GROUP BY c.nombre_c
            ORDER BY total_vendido DESC;
        """)

        filas = cursor.fetchall()

        for fila in filas:
            tabla.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_total_general_ventas():
    win_inf = tk.Toplevel()
    win_inf.title("Total General de Ventas")
    win_inf.geometry("400x300")

    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("total",),
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_y.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    # Encabezado
    tabla.heading("total", text="Total General de Ventas (COP)")
    tabla.column("total", width=300)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT SUM(total) AS total_general_ventas
            FROM factura;
        """)

        resultado = cursor.fetchone()

        total = resultado[0] if resultado[0] is not None else 0

        tabla.insert("", tk.END, values=(total,))

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_productos_mas_vendidos():
    win_inf = tk.Toplevel()
    win_inf.title("Top 10 Productos Más Vendidos")
    win_inf.geometry("700x400")

    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    tabla = ttk.Treeview(
        frame_tabla,
        columns=("codigo", "descripcion", "total"),
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_y.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    tabla.heading("codigo", text="Código Producto")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("total", text="Total Vendido")

    tabla.column("codigo", width=150)
    tabla.column("descripcion", width=300)
    tabla.column("total", width=150)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                pt.cod_producto,
                pt.descripcion,
                SUM(i.cantidad) AS total_vendido
            FROM producto_terminado pt
            JOIN incluye i ON i.cod_producto = pt.cod_producto
            JOIN pedido p ON p.num_pedido = i.num_pedido
            JOIN factura f ON f.num_pedido = p.num_pedido
            GROUP BY pt.cod_producto, pt.descripcion
            ORDER BY total_vendido DESC
            LIMIT 10;
        """)

        for fila in cursor.fetchall():
            tabla.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_clientes_top():
    win_inf = tk.Toplevel()
    win_inf.title("Top 10 Clientes con Mayor Compra")
    win_inf.geometry("700x400")

    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    tabla = ttk.Treeview(
        frame_tabla,
        columns=("id", "nombre", "total"),
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_y.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    tabla.heading("id", text="ID Cliente")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("total", text="Total Comprado")

    tabla.column("id", width=120)
    tabla.column("nombre", width=300)
    tabla.column("total", width=200)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                c.id_cliente,
                c.nombre,
                SUM(f.total) AS total_compras
            FROM cliente c
            JOIN pedido p ON p.id_cliente = c.id_cliente
            JOIN factura f ON f.num_pedido = p.num_pedido
            GROUP BY c.id_cliente, c.nombre
            ORDER BY total_compras DESC
            LIMIT 10;
        """)

        for fila in cursor.fetchall():
            tabla.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

def informe_materias_primas_usadas():
    win_inf = tk.Toplevel()
    win_inf.title("Materias Primas Más Utilizadas")
    win_inf.geometry("800x400")

    frame_tabla = tk.Frame(win_inf)
    frame_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    tabla = ttk.Treeview(
        frame_tabla,
        columns=("codigo", "tipo", "descripcion", "usos"),
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_y.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    tabla.heading("codigo", text="Código Materia")
    tabla.heading("tipo", text="Tipo")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("usos", text="Veces Usada")

    tabla.column("codigo", width=120)
    tabla.column("tipo", width=150)
    tabla.column("descripcion", width=350)
    tabla.column("usos", width=150)

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                mp.cod_materia,
                mp.tipo,
                mp.description,
                COUNT(u.cod_materia) AS veces_usada
            FROM materia_prima mp
            JOIN utiliza u ON u.cod_materia = mp.cod_materia
            GROUP BY mp.cod_materia, mp.tipo, mp.description
            ORDER BY veces_usada DESC;
        """)

        for fila in cursor.fetchall():
            tabla.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        cursor.close()
        conn.close()

    tk.Button(win_inf, text="Cerrar", command=win_inf.destroy).pack(pady=10)

# controladora.py
from tkinter import messagebox
from conexion import conectar_bd

def generar_factura(num_factura, num_pedido):
    """
    Calcula el total del pedido (SUM precio * cantidad), inserta la factura
    y devuelve True si se creó correctamente, False si hubo problema.
    """
    conn = conectar_bd()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
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
    """
    Resta las cantidades en 'producto_terminado' según los productos incluidos
    en el pedido. También puede actualizar el estado del producto.
    """
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

            # Opcional: actualizar estado (según tu lógica original)
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


# Puedes añadir aquí más funciones lógicas compartidas por las vistas,
# por ejemplo: funciones de informes, validaciones, generación de reportes, etc.
# Ejemplo de helper (no obligatorio) para obtener total de un pedido:
def obtener_total_pedido(num_pedido):
    conn = conectar_bd()
    if conn is None:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT SUM(pt.precio * i.cantidad)
            FROM incluye i
            JOIN producto_terminado pt ON i.cod_producto = pt.cod_producto
            WHERE i.num_pedido = %s
        """, (num_pedido,))
        total = cursor.fetchone()[0]
        return total
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None
    finally:
        cursor.close(); conn.close()









def generar_factura_auto(num_pedido):
    """
    Genera una factura automática para el pedido num_pedido:
    - total = (SUM de cantidades en incluye WHERE num_pedido) * abono (del pedido)
    - fecha = fecha_entrega del pedido (si existe), si no, NOW()
    Inserta la factura y devuelve una tupla (num_factura_generado, total) en caso de éxito,
    o (None, None) en caso de error.
    """
    conn = conectar_bd()
    if conn is None:
        return (None, None)

    cursor = conn.cursor()
    try:
        # Obtener abono y fecha_entrega del pedido
        cursor.execute("""
            SELECT abono, fecha_entrega
            FROM pedido
            WHERE num_pedido = %s
        """, (num_pedido,))
        fila_pedido = cursor.fetchone()
        if fila_pedido is None:
            messagebox.showwarning("Pedido inexistente", "No existe el pedido indicado.")
            return (None, None)

        abono = fila_pedido[0]   # puede ser None o decimal
        fecha_entrega = fila_pedido[1]  # puede ser None

        if abono is None:
            messagebox.showwarning("Abono nulo", "El pedido no tiene abono definido.")
            return (None, None)

        # Obtener la suma de cantidades del pedido
        cursor.execute("""
            SELECT COALESCE(SUM(cantidad), 0)
            FROM incluye
            WHERE num_pedido = %s
        """, (num_pedido,))
        suma_cant = cursor.fetchone()[0] or 0

        if suma_cant == 0:
            messagebox.showwarning("Sin productos", "El pedido no tiene productos asociados.")
            return (None, None)

        # Calcular total: cantidad_total * abono
        try:
            total = float(suma_cant) * float(abono)
        except Exception as e:
            messagebox.showerror("Error cálculo total", "No se pudo calcular el total: " + str(e))
            return (None, None)

        # Si no hay fecha_entrega, usar NOW()
        if fecha_entrega is None:
            fecha_valor = None  # dejar que la BD ponga NOW() con la consulta
            insert_fecha_expr = "NOW()"
            insert_values = (total, num_pedido)
            returning_clause = "RETURNING num_factura"
            # Insert con NOW()
            cursor.execute(f"""
                INSERT INTO factura(fecha, total, num_pedido)
                VALUES (NOW(), %s, %s)
                RETURNING num_factura
            """, (total, num_pedido))
        else:
            # Insertando con la fecha_entrega del pedido
            cursor.execute("""
                INSERT INTO factura(fecha, total, num_pedido)
                VALUES (%s, %s, %s)
                RETURNING num_factura
            """, (fecha_entrega, total, num_pedido))

        nuevo = cursor.fetchone()
        if nuevo is None:
            conn.rollback()
            messagebox.showerror("Error", "No se pudo crear la factura.")
            return (None, None)

        num_factura_generado = nuevo[0]
        conn.commit()
        messagebox.showinfo("Factura creada", f"Factura {num_factura_generado} generada correctamente.\nTotal: {total}")
        return (num_factura_generado, total)

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error al generar factura", str(e))
        return (None, None)
    finally:
        cursor.close()
        conn.close()







def generar_factura(num_pedido):
    conn = conectar_bd()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # calcular total
        cursor.execute("""
            SELECT SUM(pt.precio * i.cantidad)
            FROM incluye i
            JOIN producto_terminado pt ON i.cod_producto = pt.cod_producto
            WHERE i.num_pedido=%s
        """, (num_pedido,))
        total = cursor.fetchone()[0]

        if total is None:
            messagebox.showwarning("Sin productos", "Este pedido no tiene productos.")
            return False

        # Insertar factura
        cursor.execute("""
            INSERT INTO factura(fecha, total, num_pedido)
            VALUES (NOW(), %s, %s)
        """, (total, num_pedido))

        conn.commit()
        return True

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

    finally:
        cursor.close()
        conn.close()

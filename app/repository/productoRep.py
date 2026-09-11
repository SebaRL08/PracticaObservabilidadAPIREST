from mysql.connector import Error
from app.core.basedatos import obtener_conexion
from app.core.logCONFIG import configurar_logging

logger = configurar_logging()


def listar_productos():
    """
    Consulta todos los productos en la base de datos.
    Retorna una lista de diccionarios con los datos de cada producto.
    Lanza la excepción tal cual si hay un error de conexión, para que
    la capa de servicio la capture y decida cómo manejarla.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM productos ORDER BY id")
        resultados = cursor.fetchall()
        return resultados
    finally:
        cursor.close()
        conexion.close()


def obtener_producto_por_id(producto_id: int):
    """
    Busca un producto por su ID.
    Retorna un diccionario con los datos del producto, o None si no existe.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        cursor.close()
        conexion.close()


def crear_producto(nombre: str, descripcion: str, precio: float, stock: int):
    """
    Inserta un nuevo producto en la base de datos.
    Retorna el ID generado para el nuevo producto.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock) "
            "VALUES (%s, %s, %s, %s)",
            (nombre, descripcion, precio, stock)
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conexion.close()


def actualizar_producto(producto_id: int, nombre: str, descripcion: str, precio: float, stock: int):
    """
    Actualiza los datos de un producto existente.
    Retorna True si se actualizó una fila, False si el producto no existía.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE productos SET nombre = %s, descripcion = %s, "
            "precio = %s, stock = %s WHERE id = %s",
            (nombre, descripcion, precio, stock, producto_id)
        )
        conexion.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conexion.close()


def eliminar_producto(producto_id: int):
    """
    Elimina un producto por su ID.
    Retorna True si se eliminó una fila, False si el producto no existía.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
        conexion.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conexion.close()
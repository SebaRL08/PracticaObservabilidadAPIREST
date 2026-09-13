"""
Módulo encargado de manejar los productos en la base de datos.

Aquí se encuentran las funciones necesarias para consultar, crear,
actualizar y eliminar productos. El módulo utiliza la conexión con
MySQL para realizar las diferentes operaciones y se encarga de cerrar
correctamente las conexiones después de cada proceso.
"""

from mysql.connector import Error
from app.core.basedatos import obtener_conexion
from app.core.logCONFIG import configurar_logging

logger = configurar_logging()


def listar_productos():
    """
    Obtiene todos los productos registrados en la base de datos.

    Los productos se muestran organizados por su ID y se retornan
    como una lista de diccionarios, lo que facilita trabajar con
    la información obtenida.

    Returns:
        list[dict]: Lista que contiene los productos encontrados.

    Raises:
        mysql.connector.Error: Se presenta cuando ocurre algún problema
        con la conexión o con la consulta realizada en la base de datos.
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
    Busca un producto específico usando su ID.

    Args:
        producto_id (int): Número que identifica al producto que se quiere buscar.

    Returns:
        dict | None: Información del producto si existe. Si no se encuentra,
        retorna None.

    Raises:
        mysql.connector.Error: Se presenta si ocurre un problema con la
        conexión o con la consulta a la base de datos.
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
    Registra un nuevo producto en la base de datos.

    Después de realizar la inserción, se guardan los cambios y se
    obtiene el ID que MySQL asignó automáticamente al producto.

    Args:
        nombre (str): Nombre del producto.
        descripcion (str): Información o características del producto.
        precio (float): Valor de venta del producto.
        stock (int): Cantidad disponible del producto.

    Returns:
        int: ID asignado al nuevo producto.

    Raises:
        mysql.connector.Error: Se presenta si ocurre algún error durante
        la inserción o al conectarse con la base de datos.
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
    Modifica la información de un producto que ya existe.

    Se actualizan los datos del producto según el ID indicado y,
    después de realizar los cambios, se guardan en la base de datos.

    Args:
        producto_id (int): ID del producto que se desea modificar.
        nombre (str): Nuevo nombre del producto.
        descripcion (str): Nueva descripción del producto.
        precio (float): Nuevo precio del producto.
        stock (int): Nueva cantidad disponible.

    Returns:
        bool: Retorna True si se modificó un producto y False si
        no se encontró un producto con el ID indicado.

    Raises:
        mysql.connector.Error: Se presenta si ocurre algún problema
        al ejecutar la actualización en la base de datos.
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
    Elimina un producto de la base de datos mediante su ID.

    Una vez eliminado el registro, se guardan los cambios realizados
    para que la eliminación quede aplicada en la base de datos.

    Args:
        producto_id (int): ID del producto que se quiere eliminar.

    Returns:
        bool: Retorna True si el producto fue eliminado y False si
        no se encontró ningún producto con ese ID.

    Raises:
        mysql.connector.Error: Se presenta si ocurre algún error al
        ejecutar la eliminación en la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
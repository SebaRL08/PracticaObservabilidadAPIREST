"""
Módulo encargado de manejar la lógica de los productos.

En este archivo se realizan los procesos principales relacionados con
los productos y se conecta la capa de API con el repositorio de datos.
También se registran los tiempos de ejecución y los eventos importantes
mediante el sistema de logs. Además, se definen errores personalizados
para manejar situaciones específicas del sistema.
"""

import time
from mysql.connector import Error
from app.repository import productoRep as repo
from app.core.logCONFIG import configurar_logging

logger = configurar_logging()


class ProductoNoEncontrado(Exception):
    """
    Error que se utiliza cuando se intenta consultar, modificar o
    eliminar un producto que no existe en la base de datos.
    """
    pass


class ErrorBaseDatos(Exception):
    """
    Error utilizado cuando ocurre algún problema al conectarse
    o trabajar con la base de datos.
    """
    pass


def listar_productos_service():
    """
    Obtiene todos los productos registrados.

    También calcula cuánto tiempo tarda la consulta y registra en
    los logs si la operación fue exitosa o si ocurrió algún error.

    Returns:
        list[dict]: Lista con los productos encontrados.

    Raises:
        ErrorBaseDatos: Se genera cuando ocurre un problema al consultar
        la información en la base de datos.
    """
    inicio = time.time()
    logger.info("GET /productos - Consulta iniciada")
    try:
        productos = repo.listar_productos()
        duracion_ms = round((time.time() - inicio) * 1000, 2)
        logger.info(f"GET /productos - Consulta exitosa - {len(productos)} productos - {duracion_ms}ms")
        return productos
    except Error as e:
        logger.error(f"GET /productos - Error de conexion a base de datos - {e}")
        raise ErrorBaseDatos(str(e))


def obtener_producto_service(producto_id: int):
    """
    Busca un producto específico a partir de su ID.

    La función mide el tiempo que tarda la consulta y comprueba
    si el producto realmente existe antes de devolver la información.

    Args:
        producto_id (int): ID del producto que se desea consultar.

    Returns:
        dict: Información del producto encontrado.

    Raises:
        ProductoNoEncontrado: Se genera cuando no existe un producto
        con el ID indicado.
        ErrorBaseDatos: Se genera cuando ocurre un problema con la
        conexión a la base de datos.
    """
    inicio = time.time()
    logger.info(f"GET /productos/{producto_id} - Consulta iniciada")
    try:
        producto = repo.obtener_producto_por_id(producto_id)
        duracion_ms = round((time.time() - inicio) * 1000, 2)
        if producto is None:
            logger.error(f"GET /productos/{producto_id} - Producto no encontrado - 404")
            raise ProductoNoEncontrado(f"Producto con id {producto_id} no existe")
        logger.info(f"GET /productos/{producto_id} - Consulta exitosa - {duracion_ms}ms")
        return producto
    except Error as e:
        logger.error(f"GET /productos/{producto_id} - Error de conexion a base de datos - {e}")
        raise ErrorBaseDatos(str(e))


def crear_producto_service(nombre: str, descripcion: str, precio: float, stock: int):
    """
    Se encarga de registrar un producto nuevo.

    Después de guardar el producto, se obtiene nuevamente su información
    utilizando el ID generado para devolver todos sus datos. También se
    registra el tiempo que tomó realizar el proceso.

    Args:
        nombre (str): Nombre del producto.
        descripcion (str): Descripción del producto.
        precio (float): Precio de venta del producto.
        stock (int): Cantidad inicial disponible.

    Returns:
        dict: Información completa del producto creado.

    Raises:
        ErrorBaseDatos: Se genera cuando ocurre un problema al guardar
        el producto en la base de datos.
    """
    inicio = time.time()
    logger.info(f"POST /productos - Creacion iniciada - nombre={nombre}")
    try:
        nuevo_id = repo.crear_producto(nombre, descripcion, precio, stock)
        duracion_ms = round((time.time() - inicio) * 1000, 2)
        logger.info(f"POST /productos - Producto creado exitosamente - id={nuevo_id} - {duracion_ms}ms")
        return repo.obtener_producto_por_id(nuevo_id)
    except Error as e:
        logger.error(f"POST /productos - Error de conexion a base de datos - {e}")
        raise ErrorBaseDatos(str(e))


def actualizar_producto_service(producto_id: int, nombre: str, descripcion: str, precio: float, stock: int):
    """
    Modifica la información de un producto que ya existe.

    Primero se realiza la actualización y luego se verifica si realmente
    se encontró el producto. También se mide el tiempo utilizado y se
    registran los resultados de la operación en los logs.

    Args:
        producto_id (int): ID del producto que se quiere modificar.
        nombre (str): Nuevo nombre del producto.
        descripcion (str): Nueva descripción del producto.
        precio (float): Nuevo precio.
        stock (int): Nueva cantidad disponible.

    Returns:
        dict: Información del producto después de ser actualizado.

    Raises:
        ProductoNoEncontrado: Se genera si no existe el producto con
        el ID indicado.
        ErrorBaseDatos: Se genera cuando ocurre un problema con la
        conexión o actualización de la base de datos.
    """
    inicio = time.time()
    logger.info(f"PUT /productos/{producto_id} - Actualizacion iniciada")
    try:
        actualizado = repo.actualizar_producto(producto_id, nombre, descripcion, precio, stock)
        duracion_ms = round((time.time() - inicio) * 1000, 2)
        if not actualizado:
            logger.error(f"PUT /productos/{producto_id} - Producto no encontrado - 404")
            raise ProductoNoEncontrado(f"Producto con id {producto_id} no existe")
        logger.info(f"PUT /productos/{producto_id} - Actualizacion exitosa - {duracion_ms}ms")
        return repo.obtener_producto_por_id(producto_id)
    except Error as e:
        logger.error(f"PUT /productos/{producto_id} - Error de conexion a base de datos - {e}")
        raise ErrorBaseDatos(str(e))


def eliminar_producto_service(producto_id: int):
    """
    Elimina un producto utilizando su ID.

    Se comprueba si la eliminación se realizó correctamente y se
    registra el tiempo que tardó el proceso. Si el producto no existe,
    se genera el error correspondiente.

    Args:
        producto_id (int): ID del producto que se desea eliminar.

    Returns:
        bool: Retorna True cuando el producto fue eliminado correctamente.

    Raises:
        ProductoNoEncontrado: Se genera cuando el producto no existe.
        ErrorBaseDatos: Se genera cuando ocurre un problema con la
        conexión o con la eliminación en la base de datos.
    """
    inicio = time.time()
    logger.info(f"DELETE /productos/{producto_id} - Eliminacion iniciada")
    try:
        eliminado = repo.eliminar_producto(producto_id)
        duracion_ms = round((time.time() - inicio) * 1000, 2)
        if not eliminado:
            logger.error(f"DELETE /productos/{producto_id} - Producto no encontrado - 404")
            raise ProductoNoEncontrado(f"Producto con id {producto_id} no existe")
        logger.info(f"DELETE /productos/{producto_id} - Eliminacion exitosa - {duracion_ms}ms")
        return True
    except Error as e:
        logger.error(f"DELETE /productos/{producto_id} - Error de conexion a base de datos - {e}")
        raise ErrorBaseDatos(str(e))


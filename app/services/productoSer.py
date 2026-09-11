import time
from mysql.connector import Error
from app.repository import productoRep as repo
from app.core.logCONFIG import configurar_logging

logger = configurar_logging()


class ProductoNoEncontrado(Exception):
    """Se lanza cuando se busca un producto que no existe."""
    pass


class ErrorBaseDatos(Exception):
    """Se lanza cuando falla la conexión o una operación con la base de datos."""
    pass


def listar_productos_service():
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
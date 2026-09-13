"""
Módulo encargado de definir las rutas de los productos.

En este archivo se encuentran los endpoints de la API que permiten
consultar, registrar, modificar y eliminar productos. Las solicitudes
se comunican con la capa de servicio y los posibles errores se convierten
en respuestas HTTP para informar correctamente al cliente.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.producto import ProductoCrear, ProductoActualizar, ProductoRespuesta
from app.services import productoSer as service
from typing import List

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=List[ProductoRespuesta])
def listar_productos():
    """
    Obtiene la lista completa de productos registrados.

    La información se solicita a la capa de servicio y luego se
    devuelve como respuesta de la API.

    Returns:
        List[ProductoRespuesta]: Lista con los productos registrados.

    Raises:
        HTTPException:
            - 500: Se genera cuando existe un problema al conectarse
            con la base de datos.
    """
    try:
        return service.listar_productos_service()
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")


@router.get("/{producto_id}", response_model=ProductoRespuesta)
def obtener_producto(producto_id: int):
    """
    Busca un producto específico utilizando su ID.

    Args:
        producto_id (int): ID del producto que se desea consultar.

    Returns:
        ProductoRespuesta: Información del producto encontrado.

    Raises:
        HTTPException:
            - 404: Se genera cuando no existe un producto con el ID indicado.
            - 500: Se genera cuando ocurre un problema con la conexión
            a la base de datos.
    """
    try:
        return service.obtener_producto_service(producto_id)
    except service.ProductoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")


@router.post("/", response_model=ProductoRespuesta, status_code=201)
def crear_producto(producto: ProductoCrear):
    """
    Registra un nuevo producto en el sistema.

    Recibe los datos del producto, los cuales ya fueron validados,
    y los envía a la capa de servicio para realizar el registro.
    Si todo sale correctamente, se devuelve el producto creado.

    Args:
        producto (ProductoCrear): Datos necesarios para crear el producto,
        como nombre, descripción, precio y cantidad disponible.

    Returns:
        ProductoRespuesta: Información del producto creado junto con su ID.

    Raises:
        HTTPException:
            - 500: Se genera cuando ocurre un problema durante la conexión
            o al guardar la información en la base de datos.
    """
    try:
        return service.crear_producto_service(
            producto.nombre, producto.descripcion, producto.precio, producto.stock
        )
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")


@router.put("/{producto_id}", response_model=ProductoRespuesta)
def actualizar_producto(producto_id: int, producto: ProductoActualizar):
    """
    Actualiza los datos de un producto que ya está registrado.

    Se utiliza el ID para identificar el producto y se envían los
    nuevos datos a la capa de servicio para realizar la modificación.

    Args:
        producto_id (int): ID del producto que se quiere modificar.
        producto (ProductoActualizar): Información nueva del producto.

    Returns:
        ProductoRespuesta: Datos del producto después de ser actualizado.

    Raises:
        HTTPException:
            - 404: Se genera si no existe un producto con el ID indicado.
            - 500: Se genera si ocurre un problema con la base de datos.
    """
    try:
        return service.actualizar_producto_service(
            producto_id, producto.nombre, producto.descripcion, producto.precio, producto.stock
        )
    except service.ProductoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    """
    Elimina un producto utilizando su ID.

    La solicitud se envía a la capa de servicio, donde se realiza
    la eliminación del registro. Si la operación es correcta,
    la API responde indicando que no hay contenido para devolver.

    Args:
        producto_id (int): ID del producto que se desea eliminar.

    Returns:
        None: No devuelve información cuando la eliminación se realiza correctamente.

    Raises:
        HTTPException:
            - 404: Se genera cuando el producto no existe.
            - 500: Se genera cuando ocurre un problema con la base de datos.
    """
    try:
        service.eliminar_producto_service(producto_id)
    except service.ProductoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")



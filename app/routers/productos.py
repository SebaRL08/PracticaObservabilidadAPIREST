from fastapi import APIRouter, HTTPException
from app.schemas.producto import ProductoCrear, ProductoActualizar, ProductoRespuesta
from app.services import productoSer as service
from typing import List

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=List[ProductoRespuesta])
def listar_productos():
    try:
        return service.listar_productos_service()
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")


@router.get("/{producto_id}", response_model=ProductoRespuesta)
def obtener_producto(producto_id: int):
    try:
        return service.obtener_producto_service(producto_id)
    except service.ProductoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")


@router.post("/", response_model=ProductoRespuesta, status_code=201)
def crear_producto(producto: ProductoCrear):
    try:
        return service.crear_producto_service(
            producto.nombre, producto.descripcion, producto.precio, producto.stock
        )
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")


@router.put("/{producto_id}", response_model=ProductoRespuesta)
def actualizar_producto(producto_id: int, producto: ProductoActualizar):
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
    try:
        service.eliminar_producto_service(producto_id)
    except service.ProductoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.ErrorBaseDatos as e:
        raise HTTPException(status_code=500, detail=f"Error de conexion a base de datos: {e}")


"""
Módulo encargado de definir los datos de los productos.

En este archivo se crean los esquemas utilizados para validar la
información de los productos. Se utiliza Pydantic para comprobar que
los datos recibidos tengan el formato correcto antes de ser procesados
por la aplicación.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductoCrear(BaseModel):
    """
    Define los datos necesarios para registrar un producto nuevo.

    Aquí se establecen las condiciones que debe cumplir la información
    enviada al momento de crear un producto.

    Attributes:
        nombre (str): Nombre del producto, con una longitud de 1 a 100 caracteres.
        descripcion (Optional[str]): Descripción del producto, que puede ser opcional
        y tener hasta 255 caracteres.
        precio (float): Precio del producto, debe ser mayor que 0.
        stock (int): Cantidad disponible del producto, no puede ser negativa.
    """
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductoActualizar(BaseModel):
    """
    Define la información necesaria para modificar un producto.

    Se utilizan estas reglas para comprobar que los nuevos datos
    enviados para un producto sean válidos.

    Attributes:
        nombre (str): Nuevo nombre del producto, entre 1 y 100 caracteres.
        descripcion (Optional[str]): Nueva descripción, con un máximo de 255 caracteres.
        precio (float): Nuevo precio, debe ser mayor que 0.
        stock (int): Nueva cantidad disponible, no puede ser menor que 0.
    """
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductoRespuesta(BaseModel):
    """
    Define los datos que la API devuelve cuando trabaja con productos.

    Este esquema establece qué información se mostrará al cliente
    después de consultar, crear o actualizar un producto.

    Attributes:
        id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        descripcion (Optional[str]): Descripción del producto, si existe.
        precio (float): Precio de venta del producto.
        stock (int): Cantidad disponible actualmente.
        fecha_creacion (datetime): Fecha y hora en la que se registró el producto.
    """
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float
    stock: int
    fecha_creacion: datetime


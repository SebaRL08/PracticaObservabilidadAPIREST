from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductoCrear(BaseModel):
    """Datos requeridos para crear un producto nuevo."""
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductoActualizar(BaseModel):
    """Datos requeridos para actualizar un producto existente."""
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductoRespuesta(BaseModel):
    """Estructura de un producto tal como se devuelve en las respuestas."""
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float
    stock: int
    fecha_creacion: datetime
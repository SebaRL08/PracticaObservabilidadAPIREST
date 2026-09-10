import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Configuración básica de LOGS (Paso 2 de la guía)
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = FastAPI(title="API de Gestión de Productos")

# Base de datos simulada en memoria
productos_db = {
    1: {"id": 1, "nombre": "Laptop", "precio": 1200.0},
    2: {"id": 2, "nombre": "Mouse", "precio": 25.0}
}

class Producto(BaseModel):
    nombre: str
    precio: float

# Funcionalidad 1: Consultar todos los productos
@app.get("/productos")
def obtener_productos():
    logging.info("GET /productos - Consulta general realizada con éxito.")
    return list(productos_db.values())

# Funcionalidad 2: Consultar un producto por ID (Aquí podemos probar la FALLA 1)
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    if producto_id not in productos_db:
        logging.error(f"GET /productos/{producto_id} - ERROR: Producto no encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producto no encontrado"
        )
    
    # Simulación de FALLA 3 (Múltiples solicitudes / Error forzado si el ID es 999)
    if producto_id == 999:
        logging.critical("GET /productos/999 - ERROR CRÍTICO: Fallo de conexión simulado con la base de datos.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error interno del servidor / Base de datos no disponible"
        )

    logging.info(f"GET /productos/{producto_id} - Consulta exitosa.")
    return productos_db[producto_id]

# Funcionalidad 3: Registrar un producto (Aquí podemos probar la FALLA 2)
@app.post("/productos", status_code=status.HTTP_201_CREATED)
def crear_producto(producto: Producto):
    # Simulación de FALLA 2 (Validación / Datos incompletos o inválidos)
    if producto.precio <= 0:
        logging.warning(f"POST /productos - ADVERTENCIA: Intento de registro con precio inválido ({producto.precio}).")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El precio debe ser mayor a 0"
        )
    
    nuevo_id = max(productos_db.keys(), default=0) + 1
    nuevo_producto = {"id": nuevo_id, "nombre": producto.nombre, "precio": producto.precio}
    productos_db[nuevo_id] = nuevo_producto
    
    logging.info(f"POST /productos - Producto registrado con ID {nuevo_id}.")
    return nuevo_producto
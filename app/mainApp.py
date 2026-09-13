"""
Módulo principal de la API.

Este archivo se encarga de iniciar la aplicación FastAPI, configurar
el registro de las solicitudes y medir el rendimiento de cada petición.
También conecta las rutas de productos y proporciona los endpoints
principales de la aplicación y de consulta de métricas.
"""

import time 
from fastapi import FastAPI, Request
from app.routers import productos
from app.core.metrics import registrar_solicitud, obtener_metricas
from app.core.logCONFIG import configurar_logging

logger = configurar_logging()

app = FastAPI(
    title="API de Productos - Observabilidad",
    description="API REST para la actividad academica de Observabilidad y DevOps inteligente con IA",
    version="1.0.0"
)


@app.middleware("http")
async def middleware_metricas_y_logs(request: Request, call_next):
    """
    Controla las solicitudes que recibe la aplicación.

    Esta función se ejecuta cada vez que llega una petición HTTP.
    Registra cuándo comienza la solicitud, calcula cuánto tiempo tarda
    en procesarse y guarda información sobre el código de respuesta
    y el endpoint utilizado.

    Args:
        request (Request): Información de la solicitud recibida.
        call_next (Callable): Permite continuar con la ejecución del endpoint.

    Returns:
        Response: Respuesta generada por el endpoint solicitado.
    """
    inicio = time.time()
    logger.info(f"{request.method} {request.url.path} - Peticion recibida")

    response = await call_next(request)

    duracion_ms = round((time.time() - inicio) * 1000, 2)
    endpoint = request.url.path
    registrar_solicitud(endpoint, response.status_code, duracion_ms)

    logger.info(
        f"{request.method} {request.url.path} - Respuesta enviada - "
        f"{response.status_code} - {duracion_ms}ms"
    )

    return response


# Conecta las rutas relacionadas con los productos
app.include_router(productos.router)


@app.get("/metrics", tags=["Observabilidad"])
def metricas():
    """
    Muestra las métricas que se han registrado en la aplicación.

    Devuelve información como el número total de solicitudes,
    las solicitudes exitosas y con error, el tiempo promedio de respuesta
    y la cantidad de peticiones realizadas por código HTTP y endpoint.

    Returns:
        dict: Información actual de las métricas de la aplicación.
    """
    return obtener_metricas()


@app.get("/", tags=["Root"])
def raiz():
    """
    Comprueba que la API esté funcionando correctamente.

    Este endpoint sirve como una prueba sencilla para verificar que
    el servidor está activo y puede responder a las solicitudes.

    Returns:
        dict: Mensaje que confirma que la API está funcionando.
    """
    return {"mensaje": "API de Productos - Observabilidad funcionando correctamente"}
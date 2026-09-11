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
    Middleware que se ejecuta en TODAS las peticiones HTTP, sin importar
    el endpoint. Registra el momento en que llega la petición, mide
    cuanto tarda en procesarse, y actualiza las metricas globales una
    vez que la respuesta esta lista.
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


# Registrar las rutas de productos
app.include_router(productos.router)


@app.get("/metrics", tags=["Observabilidad"])
def metricas():
    """Expone las metricas acumuladas de la aplicacion en formato JSON."""
    return obtener_metricas()


@app.get("/", tags=["Root"])
def raiz():
    """Endpoint raiz, util para verificar que la API esta corriendo."""
    return {"mensaje": "API de Productos - Observabilidad funcionando correctamente"}
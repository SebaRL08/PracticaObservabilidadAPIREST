import time
from collections import defaultdict

# Almacenamiento en memoria de las métricas.
# Se reinicia cada vez que se reinicia el servidor (esto lo mencionaremos
# como limitación conocida en el informe).
metricas = {
    "total_solicitudes": 0,
    "solicitudes_exitosas": 0,
    "solicitudes_con_error": 0,
    "por_codigo_http": defaultdict(int),
    "por_endpoint": defaultdict(int),
    "tiempos_respuesta_ms": [],  # lista de tiempos, usada para calcular el promedio
}


def registrar_solicitud(endpoint: str, codigo_http: int, duracion_ms: float):
    """
    Registra una solicitud completada, actualizando todos los contadores
    relevantes. Se llama una vez por cada petición HTTP recibida.
    """
    metricas["total_solicitudes"] += 1
    metricas["por_codigo_http"][codigo_http] += 1
    metricas["por_endpoint"][endpoint] += 1
    metricas["tiempos_respuesta_ms"].append(duracion_ms)

    if 200 <= codigo_http < 400:
        metricas["solicitudes_exitosas"] += 1
    else:
        metricas["solicitudes_con_error"] += 1


def obtener_metricas():
    """
    Retorna un resumen de las métricas actuales, incluyendo el
    tiempo promedio de respuesta calculado en el momento de la consulta.
    """
    tiempos = metricas["tiempos_respuesta_ms"]
    promedio = round(sum(tiempos) / len(tiempos), 2) if tiempos else 0

    return {
        "total_solicitudes": metricas["total_solicitudes"],
        "solicitudes_exitosas": metricas["solicitudes_exitosas"],
        "solicitudes_con_error": metricas["solicitudes_con_error"],
        "tiempo_promedio_respuesta_ms": promedio,
        "solicitudes_por_codigo_http": dict(metricas["por_codigo_http"]),
        "solicitudes_por_endpoint": dict(metricas["por_endpoint"]),
    }
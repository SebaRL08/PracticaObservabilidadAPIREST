"""
Módulo encargado de recopilar y administrar métricas de la aplicación.

Este módulo permite registrar información sobre las solicitudes realizadas
a la aplicación, como la cantidad de peticiones, los códigos HTTP utilizados,
los endpoints consultados y el tiempo de respuesta. Estos datos se almacenan
temporalmente en memoria para generar un resumen de las métricas.

Limitación:
    Las métricas se almacenan únicamente en la memoria RAM. Por esta razón,
    todos los datos se perderán cuando el servidor se reinicie.
"""

import time
from collections import defaultdict

# Diccionario donde se guardan temporalmente las métricas de la aplicación.
# La información se pierde cuando el servidor se reinicia.
metricas = {
    "total_solicitudes": 0,
    "solicitudes_exitosas": 0,
    "solicitudes_con_error": 0,
    "por_codigo_http": defaultdict(int),
    "por_endpoint": defaultdict(int),
    "tiempos_respuesta_ms": [],  # Guarda los tiempos para calcular el promedio
}


def registrar_solicitud(endpoint: str, codigo_http: int, duracion_ms: float) -> None:
    """
    Guarda la información de una solicitud que ya fue procesada.

    Se actualizan los contadores generales, el endpoint utilizado,
    el código de respuesta HTTP y el tiempo que tardó la solicitud.
    También se identifica si la respuesta fue exitosa o si presentó un error.

    Args:
        endpoint (str): Ruta utilizada para realizar la solicitud.
        codigo_http (int): Código HTTP obtenido en la respuesta.
        duracion_ms (float): Tiempo de respuesta de la solicitud en milisegundos.

    Returns:
        None
    """
    metricas["total_solicitudes"] += 1
    metricas["por_codigo_http"][codigo_http] += 1
    metricas["por_endpoint"][endpoint] += 1
    metricas["tiempos_respuesta_ms"].append(duracion_ms)

    if 200 <= codigo_http < 400:
        metricas["solicitudes_exitosas"] += 1
    else:
        metricas["solicitudes_con_error"] += 1


def obtener_metricas() -> dict:
    """
    Obtiene un resumen de las métricas registradas hasta el momento.

    El tiempo promedio de respuesta se calcula utilizando los tiempos
    almacenados. Además, los defaultdict se convierten en diccionarios
    normales para facilitar la consulta y el envío de la información.

    Returns:
        dict: Resumen con el total de solicitudes, solicitudes exitosas,
        solicitudes con error, tiempo promedio de respuesta, cantidad
        de solicitudes por código HTTP y cantidad por endpoint.
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

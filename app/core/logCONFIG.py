"""
Módulo de Configuración de Observabilidad y Logging.

Este módulo inicializa y configura el sistema centralizado de registros (logs) 
de la aplicación. Garantiza la creación automática del directorio de almacenamiento 
y establece un doble manejador (handlers) para persistir los eventos tanto en 
un archivo físico como en la salida estándar de la consola.
"""

import logging
import os

# Aseguramos que exista la carpeta logs/ antes de escribir en ella
os.makedirs("logs", exist_ok=True)

def configurar_logging():
    """
    Configura y retorna el sistema de logging global de la aplicación.

    Establece el nivel base en INFO, define un formato estandarizado que incluye 
    marca de tiempo, severidad y mensaje, y configura manejadores duales para 
    escribir los registros en el archivo 'logs/app.log' (con codificación UTF-8) 
    y mostrarlos simultáneamente en la consola.

    Returns:
        logging.Logger: Instancia del registrador configurado bajo el nombre 
        'observabilidad_api' listo para ser utilizado en el sistema.
    """
    formato = "%(asctime)s %(levelname)s %(message)s"
    fecha_formato = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.INFO,
        format=formato,
        datefmt=fecha_formato,
        handlers=[
            logging.FileHandler("logs/app.log", encoding="utf-8"),
            logging.StreamHandler()  # también muestra los logs en consola
        ]
    )

    return logging.getLogger("observabilidad_api")

# ------------------------------------------------------------
# Bloque de prueba temporal — lo eliminaremos más adelante
# ------------------------------------------------------------
if __name__ == "__main__":
    logger = configurar_logging()
    logger.info("Prueba de log - sistema de logging funcionando correctamente")
    logger.error("Prueba de log de error - simulación")

import logging
import os

# Aseguramos que exista la carpeta logs/ antes de escribir en ella
os.makedirs("logs", exist_ok=True)

def configurar_logging():
    """
    Configura el sistema de logging de la aplicación.
    Los logs se escriben tanto en un archivo (logs/app.log) como
    en la consola, con un formato que incluye fecha, hora, nivel
    del log y el mensaje descriptivo.
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

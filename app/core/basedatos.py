import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env al entorno del proceso
load_dotenv()

# Configuración de conexión a MySQL, leída desde variables de entorno
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


def obtener_conexion():
    """
    Crea y retorna una nueva conexión a la base de datos MySQL.
    Lanza una excepción si la conexión falla (por ejemplo, si el
    servidor MySQL está apagado o las credenciales son incorrectas).
    Esta excepción será capturada más adelante por el repositorio
    y registrada en los logs como un error de conexión.
    """
    conexion = mysql.connector.connect(**DB_CONFIG)
    return conexion


# ------------------------------------------------------------
# Bloque de prueba temporal — lo eliminaremos más adelante
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        conexion = obtener_conexion()
        print("✅ Conexión exitosa a la base de datos:", DB_CONFIG["database"])
        conexion.close()
    except Error as e:
        print("❌ Error al conectar a la base de datos:", e)
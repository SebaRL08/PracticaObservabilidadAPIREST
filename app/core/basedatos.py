"""
Modulo de Configuracion y Conexion a Base de Datos.

Este modulo se encarga de gestionar la conexion con una base de datos MySQL 
utilizando credenciales seguras cargadas desde variables de entorno a traves 
de la libreria python-dotenv.

Dependencias principales:
    - mysql.connector: Conector oficial de MySQL para Python.
    - python-dotenv: Gestor de variables de entorno desde archivos .env.
"""

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
    Crea y retorna una nueva conexión activa a la base de datos MySQL.

    La función toma los parámetros de configuración definidos en el diccionario 
    global DB_CONFIG, los cuales se alimentan directamente de las variables 
    de entorno del sistema.

    Returns:
        mysql.connector.connection.MySQLConnection: Objeto que representa 
        la conexión establecida con la base de datos.

    Raises:
        mysql.connector.Error: Si ocurre un fallo al intentar conectar 
        (por ejemplo, servidor apagado, credenciales incorrectas o base de datos inexistente).
        ValueError: Si alguna variable de entorno numérica (como el puerto) no es válida.
        
    Note:
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
"""
Módulo para iniciar el servidor de la aplicación.

Este archivo permite ejecutar la API utilizando Uvicorn como servidor.
Está configurado para trabajar de forma local y reiniciar automáticamente
el servidor cuando se realicen cambios en el código durante el desarrollo.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.mainApp:app", host="127.0.0.1", port=8000, reload=True)




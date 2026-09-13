# PracticaObservabilidadAPIREST

API REST liviana para la gestión de un catálogo de productos, integrada con un sistema de registro de eventos estructurado para garantizar el monitoreo, rastreo de errores y observabilidad del servicio en tiempo real. Este proyecto corresponde a la Sesión 7: Observabilidad y DevOps inteligente con IA del módulo de Fundamentos de Programación Avanzada con IA[cite: 1].

---

## Descripción
---
Desarrollar una aplicación multicapa con prácticas de DevOps e introducir mecanismos de observabilidad (logs, métricas y análisis inteligente con IA) para la detección temprana de incidentes en una API de gestión de productos[cite: 1].

El sistema está construido utilizando Python, FastAPI, Uvicorn, MySQL Connector (`mysql.connector`), Pydantic y Python-dotenv[cite: 1], estructurado modularmente en capas: Enrutamiento, Servicios, Repositorio y Núcleo.

---

## Objetivo
---
Implementar una arquitectura de software robusta que permita registrar operaciones, recolectar métricas de rendimiento en tiempo real y manejar excepciones de negocio de forma centralizada, facilitando el análisis y la detección de anomalías mediante herramientas de Inteligencia Artificial[cite: 1].

---

## Requerimientos principales
---
* **Consultar Productos:** Permite listar el inventario completo ordenado por ID o buscar un producto específico mediante su identificador[cite: 1].
* **Registrar Producto:** Inserción de nuevos artículos validando restricciones comerciales y de stock.
* **Actualizar Producto:** Modificación de atributos de un artículo existente.
* **Eliminar Producto:** Baja de un registro por medio de su ID[cite: 1].
* **Monitoreo y Métricas (`/metrics`):** Endpoint dedicado a exponer contadores en tiempo real, tasas de éxito/error y tiempos promedio de respuesta.

---

## Pruebas de funcionamiento y situaciones de falla
---
* **Consulta de un registro inexistente:** Petición `GET /productos/999` que retorna un código HTTP `404 Not Found` y genera un log estructurado de nivel `ERROR`.
* **Envío de información incompleta:** Petición `POST /productos` validada automáticamente por Pydantic con respuesta HTTP `422 Unprocessable Entity`.
* **Falla de conexión con la base de datos:** Simulación de caída del motor MySQL que arroja un error controlado HTTP `500 Internal Server Error`.

---

## Análisis mediante Inteligencia Artificial
---
Auditoría de los registros del sistema utilizando un modelo de lenguaje especializado en ingeniería DevOps[cite: 1] para evaluar el aislamiento de errores, el rendimiento y proponer mejoras de persistencia hacia entornos de producción.
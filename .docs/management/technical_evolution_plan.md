# Plan de Evolución Técnica: Tradefish Full-Stack

Este documento define la arquitectura técnica para evolucionar el prototipo actual hacia una aplicación sólida y escalable.

## 1. Arquitectura del Frontend (Modular JS)

Para que el frontend sea "fácil de iterar", pasaremos de un script único a una estructura de **servicios**.

*   **`api.js`**: Único punto de contacto con el backend. Centraliza los `fetch`.
*   **`store.js`**: Estado global de la aplicación (usuario actual, cartera cargada).
*   **`ui.js`**: Lógica de renderizado de componentes (tablas, cards, modales).
*   **`app.js`**: Orquestación y rutas.

> [!TIP]
> Esta estructura permite que si mañana cambias el backend de LocalStorage a FastAPI, solo tengas que tocar `api.js`.

---

## 2. El "Escudo Triple" de Seguridad

No necesitamos ser expertos si aplicamos esta arquitectura delegada:

1.  **Capa Exterior (Cloudflare)**: Detiene ataques DDoS y oculta la IP real de Google.
2.  **Capa de Cómputo (Cloud Run)**: Contenedores aislados y efímeros (Serverless).
3.  **Capa de Identidad (Firebase/GCP)**: Autenticación con estándares bancarios delegada en Google.

---

## 3. Mapa de Relaciones y Flujo E2E

### Relaciones de Datos
*   **1 Usuario : N Posiciones**: Cada posición pertenece a un `UID` único de Firebase.
*   **Señal -> Posición**: Una posición de usuario siempre referencia a una `Signal` (Señal) del Admin.

### Flujo Crítico (Registro de Inversión)
1.  **UI**: El usuario pulsa "Sincronizar" -> Modal captura `Asset` y `Capital`.
2.  **API**: `POST /api/v1/positions` con el Token de Firebase.
3.  **Backend**: Valida Token, calcula "Capital Disponible" en **transacción atómica**.
4.  **DB**: Inserta en Postgres y devuelve éxito.

---

## 4. Stack Tecnológico & Infra (GCP)

*   **Backend**: FastAPI + Python 3.12 + SQLModel.
*   **BBDD**: PostgreSQL en **Cloud SQL**.
*   **Hosting**: **Google Cloud Run** (Escalado a 0 = Cero coste sin tráfico).
*   **IA**: Integración con **Vertex AI** para análisis de señales.

## 5. Próximos Pasos (Hoja de Ruta)

1.  **Consolidación de Identidad**: Configurar Firebase Auth (Google Login).
2.  **Backend MVP**: Skeleton de FastAPI con salud de conexión a DB.
3.  **Refactor Frontend**: Extraer lógica de `index.html` a módulos JS.
4.  **Seguridad**: Configurar alertas de presupuesto (al 25%, 50%, 100%) en GCP.

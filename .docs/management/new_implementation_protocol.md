# Protocolo para Nuevas Implementaciones (Herramientas, Infra y Tech-Stack)

Este protocolo se activa cuando el usuario propone añadir un elemento **nuevo** al ecosistema que no existía previamente (una nueva base de datos, una librería, un servicio de nube o una herramienta externa).

## 1. El Interrogatorio Crítico (Discovery)
Antes de aceptar la herramienta, la IA debe preguntar:
*   **Input/Output Exacto**: ¿Qué datos entran y salen? No se aceptan "vaguetades".
*   **Análisis de Acoplamiento**: ¿Cómo afecta esto al código actual? ¿Es una dependencia necesaria o un "capricho" técnico?
*   **Plan de Contingencia**: ¿Qué pasa si la herramienta falla?

## 2. Investigación Autónoma (Validación)
La IA lanzará un sub-agente de navegación para:
*   Extraer la **última versión estable** y sus cambios recientes (Breaking Changes).
*   Validar la compatibilidad real con el stack actual (Python 3.x, FastAPI, etc.).
*   Identificar "Gotchas" (problemas conocidos) en foros y documentación oficial.

## 3. La "Ficha Técnica" (Documentación de Verdad)
No se implementará nada sin un archivo en `docs/tech-stack/` o `docs/features/active/` que contenga:
*   **Contrato Técnico**: Definición final de la implementación.
*   **Zonas Grises**: Marcadas explícitamente como `[PENDIENTE]` si no hay información clara.

## 4. El Stress Test de Integración
Cuestionamiento final: ¿Estamos duplicando funciones que ya tiene otra herramienta? ¿Aporta valor real o solo complejidad?

---
> [!IMPORTANT]
> Este archivo complementa al `feedback_protocol.md`. Mientras que aquel gestiona **cambios**, este gestiona **nacimientos** de nuevas tecnologías.

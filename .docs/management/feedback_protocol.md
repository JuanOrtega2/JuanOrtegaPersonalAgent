# Protocolo de Cambios y Feedback: "Definición-Primero"

Este documento define cómo gestionamos los cambios en Tradefish para mantener la robustez técnica.

## 1. El Ciclo de 5 Pasos (Unificado)

Ante cualquier cambio, idea o corrección tarde ("Oh, falta X"), seguiremos este flujo:

1.  **Análisis de Impacto (IA)**: Analizo IU, API y DB. ¿Qué se rompe? ¿Qué cambia?
2.  **Stress Test Técnico**: Me detendré a cuestionar la decisión (¿Es mediocre? ¿Escala?).
3.  **Investigación Proactiva**: Máximo 2 minutos de búsqueda web si hay dudas técnicas.
4.  **Actualización de Documentos**: Reflejo el cambio en `docs/features/active/`.
5.  **Luz Verde y Ejecución**: Programo solo tras tu OK explícito en el documento de feature.

## 2. Herramientas de Soporte (Contratos)
Usaremos diagramas de secuencia (`mermaid`) y tablas de API para que siempre sepas "qué recibe el dato" antes de que se escriba el código.

---
> [!TIP]
> Si el cambio implica una tecnología totalmente nueva, consulta primero el `new_implementation_protocol.md`.

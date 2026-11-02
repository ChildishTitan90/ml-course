# Capítulo 5: Aprendizaje Supervisado

[Índice en Notion](https://app.notion.com/p/40b81a767e1781f88b7eda0939579e98)

Guías detalladas con ejemplos explicados y diagramas. Los bloques de Python de cada unidad se ejecutan en orden; no requieren descargas de datos.

## Unidades y navegación

| Unidad | Qué se explica | Guía |
| --- | --- | --- |
| 1 · Datos y evaluación | Entradas, etiquetas, fit, separación, validación y fuga | [Unidad 1: Análisis de datos basado en aprendizaje automático](guias/unidad_01_analisis_con_ml.md) · [Notion](https://app.notion.com/p/40b81a767e17815abdfbcccb86a08092) |
| 2 · Predicción numérica | Coeficientes, pérdida, residuos, métricas y regularización | [Unidad 2: Modelos para predicción numérica](guias/unidad_02_prediccion_numerica.md) · [Notion](https://app.notion.com/p/40b81a767e17810ca4f9f956627aa5bc) |
| 3 · Clasificación | Logística, probabilidades, umbrales y matriz de confusión | [Unidad 3: Modelos para clasificación](guias/unidad_03_clasificacion.md) · [Notion](https://app.notion.com/p/40b81a767e178158ace8ffe2fd94c165) |
| 4 · Árboles de decisión | Divisiones, Gini, entropía, hojas y poda | [Unidad 4: Árboles de decisión](guias/unidad_04_arboles_decision.md) · [Notion](https://app.notion.com/p/40b81a767e17819c93a5d12fc9b207af) |
| 5 · KNN | Distancias, vecinos, escalado y elección de k | [Unidad 5: K vecinos más cercanos (KNN)](guias/unidad_05_knn.md) · [Notion](https://app.notion.com/p/40b81a767e178199af46c209a41a8b82) |
| 6 · SVM | Frontera, normal, margen, C y kernels | [Unidad 6: Máquinas de vectores de soporte (SVM)](guias/unidad_06_svm.md) · [Notion](https://app.notion.com/p/40b81a767e17811b869ac679521eb20f) |
| 7 · Conjuntos | Votación, bootstrap, Random Forest y boosting | [Unidad 7: Algoritmos de conjunto](guias/unidad_07_algoritmos_conjunto.md) · [Notion](https://app.notion.com/p/40b81a767e1781f4aa66dd8eb1c2271e) |

## Cómo se conecta con los capítulos anteriores

- Capítulo 1 define la tarea, los datos disponibles y los límites de las aplicaciones.
- Capítulo 2 aporta funciones, distancias, productos internos, matrices y derivadas.
- Capítulo 3 organiza las entradas y aprende una preparación consistente.
- Capítulo 4 ayuda a distinguir estimación, variación y evidencia.
- Este capítulo combina esas bases para ajustar modelos y evaluar predicciones.

## Equivalencia con Canvas

| Tema visible en Canvas | Unidades de esta guía |
| --- | --- |
| 5.1 · Análisis de datos basado en aprendizaje automático | 1 |
| 5.2 · Modelos para predicción numérica | 2 |
| 5.3 · Modelos para clasificación | 3 |
| 5.4 · Árboles de decisión | 4 |
| 5.5 · KNN y SVM | 5 y 6 |
| 5.6 · Algoritmos de conjunto | 7 |

## Vocabulario transversal

| Término | Significado en el flujo |
| --- | --- |
| Característica | Información de entrada disponible al predecir |
| Objetivo | Respuesta conocida en entrenamiento |
| Parámetro | Valor ajustado por el algoritmo |
| Hiperparámetro | Configuración comparada durante el desarrollo |
| Pérdida | Criterio utilizado para ajustar el modelo |
| Métrica | Resumen del desempeño que queremos interpretar |
| Baseline | Referencia sencilla para comparar |
| Generalización | Desempeño en casos nuevos pertinentes |
| Fuga de información | Uso indebido de información durante el desarrollo |
| Validación | Datos o particiones para elegir alternativas |
| Test | Datos reservados para la evaluación final |
| Residuo | Valor real menos predicción numérica |
| Umbral | Regla para convertir un puntaje en decisión |
| Regularización | Restricciones o penalizaciones que controlan el ajuste |
| Calibración | Correspondencia entre probabilidades estimadas y frecuencias observadas |
| Ensemble | Combinación de estimadores |

## Fuentes y alcance

[Temario en Canvas](https://udem.instructure.com/courses/36648/pages/5-aprendizaje-supervisado) · [Presentación](https://udem.instructure.com/courses/36648/pages/recursos-didacticos-del-capitulo-5-2?module_item_id=5019830). Se revisaron los índices y secciones representativas; las explicaciones, cuentas y diagramas son originales. Los ejemplos no resuelven las actividades oficiales.

Los siete ejemplos completos se comprobaron con el entorno del proyecto. Sus salidas están documentadas en cada unidad y en ../recursos/resultados_validacion.json.

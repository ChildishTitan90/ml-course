# Revisión de las guías de Machine Learning

Revisión del 31 de octubre de 2026.

## Contenido entregado

- 17 unidades de los capítulos 1–4 ampliadas, conservando sus apartados del temario.
- Cinco guías prácticas de Python y tres explicaciones de actividades con apoyos visuales.
- Siete unidades nuevas del capítulo 5, su índice local y sus páginas en Notion.
- 30 diagramas originales en SVG y PNG, con lecturas guiadas junto a los conceptos.
- Ejemplos desarrollados y resultados interpretados; no se añadieron autoevaluaciones.

[Índice general local](../README_guias.md) · [Capítulo 5](../chapter_05/README.md) · [Índice de Notion](https://app.notion.com/p/3fe81a767e17803abd37f5d928898d38) · [Capítulo 5 en Notion](https://app.notion.com/p/40b81a767e1781f88b7eda0939579e98).

## Alcance de las fuentes

Los capítulos 1–4 parten de sus guías existentes y se contrastaron con sus páginas de Notion; se conservaron las notas e imágenes adicionales de esas páginas. Se amplió el desarrollo conceptual y se sustituyeron los cierres de preguntas por conexiones explicadas.

Para el capítulo 5 se consultaron el índice de Canvas y los índices y secciones representativas de su presentación de 285 diapositivas. No se presenta esta revisión como transcripción o inspección visual de cada una de las 285 láminas. Las fórmulas, ejemplos y diagramas son desarrollos propios, con referencias primarias de las bibliotecas junto a las guías.

La conversación y el índice de la guía de CCNA sirvieron como referencia de organización y apoyo visual. No se trasladaron sus autoevaluaciones.

## Correcciones y aclaraciones destacadas

Se distinguieron multiclase y multietiqueta, exactitud y precisión positiva, parámetro e hiperparámetro, puntaje y probabilidad, fit y transform, y desviación y error estándar. Se detallaron los denominadores de Bayes, la interpretación de intervalos y p-valores, las dimensiones de arrays y las reglas de escalado.

En el capítulo 5 se precisó que Lasso puede producir coeficientes cero, que KNN sí tiene una fase fit, que Random Forest puede sobreajustar y que el efecto del umbral sobre precision no es estrictamente monótono. Se anotó el cambio de SVC relacionado con probabilidades en scikit-learn 1.9.

## Comprobaciones realizadas

Los siete ejemplos completos del capítulo 5 se ejecutaron en un contexto nuevo por unidad, reuniendo sus bloques de Python en orden. Se comprobaron las cuentas numéricas y los enlaces locales; los 30 SVG se analizaron como XML y se revisaron sus vistas PNG. Los resultados se guardan en [resultados_validacion.json](resultados_validacion.json).

Entorno observado: NumPy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1 y Matplotlib 3.11.2. Los avisos de FigureCanvasAgg del informe se deben al renderizado sin ventana durante la comprobación; los ejemplos se completaron.

Se verificó por el conector la presencia de las siete páginas nuevas, sus imágenes, bloques de Python y resultados explicados. El código guardado en Notion coincide con el ejecutado localmente. La vista web de Notion requirió inicio de sesión, por lo que la comprobación del contenido guardado se realizó mediante el conector, y la visual mediante los PNG locales. La correspondencia de archivos y páginas se conserva en [mapa_notion.json](mapa_notion.json).

Los notebooks y proyectos del curso no se modificaron como parte de esta revisión. Los cambios locales de esta tarea están dentro de workspace/.

## Reproducir los apoyos visuales y la comprobación

Ejecutar desde la raíz del repositorio:

```powershell
uv run python workspace/my_lectures/recursos/generar_diagramas.py
uv run python workspace/my_lectures/recursos/validar_guias.py
```

La ejecución del segundo comando comprueba los ejemplos actuales, no vuelve a publicar páginas de Notion.

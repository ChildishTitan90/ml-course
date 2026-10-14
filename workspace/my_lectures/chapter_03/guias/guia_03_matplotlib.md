# Guía de estudio: Matplotlib y Seaborn

Basada en `my_03_matplotlib.ipynb`. Incluye cómo elegir y leer gráficas para que puedas realizar la Parte 3 de la actividad por tu cuenta, sin proporcionar sus soluciones.

## 1. Qué aporta la visualización

NumPy permite calcular; pandas permite explorar y transformar tablas; Matplotlib permite representar los datos visualmente.

Una gráfica ayuda a observar cambios, distribuciones, relaciones y posibles valores atípicos. Antes de dibujar, escribe qué pregunta quieres responder.

| Pregunta general | Gráfica habitual |
|---|---|
| ¿Cómo cambia algo a lo largo del tiempo? | Líneas |
| ¿Qué relación hay entre dos medidas? | Dispersión |
| ¿Cómo se comparan cantidades por categoría? | Barras |
| ¿Cómo se distribuyen los valores de una medida? | Histograma |
| ¿Cómo cambian las distribuciones entre grupos? | Boxplot o histogramas por grupo |
| ¿Qué valores contiene una matriz? | Mapa de calor |

## 2. Datos de práctica e imports

Ejecuta los ejemplos en orden en un notebook de trabajo. Cada gráfica posterior comienza creando su propia figura.

```python
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dias_ejemplo = np.array([1, 2, 3, 4])
temperaturas = np.array([18, 21, 19, 23])

libros = pd.DataFrame({
    "genero": ["novela", "ciencia", "novela", "ciencia", "novela", "ciencia"],
    "paginas": [180, 240, 120, 300, 210, 150],
    "horas_lectura": [6, 8, 5, 11, 7, 6],
    "formato": ["papel", "digital", "digital", "papel", "papel", "digital"],
})
```

Son datos pequeños para entender las instrucciones. Para explorar distribuciones reales conviene disponer de más observaciones.

## 3. Figure, Axes y las dos interfaces

- **Figure**: la figura completa.
- **Axes**: un área de dibujo con su título y sus ejes horizontal y vertical.

```python
fig, ax = plt.subplots()
```

`fig` identifica la figura y `ax`, el área donde dibujas. **`ax` no es el parámetro `axis` de NumPy.**

La interfaz `pyplot` usa instrucciones como `plt.plot(...)` y `plt.title(...)`. La interfaz orientada a objetos utiliza `ax.plot(...)` y `ax.set_title(...)` para indicar explícitamente dónde dibujar. Esta guía utiliza la segunda.

## 4. Una gráfica de líneas completa

```python
fig, ax = plt.subplots()
ax.plot(dias_ejemplo, temperaturas, marker="o", label="sensor A")
ax.set_title("Temperatura durante cuatro días")
ax.set_xlabel("Día")
ax.set_ylabel("Temperatura (°C)")
ax.legend()
ax.grid(alpha=0.3)
plt.show()
```

`plot(x, y)` empareja los elementos por posición y conecta los puntos en el orden recibido. Las secuencias deben tener la misma longitud. Si el orden está desorganizado, la línea también lo estará.

Para varias series, llama varias veces a `ax.plot(...)` sobre el mismo `ax`. Usa un `label` diferente en cada serie y después muestra la leyenda.

Toda gráfica debe explicar qué representa: título, etiquetas con unidades y leyenda cuando hay varias series o grupos.

## 5. Personalización y referencias

| Parámetro o método | Para qué sirve |
|---|---|
| `color` | Elegir el color |
| `marker="o"` | Marcar las observaciones con círculos |
| `linestyle="--"` | Usar línea discontinua |
| `linewidth` | Ajustar grosor |
| `alpha` | Transparencia: cero invisible, uno opaco |
| `label` | Texto de la leyenda |
| `ax.set_xlim(...)` / `ax.set_ylim(...)` | Límites de los ejes |
| `ax.set_xticks(...)` | Posiciones de las marcas horizontales |
| `ax.axhline(...)` | Línea horizontal de referencia |
| `ax.axvline(...)` | Línea vertical de referencia |

`fill_between(x, inferior, superior)` sombrea una banda entre dos series. Puede representar incertidumbre, pero debes indicar qué significan esos límites: no toda banda es un intervalo de confianza.

## 6. Dispersión: una observación por punto

`ax.scatter(x, y)` representa dos medidas sin conectar observaciones. El notebook también usa `sns.scatterplot` para trabajar directamente con un DataFrame:

```python
fig, ax = plt.subplots()
sns.scatterplot(
    data=libros,
    x="paginas",
    y="horas_lectura",
    hue="genero",
    ax=ax,
)
ax.set_title("Páginas y horas de lectura")
ax.set_xlabel("Páginas")
ax.set_ylabel("Horas de lectura")
plt.show()
```

Cada punto es un libro. `hue` distingue géneros mediante colores. Puedes observar tendencias, grupos, dispersión y puntos alejados.

Una asociación no demuestra causalidad. Tampoco debes conectar observaciones independientes solo porque tienen dos medidas.

## 7. Barras: conteos, medias y totales

Estas herramientas pueden producir gráficas parecidas, pero hacen cosas distintas:

| Herramienta | Qué representa |
|---|---|
| `ax.bar(categorias, valores)` | Los valores que tú preparaste |
| `ax.barh(categorias, valores)` | Lo mismo, con barras horizontales |
| `sns.countplot(data=tabla, x="categoria")` | Cantidad de registros por categoría |
| `sns.barplot(data=tabla, x="categoria", y="medida")` | Por defecto, media de la medida por categoría |

`countplot` se relaciona con `value_counts()`. `barplot` se relaciona con `groupby(...).mean()`.

En Matplotlib, `ax.bar_label(barras)` permite mostrar el valor sobre las barras creadas.

**Antes de dibujar, decide si necesitas un conteo, una suma o una media.** Seaborn no sabe qué pregunta quieres responder: no asumas que `barplot` calcula un total.

Las barras de error de un `barplot` muestran incertidumbre según su configuración; no son, por defecto, el mínimo y máximo del grupo.

## 8. Histograma: valores agrupados en intervalos

```python
fig, ax = plt.subplots()
sns.histplot(data=libros, x="paginas", bins=4, ax=ax)
ax.set_title("Distribución de páginas")
ax.set_xlabel("Páginas")
ax.set_ylabel("Número de libros")
plt.show()
```

Cada barra representa un intervalo numérico. Su altura indica cuántos registros están dentro, cuando se usa el conteo predeterminado.

`bins` controla cuántos intervalos se forman. Pocos ofrecen una vista general; demasiados pueden hacer la gráfica irregular.

Al leerla, pregunta dónde se concentran los datos, qué rango ocupan y si hay una cola hacia valores altos o bajos.

### Comparar grupos de distintos tamaños

Un grupo puede tener barras más altas simplemente porque tiene más registros. El notebook utiliza `stat="density"` y `common_norm=False` para normalizar por separado y comparar la forma de las distribuciones. En ese caso, el eje vertical ya no es un conteo; el área de cada distribución normalizada vale uno.

## 9. Boxplot y cuartiles

El boxplot conecta las gráficas con los percentiles de `describe()`:

- La caja va de Q1 a Q3 y representa aproximadamente la mitad central de los datos.
- La línea dentro de la caja indica la mediana.
- Los bigotes alcanzan ciertos valores extremos según una regla.
- Los puntos separados son posibles valores atípicos según esa regla.

**Los bigotes no siempre representan el mínimo y máximo absolutos.** Con la regla habitual, se calcula `IQR = Q3 - Q1`; los bigotes alcanzan los valores observados más extremos dentro de los límites `Q1 - 1.5 * IQR` y `Q3 + 1.5 * IQR`.

Un punto separado no implica automáticamente un error. Puede ser una observación válida que merece investigación.

Al comparar categorías con `sns.boxplot(data=tabla, x="grupo", y="medida")`, observa medianas, tamaños de las cajas, bigotes y puntos. Ten presente cuántos datos hay en cada grupo.

## 10. Argumentos de Seaborn

Seaborn está construido sobre Matplotlib y trabaja cómodamente con pandas:

| Argumento | Significado |
|---|---|
| `data` | DataFrame que contiene los datos |
| `x`, `y` | Nombres de las columnas representadas |
| `hue` | Columna que distingue grupos por colores |
| `size` | Columna que controla el tamaño de puntos, cuando corresponde |
| `ax` | Área de Matplotlib donde dibujar |

`hue` no crea otra gráfica: diferencia grupos dentro de la misma. Las leyendas de grupos suelen generarse automáticamente.

## 11. Varios gráficos con subplots

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].plot(dias_ejemplo, temperaturas, marker="o")
axes[0].set_title("Evolución")
axes[0].set_xlabel("Día")
axes[0].set_ylabel("Temperatura (°C)")

axes[1].hist(temperaturas, bins=3)
axes[1].set_title("Distribución")
axes[1].set_xlabel("Temperatura (°C)")
axes[1].set_ylabel("Número de mediciones")

fig.suptitle("Dos perspectivas de las mismas mediciones")
plt.tight_layout()
plt.show()
```

Con una fila y dos columnas, seleccionas `axes[0]` y `axes[1]`. Con `plt.subplots(2, 2)`, normalmente recibes un array bidimensional y seleccionas `axes[fila, columna]`. Con una sola gráfica, recibes directamente `ax`.

`axes.flat` permite recorrer las áreas de una rejilla. `sharex=True` o `sharey=True` comparte escalas. `figsize` se expresa en pulgadas.

## 12. Matrices, imágenes y mapas de calor

`ax.imshow(M)` convierte una matriz numérica en una imagen. En una imagen RGB, la forma habitual es `(alto, ancho, 3)` para los canales rojo, verde y azul.

`sns.heatmap(M)` facilita representar matrices con etiquetas y valores escritos dentro:

```python
matriz_ejemplo = np.array([[1, 3, 2], [4, 2, 5]])

fig, ax = plt.subplots()
sns.heatmap(matriz_ejemplo, annot=True, fmt="d", cmap="viridis", ax=ax)
ax.set_title("Valores de una matriz de ejemplo")
ax.set_xlabel("Columna")
ax.set_ylabel("Fila")
plt.show()
```

`cmap` elige la escala de colores. `annot=True` escribe los valores. `fmt` indica su formato. La barra de color conecta colores con valores numéricos y no equivale a una leyenda de categorías.

Con `imshow`, guarda el objeto que devuelve y utiliza `fig.colorbar(objeto, ax=ax)` si necesitas esa escala.

## 13. Correlación

El notebook calcula `.corr()` sobre columnas numéricas y representa el resultado con un mapa de calor.

- Cerca de `+1`: asociación lineal positiva.
- Cerca de `-1`: asociación lineal negativa.
- Cerca de `0`: poca asociación lineal.

La diagonal suele ser uno porque cada variable se compara consigo misma, siempre que su correlación esté definida. Una variable constante no tiene una correlación definida.

Una correlación cercana a cero no descarta una relación curva. Una correlación alta tampoco prueba una causa. Fijar `vmin=-1` y `vmax=1` permite mantener una escala comparable entre mapas de correlación.

## 14. Las gráficas de Machine Learning del notebook

Esta sección es más avanzada. Primero entiende qué pregunta responde cada gráfica; no necesitas dominar el entrenamiento de modelos para practicar visualización básica.

| Gráfica | Qué muestra |
|---|---|
| Pérdida por época | Cómo cambia el error durante el entrenamiento |
| Frontera de decisión | Regiones que el clasificador asigna a cada clase |
| Matriz de confusión | Aciertos y errores, separados por clases |
| Ajustes de distinta complejidad | Modelos demasiado simples o demasiado ajustados a los datos |
| Error frente a complejidad | Qué complejidad funciona mejor en validación |
| Predicción frente a valor real | Cercanía de las predicciones a la diagonal de igualdad |
| Distribución de residuos | Diferencias entre lo observado y lo predicho |

### Entrenamiento y evaluación

Una época es una pasada por los datos de entrenamiento. Una pérdida menor suele indicar mejor ajuste bajo la medida elegida.

Si la pérdida de entrenamiento baja mientras la de validación aumenta, puede haber **sobreajuste**. Si el modelo no captura el patrón, puede haber **subajuste**. Que ambas curvas bajen es útil, pero por sí solo no garantiza un modelo adecuado.

En un flujo habitual, validación sirve para orientar decisiones y test para una evaluación final independiente. El ejemplo del notebook usa etiquetas de validación y test de forma simplificada.

### Fronteras y matriz de confusión

`meshgrid` crea una rejilla de posiciones. `contourf` colorea regiones y `contour` dibuja líneas de igual valor, como un umbral de probabilidad.

En la matriz de confusión del notebook, las filas son las clases reales y las columnas, las predichas. La diagonal representa aciertos. La interpretación de cada celda depende de esas etiquetas.

### Residuos

`residuo = valor real - valor predicho`. Un residuo positivo indica una predicción demasiado baja; uno negativo, demasiado alta. Estar centrados cerca de cero es una comprobación, pero conviene buscar también patrones de los residuos frente a las predicciones.

## 15. Estilos y guardar figuras

Un estilo modifica la apariencia, no los datos. `plt.style.context(...)` lo aplica dentro de un bloque. `rcParams` configura valores predeterminados como tamaño o resolución.

Para guardar una figura, hazlo antes de `plt.show()`. Por ejemplo, reutilizando `fig` de la última gráfica, y ejecutando desde la raíz del repositorio:

```python
carpeta_figuras = Path("workspace/my_lectures/chapter_03/figuras")
carpeta_figuras.mkdir(parents=True, exist_ok=True)
fig.savefig(carpeta_figuras / "ejemplo_matriz.png", dpi=150, bbox_inches="tight")
```

PNG guarda una imagen de píxeles; PDF puede conservar elementos vectoriales. `dpi` controla la resolución de elementos rasterizados y `bbox_inches="tight"` ajusta el área al contenido.

## 16. Cómo abordar los ejercicios nuevos por tu cuenta

La Parte 3 utiliza arrays de la cafetería, el DataFrame de propinas y un nuevo DataFrame de pingüinos. Debes elegir la representación, no solo copiar una función.

Antes de cada gráfica:

1. Escribe la pregunta que quieres responder.
2. Identifica qué representa cada observación.
3. Decide si necesitas datos individuales, conteos, medias o totales.
4. Elige la gráfica y las variables de los ejes.
5. Decide si debes distinguir grupos por colores.
6. Añade título, etiquetas con unidades y leyenda cuando corresponda.
7. Describe lo observado sin afirmar causas que los datos no demuestran.

Explora primero los tipos y faltantes de cualquier dataset nuevo. Usa los nombres actuales de las columnas: si ya las renombraste, los nombres originales no funcionarán.

Para practicar fuera de la actividad, representa la evolución de las temperaturas, compara el número de libros por formato y organiza dos vistas de los libros en una misma figura. Explica por qué elegiste cada tipo de gráfica.

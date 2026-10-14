# Guía de estudio: pandas

Basada en `my_02_pandas.ipynb` y en las dudas que trabajamos durante la actividad.
Los ejemplos usan una tabla de libros y no resuelven la actividad del curso.

## 1. Para qué sirve pandas

pandas permite cargar, explorar y transformar tablas. Un **DataFrame** es una tabla de filas y columnas. Una **Series** representa una columna con un índice.

A diferencia de un array numérico de NumPy, un DataFrame puede tener columnas de diferentes tipos: números, texto, fechas y booleanos.

Ejecuta los bloques en orden en un notebook de trabajo. Empieza por los imports y la tabla de ejemplo:

```python
import numpy as np
import pandas as pd

libros = pd.DataFrame({
    "titulo": ["Bosque", "Órbita", "Río", "Atlas", "Luna", "Huerto"],
    "genero": ["novela", "ciencia", "novela", "ciencia", "novela", "ciencia"],
    "paginas": [180, 240, 120, 300, 210, 150],
    "formato": ["papel", "digital", "digital", "papel", "papel", "digital"],
    "horas_lectura": [6.0, 8.0, 4.0, 10.0, 7.0, np.nan],
})
```

Cada fila representa un libro. El último tiene un valor faltante en `horas_lectura` para practicar cómo detectarlo.

## 2. Series e índices

```python
temperaturas = pd.Series(
    [18, 21, 19],
    index=["lunes", "martes", "miércoles"],
    name="temperatura",
)

print(temperaturas["martes"])
print(temperaturas.mean())
```

El índice asigna etiquetas a los valores. La cantidad de etiquetas debe coincidir con la cantidad de elementos.

Una lista que contiene un array, como `[np.array([1, 2, 3])]`, contiene un elemento exterior; no equivale a una Series con tres valores numéricos independientes.

## 3. Cargar un archivo

La estructura para un CSV es `pd.read_csv(ruta)`. El archivo se convierte en un DataFrame, que debes guardar en una variable.

Si `DATA_DIR` ya apunta a `data/`, añade únicamente el nombre del archivo. Añadir otra vez `data/` buscaría una carpeta duplicada.

`index_col` indica qué columna del archivo se utilizará como índice. No es la cantidad de columnas ni de filas. Si no necesitas un índice especial, omite ese argumento.

Otras herramientas del notebook son `read_excel`, `read_json`, `read_parquet` y `read_sql`; cada una carga un formato o una fuente diferente.

## 4. Explorar la tabla

```python
print("Filas y columnas:", libros.shape)
print(libros.head())
libros.info()
print(libros.describe())
```

**`shape` no lleva paréntesis:** es un atributo. `head()`, `info()` y `describe()` sí los llevan: son métodos.

En Jupyter, normalmente solo se muestra automáticamente la última expresión de una celda. Puedes ejecutar cada exploración en una celda diferente o usar `print` para mostrar varios resultados. `info()` ya imprime su informe.

| Herramienta | Pregunta que responde |
|---|---|
| `.shape` | ¿Cuántas filas y columnas hay? |
| `.head()` / `.tail()` | ¿Cómo son los primeros o últimos registros? |
| `.sample(3, random_state=42)` | ¿Cómo son algunos registros elegidos al azar? |
| `.columns` | ¿Cuáles son los nombres de las columnas? |
| `.dtypes` | ¿Qué tipo tiene cada columna? |
| `.info()` | ¿Qué tipos y cuántos valores no nulos hay? |
| `.isna().sum()` | ¿Cuántos faltantes hay por columna? |
| `.nunique()` | ¿Cuántos valores diferentes hay por columna? |
| `.value_counts()` en una Series | ¿Cuántas veces aparece cada valor? |

Que no haya nulos no garantiza que todos los datos sean correctos. También puede haber duplicados o valores imposibles.

## 5. Interpretar describe

Por defecto, `describe()` resume las columnas numéricas:

| Fila | Significado |
|---|---|
| `count` | Cantidad de valores presentes |
| `mean` | Media: suma dividida entre cantidad de valores presentes |
| `std` | Desviación estándar: medida de dispersión |
| `min` | Mínimo |
| `25%` | Primer cuartil: posición del 25 % en los datos ordenados |
| `50%` | Mediana |
| `75%` | Tercer cuartil |
| `max` | Máximo |

Los porcentajes de esas filas describen posiciones en la distribución; no son porcentajes de la variable medida.

La media y la mediana pueden ser distintas. Valores extremos pueden desplazar la media. Además, los máximos de distintas columnas no necesariamente pertenecen a la misma fila.

Puedes explorar columnas no numéricas con `libros.describe(exclude="number")`. Su resumen incluye información como valores distintos y categorías frecuentes.

## 6. Seleccionar columnas y filas

```python
una_columna = libros["paginas"]
varias_columnas = libros[["titulo", "paginas"]]
```

La primera selección devuelve una Series. La segunda, un DataFrame: los corchetes interiores forman una lista de nombres.

| Herramienta | Selección por | Intervalos |
|---|---|---|
| `.iloc` | Posición numérica | Excluyen el final |
| `.loc` | Etiquetas | Incluyen el final en slicing por etiquetas |

```python
print(libros.iloc[0, 2])
print(libros.loc[0, "paginas"])
print(libros.iloc[:3, :2])
```

Al principio, las etiquetas del índice pueden coincidir con las posiciones. Después de filtrar, la primera fila conservada podría tener etiqueta tres pero posición cero.

## 7. Filtrar, contar y ordenar

```python
mascara = (libros["paginas"] > 150) & (libros["genero"] == "novela")
seleccion = libros.loc[mascara, ["titulo", "paginas"]]

print(seleccion)
print("Registros seleccionados:", mascara.sum())
print(libros["genero"].value_counts())
```

Usa `&` para exigir ambas condiciones, `|` para aceptar alguna y `~` para negar. Las comparaciones van entre paréntesis.

- `.isin(["valor_1", "valor_2"])`: pertenece a una lista.
- `.between(a, b)`: está entre los límites; por defecto incluye ambos.
- `.query("condición")`: expresa un filtro mediante texto.
- `.sort_values("columna", ascending=False)`: ordena de mayor a menor.

```python
print(libros.query("genero == 'novela' and paginas > 150"))
print(libros.sort_values("paginas", ascending=False).head(2))
```

`value_counts()` cuenta registros por categoría; no suma los valores de otra columna. Por defecto no cuenta los valores faltantes; `dropna=False` permite incluirlos.

## 8. Crear y transformar columnas

```python
libros["horas_estimadas"] = libros["paginas"] / 30
libros["extension"] = np.where(libros["paginas"] > 200, "larga", "corta")
libros["formato_codigo"] = libros["formato"].map({"papel": 0, "digital": 1})
```

Cada operación produce un valor por fila. `np.where` tiene la estructura: condición, resultado si se cumple y resultado si no se cumple.

`map` transforma valores mediante un diccionario. Si un valor no tiene correspondencia, normalmente se convierte en faltante. Revisa las categorías antes y después.

### Clasificar por intervalos

```python
libros["rango_paginas"] = pd.cut(
    libros["paginas"],
    bins=[0, 150, 250, 400],
    labels=["breve", "media", "extensa"],
)
```

Por defecto, esos intervalos son `(0, 150]`, `(150, 250]` y `(250, 400]`: incluyen el extremo derecho. Valores fuera de los intervalos quedan sin categoría.

### Renombrar, eliminar y modificar

- `rename(columns={"nombre_actual": "nombre_nuevo"})` cambia nombres.
- `drop(columns=["columna"])` elimina columnas.
- `.apply(funcion)` aplica una función propia a cada valor; las operaciones vectorizadas suelen ser preferibles para tareas sencillas.

Muchos métodos devuelven un resultado nuevo. Conserva el cambio asignándolo, como en `tabla = tabla.rename(...)`. Para cambiar ciertos valores, utiliza `tabla.loc[filas, columna] = valor`.

Si quieres experimentar sin modificar una tabla existente, crea antes una copia con `.copy()`.

## 9. Agrupar y resumir

`groupby` sigue tres pasos: dividir las filas en grupos, calcular dentro de cada grupo y combinar los resultados.

```python
print(libros.groupby("genero")["paginas"].mean())
print(libros.groupby("genero")["paginas"].agg(["count", "mean", "median"]))

resumen = libros.groupby("genero").agg(
    n_libros=("paginas", "size"),
    paginas_medias=("paginas", "mean"),
    horas_registradas=("horas_lectura", "count"),
)
print(resumen)
```

En cada agregación con nombre, la tupla indica la columna de origen y la función.

**`size` cuenta filas; `count` cuenta valores no nulos de la columna elegida.** Las medias de pandas también omiten normalmente los faltantes.

Agrupar por una lista, como `["genero", "formato"]`, permite resumir cada combinación.

## 10. Tablas dinámicas y cruzadas

```python
dinamica = pd.pivot_table(
    libros,
    values="paginas",
    index="genero",
    columns="formato",
    aggfunc="mean",
)
cruzada = pd.crosstab(libros["genero"], libros["formato"])

print(dinamica)
print(cruzada)
```

La tabla dinámica resume una medida: aquí, páginas medias. La tabla cruzada cuenta combinaciones de categorías.

En `crosstab`, `normalize="index"` convierte los conteos en proporciones dentro de cada fila. Sin normalización, conserva los conteos.

## 11. Combinar tablas

`merge` conecta registros mediante una clave común:

```python
info_generos = pd.DataFrame({
    "genero": ["novela", "ciencia"],
    "seccion": ["literatura", "divulgación"],
})

libros_ampliados = libros.merge(info_generos, on="genero", how="left")
```

| `how` | Qué conserva |
|---|---|
| `inner` | Coincidencias de ambas tablas |
| `left` | Registros de la izquierda |
| `right` | Registros de la derecha |
| `outer` | Claves de ambas tablas |

Si una clave coincide con varias filas en la tabla auxiliar, un registro original puede generar varias filas. Comprueba las claves y la cantidad de registros después de unir.

`concat` reúne tablas por filas o columnas. Para apilar registros, `ignore_index=True` crea un índice consecutivo nuevo.

## 12. Fechas y conversión a NumPy

Una columna que parece una fecha puede ser texto. `pd.to_datetime(...)` la convierte; después `.dt.year`, `.dt.month` y `.dt.dayofweek` extraen componentes. En `dayofweek`, lunes es cero y domingo, seis.

Con fechas en el índice, `resample(...)` permite agrupar por periodos; el notebook usa `"ME"` para fin de mes.

Para convertir columnas a NumPy:

```python
X = libros[["paginas", "horas_estimadas"]].to_numpy()
print(X.shape)
```

El array conserva el orden de las columnas seleccionadas, pero pierde sus nombres y las etiquetas del índice. Después debes recordar qué representa cada posición.

## 13. Interpretar antes de concluir

- Total, media y cantidad de registros responden preguntas distintas.
- La media de porcentajes no suele coincidir con el porcentaje calculado a partir de totales.
- Un porcentaje necesita un denominador claro: ¿porcentaje de qué conjunto?
- Una media calculada con pocos registros tiene menos respaldo para generalizar.
- Una diferencia entre grupos no demuestra su causa; también puede cambiar la composición de esos grupos.
- La media de valores cero y uno es la proporción de unos, si no hay faltantes que cambien el conjunto considerado.

Practica con `libros`: cuenta libros por formato, localiza faltantes, compara páginas medias por género y construye una tabla cruzada. Antes de ejecutar, explica qué representa cada fila de tu resultado.

# Unidad 2: Exploración de datos con pandas

## Objetivo y forma de estudiar

Aprenderás a leer una tabla, seleccionar información, combinar fuentes y resumirla. Los apartados son 2.1–2.4. En una exploración real comenzaremos con preguntas antes de concluir qué dicen los datos.

## 2.1. Pipelines: estructura de datos según el tipo de datos

Una **canalización de datos** organiza etapas de trabajo: obtener, interpretar, transformar y utilizar información.

```mermaid
flowchart LR
    A["Fuente: archivo, base de datos o servicio"] --> B["Lectura y estructura"]
    B --> C["Comprobar tipos, unidades y calidad"]
    C --> D["Seleccionar, combinar y resumir"]
    D --> E["Responder la pregunta y comunicar límites"]
```

Un CSV guarda texto separado por delimitadores; el programa interpreta ese contenido para construir columnas con tipos. Una base de datos puede entregar tablas; una fuente de texto o imágenes requiere otra representación.

El término pipeline aquí describe el flujo general de datos. La clase Pipeline de scikit-learn implementa una forma específica de encadenar transformaciones y modelos, que conectaremos con la unidad 3.

**Antes de cargar:** ¿qué representa una fila?, ¿qué columna identifica un registro?, ¿qué unidades y tipos esperamos?

## 2.2. Series de pandas y DataFrames

Una **Series** es una estructura de una dimensión con etiquetas. Un **DataFrame** organiza columnas, cada una con su tipo, y comparte un índice de filas.

```python
import pandas as pd

trips = pd.DataFrame({
    "trip_id": [1, 2, 3, 4],
    "zone": ["norte", "sur", "norte", "sur"],
    "distance": [2., 5., 3., 7.],
    "minutes": [9., 18., 12., 24.],
}, index=["a", "b", "c", "d"])

print(type(trips["minutes"]))       # Series
print(type(trips[["minutes"]]))     # DataFrame
print(trips.head())
print(trips.shape)
print(trips.dtypes)
```

Una selección con una cadena devuelve una Series; con una lista de columnas conserva el DataFrame. El índice etiqueta filas; no implica que esas etiquetas sean una característica útil para un modelo.

### Selección por etiqueta, posición y condición

```python
print(trips.loc["b", "minutes"])       # etiqueta: 18
print(trips.iloc[1, 3])                # posición: 18
print(trips.loc["a":"c", ["zone", "minutes"]])
print(trips.iloc[:2])                  # primeras dos posiciones
mask = (trips["zone"] == "norte") & (trips["minutes"] > 10)
selected = trips.loc[mask, ["trip_id", "minutes"]].copy()
print(selected)
```

**loc** utiliza etiquetas y sus cortes pueden incluir ambos extremos. **iloc** usa posiciones y excluye el límite final del corte. Las máscaras guardan una decisión verdadera/falsa por fila.

Al modificar datos utiliza una asignación explícita como **trips.loc[condicion, "minutes"] = valor**. Evita encadenar selecciones para escribir.

### Operaciones y eliminación

```python
trips["minutes_per_km"] = trips["minutes"] / trips["distance"]
without_zone = trips.drop(columns=["zone"])
ordered = trips.sort_values("minutes", ascending=False)
print(trips["minutes"] + 2)
```

La división se aplica fila por fila porque las Series se alinean por índice. Comprueba denominadores cero y unidades antes de crear una razón. **drop** devuelve por defecto un resultado nuevo: asigna el resultado si deseas conservarlo.

**Alineación:** al operar entre dos Series, pandas alinea sus etiquetas, no solo sus posiciones. Etiquetas sin pareja pueden originar faltantes.

## 2.3. Fusión y vinculación de DataFrames

**merge** relaciona registros por una clave. **concat** apila o coloca estructuras juntas según un eje.

Imagina una tabla de recorridos y otra de zonas. Antes de unirlas, comprueba qué significa la clave y si es única en la tabla de referencia.

```python
zones = pd.DataFrame({
    "zone": ["norte", "sur", "este"],
    "manager": ["Ana", "Luis", "Sol"],
})
joined = trips.merge(zones, on="zone", how="left", validate="many_to_one")
print(joined)
```

- **inner:** conserva claves con coincidencia en ambas tablas.
- **left:** conserva las filas de la izquierda y añade coincidencias.
- **right:** conserva las de la derecha.
- **outer:** conserva claves presentes en cualquiera de las dos.

Si una clave aparece varias veces en ambas tablas, una unión puede multiplicar filas. **validate** permite comprobar la relación esperada. Compara el número de filas antes y después.

**concat** con axis = 0 apila filas y con axis = 1 alinea columnas por índice. Unir por índice o por clave son decisiones distintas.

## 2.4. Estadísticas descriptivas y muestras de datos

![Dividir recorridos por zona, calcular medias y reunir resultados](../../imagenes/c03_pandas.svg)

**Lectura del diagrama:** al principio una fila es un recorrido; al final una fila es una zona. groupby cambia la unidad representada por cada fila. Para norte, las duraciones 9 y 12 dan (9+12)/2=10.5; para sur, 18 y 24 dan 21. El número de filas del resumen no tiene que coincidir con el de la tabla original.

### Conteo, suma y media no se intercambian

Si un grupo tiene duraciones [9,12,ausente], size cuenta 3 filas, count cuenta 2 mediciones y mean calcula 10.5 con las dos presentes. El total observado es 21 minutos, sin afirmar que el valor ausente fuera cero. Al comparar grupos conviene mostrar el tamaño y los faltantes junto al promedio.

### Etiqueta y posición después de filtrar

Supón un índice [10,20,30] y que conservamos las dos últimas filas. La primera posición del resultado es 0, pero su etiqueta sigue siendo 20. iloc[0] accede a esa primera posición y loc[20] a esa etiqueta. reset_index puede cambiar etiquetas, pero no es necesario para entender ni utilizar el resultado.

### Una unión puede cambiar el tamaño de la tabla

Si dos recorridos tienen zona “norte” y la tabla de referencia contiene dos filas para “norte”, cada recorrido coincide con ambas: se generan cuatro filas. No fue una suma ni un muestreo; fue una combinación de coincidencias. validate="many_to_one" exige que la tabla derecha tenga una referencia única por clave y ayuda a detectar ese problema.

También puede haber claves sin coincidencia. En una unión left, el recorrido permanece y los atributos de referencia quedan ausentes. Antes de imputarlos, conviene comprobar que la clave esté bien escrita y que la fuente auxiliar cubra esa zona.

Antes de interpretar una tabla, investiga:

1. ¿Qué significa cada columna y qué representa cada fila?
2. ¿Cuántas observaciones hay? ¿Faltan valores en alguna variable?
3. ¿Las unidades, tipos y rangos tienen sentido?
4. ¿Los grupos tienen tamaños comparables?
5. ¿Qué muestra un gráfico que un promedio podría ocultar?

Herramientas para obtener evidencia:

```python
print(trips.info())
print(trips.describe())
print(trips["zone"].value_counts(dropna=False))
print(trips.isna().sum())
print(trips.groupby("zone")["minutes"].agg(["count", "mean", "median"]))
print(trips[["distance", "minutes"]].corr())
print(trips.sample(n=2, random_state=42))
```

**describe** resume variables, pero no sustituye su interpretación. La media puede cambiar mucho por extremos; la mediana describe otra característica. **groupby** separa grupos, aplica una operación y combina resultados.

**count** cuenta valores no faltantes; **size** cuenta filas de un grupo. Correlación describe asociación, no demuestra causalidad. Una muestra pequeña o las primeras filas no garantizan representar toda la tabla.

Los datos del ejemplo fueron inventados para practicar herramientas. No constituyen evidencia sobre recorridos reales.

## Errores frecuentes

Confundir etiquetas con posiciones; crear una columna y olvidar sus unidades; asumir que cualquier unión conserva filas; interpretar códigos como cantidades; y saltar de un resumen a una conclusión sin revisar faltantes y distribución.

## Conexión de las ideas

Una exploración fiable conserva el significado de la fila y de los denominadores. Seleccionar reduce el conjunto observado; agrupar cambia su nivel de resumen; unir añade relaciones y puede multiplicar coincidencias. La interpretación del resultado depende de identificar cuál de estas operaciones ocurrió.

## Fuentes

[Capítulo 3 en Canvas](https://udem.instructure.com/courses/36648/pages/recursos-didacticos-del-capitulo-3-2?module_item_id=5019822), unidad 2, diapositivas 35–75. Complemento: **notebooks/lectures/chapter_03/02_pandas.ipynb**.

Para consultar diferencias entre selección por etiqueta y posición: [documentación oficial de pandas](https://pandas.pydata.org/docs/user_guide/indexing.html).


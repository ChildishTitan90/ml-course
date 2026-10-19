# Guía de estudio: transformación, codificación y escalado

Basada en [05_transformacion_y_escalado.ipynb](../../../../notebooks/lectures/chapter_03/05_transformacion_y_escalado.ipynb).
Continúa la [guía de limpieza y valores atípicos](guia_04_limpieza_y_outliers.md).

Los ejemplos utilizan paquetes de mensajería y no resuelven las actividades del curso.

## 1. El objetivo de esta clase

Una tabla limpia todavía puede necesitar preparación para un modelo:

| Necesidad | Herramienta |
|---|---|
| Comprimir una cola larga | Transformación logarítmica |
| Crear información a partir de columnas existentes | Ingeniería de variables |
| Representar categorías sin orden | One-hot encoding |
| Representar categorías con orden | Codificación ordinal |
| Hacer comparables las escalas | Estandarización o min-max |
| Evaluar con datos reservados | Separación train/test |
| Repetir el tratamiento sin inconsistencias | Pipeline y ColumnTransformer |

**Transformar, codificar y escalar no son sinónimos.** Cada operación responde a una necesidad distinta y no todos los modelos necesitan el mismo tratamiento.

## 2. Datos de práctica

Ejecuta los bloques en orden en un notebook de trabajo. Los imports están al principio:

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    FunctionTransformer,
    MinMaxScaler,
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
)

paquetes = pd.DataFrame({
    "peso_kg": [1, 2, 1.5, 4, 3, 2.5, 5, 0.8, 6, 2, 3.5, 4.5],
    "distancia_km": [2, 5, 3, 20, 8, 12, 60, 1, 200, 4, 15, 35],
    "zona": [
        "norte", "sur", "centro", "norte", "sur", "centro",
        "norte", "sur", "centro", "norte", "sur", "centro",
    ],
    "prioridad": [
        "baja", "media", "alta", "media", "baja", "alta",
        "media", "baja", "alta", "media", "baja", "alta",
    ],
    "tiempo_h": [3, 4, 2, 7, 5, 4, 12, 3, 30, 4, 6, 8],
})
```

Cada fila es un paquete. Imaginaremos que quieres predecir `tiempo_h`. Son datos didácticos pequeños, no un conjunto suficiente para evaluar un modelo real.

## 3. Transformar una variable asimétrica

Una cola larga significa que muchos valores se concentran en una zona y algunos se extienden mucho hacia un extremo. No demuestra por sí sola que haya errores.

```python
distancia_log = np.log1p(paquetes["distancia_km"])
print("Asimetría original:", paquetes["distancia_km"].skew())
print("Asimetría transformada:", distancia_log.skew())
```

`np.log1p(x)` calcula `log(1 + x)`. Acepta cero y comprime las diferencias entre valores grandes, manteniendo su orden.

| Valor original | `log1p`, aproximadamente |
|---|---:|
| 0 | 0.00 |
| 1 | 0.69 |
| 10 | 2.40 |
| 100 | 4.62 |

El resultado está en otra escala: no son kilómetros. Para valores reales finitos, el dominio es `x > -1`. No apliques este logaritmo automáticamente a columnas con negativos.

`.skew()` mide asimetría: positivo suele indicar cola derecha y negativo, izquierda. Estar cerca de cero no demuestra normalidad ni simetría perfecta. Un logaritmo puede ayudar, pero no garantiza una distribución normal ni una mejora del modelo.

## 4. Ingeniería de variables

Consiste en crear características útiles a partir de información disponible. Ejemplos: partes de una fecha, razones entre medidas o conteos acumulados hasta el momento de predecir.

Antes de crear una variable, pregunta: **¿tendré esta información cuando llegue un caso nuevo?**

Si quieres predecir `tiempo_h`, no puedes usar como entrada `distancia_km / tiempo_h`: esa razón ya contiene el resultado que quieres adivinar. Sería fuga de información del objetivo.

Tampoco uses información registrada después del evento si la predicción debe hacerse antes.

### Agrupar en tramos

`pd.cut` transforma números en categorías por intervalos. Es útil si el tramo tiene significado, pero pierde detalle: dos valores diferentes pueden quedar en la misma categoría.

No confundas una transformación que conserva el orden de todos los valores, como el logaritmo en su dominio, con una clasificación que reúne valores diferentes en un mismo grupo.

## 5. Categorías nominales, binarias y ordinales

| Tipo | Ejemplo | Tratamiento habitual |
|---|---|---|
| Nominal | Zona norte, sur o centro | One-hot |
| Binaria | Embalaje especial: sí/no | Una columna cero/uno |
| Ordinal | Prioridad baja, media o alta | Códigos con orden explícito |

La mayoría de los modelos que usarás en esta etapa necesita entradas numéricas. Asignar códigos arbitrarios a categorías nominales puede introducir un orden o distancias artificiales en modelos que los interpreten numéricamente.

### One-hot con pandas

```python
print(pd.get_dummies(paquetes["zona"], prefix="zona", dtype=int).head())
```

Se crea una columna por categoría. Cada fila indica con uno su categoría y con cero las demás.

`drop_first=True` elimina una categoría de referencia. Es útil, por ejemplo, para evitar dependencias exactas en regresiones lineales con intercepto y sin regularización. No es una obligación universal para todos los modelos.

### Codificación ordinal

El orden debe tener sentido para el problema. `OrdinalEncoder` con valores de texto suele inferir un orden alfabético, que puede no coincidir con el orden real.

```python
orden_prioridad = {"baja": 0, "media": 1, "alta": 2}
print(paquetes["prioridad"].map(orden_prioridad).head())
```

Incluso cuando el orden es válido, los códigos cero, uno y dos implican separaciones numéricas iguales. Que esa representación sea adecuada depende del modelo y del significado de los niveles.

## 6. Separar entradas, objetivo, entrenamiento y prueba

- `X`: características que tendrás disponibles para predecir.
- `y`: objetivo que quieres predecir.
- `train`: datos para aprender.
- `test`: datos reservados para una evaluación final independiente.

```python
X = paquetes.drop(columns=["tiempo_h"])
y = paquetes["tiempo_h"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42,
)
print(X_train.shape, X_test.shape)
```

La división mantiene alineadas las características y su objetivo. `random_state=42` permite reproducirla.

Este reparto aleatorio es apropiado para el ejemplo. Si hay fechas, personas repetidas o grupos dependientes, puede ser necesario separar por tiempo o por grupo para no mezclar información relacionada.

**Separa antes de aprender medianas, medias, categorías o límites estadísticos.** La limpieza con reglas conocidas de formato no aprende esos parámetros; si utilizas la distribución completa para decidir umbrales o categorías, sí puedes contaminar la evaluación.

En la clase se exploran algunas herramientas con toda la tabla para explicar su funcionamiento. En un flujo predictivo, aplica la regla train/test desde que empieces a aprender parámetros.

## 7. fit, transform y fit_transform

| Método | Qué hace | Dónde se utiliza |
|---|---|---|
| `fit` | Aprende parámetros | Entrenamiento |
| `transform` | Aplica parámetros ya aprendidos | Entrenamiento, test y casos futuros |
| `fit_transform` | Aprende y aplica | Entrenamiento |

```text
Entrenamiento ── fit ──► parámetros aprendidos
Entrenamiento ── transform con esos parámetros ──► entrenamiento preparado
Test ────────── transform con esos parámetros ──► test preparado
```

No hagas `fit` ni `fit_transform` sobre test durante esta evaluación. Ajustar de nuevo sobre test cambia la regla y utiliza información que debía permanecer reservada.

## 8. Escalado: cambiar unidades, no la forma de la distribución

El peso y la distancia tienen escalas diferentes. En métodos basados en distancias, una columna con números grandes puede dominar el cálculo por sus unidades.

El escalado suele ser importante en KNN, SVM, clustering, modelos regularizados y redes neuronales. Los árboles de decisión no suelen necesitarlo. La necesidad exacta depende del modelo y su implementación.

### Estandarización

```text
valor estandarizado = (valor - media de train) / desviación de train
```

```python
escalador = StandardScaler()
peso_train = escalador.fit_transform(X_train[["peso_kg"]])
peso_test = escalador.transform(X_test[["peso_kg"]])

print("Media aprendida:", escalador.mean_)
print("Escala aprendida:", escalador.scale_)
```

En una columna no constante de entrenamiento, la media queda aproximadamente en cero y la desviación poblacional en uno. En test no tienen por qué ser cero y uno; se usa la regla aprendida en train.

Los valores negativos son normales: indican valores por debajo de la media de entrenamiento. No significa que el peso original fuera negativo.

`StandardScaler` usa desviación con `ddof=0`; `Series.std()` de pandas usa `ddof=1` por defecto. Por eso una comprobación manual puede dar pequeñas diferencias. Con una columna constante, el escalador evita dividir entre cero y la deja centrada en cero.

### Min-max

```text
valor escalado = (valor - mínimo de train) / (máximo de train - mínimo de train)
```

```python
minmax = MinMaxScaler()
distancia_train = minmax.fit_transform(X_train[["distancia_km"]])
distancia_test = minmax.transform(X_test[["distancia_km"]])
```

Con el rango predeterminado, los valores de entrenamiento quedan entre cero y uno. **Un valor nuevo fuera de los extremos de entrenamiento puede quedar fuera de ese rango.** No lo interpretes automáticamente como un fallo.

Min-max es sensible a extremos y StandardScaler también utiliza estadísticas sensibles a ellos. Ninguno elimina valores atípicos.

**Escalar no convierte una cola larga en una distribución simétrica.** El logaritmo cambia la forma; un escalado afín mueve y estira la escala. Son operaciones distintas que pueden combinarse.

## 9. Codificadores que aprenden con train

```python
codificador = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
zona_train = codificador.fit_transform(X_train[["zona"]])
zona_test = codificador.transform(X_test[["zona"]])
print(codificador.categories_)
```

`fit` aprende las categorías y `transform` conserva las mismas columnas. Con `handle_unknown="ignore"`, una categoría nueva produce ceros en las columnas de esa variable. El modelo no ha aprendido un efecto específico para ella.

Si calculas `get_dummies` por separado en train y test, podrían salir columnas distintas. El codificador ajustado evita esa inconsistencia.

Para categorías ordinales, indica el orden explícitamente:

```python
ordinal = OrdinalEncoder(categories=[["baja", "media", "alta"]])
prioridad_train = ordinal.fit_transform(X_train[["prioridad"]])
prioridad_test = ordinal.transform(X_test[["prioridad"]])
```

Ese codificador no acepta categorías nuevas por defecto. Cuando puedan aparecer, define una política explícita; por ejemplo, una codificación de desconocidos compatible con tu modelo.

Los dobles corchetes mantienen una tabla de dos dimensiones: scikit-learn espera normalmente `(n_filas, n_columnas)`, aunque selecciones una sola columna.

## 10. Pipeline: pasos sucesivos sobre los mismos datos

```python
pipeline_distancia = Pipeline([
    ("imputar", SimpleImputer(strategy="median")),
    ("log", FunctionTransformer(np.log1p, feature_names_out="one-to-one")),
    ("escalar", StandardScaler()),
])
```

Se ejecuta de arriba abajo:

1. Aprende con train cómo rellenar posibles faltantes y los rellena.
2. Aplica el logaritmo.
3. Aprende la media y escala de los datos ya transformados, y estandariza.

`FunctionTransformer` permite integrar una función, como `log1p`, en la secuencia. Esa función fija no aprende una media, pero sigue necesitando datos dentro de su dominio.

El orden importa: estandarizar primero podría crear valores negativos incompatibles con `log1p`.

## 11. ColumnTransformer: un tratamiento por grupo de columnas

Un Pipeline encadena pasos. Un ColumnTransformer reparte columnas entre tratamientos y reúne sus salidas.

```python
pipeline_peso = Pipeline([
    ("imputar", SimpleImputer(strategy="median")),
    ("escalar", StandardScaler()),
])

preprocesador = ColumnTransformer([
    ("peso", pipeline_peso, ["peso_kg"]),
    ("distancia", pipeline_distancia, ["distancia_km"]),
    ("zona", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["zona"]),
    ("prioridad", OrdinalEncoder(categories=[["baja", "media", "alta"]]), ["prioridad"]),
])
preprocesador.set_output(transform="pandas")

X_train_preparado = preprocesador.fit_transform(X_train)
X_test_preparado = preprocesador.transform(X_test)
print(X_train_preparado.head())
```

Cada tupla contiene nombre, transformador y lista de columnas. El objetivo no se incluye. Por defecto, las columnas no seleccionadas se descartan.

`set_output(transform="pandas")` conserva una salida con nombres. El notebook también muestra una configuración global de scikit-learn para ese propósito. `sparse_output=False` hace que el one-hot produzca una salida densa compatible con este ejemplo.

Los nombres resultantes incluyen prefijos como `peso__` o `zona__`, que indican de qué rama proceden. Train y test deben tener las mismas columnas de salida y no contener nulos en este ejemplo.

Este preprocesador prepara entradas; todavía no entrena un predictor del tiempo. El ejemplo no imputa las categorías: si faltaran, tendrías que definir también su tratamiento.

## 12. Preparar un caso nuevo

```python
nuevo_paquete = pd.DataFrame({
    "peso_kg": [2.2],
    "distancia_km": [18],
    "zona": ["este"],
    "prioridad": ["media"],
})

nuevo_preparado = preprocesador.transform(nuevo_paquete)
print(nuevo_preparado)
```

El caso nuevo tiene las características originales, no el objetivo. Se aplica `transform` con el objeto ya ajustado. No calcules nuevas medias ni vuelvas a ajustar el codificador.

La zona desconocida se trata con la regla configurada. La prioridad sí pertenece al orden definido.

## 13. Comprobaciones y errores comunes

Antes de entrenar, revisa:

- ¿Las características estarán disponibles al predecir?
- ¿Separaste train y test antes de aprender estadísticas?
- ¿Usaste `fit_transform` solo en train y `transform` en test?
- ¿Las entradas preparadas son numéricas y tienen columnas consistentes?
- ¿Quedan nulos o valores fuera del dominio del logaritmo?
- ¿El orden ordinal es explícito y tiene sentido?
- ¿Definiste qué hacer con categorías desconocidas?

Errores frecuentes: incluir el objetivo entre las entradas, aprender un escalador diferente para test, esperar que test tenga media cero o pensar que one-hot y escalado hacen la misma operación.

## 14. Practicar sin resolver la actividad

1. Explica qué parámetros aprende un imputador y cuáles aprende un escalador.
2. Comprueba que la cantidad de filas se conserva después del preprocesamiento.
3. Explica por qué puede aumentar la cantidad de columnas.
4. Compara las medias de una columna escalada en train y test sin volver a ajustar.
5. Describe qué ocurre con la zona `"este"` y qué ocurriría con una prioridad no definida.
6. Dibuja en papel las ramas del ColumnTransformer y el orden de los pasos de distancia.

La idea que conecta toda la clase es conservar una única regla aprendida con entrenamiento y aplicarla de forma consistente a los demás datos.

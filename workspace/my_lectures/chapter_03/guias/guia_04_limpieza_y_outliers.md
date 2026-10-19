# Guía de estudio: limpieza de datos y valores atípicos

Basada en [04_limpieza_y_outliers.ipynb](../../../../notebooks/lectures/chapter_03/04_limpieza_y_outliers.ipynb).
Continúa la [guía de pandas](guia_02_pandas.md) y se conecta con la [guía de transformación y escalado](guia_05_transformacion_y_escalado.md).

Los ejemplos son distintos de las actividades del curso. La finalidad es que puedas decidir qué hacer y explicar por qué, sin copiar una solución.

## 1. Qué cambia respecto a pandas

Ya sabes seleccionar, filtrar y resumir tablas. Ahora usarás esas herramientas para diagnosticar problemas y decidir cómo tratarlos.

| Problema | Ejemplo | Qué debes investigar |
|---|---|---|
| Duplicados | El mismo registro aparece dos veces | ¿Es una repetición accidental o un evento real? |
| Texto inconsistente | `"Norte"`, `"NORTE"`, `" norte "` | ¿Representan la misma categoría? |
| Tipo incorrecto | Una temperatura aparece como `"18.0 °C"` | ¿Cómo separar el número de su formato? |
| Faltantes | No se registraron horas de uso | ¿Por qué faltan y qué estrategia conviene? |
| Valores atípicos | Una medición está muy lejos del resto | ¿Es un error o una observación válida? |

**Limpiar no significa borrar todo lo raro ni dejar todos los valores parecidos.** Significa corregir problemas y conservar información útil.

## 2. Datos para practicar

Ejecuta los bloques en orden en un notebook de trabajo. Los imports van al principio:

```python
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

registros = pd.DataFrame({
    "id": [1, 2, 2, 3, 4, 5, 6, 7],
    "sede": [" norte ", "SUR", "SUR", "Norte", np.nan, "sur", "norte", "sur"],
    "temperatura_texto": [
        "18.0 °C", "21.0 °C", "21.0 °C", "error",
        "19.5 °C", "20.0 °C", "210.0 °C", "22.0 °C",
    ],
    "horas_uso": [12, np.nan, np.nan, 36, 24, 18, 30, 48],
})
```

Son registros pequeños de sensores. Los ejemplos de imputación muestran alternativas; no necesitas aplicar todas sobre una misma columna.

## 3. Diagnosticar antes de modificar

```python
print(registros.shape)
registros.info()
print(registros.describe())
print(registros["sede"].value_counts(dropna=False))
print("Duplicados:", registros.duplicated().sum())

diagnostico = pd.DataFrame({
    "nulos": registros.isna().sum(),
    "porcentaje_nulos": registros.isna().mean() * 100,
})
print(diagnostico)
```

`isna()` produce booleanos. Sumarlos cuenta faltantes; calcular su media da la proporción de faltantes. Multiplicar por cien la convierte en porcentaje.

Para ver las filas que tienen al menos un faltante:

```python
print(registros.loc[registros.isna().any(axis=1)])
```

`any(axis=1)` reúne las columnas de cada fila y pregunta si **alguna** contiene un faltante. No cuenta cuántos: devuelve una decisión por fila.

El valor `"error"` no es automáticamente un nulo. Tampoco un número incorrecto deja de ser incorrecto por estar presente.

## 4. Duplicados

```python
registros = registros.drop_duplicates().copy()
print(registros.duplicated(subset=["id"]).sum())
```

Sin `subset`, se comparan todas las columnas. Por defecto se conserva la primera aparición y se eliminan las repeticiones posteriores.

Con `subset=["id"]`, buscas identificadores repetidos aunque otros campos difieran. Detectarlos no decide cuál es correcto: puede haber versiones, actualizaciones o errores que requieren revisión.

Dos mediciones iguales no necesariamente son duplicados: podrían haberse realizado en instantes diferentes. La definición depende de qué representa cada fila.

## 5. Homogeneizar texto y corregir tipos

```python
registros["sede"] = registros["sede"].str.strip().str.lower()

texto_numerico = registros["temperatura_texto"].str.replace(
    " °C", "", regex=False,
)
registros["temperatura"] = pd.to_numeric(texto_numerico, errors="coerce")

fallos_conversion = registros["temperatura_texto"].notna() & registros["temperatura"].isna()
print(registros.loc[fallos_conversion, ["id", "temperatura_texto"]])
```

- `.str.strip()` elimina espacios al principio y al final, no todos los espacios interiores.
- `.str.lower()` convierte a minúsculas.
- `.str.capitalize()` pone en mayúscula la primera letra y en minúscula las demás; no siempre es apropiado para siglas o nombres propios.
- `.str.replace(..., regex=False)` sustituye texto literal.
- `pd.to_numeric` convierte a número.

`errors="coerce"` convierte entradas no interpretables en faltantes. **Comprueba cuáles fueron**: no es una reparación del dato original.

Antes de quitar comas o puntos, comprueba si representan separadores de miles o decimales. El mismo símbolo puede tener significados distintos según el archivo.

Para fechas se usa `pd.to_datetime(...)`; después puedes usar `.dt.year`, `.dt.month` y otros componentes.

## 6. Faltantes: la decisión empieza por su causa

| Posible causa | Ejemplo | Por qué importa |
|---|---|---|
| Ausencia aproximadamente al azar | Se perdió un registro por un fallo ocasional | Puede ser razonable imputar, según el contexto |
| Depende de otra variable observada | Fallan más los sensores antiguos | Un resumen por grupo podría ser más adecuado |
| Depende del propio valor faltante | Un dispositivo deja de registrar al superar un límite | Sustituir por la media podría ocultar el problema |

No puedes demostrar la causa solo porque una columna tenga cierto porcentaje de nulos. Investiga cómo se recogieron los datos.

### Eliminar filas o columnas

`dropna(subset=["columna"])` elimina filas que no tienen esa información. `drop(columns=["columna"])` elimina una columna completa.

Eliminar puede ser razonable si la información es imprescindible o casi no existe. Sin embargo, incluso pocos nulos pueden introducir sesgo si se concentran en un grupo concreto.

### Imputar: rellenar con una estimación

| Estrategia | Para qué puede servir | Límite importante |
|---|---|---|
| Media | Datos numéricos sin extremos fuertes | Los extremos desplazan la media |
| Mediana | Datos numéricos asimétricos o con extremos | No recupera el dato real |
| Moda | Categorías | Puede reforzar demasiado la categoría dominante |
| Categoría `"desconocido"` | Conservar explícitamente la ausencia | Es una categoría nueva, no una observación recuperada |
| Resumen por grupo | Datos que varían entre grupos | Un grupo puede no tener datos suficientes |

```python
mediana_horas = registros["horas_uso"].median()
propuesta_mediana = registros["horas_uso"].fillna(mediana_horas)

modas_sede = registros["sede"].mode()
propuesta_moda = registros["sede"].fillna(modas_sede.iloc[0])
```

`mode()` devuelve una Series porque puede haber varias modas. Si no hay valores observados, no habrá una primera moda que seleccionar.

Imputar con un único valor tiende a reducir la variabilidad y aumentar su frecuencia. No hace que los datos queden completos en el sentido de conocer su valor verdadero.

### Indicador de ausencia

Créalo **antes** de rellenar:

```python
registros["horas_faltantes"] = registros["horas_uso"].isna().astype(int)
```

Uno significa que faltaba el dato y cero, que estaba presente. Después de imputar ya no podrías recuperar esa distinción usando solo la columna rellenada.

### Imputación por grupo

```python
medianas_por_fila = registros.groupby("sede")["horas_uso"].transform("median")
propuesta_grupo = registros["horas_uso"].fillna(medianas_por_fila)
print(propuesta_grupo.isna().sum())
```

`groupby(...).median()` devuelve un valor por grupo. `transform("median")` devuelve un valor por fila, alineado con la tabla original, para facilitar el relleno.

Si falta la sede o un grupo no tiene horas observadas, puede seguir habiendo nulos. Define una alternativa cuando corresponda, como una mediana global aprendida con entrenamiento.

## 7. fit y transform: aprender frente a aplicar

`SimpleImputer` organiza la imputación en dos pasos:

- `fit`: aprende, por ejemplo, la mediana de cada columna.
- `transform`: aplica los valores aprendidos y rellena faltantes.
- `fit_transform`: aprende y aplica sobre el mismo conjunto.

```python
X_train, X_test = train_test_split(
    registros[["horas_uso", "temperatura"]],
    test_size=0.3,
    random_state=42,
)

imputador = SimpleImputer(strategy="median")
X_train_imputado = imputador.fit_transform(X_train)
X_test_imputado = imputador.transform(X_test)
print("Valores aprendidos:", imputador.statistics_)
```

Por defecto, este transformador devuelve arrays. `strategy` también admite `"mean"`, `"most_frequent"` y `"constant"`.

**En una evaluación predictiva, aprende las estadísticas solo con entrenamiento.** Los ejemplos anteriores muestran las técnicas descriptivamente; calcular una mediana con toda la tabla antes de reservar test dejaría entrar información del test.

## 8. Un valor atípico es un candidato a revisión

Un dato alejado puede ser un error o un valor real. Usa histogramas y boxplots para observar la distribución, y revisa las filas completas para entender los candidatos.

### Z-score

```python
serie = pd.Series([18, 19, 20, 21, 22, 23, 210], dtype=float)
z = (serie - serie.mean()) / serie.std()
candidatos_z = z.abs() > 3
print(serie[candidatos_z])
```

La fórmula indica cuántas desviaciones estándar separan un valor de la media. `abs(z) > 3` es una regla habitual, no una prueba universal de error.

**Los extremos también afectan a la media y la desviación.** Un extremo enorme puede inflar la desviación y dejar de parecer tan alejado bajo esta regla; puede ocurrir especialmente en muestras pequeñas. Eso se relaciona con el enmascaramiento.

Si todos los valores son iguales, la desviación es cero y no debes interpretar la división como un z-score válido.

### Rango intercuartílico: IQR

```python
q1, q3 = serie.quantile([0.25, 0.75])
iqr = q3 - q1
limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

candidatos_iqr = (serie < limite_inferior) | (serie > limite_superior)
print(serie[candidatos_iqr])
```

El IQR mide la amplitud del 50 % central. Los cuartiles son más resistentes a extremos que la media y la desviación, pero no son inmunes a cualquier cambio de datos.

Esta es la regla habitual que produce los puntos separados del boxplot. Fuera de los límites significa candidato estadístico, no error confirmado.

### Criterio del problema

Investiga unidades, límites del instrumento, condiciones de medición y registros originales. Una temperatura alta puede ser imposible para una oficina ocupada y perfectamente válida en un horno.

No copies un umbral de otro problema sin justificarlo.

## 9. Tratar valores atípicos

| Situación | Acción posible |
|---|---|
| Error confirmado con valor correcto conocido | Corregir y documentar |
| Error confirmado sin valor recuperable | Marcar como faltante o eliminar según el caso |
| Extremo real que aporta información | Conservar |
| Extremo real que domina una medida | Evaluar recorte o un método más robusto |
| Cola larga propia de la variable | Evaluar una transformación, como un logaritmo |

### Winsorización o recorte

```python
p01, p99 = serie.quantile([0.01, 0.99])
serie_recortada = serie.clip(lower=p01, upper=p99)
```

Los valores bajo el límite inferior se sustituyen por ese límite; los que superan el superior, por el superior. Los demás se conservan. No elimina filas, pero **sí cambia observaciones**.

El recorte por percentiles es una opción, no una regla que deba aplicarse a todas las columnas. Para datos predictivos, los límites estimados se aprenden solo con entrenamiento.

Una distribución con cola larga puede producir muchos candidatos IQR sin contener errores. Eliminarla o recortarla automáticamente puede borrar precisamente los casos que quieres aprender a predecir.

## 10. Cómo comprobar tu trabajo

Compara antes y después: cantidad de filas, duplicados, nulos, categorías, tipos y distribuciones. Anota qué cambió y por qué.

No basta con obtener cero nulos: podrías haber eliminado muchas observaciones o introducido un relleno poco razonable.

Practica con los sensores:

1. Explica qué diferencia hay entre un faltante original y uno producido al convertir texto.
2. Comprueba por qué `transform("median")` conserva una salida por fila.
3. Compara los candidatos de z-score e IQR sin asumir que deben coincidir.
4. Explica qué información se pierde al imputar o recortar.
5. Describe cómo cambiaría el tratamiento si los sensores midieran un horno en lugar de una oficina.

## 11. Errores que conviene evitar

- Borrar toda fila rara sin investigar su significado.
- Rellenar texto o identificadores con medias numéricas.
- Crear el indicador de ausencia después de rellenar.
- Usar `errors="coerce"` sin revisar los nuevos faltantes.
- Calcular medianas o percentiles con train y test juntos.
- Pensar que limpiar significa conservar siempre todas las filas o eliminarlas siempre.

La técnica señala opciones; la decisión debe apoyarse en cómo se obtuvieron los datos y para qué se utilizarán.

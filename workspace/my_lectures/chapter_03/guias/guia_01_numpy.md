# Guía de estudio: NumPy

Basada en `my_01_numpy.ipynb` y en las dudas que trabajamos durante la actividad.
Los ejemplos usan otros datos: esta guía no contiene las soluciones de la actividad.

## 1. Para qué sirve NumPy

NumPy permite trabajar con números organizados en **arrays**. En una tabla numérica, normalmente cada fila representa una observación y cada columna, una característica.

Su ventaja principal es que puedes expresar operaciones sobre muchos elementos sin escribir un bucle de Python. Eso se llama **vectorizar**.

Para practicar, ejecuta los bloques de esta guía en orden en un notebook de trabajo. Los imports van al principio:

```python
import numpy as np
```

## 2. Una lista y un array no se comportan igual

```python
lista = [2, 4, 6]
array = np.array([2, 4, 6])

print(lista * 2)  # Repite la lista.
print(array * 2)  # Multiplica cada número por dos.
```

Con arrays, `+`, `-`, `*`, `/` y `**` actúan elemento a elemento, cuando las formas son compatibles. `A * B` no es multiplicación matricial; para eso se usa `A @ B`.

## 3. Crear arrays

| Herramienta | Qué crea |
|---|---|
| `np.array([2, 4, 6])` | Un vector a partir de una lista |
| `np.array([[1, 2], [3, 4]])` | Una matriz a partir de listas anidadas |
| `np.zeros((3, 2))` | Tres filas y dos columnas de ceros |
| `np.ones((3, 2))` | Tres filas y dos columnas de unos |
| `np.full((3, 2), 8)` | Tres filas y dos columnas llenas de ochos |
| `np.eye(3)` | Una matriz identidad: unos en la diagonal y ceros fuera |
| `np.arange(0, 10, 2)` | Una secuencia con paso dos; excluye diez |
| `np.linspace(0, 1, 5)` | Cinco puntos igualmente separados; incluye los extremos |
| `np.zeros_like(A)` | Ceros con la forma y, por defecto, el tipo de `A` |

**Error común:** `np.full(28, 5)` crea 28 elementos cuyo valor es cinco. El segundo argumento no indica el número de columnas. Una forma de dos dimensiones se expresa con una tupla: `(filas, columnas)`.

`arange` es útil cuando conoces el paso; `linspace`, cuando conoces la cantidad de puntos.

## 4. Leer la forma y el tipo

Usaremos tres días de mediciones en dos sensores:

```python
mediciones = np.array([
    [18, 22],
    [20, 24],
    [16, 26],
])

print(mediciones.shape)
print(mediciones.ndim)
print(mediciones.size)
print(mediciones.dtype)
```

| Atributo | Significado | En el ejemplo |
|---|---|---|
| `.shape` | Tamaño de cada dimensión | `(3, 2)` |
| `.ndim` | Número de dimensiones | `2` |
| `.size` | Número total de elementos | `6` |
| `.dtype` | Tipo de los elementos | Un tipo entero |

Estos son **atributos** y se consultan sin paréntesis. En cambio, `.sum()` o `.mean()` son métodos que ejecutan una operación.

No confundas estas formas:

- `(6,)`: un vector de seis elementos.
- `(6, 1)`: una matriz de seis filas y una columna.
- `(1, 6)`: una matriz de una fila y seis columnas.

La coma en `(6,)` indica una tupla de una sola entrada: no falta una segunda dimensión.

Un array tiene un único `dtype`. Mezclar enteros y decimales normalmente hace que los enteros se conviertan a decimales.

```python
decimales = np.array([1.7, 2.2, 3.9])
print(decimales.astype(int))  # Elimina la parte decimal; no redondea.
```

`float32` ocupa cuatro bytes por elemento y `float64`, ocho. `.nbytes` indica cuántos bytes ocupan los elementos del array.

## 5. Índices y slicing

Los índices empiezan en cero. Los negativos cuentan desde el final.

```python
a = np.array([8, 12, 16, 20, 24])

print(a[0])
print(a[-1])
print(a[1:4])
print(a[::2])
print(a[::-1])
```

La estructura de un intervalo es `inicio:fin:paso`. **Incluye el inicio y excluye el final.** Si omites un límite, se usa el extremo correspondiente.

En una matriz, escribe `matriz[filas, columnas]`:

```python
print(mediciones[1, 0])   # Segundo día, primer sensor.
print(mediciones[0, :])   # Primera fila completa.
print(mediciones[:, 1])  # Segunda columna completa.
print(mediciones[:2, :]) # Primeros dos días, ambos sensores.
```

| Selección | Significado |
|---|---|
| `M[:2]` | Primeras dos filas |
| `M[:, :2]` | Todas las filas, primeras dos columnas |
| `M[-2:, :]` | Últimas dos filas |
| `M[:, 1:]` | Desde la segunda columna hasta el final |

**La coma separa filas de columnas.** `M[0:2]` selecciona filas; no columnas.

Un índice entero puede eliminar una dimensión: `M[:, 1]` es un vector. Un intervalo conserva esa dimensión: `M[:, 1:2]` es una matriz de una columna.

## 6. Cambiar la forma

`reshape` reorganiza los elementos y conserva su orden de recorrido habitual. El número de posiciones debe coincidir:

```python
datos = np.arange(6)
print(datos.reshape(2, 3))
print(datos.reshape(3, 2))
print(datos.reshape(2, -1))
```

`-1` permite calcular una dimensión automáticamente. Solo puede haber una dimensión desconocida.

Otras operaciones:

- `M.T`: intercambia filas y columnas en una matriz.
- `M.ravel()`: aplana los elementos en un vector.
- `np.concatenate([A, B], axis=0)`: une arrays a lo largo de una dimensión existente; aquí añade filas de matrices compatibles.
- `np.vstack([A, B])`: apila matrices verticalmente.
- `np.hstack([A, B])`: une matrices horizontalmente.
- `np.stack([A, B])`: crea una dimensión nueva para reunir arrays de la misma forma.

Cambiar la forma y transponer no son operaciones equivalentes.

## 7. Broadcasting

Permite operar con formas distintas, pero compatibles:

```python
ajustes = np.array([1, -2])
corregidas = mediciones + ajustes
print(corregidas)
```

La matriz tiene forma `(3, 2)` y el vector `(2,)`. NumPy aplica un ajuste por columna a todas las filas.

La regla general compara las dimensiones desde la derecha: deben ser iguales o una de ellas debe valer uno. No cualquier par de formas es compatible.

## 8. Agregaciones y axis

Una agregación resume varios datos: suma, media, mínimo o máximo.

```python
print(mediciones.mean())        # Una media global.
print(mediciones.mean(axis=0))  # Una media por sensor.
print(mediciones.mean(axis=1))  # Una media por día.
```

| En una matriz | Qué se reduce | Resultado |
|---|---|---|
| Sin `axis` | Todos los elementos | Un número |
| `axis=0` | Las filas entre sí | Un resultado por columna |
| `axis=1` | Las columnas entre sí | Un resultado por fila |

Piensa primero en **qué quieres conservar**. Para un resultado por fila, reduces las columnas. Para un resultado por columna, reduces las filas.

La misma idea se aplica a `.sum()`, `.min()` y `.max()`.

### Seleccionar antes de resumir

```python
bloque = mediciones[:, :1]
promedio_bloque = bloque.mean()
print(promedio_bloque)
```

Primero eliges el bloque y después calculas la media. `M.mean()[0:2]` falla porque la media global ya es un número y no puedes hacer slicing sobre él.

### Valor máximo frente a posición máxima

- `.max()` devuelve el valor máximo.
- `.argmax()` devuelve su posición; en un vector, puedes usarla para buscar una etiqueta correspondiente.
- `.min()` y `.argmin()` funcionan de forma equivalente para el mínimo.

Si hay empate, `argmax()` devuelve la primera posición máxima. Sin `axis`, en una matriz devuelve una posición en el recorrido aplanado.

## 9. Máscaras y etiquetas

```python
alturas = np.array([12, 19, 15, 23])
mascara = alturas > alturas.mean()

print(mascara)
print(alturas[mascara])
print(mascara.sum())
```

La comparación produce booleanos. La selección conserva los valores donde hay `True`. La suma de la máscara cuenta cuántos cumplen, porque `True` actúa como uno y `False`, como cero.

Para combinar condiciones, usa `&` (y), `|` (o) y `~` (negación). Pon las comparaciones entre paréntesis:

```python
en_intervalo = (alturas > 10) & (alturas < 20)
print(alturas[en_intervalo])
```

`np.where` asigna una salida a cada posición:

```python
etiquetas = np.where(mascara, "alta", "baja")
print(etiquetas)
```

Filtrar conserva solo ciertos elementos. Clasificar con `where` produce una etiqueta para cada elemento original.

## 10. Otras operaciones útiles

- `%`: resto de una división; sirve para identificar ciclos.
- `np.round(valores, 1)`: redondea a un decimal.
- `np.sqrt`, `np.exp`, `np.sin`, `np.abs`: funciones matemáticas elemento a elemento.
- `np.log1p(x)`: calcula `log(1 + x)`; no admite cualquier valor negativo.
- `np.clip(x, minimo, maximo)`: limita los valores al intervalo indicado.

Un porcentaje se calcula como `parte / total * 100`. Identifica siempre el total de referencia. Los porcentajes redondeados pueden no sumar exactamente cien.

Para generar datos aleatorios reproducibles:

```python
rng = np.random.default_rng(42)
ejemplo_aleatorio = rng.normal(size=(3, 2))
```

## 11. Comprobaciones para trabajar por tu cuenta

Antes de escribir una operación, identifica qué representan las filas y columnas. Después anticipa la forma del resultado y compruébala con `.shape`.

Practica con `mediciones`, sin usar los datos de la actividad:

1. Selecciona los últimos dos días.
2. Obtén un máximo por sensor y explica qué `axis` elegiste.
3. Obtén un total por día y anticipa cuántos valores saldrán.
4. Cuenta las mediciones del primer sensor que superan un límite elegido por ti.
5. Explica la diferencia entre el número de elementos y la suma de sus valores.

La cantidad de registros y la cantidad medida no son lo mismo: seis registros de temperatura no significan seis grados.

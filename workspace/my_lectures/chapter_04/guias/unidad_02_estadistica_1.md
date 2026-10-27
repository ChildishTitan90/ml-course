# Unidad 2: Comprensión de la estadística I

## Objetivo y conexión

Distinguirás densidad de probabilidad, interpretarás la normal y la t de Student y estudiarás relaciones entre variables. Los apartados siguen 2.1–2.2. En 2.2 las diapositivas ponen especial énfasis en correlación; aquí la conectamos con probabilidad conjunta.

## 2.1. Densidad de probabilidad continua

Una variable continua se describe mediante una **densidad f(x)**. Las probabilidades corresponden a áreas:

$$
P(a\le X\le b)=\int_a^b f(x)\,dx
$$

f(x) debe ser no negativa y el área total debe ser 1. La integral acumula área sobre un intervalo.

Para una variable con densidad, P(X = x) = 0 en un punto exacto, aunque valores de un intervalo cercano puedan tener probabilidad positiva. La altura f(x) puede superar 1: lo que debe estar entre 0 y 1 es la probabilidad, obtenida por área.

**Ejemplo:** si el tiempo se distribuye uniformemente entre 0 y 0.5 segundos, su densidad es 2 por segundo en ese intervalo. La probabilidad de caer entre 0.1 y 0.2 es 2×0.1 = 0.2.

La **acumulada** F(t) = P(X ≤ t) da el área hasta t. Es distinta de la densidad.

```text
densidad = altura de la curva
probabilidad en un intervalo = área bajo la curva

a |======= área del intervalo =======| b
```

### Distribución normal

Es una familia de curvas simétricas en forma de campana:

$$
X\sim\mathcal N(\mu,\sigma^2),\qquad \sigma>0
$$

μ fija el centro y σ determina la escala o dispersión. La segunda cantidad en esta notación es la **varianza**, no la desviación estándar.

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}
\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

La diferencia x − μ mide cuánto nos alejamos del centro; dividir por σ expresa ese alejamiento en unidades de desviación estándar. El exponente reduce la altura conforme nos alejamos.

Para una normal, aproximadamente 68 % del área está dentro de una desviación del centro, 95 % dentro de dos y 99.7 % dentro de tres. Son propiedades de esta familia, no de toda distribución.

### Estandarización y combinaciones

$$
Z=\frac{X-\mu}{\sigma}
$$

Si X es normal, Z es normal estándar N(0, 1). Si μ = 10, σ = 2 y x = 14, su puntuación z es 2: está dos desviaciones por encima de la media.

Estandarizar una variable que no es normal cambia centro y escala; no la convierte automáticamente en normal.

Si X e Y son normales independientes, sus sumas y diferencias son normales:

$$
E[X\pm Y]=\mu_X\pm\mu_Y,\qquad
\operatorname{Var}(X\pm Y)=\sigma_X^2+\sigma_Y^2
$$

Las varianzas se suman también al restar las variables independientes. Sin independencia hay que considerar la covarianza: aparece un término adicional con su signo correspondiente.

### Distribución t de Student

La t es simétrica alrededor de cero y tiene colas más pesadas que la normal estándar para grados de libertad finitos. Los **grados de libertad ν** controlan su forma. Al aumentar ν se aproxima a la normal estándar.

Aparece al estudiar una media normal cuando sustituimos σ desconocida por una desviación estimada s:

$$
T=\frac{\bar X-\mu}{S/\sqrt n}
\sim t_{n-1}
$$

Esta distribución exacta requiere observaciones independientes de una población normal. Con otros datos puede funcionar como aproximación bajo condiciones adecuadas.

La media de la t es 0 cuando ν > 1; su varianza es ν/(ν − 2) cuando ν > 2. Para grados menores esos momentos no son finitos en el sentido usual. Esto explica por qué las colas importan al hablar de promedios y dispersión.

## 2.2. Probabilidad conjunta

Una distribución conjunta describe lo que ocurre **simultáneamente** con X e Y. Una marginal describe una variable sin condicionar por la otra.

Ejemplo hipotético de dos indicadores binarios:

<table header-row="true">
<tr><td></td><td>Y = 0</td><td>Y = 1</td><td>Total</td></tr>
<tr><td>X = 0</td><td>0.30</td><td>0.20</td><td>0.50</td></tr>
<tr><td>X = 1</td><td>0.10</td><td>0.40</td><td>0.50</td></tr>
<tr><td>Total</td><td>0.40</td><td>0.60</td><td>1.00</td></tr>
</table>

Cada celda interior es una probabilidad conjunta. Los totales de filas y columnas son marginales. P(X = 1, Y = 1) = 0.40; P(X = 1) = 0.50.

Si fueran independientes, esa celda tendría que valer 0.50×0.60 = 0.30. En este ejemplo no coincide. Una condicional se obtiene dividiendo la conjunta por la marginal apropiada.

En variables continuas, una densidad conjunta asigna probabilidades mediante áreas bidimensionales; integrar respecto a una variable produce la marginal de la otra.

### Covarianza y correlación

La **covarianza** mide cómo varían conjuntamente las desviaciones respecto a las medias:

$$
\operatorname{Cov}(X,Y)=E[(X-\mu_X)(Y-\mu_Y)]
$$

Su magnitud depende de las unidades. La **correlación de Pearson** normaliza:

$$
\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y}
$$

Si ambas desviaciones son positivas y finitas, está entre −1 y 1. Valores positivos señalan asociación lineal creciente y negativos decreciente. Si una variable es constante, esta correlación no está definida.

**Cero correlación lineal no permite concluir que no hay relación ni que la relación tiene que ser no lineal.** Podría no haber relación, o existir una estructura que esa medida no capta. Un patrón como Y = X² con X distribuida simétricamente puede tener correlación cero y dependencia clara.

Independencia implica covarianza cero cuando existen los momentos necesarios; la afirmación inversa no vale en general. Correlación tampoco demuestra causalidad: pueden existir variables de confusión u otros mecanismos.

```mermaid
flowchart LR
    A["Datos de dos variables"] --> B["Gráfico y contexto"]
    B --> C["Medida de asociación"]
    C --> D["Examinar límites, grupos y posibles explicaciones"]
```

## Práctica sin resolver

1. ¿Por qué una densidad de altura 2 puede ser válida?
2. Explica la diferencia entre f(x), F(x) y P(a ≤ X ≤ b).
3. Si μ = 20 y σ = 4, interpreta el z de x = 12.
4. ¿Estandarizar una variable garantiza una campana normal?
5. ¿Por qué al restar normales independientes no se restan las varianzas?
6. Diferencia una probabilidad conjunta, marginal y condicional.
7. ¿Qué puedes concluir, y qué no, de una correlación cero?
8. ¿Por qué la t de Student depende de grados de libertad?

**Estado:** guía lista; evaluación pendiente en el chat.

## Fuente

[Capítulo 4 en Canvas](https://udem.instructure.com/courses/36648/pages/recursos-didacticos-del-capitulo-4-2?module_item_id=5019826), unidad 2, diapositivas 33–53. Los ejemplos y las conexiones entre conjunta, marginal, densidad y correlación son elaboración de tutoría.


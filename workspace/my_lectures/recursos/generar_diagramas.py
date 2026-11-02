"""Genera los diagramas originales de las guías. Ejecutar desde la raíz del repo.

Uso: uv run python workspace/my_lectures/recursos/generar_diagramas.py
Los ejemplos son didácticos y usan datos construidos o simulados con semilla 42.
"""

from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np
from scipy.stats import norm, t

OUT = Path("workspace/my_lectures/imagenes")
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                     "svg.fonttype": "none", "axes.spines.top": False,
                     "axes.spines.right": False, "figure.facecolor": "#f5f8fc",
                     "axes.facecolor": "#f5f8fc", "text.color": "#17334e",
                     "axes.labelcolor": "#17334e", "axes.titlesize": 15})
BLUE, TEAL, ORANGE, RED = "#2878bd", "#168578", "#d58225", "#be4555"
PALE = ["#deedfc", "#d9f1e9", "#fff0d5", "#f8dfe5"]
rng = np.random.default_rng(42)


def canvas(title, subtitle="", panels=1, height=6):
    fig, axes = plt.subplots(1, panels, figsize=(13.5, height), squeeze=False)
    fig.suptitle(title, fontsize=22, fontweight="bold", x=.06, ha="left", y=.98)
    if subtitle:
        fig.text(.06, .895, subtitle, fontsize=12)
    fig.subplots_adjust(left=.075, right=.96, top=.80, bottom=.14, wspace=.30)
    return fig, list(axes[0])


def save(fig, name):
    fig.text(.06, .035, "ML · Guías visuales | Ejemplo didáctico original", fontsize=10, color="#587086")
    fig.savefig(OUT / f"{name}.svg")
    fig.savefig(OUT / f"{name}.png", dpi=115)
    plt.close(fig)


def blank(ax):
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")


def box(ax, x, y, w, h, title, body="", color=0):
    ax.add_patch(FancyBboxPatch((x,y), w,h, boxstyle="round,pad=0.012,rounding_size=.02",
                              facecolor=PALE[color], edgecolor="#b8cadb", linewidth=1.2))
    ax.text(x+w/2, y+h*.72 if body else y+h/2, title, ha="center", va="center", fontsize=14, weight="bold")
    if body:
        ax.text(x+w/2, y+h*.32, body, ha="center", va="center", fontsize=12)


def arrow(ax, start, end, text=""):
    ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle":"->", "color":"#587086", "lw":2})
    if text:
        ax.text((start[0]+end[0])/2, (start[1]+end[1])/2+.045, text, fontsize=11, ha="center")


def flow(name, title, steps, subtitle=""):
    fig, (ax,) = canvas(title, subtitle)
    blank(ax)
    n = len(steps)
    width = .88/n
    for i, (head, body) in enumerate(steps):
        x=.025+i*.97/n
        box(ax,x,.32,width,.40,head,body,i%4)
        if i < n-1:
            arrow(ax,(x+width+.008,.52),(.025+(i+1)*.97/n-.008,.52))
    save(fig,name)


# Capítulo 1: relaciones entre conceptos y flujos de una aplicación.
fig, (ax,) = canvas("IA, aprendizaje automático y aprendizaje profundo", "Cada caja pequeña pertenece también a las cajas que la contienen.")
blank(ax)
for x,y,w,h,c in [(.03,.02,.94,.94,0),(.10,.09,.79,.64,1),(.20,.15,.56,.30,2)]:
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.015",facecolor=PALE[c],edgecolor="#91aec2"))
ax.text(.08,.84,"INTELIGENCIA ARTIFICIAL",weight="bold",fontsize=19)
ax.text(.15,.61,"MACHINE LEARNING · aprende de datos",weight="bold",fontsize=16)
ax.text(.25,.30,"DEEP LEARNING",weight="bold",fontsize=17)
ax.text(.25,.20,"Redes neuronales de varias capas",fontsize=13)
ax.text(.80,.50,"Árboles\nKNN\nSVM",ha="center")
save(fig,"c01_ia_mapa")

fig, axes = canvas("Una imagen, tres preguntas diferentes", "La salida necesaria determina la tarea y cómo se evalúa.",3)
for i,ax in enumerate(axes):
    blank(ax)
    ax.add_patch(Rectangle((.08,.22),.84,.60,facecolor="#e2e8ef",edgecolor="#94a9bb"))
    ax.add_patch(Rectangle((.36,.30),.25,.33,facecolor=TEAL,alpha=.85))
    ax.add_patch(Rectangle((.43,.63),.11,.10,facecolor=TEAL))
    ax.set_title(["Clasificación","Detección","Segmentación"][i])
    if i==1: ax.add_patch(Rectangle((.30,.26),.38,.51,fill=False,edgecolor=RED,lw=3))
    if i==2:
        for a,b in [(.36,.30),(.36,.41),(.36,.52),(.47,.30),(.47,.41),(.47,.52),(.43,.63)]:
            ax.add_patch(Rectangle((a,b),.11,.10,facecolor=ORANGE,alpha=.75,edgecolor="white"))
    ax.text(.5,.08,["Etiqueta: botella","Caja + etiqueta","Etiqueta por píxel"][i],ha="center",fontsize=13)
save(fig,"c01_vision")

fig, (ax,) = canvas("Aprendizaje por refuerzo: decidir y observar consecuencias", "La recompensa orienta el aprendizaje de una política; puede llegar varios pasos después.")
blank(ax)
box(ax,.04,.35,.30,.36,"AGENTE","Observa y elige acción",0)
box(ax,.65,.35,.30,.36,"ENTORNO","Cambia tras la acción",1)
arrow(ax,(.35,.62),(.64,.62),"acción")
arrow(ax,(.64,.40),(.35,.40),"observación + recompensa")
ax.text(.50,.12,"Ejemplo: robot → moverse → nueva posición y puntuación",ha="center",fontsize=14)
save(fig,"c01_refuerzo")
flow("c01_sectores","De una capacidad técnica a una aplicación útil",[("Problema","Demanda de agua"),("Datos","Sensores + contexto"),("Estimación","Necesidad de riego"),("Decisión","Plan de operación"),("Seguimiento","Consumo y errores")],"Ejemplo conceptual: una buena métrica del modelo debe traducirse en un proceso útil.")
flow("c01_ruta","Cómo se conectan los capítulos 1–5",[("1 · Contexto","Tarea y objetivo"),("2 · Matemáticas","Vectores y funciones"),("3 · Datos","Tablas y limpieza"),("4 · Estadística","Variación y evidencia"),("5 · Modelos","Aprender y evaluar")])

# Capítulo 2: funciones, geometría, dimensiones y cambios.
fig, axes = canvas("Tres funciones que volverán a aparecer en ML", "Lee entrada, salida, dominio y forma antes de utilizar una fórmula.",3)
x=np.linspace(-4,4,300)
axes[0].plot(x,2*x+1,color=BLUE); axes[0].set(title="Lineal: 2x + 1",xlabel="x",ylabel="f(x)"); axes[0].axhline(0,color="#aab8c5",lw=.7)
xp=np.linspace(.05,5,300);axes[1].plot(xp,np.log(xp),color=TEAL);axes[1].set(title="Logaritmo: ln(x), x > 0",xlabel="x",ylabel="ln(x)");axes[1].axhline(0,color="#aab8c5",lw=.7)
axes[2].plot(x,1/(1+np.exp(-x)),color=ORANGE);axes[2].scatter([0],[.5],color=RED);axes[2].set(title="Logística: salida entre 0 y 1",xlabel="z",ylabel="σ(z)",ylim=(-.05,1.05));axes[2].axhline(.5,color="#aab8c5",ls="--")
save(fig,"c02_funciones")
fig, axes = canvas("Norma, distancia y perpendicularidad", "Las componentes describen un desplazamiento; la norma resume su longitud.",2)
ax=axes[0];ax.arrow(0,0,3,4,width=.025,length_includes_head=True,color=BLUE);ax.plot([0,3,3],[0,0,4],"--",color=ORANGE);ax.text(1.2,2.6,"‖(3,4)‖ = 5",fontsize=14);ax.set(xlim=(-.5,4.5),ylim=(-.5,5),xlabel="componente 1",ylabel="componente 2",title="Pitágoras: √(3² + 4²) = 5");ax.set_aspect("equal")
ax=axes[1];ax.arrow(0,0,1,2,width=.025,length_includes_head=True,color=BLUE);ax.arrow(0,0,2,-1,width=.025,length_includes_head=True,color=TEAL);ax.text(1,2.25,"u = (1,2)");ax.text(1.25,-1.5,"v = (2,−1)");ax.set(xlim=(-.8,3.4),ylim=(-2,3),xlabel="x",ylabel="y",title="u · v = 1×2 + 2×(−1) = 0");ax.set_aspect("equal");ax.axhline(0,color="#bac9d7");ax.axvline(0,color="#bac9d7")
save(fig,"c02_vectores")
fig, (ax,) = canvas("Producto matricial: una suma ponderada por fila", "Las dimensiones interiores coinciden; las exteriores dan la forma del resultado.")
blank(ax);box(ax,.02,.35,.30,.38,"X · forma (3, 2)","[1, 2]   [3, 4]   [5, 6]",0);box(ax,.40,.35,.20,.38,"w · forma (2,)","[10, 1]",1);box(ax,.69,.35,.29,.38,"X @ w · forma (3,)","[12, 34, 56]",2);arrow(ax,(.33,.55),(.39,.55),"@");arrow(ax,(.61,.55),(.68,.55),"=");ax.text(.5,.12,"Primera fila: 1×10 + 2×1 = 12. Se repite una vez por observación.",ha="center",fontsize=14)
save(fig,"c02_matrices")
fig, axes = canvas("Derivar describe un cambio; optimizar utiliza ese cambio", "Izquierda: pendiente local. Derecha: un paso hacia una pérdida menor.",2)
xx=np.linspace(0,4.5,200);axes[0].plot(xx,xx**2,color=BLUE,label="f(x) = x²");axes[0].plot(xx,6*(xx-3)+9,"--",color=ORANGE,label="Tangente en x=3");axes[0].scatter([3],[9],color=RED);axes[0].set(xlabel="x",ylabel="f(x)",ylim=(-1,21),title="f′(3) = 6");axes[0].legend(fontsize=10)
ww=np.linspace(-1,5,200);axes[1].plot(ww,(ww-2)**2,color=TEAL);axes[1].scatter([4,3.2],[4,1.44],color=RED);axes[1].annotate("",xy=(3.2,1.44),xytext=(4,4),arrowprops={"arrowstyle":"->","color":RED,"lw":2});axes[1].set(xlabel="parámetro w",ylabel="pérdida L(w)",title="L=(w−2)²; w nuevo = 4 − 0.2×4 = 3.2")
save(fig,"c02_derivadas")

# Capítulo 3: estructuras y preparación de datos.
fig, (ax,) = canvas("NumPy: axis indica qué eje se reduce", "M = [[2,4,6], [8,10,12]] tiene forma (2,3). Reducir un eje elimina esa dimensión.")
blank(ax)
for i,row in enumerate([[2,4,6],[8,10,12]]):
    for j,value in enumerate(row):
        box(ax,.10+j*.14,.59-i*.24,.12,.19,str(value),color=i)
for j,value in enumerate([10,14,18]):ax.text(.16+j*.14,.20,str(value),ha="center",weight="bold",fontsize=18)
ax.text(.06,.08,"sum(axis=0) → [10,14,18] · forma (3,)",fontsize=14)
ax.text(.63,.68,"2 + 4 + 6 = 12",fontsize=17);ax.text(.63,.44,"8 + 10 + 12 = 30",fontsize=17)
ax.text(.60,.20,"sum(axis=1) → [12,30]",fontsize=14)
ax.text(.60,.09,"forma (2,)",fontsize=14)
save(fig,"c03_numpy_ejes")
flow("c03_pandas","groupby: dividir, calcular y reunir",[("Tabla","norte: 9, 12 min\nsur: 18, 24 min"),("Dividir","Un grupo por zona"),("Agregar","norte: 21/2\nsur: 42/2"),("Resultado","norte: 10.5 min\nsur: 21 min")],"Cada fila del resultado representa un grupo; ya no representa un recorrido individual.")
flow("c03_preprocesamiento","fit aprende referencias; transform las conserva",[("Separar","Train / validación\n/ test"),("fit en train","Mediana, media,\nescala, categorías"),("transform","Mismas referencias\nen los otros datos"),("Modelo","Aprender y evaluar\nsin fuga de datos")],"También durante validación cruzada, cada fold ajusta sus transformaciones dentro de su entrenamiento.")
fig, axes = canvas("Categorías: representar sin inventar distancias", "Nominal: no hay un orden natural. Ordinal: hay orden, pero no necesariamente distancias iguales.",2)
for ax in axes:blank(ax)
box(axes[0],.05,.30,.90,.48,"One-hot: zona","norte → [1,0,0]\nsur → [0,1,0]\neste → [0,0,1]",0)
box(axes[1],.05,.30,.90,.48,"Ordinal: prioridad","baja → 0\nmedia → 1\nalta → 2",1)
axes[0].text(.5,.10,"Los números son indicadores, no kilómetros.",ha="center",fontsize=11)
axes[1].text(.5,.10,"El orden debe fijarse explícitamente.",ha="center",fontsize=11)
save(fig,"c03_codificacion")
fig, axes = canvas("Escalar y transformar responden preguntas distintas", "Datos positivos simulados: el escalado lineal conserva la cola; el logaritmo puede cambiarla.",3)
data=rng.lognormal(1,.8,1000)
for ax,values,title in zip(axes,[data,(data-data.mean())/data.std(),np.log1p(data)],["Original","Z-score: mismas proporciones","log1p: comprime la cola"]):
    ax.hist(values,bins=25,color=BLUE,edgecolor="white");ax.set(xlabel="valor",ylabel="frecuencia",title=title)
save(fig,"c03_escalado")
fig, axes = canvas("Elegir un gráfico comienza por la pregunta", "Estos paneles usan datos construidos: cada marca tiene un significado diferente.",3)
axes[0].scatter([1,2,3,4,5],[6,10,11,16,18],color=BLUE,s=55);axes[0].set(title="Relación: dispersión",xlabel="distancia (km)",ylabel="duración (min)")
axes[1].hist([2,2,3,3,3,4,4,5,7],bins=[1.5,3.5,5.5,7.5],color=TEAL,edgecolor="white");axes[1].set(title="Distribución: histograma",xlabel="valor numérico",ylabel="número de observaciones")
axes[2].bar(["norte","sur"],[3,6],color=[BLUE,ORANGE]);axes[2].set(title="Categorías: barras",xlabel="zona",ylabel="número de recorridos",ylim=(0,7))
save(fig,"c03_graficos")
fig, (ax,) = canvas("Boxplot: la caja y los bigotes tienen papeles distintos", "Ejemplo construido: Q1=4, mediana=6, Q3=8. Las cercas son −2 y 14.")
ax.bxp([{"med":6,"q1":4,"q3":8,"whislo":2,"whishi":12,"fliers":[18]}],orientation="horizontal",patch_artist=True,boxprops={"facecolor":PALE[0]},medianprops={"color":RED,"lw":2})
ax.set(xlim=(-3,20),yticks=[],xlabel="valor observado")
for x,label in [(4,"Q1"),(6,"Mediana"),(8,"Q3"),(2,"Bigote"),(12,"Bigote"),(18,"Punto exterior")]:
    ax.annotate(label,xy=(x,1),xytext=(x,1.32 if x in [4,8,18] else .68),ha="center",arrowprops={"arrowstyle":"->","color":"#587086"},fontsize=12)
for x in [-2,14]:ax.axvline(x,ls="--",color=ORANGE,alpha=.8)
ax.text(.5,.93,"Los bigotes llegan a datos observados dentro de las cercas; no llegan necesariamente a las cercas.",transform=ax.transAxes,ha="center",fontsize=11)
save(fig,"c03_boxplot")

# Capítulo 4: denominadores, distribuciones e inferencia.
fig, (ax,) = canvas("Bayes: al conocer el defecto, cambia el denominador", "Fábrica hipotética con 10 000 piezas. El árbol conserva los conteos de cada rama.")
blank(ax);box(ax,.34,.78,.32,.17,"10 000 piezas",color=0);box(ax,.06,.42,.36,.20,"A: 6 000","2 % defectos → 120",1);box(ax,.59,.42,.36,.20,"B: 4 000","5 % defectos → 200",2);arrow(ax,(.42,.77),(.24,.63));arrow(ax,(.60,.77),(.77,.63));box(ax,.30,.07,.40,.19,"320 defectuosas","P(B | defecto) = 200/320 = 62.5 %",3);arrow(ax,(.24,.41),(.40,.27));arrow(ax,(.77,.41),(.60,.27))
save(fig,"c04_bayes")
fig, axes = canvas("Masa discreta y densidad continua", "En discreta se suman probabilidades. En continua se calcula el área de un intervalo.",2)
axes[0].bar([0,1,2],[.5,.3,.2],color=BLUE,width=.6);axes[0].set(xticks=[0,1,2],xlabel="número de alertas",ylabel="P(X=x)",title="0.5 + 0.3 + 0.2 = 1",ylim=(0,.65))
xx=np.linspace(-4,4,400);yy=norm.pdf(xx);axes[1].plot(xx,yy,color=TEAL);mask=(xx>=-1)&(xx<=1);axes[1].fill_between(xx,0,yy,where=mask,color=TEAL,alpha=.3);axes[1].set(xlabel="valor de X",ylabel="densidad f(x)",title="P(−1 ≤ X ≤ 1) ≈ 0.683")
save(fig,"c04_distribuciones")
fig, axes=canvas("El TLC describe medias de muestras, no cambia los datos", "Simulación con semilla 42: observaciones exponenciales y medias de 3 000 muestras de 40 casos.",2)
pop=rng.exponential(2,10000);means=rng.exponential(2,(3000,40)).mean(axis=1)
axes[0].hist(pop,bins=45,color=BLUE);axes[0].set(xlabel="valor individual",ylabel="frecuencia",title="Datos: asimétricos")
axes[1].hist(means,bins=35,color=TEAL);axes[1].set(xlabel="media de 40 observaciones",ylabel="frecuencia de medias",title="Medias: aproximadamente normales")
save(fig,"c04_tlc")
fig, axes=canvas("Intervalos de confianza y p-valor: dos lecturas distintas", "Ilustraciones didácticas. Ambas interpretaciones dependen del modelo y de sus supuestos.",2)
interval_centers=np.array([49,51,48,52,50,54,49,51]);axes[0].errorbar(interval_centers,np.arange(8),xerr=3,fmt="o",color=BLUE);axes[0].axvline(50,color=RED,label="μ fijo = 50");axes[0].set(xlabel="media e intervalo",ylabel="muestra repetida",title="Cada muestra produce otro intervalo");axes[0].legend(fontsize=10)
xx=np.linspace(-4,4,400);pdf=t.pdf(xx,15);axes[1].plot(xx,pdf,color=TEAL);axes[1].fill_between(xx,0,pdf,where=np.abs(xx)>=2,color=ORANGE,alpha=.5);axes[1].set(xlabel="estadístico t bajo H₀",ylabel="densidad",title="Dos colas: p = P(|T| ≥ 2) ≈ 0.064")
save(fig,"c04_inferencia")

# Capítulo 5: modelos, evaluación y combinación de predicciones.
flow("c05_flujo","Del ejemplo etiquetado a la predicción de un caso nuevo",[("X e y","Características\ny respuesta real"),("Entrenar","fit(X_train, y_train)"),("Validar","Elegir configuración\ncon datos reservados"),("Inferir","predict(X_nuevo)"),("Evaluar","Comparar ŷ con y\nen test")])
fig, axes=canvas("Regresión: una recta produce cantidades y deja residuos", "Ejemplo didáctico: ŷ = 4 + 3x. Residuo = valor real − predicción.",2)
xx=np.array([1,2,3,4,5]);real=np.array([6,11,12,17,18]);pred=4+3*xx
axes[0].scatter(xx,real,color=BLUE,label="observado");axes[0].plot(xx,pred,color=TEAL,label="predicción");axes[0].vlines(xx,real,pred,color=ORANGE,lw=2);axes[0].set(xlabel="distancia (km)",ylabel="duración (min)",title="Segmento vertical = residuo");axes[0].legend(fontsize=10)
axes[1].scatter(pred,real-pred,color=BLUE);axes[1].axhline(0,color=RED);axes[1].set(xlabel="duración predicha (min)",ylabel="residuo (min)",title="Buscar estructura en los errores")
save(fig,"c05_regresion")
fig, axes=canvas("Clasificación: probabilidad estimada y decisión", "El umbral convierte un valor continuo en una clase. Cambiarlo cambia los tipos de error.",2)
zz=np.linspace(-6,6,400);axes[0].plot(zz,1/(1+np.exp(-zz)),color=BLUE);axes[0].axhline(.5,ls="--",color=RED);axes[0].axvline(0,ls=":",color=RED);axes[0].set(xlabel="z = w·x + b",ylabel="p̂(clase positiva)",title="Regresión logística",ylim=(0,1))
ax=axes[1];blank(ax)
box(ax,.02,.59,.30,.23,"0.35", "p estimada",0);box(ax,.48,.64,.48,.22,"umbral 0.50","Clase negativa",1);box(ax,.48,.23,.48,.22,"umbral 0.30","Clase positiva",2);arrow(ax,(.33,.70),(.46,.75));arrow(ax,(.33,.68),(.46,.34));ax.text(.5,.02,"La probabilidad no cambió; cambió la regla de decisión.",ha="center",fontsize=11)
save(fig,"c05_logistica")
fig, (ax,) = canvas("Matriz de confusión: primero fija qué significa «positivo»", "100 correos hipotéticos: positivo = spam. Filas reales, columnas predichas.")
matrix=np.array([[80,5],[3,12]]);ax.imshow(matrix,cmap="Blues",vmin=0,vmax=100)
for i in range(2):
    for j in range(2):ax.text(j,i,f"{['VN','FP','FN','VP'][2*i+j]}\n{matrix[i,j]}",ha="center",va="center",fontsize=21,color="white" if matrix[i,j]>50 else "#17334e")
ax.set(xticks=[0,1],xticklabels=["Legítimo","Spam"],yticks=[0,1],yticklabels=["Legítimo","Spam"],xlabel="clase predicha",ylabel="clase real")
save(fig,"c05_confusion")
fig, (ax,) = canvas("Árbol de decisión: un caso sigue una ruta hasta una hoja", "Árbol didáctico construido a mano. Las reglas de un árbol entrenado se eligen a partir de datos.")
blank(ax);box(ax,.35,.75,.30,.19,"¿Distancia ≤ 3 km?",color=0);box(ax,.05,.37,.35,.21,"Hoja: 10 min","Promedio de 8 y 12",1);box(ax,.59,.37,.35,.21,"¿Hora punta?",color=0);arrow(ax,(.41,.74),(.23,.60),"sí");arrow(ax,(.61,.74),(.76,.60),"no");box(ax,.50,.02,.22,.18,"Hoja: 18 min",color=2);box(ax,.76,.02,.22,.18,"Hoja: 25 min",color=3);arrow(ax,(.70,.36),(.61,.21),"no");arrow(ax,(.83,.36),(.87,.21),"sí")
save(fig,"c05_arbol")
fig, axes=canvas("KNN y SVM utilizan la geometría de maneras diferentes", "Coordenadas construidas en escalas comparables. Son esquemas conceptuales, no una comparación de rendimiento.",2)
a=np.array([[1,1],[1.5,2],[2,1.4],[2.8,3]]);b=np.array([[4,3],[4.5,4],[5,3],[4,4.5]])
for ax in axes:
    ax.scatter(*a.T,color=BLUE,label="clase A",s=55);ax.scatter(*b.T,color=ORANGE,label="clase B",s=55);ax.set(xlim=(0,6),ylim=(0,5.5),xlabel="característica 1",ylabel="característica 2")
axes[0].scatter([2.4],[2],color=RED,marker="*",s=200,label="caso nuevo");axes[0].add_patch(Circle((2.4,2),1.2,fill=False,ls="--",color=RED));axes[0].set_title("KNN: consultar a los vecinos cercanos");axes[0].legend(fontsize=9)
yy=np.array([0,5.5]);axes[1].plot(np.full(2,3.3),yy,color=TEAL);axes[1].plot(np.full(2,2.8),yy,"--",color=TEAL);axes[1].plot(np.full(2,3.8),yy,"--",color=TEAL);axes[1].set_title("SVM: una frontera con margen");axes[1].text(3.3,5.15,"margen",ha="center",fontsize=10)
save(fig,"c05_knn_svm")
fig, axes=canvas("Conjuntos: diversidad y corrección progresiva", "Bagging y boosting entrenan modelos de maneras distintas y luego combinan sus predicciones.",2)
for ax in axes:blank(ax)
box(axes[0],.27,.80,.46,.15,"Datos de train",color=0)
for x in [.02,.36,.70]:
    box(axes[0],x,.43,.28,.18,"Modelo","remuestreo",1);arrow(axes[0],(.50,.79),(x+.14,.63));arrow(axes[0],(x+.14,.42),(.50,.23))
box(axes[0],.18,.03,.64,.18,"Votar o promediar",color=2);axes[0].set_title("Bagging: modelos en paralelo")
for x,label in [(.02,"Modelo 1"),(.37,"Modelo 2"),(.72,"Modelo 3")]:box(axes[1],x,.45,.25,.25,label,color=1)
arrow(axes[1],(.28,.57),(.36,.57));arrow(axes[1],(.63,.57),(.71,.57));axes[1].text(.5,.25,"Cada etapa usa información del error anterior.\nSe suman contribuciones con una tasa de aprendizaje.",ha="center",fontsize=12);axes[1].set_title("Boosting: modelos por etapas")
save(fig,"c05_conjuntos")

fig, (ax,) = canvas("Validación cruzada: cada parte valida una vez", "Ejemplo Iris: 120 casos para desarrollo; 30 de test permanecen fuera de este proceso.")
blank(ax)
for row in range(5):
    ax.text(.02,.85-row*.17,f"Fold {row+1}",va="center",fontsize=13)
    for col in range(5):
        box(ax,.16+col*.15,.79-row*.17,.135,.12,"validar" if col==row else "train",color=2 if col==row else 0)
ax.text(.53,-.06,"En cada fila: 96 casos entrenan y 24 validan; el Pipeline se ajusta de nuevo.",ha="center",fontsize=12)
save(fig,"c05_validacion")

fig, (ax,) = canvas("Complejidad y generalización", "Esquema conceptual: las curvas representan comportamientos posibles, no mediciones de un experimento.")
complexity=np.linspace(0,10,200)
ax.plot(complexity,3*np.exp(-complexity/2)+.2,color=BLUE,label="error de entrenamiento")
ax.plot(complexity,.10*(complexity-4)**2+1,color=ORANGE,label="error de validación")
ax.axvspan(0,2,color=BLUE,alpha=.07);ax.axvspan(7,10,color=RED,alpha=.07)
ax.text(1,4,"Subajuste",ha="center");ax.text(8.5,4,"Sobreajuste",ha="center")
ax.set(xlabel="complejidad del modelo",ylabel="error (esquema)",ylim=(0,5));ax.legend()
save(fig,"c05_complejidad")

from sklearn.metrics import precision_recall_curve, roc_curve
truth=np.array([0,0,0,1,0,1,0,1,0,1]);scores=np.array([.05,.15,.20,.30,.40,.45,.55,.65,.75,.90])
fpr,tpr,_=roc_curve(truth,scores);precision,recall,_=precision_recall_curve(truth,scores)
fig, axes=canvas("ROC y precisión–recall recorren distintos umbrales", "Ejemplo construido con 10 casos y 4 positivos. Los ejes responden preguntas diferentes.",2)
axes[0].plot(fpr,tpr,marker="o",color=BLUE);axes[0].plot([0,1],[0,1],"--",color="#a8bac9");axes[0].set(xlabel="FP / (FP + VN)",ylabel="VP / (VP + FN)",title="ROC: falsos positivos frente a sensibilidad",xlim=(-.03,1.03),ylim=(-.03,1.03))
axes[1].step(recall,precision,where="post",color=TEAL);axes[1].axhline(.4,ls="--",color=ORANGE,label="proporción positiva: 0.4");axes[1].set(xlabel="recall: VP / (VP + FN)",ylabel="precision: VP / (VP + FP)",title="Precisión–recall: calidad de las alertas",xlim=(-.03,1.03),ylim=(-.03,1.03));axes[1].legend(fontsize=9)
save(fig,"c05_roc_pr")

print(f"Diagramas generados: {len(list(OUT.glob('*.svg')))} SVG y sus vistas PNG.")

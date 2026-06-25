---

## subject: "precalculo"
topic: "funciones_trigonometricas_dominio_rango_y_grafica"
content_type: "base_teorica_socrática"

# Funciones Trigonométricas — Dominio, Rango y Gráfica

## Sustento Axiomático y Conceptual

Las funciones trigonométricas (o circulares) extienden las razones geométricas del triángulo rectángulo hacia el dominio continuo de los números reales $\mathbb{R}$. Axiomáticamente, se definen a partir del comportamiento dinámico de las coordenadas de un punto móvil $P(x, y)$ sobre una circunferencia de radio unitario ($r = 1$).

Si un ángulo $\theta$ (medido estrictamente en radianes) describe la rotación del rayo inicial respecto al origen, las proyecciones horizontales y verticales sobre los ejes cartesianos formalizan analíticamente las funciones base:

$$\cos(\theta) = x \quad \land \quad \sin(\theta) = y$$

Las cuatro funciones trigonométricas restantes ($\tan(\theta), \cot(\theta), \sec(\theta), \csc(\theta)$) se construyen mediante el álgebra de cocientes de estas dos funciones fundamentales.

### 1. Funciones Fundamentales: Seno y Coseno

* **Seno ($f(\theta) = \sin(\theta)$):** Modela la oscilación continua de la ordenada $y$.
* **Coseno ($f(\theta) = \cos(\theta)$):** Modela la oscilación continua de la abscisa $x$.

Debido a que el punto $P(x, y)$ gira infinitamente sobre la curva acotada del círculo unitario, se deducen formalmente las siguientes propiedades operacionales:

* **Dominio:** Las variables angulares no poseen ninguna barrera algebraica aditiva de existencia en la recta numérica:

$$\text{Dom}(\sin) = \text{Dom}(\cos) = \mathbb{R} = (-\infty, +\infty)$$


* **Rango:** Al estar atrapadas geométricamente dentro del perímetro del círculo unitario, sus salidas escalares quedan estrictamente confinadas en el intervalo cerrado:

$$\text{Ran}(\sin) = \text{Ran}(\cos) = [-1, 1]$$


* **Periodicidad:** Ambas funciones completan una revolución unívoca y exacta sobre el círculo al alcanzar el periodo fundamental de $T_0 = 2\pi$ radianes.

### 2. Funciones Racionales Asintóticas: Tangente y Secante

* **Tangente ($f(\theta) = \tan(\theta) = \frac{\sin(\theta)}{\cos(\theta)}$):** Su dominio se encuentra restringido en aquellos puntos singulares donde la proyección del coseno se anula ($\cos(\theta) = 0$). Axiomáticamente, esto genera infinitas asíntotas verticales:

$$\text{Dom}(\tan) = \left\{ \theta \in \mathbb{R} \ \Big| \ \theta \neq \frac{\pi}{2} + k\pi, \ k \in \mathbb{Z} \right\}$$


$$\text{Ran}(\tan) = \mathbb{R} = (-\infty, +\infty) \quad \land \quad \text{Periodo Fundamental: } T_0 = \pi \text{ rad}$$


* **Secante ($f(\theta) = \sec(\theta) = \frac{1}{\cos(\theta)}$):** Al ser el recíproco multiplicativo del coseno, hereda exactamente las mismas restricciones de dominio que la tangente. Sin embargo, su rango excluye la región interna del círculo unitario:

$$\text{Dom}(\sec) = \left\{ \theta \in \mathbb{R} \ \Big| \ \theta \neq \frac{\pi}{2} + k\pi, \ k \in \mathbb{Z} \right\} \quad \land \quad \text{Ran}(\sec) = (-\infty, -1] \cup [1, +\infty)$$



### 3. Funciones Racionales Asintóticas: Cotangente y Cosecante

* **Cotangente ($f(\theta) = \cot(\theta) = \frac{\cos(\theta)}{\sin(\theta)}$):** Su dominio se interrumpe donde la proyección vertical del seno se extingue ($\sin(\theta) = 0$):

$$\text{Dom}(\cot) = \{\theta \in \mathbb{R} \ | \ \theta \neq k\pi, \ k \in \mathbb{Z}\} \quad \land \quad \text{Ran}(\cot) = \mathbb{R}$$


* **Cosecante ($f(\theta) = \csc(\theta) = \frac{1}{\sin(\theta)}$):** Recíproco de la función seno, compartiendo sus asíntotas verticales en múltiplos enteros de $\pi$:

$$\text{Dom}(\csc) = \{\theta \in \mathbb{R} \ | \ \theta \neq k\pi, \ k \in \mathbb{Z}\} \quad \land \quad \text{Ran}(\csc) = (-\infty, -1] \cup [1, +\infty)$$



## Errores Algebraicos Comunes

El análisis didáctico de la ingeniería inicial en la UCA identifica los siguientes sesgos procedimentales y analíticos recurrentes:

* **Confundir la escala del dominio al graficar:** Intentar tabular el eje horizontal $x$ utilizando la escala discreta de enteros de campo ($1, 2, 3\dots$) en lugar de la escala continua de radianes en términos del número irracional $\pi$ ($\frac{\pi}{2}, \pi, \frac{3\pi}{2}, 2\pi$), distorsionando la geometría de la onda oscilatoria.
* **Suponer que el rango de la secante y cosecante es el inverso fraccionario de $[-1,1]$:** Creer de forma errónea que al calcular el recíproco, el rango se invierte a $[-1, 1]$ en lugar de expandirse hacia las regiones exteriores $(-\infty, -1] \cup [1, +\infty)$.
* **Trazar curvas tangenciales continuas cruzando las asíntotas:** Dibujar la gráfica de la tangente como una línea continua y unificada de izquierda a derecha, ignorando las discontinuidades no evitables (saltos al infinito) en cada múltiplo impar de $\frac{\pi}{2}$.
* **Modificación ilegal de la amplitud interna:** Confundir el coeficiente multiplicativo de la amplitud con una alteración del argumento angular, asumiendo falsamente que en $f(x) = 3\sin(x)$ las ondas se repiten con el triple de frecuencia horizontal.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Canónica y Escrutinio de la Base Geométrica

**Objetivo:** Guiar al estudiante a identificar la función trigonométrica analizada y predecir cualitativamente el comportamiento del rango y periodo sin trazar líneas ni tabular puntos de forma explícita.

* *Observa la función circular de tu ejercicio. ¿Se trata de una de las funciones fundamentales acotadas (seno o coseno) o es una función estructurada en forma de cociente racional (tangente, secante)?*
* *Si la función depende de una fracción como $\frac{1}{\cos(\theta)}$, ¿qué ocurre axiomáticamente con la existencia de todo el término cuando la proyección de la variable del denominador tiende a alcanzar el valor cero?*
* *Recuerda la correspondencia en el círculo unitario. ¿Cuál es la altura máxima y mínima que puede registrar de forma natural la coordenada de la ordenada $y$ durante una revolución completa? ¿Cómo limita esto el rango base?*

### Nivel 2: Descomposición de Operadores de Transformación y Evidencia del Error

**Objetivo:** Forzar la autovalidación cognitiva del estudiante confrontándolo con sus imprecisiones al interpretar desplazamientos o amplitudes mediante la evaluación de ángulos notables.

* *Al evaluar la expresión modificada $f(x) = \sin(x) + 2$, tu conjetura te sugiere que el rango de la función sigue siendo $[-1, 1]$. Probemos numéricamente con un ángulo notable: si evaluamos $x = \frac{\pi}{2}$, sabemos axiomáticamente que $\sin\left(\frac{\pi}{2}\right) = 1$. Si le sumas de forma externa la constante $+2$, ¿cuál es el output real del sistema? ¿Sigue perteneciendo a tu intervalo propuesto? ¿Hacia qué dirección vertical se desplazó toda la barrera elástica del rango?*
* *Sostienes que para la función tangente, es legal colocar un punto coordenado sólido de intersección en $x = \frac{\pi}{2}$. Intentemos realizar la división formal: $\tan\left(\frac{\pi}{2}\right) = \frac{\sin(\pi/2)}{\cos(\pi/2)} = \frac{1}{0}$. ¿Qué tipo de número o indeterminación se genera al dividir por cero en el campo real? ¿Qué objeto geométrico vertical debe gobernar esa frontera exacta en lugar de una curva sólida?*
* *Si te enfrentas a la función de onda $g(x) = \cos(3x)$, ¿qué parámetro se encuentra modificado? ¿El coeficiente interno $3$ altera el tamaño de la altura de la cresta vertical o comprime el tiempo que tarda la variable en completar un periodo de $2\pi$?*

### Nivel 3: Formalización Analítica e Integridad Estructural en Ingeniería

**Objetivo:** Inducir al estudiante a modelar formalmente las exclusiones de dominio y justificar científicamente el diseño periódico de la onda bajo los estándares rigurosos de la UCA.

* *Modela con total rigor científico el dominio y el rango de la función trigonométrica compuesta definida por la regla $h(x) = 2\sec(x - \pi)$. Traduce las transformaciones rígidas aplicadas al espacio geométrico: plantea de forma exacta las inecuaciones que aíslan a las asíntotas verticales del dominio y reestructura analíticamente el intervalo del rango basándote en la amplificación de la amplitud. Expresa tu respuesta final utilizando la notación formal de conjuntos.*
* *Explica mediante un breve argumento meta-cognitivo cómo el concepto de periodicidad y el comportamiento asintótico de las funciones trigonométricas son esenciales para evitar fallos de desbordamiento en el procesamiento de señales de ingeniería. ¿Por qué omitir la declaración formal de las discontinuidades angulares en una arquitectura RAG local podría corromper la consistencia científica de un modelo de simulación automatizada?*
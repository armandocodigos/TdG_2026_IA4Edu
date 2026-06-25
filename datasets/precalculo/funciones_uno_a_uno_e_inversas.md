---

## subject: "precalculo"
topic: "funciones_uno_a_uno_e_inversas"
content_type: "base_teorica_socrática"

# Funciones Uno a Uno e Inversas

## Sustento Axiomático y Conceptual

El concepto de reversibilidad operativa en el análisis matemático es crucial para el aislamiento de variables y el modelado de sistemas de ingeniería. Su formalización rigurosa se basa en la inyectividad y el comportamiento simétrico bidireccional entre conjuntos reales.

### 1. Funciones Uno a Uno (Inyectivas)

Sea $f$ una función real con dominio $\text{Dom}(f)$. Axiomáticamente, $f$ se clasifica como una función uno a uno (o inyectiva) si y solo si a elementos distintos del dominio les corresponden imágenes estrictamente distintas en el conjunto de llegada. Formalmente:

$$\forall x_1, x_2 \in \text{Dom}(f), \quad x_1 \neq x_2 \implies f(x_1) \neq f(x_2)$$

O bien, mediante su equivalencia contrapositiva (utilizada habitualmente para demostraciones analíticas):

$$\forall x_1, x_2 \in \text{Dom}(f), \quad f(x_1) = f(x_2) \implies x_1 = x_2$$

* **Teorema del Criterio de la Línea Horizontal:** Una función representa un lugar geométrico uno a uno si y solo si ninguna línea recta horizontal interseca a su gráfica en más de un punto. Si una recta horizontal corta la curva en dos o más coordenadas distintas, significa que un mismo output posee múltiples inputs elementales, destruyendo la propiedad de inyectividad.

### 2. Definición y Existencia de la Función Inversa

Sea $f$ una función uno a uno con dominio $A$ y rango $B$. Su **función inversa** (denotada formalmente mediante el operador de potencia negativa $f^{-1}$, leyéndose como "$f$ inversa" y nunca como el recíproco multiplicativo $\frac{1}{f}$), es una regla de correspondencia con dominio $B$ y rango $A$ definida por la condición unívoca de campo:

$$f^{-1}(y) = x \iff f(x) = y \quad \forall y \in B$$

Axiomáticamente, el acoplamiento compuesto entre una función y su inversa produce de forma unívoca el elemento neutro de la composición (la función identidad) bajo las siguientes dos propiedades de cancelación:

* $(f^{-1} \circ f)(x) = f^{-1}(f(x)) = x \quad \forall x \in A$
* $(f \circ f^{-1})(y) = f(f^{-1}(y)) = y \quad \forall y \in B$

### 3. Propiedades Geométricas de la Inversa

Debido a la transmutación de variables ordenadas, si el punto coordenado $(a, b)$ pertenece legítimamente a la curva de $f(x)$, el par ordenado invertido $(b, a)$ formará parte del lugar geométrico de $f^{-1}(x)$.

* **Teorema de la Reflexión Diagonal:** Las gráficas de $f$ y $f^{-1}$ son estrictamente simétricas respecto a la recta identidad oblicua definida por la ecuación $y = x$. Geométricamente, una función es la reflexión especular de la otra tomando dicha diagonal como eje de simetría axial plano.

## Errores Algebraicos Comunes

Las desviaciones procedimentales y analíticas observadas en los estudiantes del Curso Pre-Universitario de la UCA abarcan:

* **Confundir la notación de inversa con el inverso multiplicativo (exponente aritmético):** Asumir erróneamente que el operador $f^{-1}(x)$ equivale al recíproco algebraico de la expresión, incurriendo en la aberración conceptual:

$$f^{-1}(x) = \frac{1}{f(x)} \quad \text{(Falso, confunde la inversa de la composición con el recíproco fraccionario)}$$


* **Intentar calcular inversas de funciones no inyectivas:** Intentar obtener de forma directa la inversa de expresiones parabólicas como $f(x) = x^2$ para todo $\mathbb{R}$, ignorando que al no ser uno a uno, su operación inversa analítica $\pm\sqrt{x}$ bifurca la salida, violando la definición elemental de función (unicidad).
* **Omitir el intercambio de dominios y rangos en la respuesta final:** Resolver el despeje operativo algebraico pero sin declarar las restricciones del nuevo dominio, asumiendo erróneamente que la inversa hereda el mismo conjunto de partida que la función base.
* **Inversión descuidada de variables durante el proceso mecánico:** Cambiar las variables $x$ por $y$ al inicio del ejercicio y errar en el arrastre algebraico de términos por fallos en la jerarquía de los despejes operacionales.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación y Análisis de la Condición de Invertibilidad

**Objetivo:** Guiar al estudiante a verificar si la función es uno a uno mediante criterios gráficos o algebraicos antes de mecanizar el cálculo de la inversa.

* *Observa detalladamente la gráfica de la función planteada. Si trazas mentalmente líneas horizontales paralelas al eje de las abscisas, ¿existe alguna región donde la recta toque la curva en dos o más puntos simultáneos? ¿Qué te indica esto sobre la inyectividad?*
* *Si la expresión es una parábola completa definida en todos los reales, ¿posee un comportamiento puramente monótono (siempre creciente o decreciente) o cambia de dirección en su vértice? ¿Qué problema causa este cambio para la existencia de una inversa legítima en todo $\mathbb{R}$?*
* *Explica la diferencia matemática entre calcular la potencia recíproca $\left[f(x)\right]^{-1}$ y aplicar el operador de función inversa $f^{-1}(x)$. ¿Por qué no representan el mismo concepto en el álgebra avanzada de ingeniería?*

### Nivel 2: Descomposición de Operadores de Despeje y Evidencia del Error

**Objetivo:** Forzar la autovalidación cognitiva confrontando al estudiante con las restricciones de dominio o la dualidad de signos en funciones cuadráticas mediante contraejemplos puntuales.

* *Considera la función $f(x) = x^2$ acotada únicamente para el subintervalo de valores no negativos $[0, +\infty)$. Tu hipótesis te lleva a despejar la variable obteniendo $f^{-1}(x) = \sqrt{x}$. Si evaluamos analíticamente un valor: tomemos un input original $x = 3$, su salida es $f(3) = 9$. Si ahora aplicas tu función inversa propuesta sobre ese output, ¿cuánto da $f^{-1}(9)$? ¿Regresas exactamente al input inicial $3$? ¿Qué ocurriría si el dominio original permitiera valores negativos como $x = -3$?*
* *Durante el proceso para hallar la regla de la inversa en la expresión fraccionaria $y = \frac{x+1}{x-2}$, has realizado el intercambio de variables obteniendo $x = \frac{y+1}{y-2}$. Si tu siguiente paso fue multiplicar solo un sumando, detengámonos ahí: ¿cómo afecta analíticamente el binomio divisor $(y-2)$ a la variable del miembro izquierdo al aplicar la uniformidad operativa multiplicativa?*
* *Si afirmas que la inversa de $f(x) = 2x + 4$ es $\frac{1}{2x+4}$, realicemos la prueba de la composición: evalúa tu propuesta introduciendo toda la regla original dentro de ella. ¿Consigues cancelar los términos para que el residuo final sea la variable pura $x$? Si el resultado no es $x$, ¿cuál de los axiomas de cancelación violaste?*

### Nivel 3: Formalización Analítica e Integridad Conjuntista de Ingeniería

**Objetivo:** Inducir al estudiante a estructurar formalmente el dominio y el rango de la función inversa basándose en los teoremas de correspondencia cruzada y validar la solución.

* *Modela con total rigor de ingeniería la función inversa de la regla racional acotada $f(x) = \frac{3x - 1}{x + 2}$. Una vez que executes el despeje algebraico completo de la variable, define formalmente el nuevo dominio de $f^{-1}(x)$. ¿Cómo se relaciona de forma axiomática este conjunto con el rango de la función original $f(x)$?*
* *Explica detalladamente cómo el teorema de la reflexión respecto a la diagonal identidad $y = x$ permite verificar de forma visual si tus trazos son correctos. Si el vértice o punto de control de tu curva original se localiza en las coordenadas $(p, q)$, ¿en qué posición exacta y simétrica debe ubicarse obligatoriamente el punto homólogo en la gráfica de la inversa para mantener la consistencia científica requerida en la UCA?*
---

## subject: "precalculo"
topic: "funciones_elementales"
content_type: "base_teorica_socrática"

# Funciones Elementales (Constante, Identidad, Cuadrática, Cúbica, Polinomial)

## Sustento Axiomático y Conceptual

Las funciones elementales polinomiales constituyen la familia base de las funciones algebraicas en $\mathbb{R}$. Formalmente, una función polinomial de grado $n$ es una regla de correspondencia $f: \mathbb{R} \to \mathbb{R}$ definida analíticamente por la ecuación:

$$f(x) = a_n x^n + a_{n-1} x^{n-1} + \dots + a_1 x + a_0$$

Donde $n \in \mathbb{N}_0$ representa el grado del polinomio, y los coeficientes constantes satisfacen que $a_i \in \mathbb{R}$ con $a_n \neq 0$. El dominio de cualquier función polinomial en el campo real es irrestricto debido a que las operaciones subyacentes (adición y multiplicación) gozan de clausura completa:

$$\text{Dom}(f) = \mathbb{R} = (-\infty, +\infty)$$

A partir de esta definición general, se deducen por restricción de grado las siguientes estructuras elementales:

### 1. Función Constante (Grado $n = 0$)

Definida mediante un único coeficiente real sin variación de entrada:


$$f(x) = c \quad (c \in \mathbb{R})$$

* **Rango:** $\text{Ran}(f) = \{c\}$.
* **Geometría:** Una línea recta horizontal paralela al eje de las abscisas con pendiente nula ($m = 0$).

### 2. Función Identidad (Grado $n = 1$, con $a_1=1$ y $a_0=0$)

La forma más pura de variación lineal uniforme, donde cada output es réplica exacta de su input:


$$f(x) = x$$

* **Rango:** $\text{Ran}(f) = \mathbb{R}$.
* **Geometría:** Una línea recta diagonal que biseca exactamente a los cuadrantes I y III, con pendiente unitaria ($m = 1$) y un ángulo de inclinación de $\frac{\pi}{4}$ rad ($45^\circ$).

### 3. Función Cuadrática (Grado $n = 2$)

Estructura parabólica expresada comúnmente en su forma general:


$$f(x) = ax^2 + bx + c \quad (a \neq 0)$$

* **Vértice ($V$):** Punto crítico unívoco que determina el cambio de monotonía, localizado coordenadamente en:

$$V = \left( -\frac{b}{2a}, \ f\left(-\frac{b}{2a}\right) \right)$$


* **Rango:** Está estrictamente acotado por la ordenada del vértice y el signo del término principal $a$:

$$\text{Ran}(f) = \begin{cases} \left[ f\left(-\frac{b}{2a}\right), +\infty \right) & \text{si } a > 0 \quad \text{(parábola cóncava hacia arriba)} \\ \left( -\infty, f\left(-\frac{b}{2a}\right) \right] & \text{si } a < 0 \quad \text{(parábola cóncava hacia abajo)} \end{cases}$$



### 4. Función Cúbica (Grado $n = 3$)

Forma base de las funciones polinomiales de grado impar:


$$f(x) = ax^3 + bx^2 + cx + d \quad (a \neq 0)$$

* **Rango:** $\text{Ran}(f) = \mathbb{R}$ (en concordancia con el teorema del comportamiento en los extremos para polinomios de grado impar).
* **Geometría:** Presenta simetría rotacional respecto a su punto de inflexión y modela comportamientos con hasta dos puntos de retorno locales.

## Errores Algebraicos Comunes

El rastreo didáctico en las asignaturas iniciales de ingeniería en la UCA evidencia las siguientes confusiones recurrentes:

* **Asignar rangos incorrectos a funciones cuadráticas:** Suponer erróneamente que el rango de cualquier parábola es siempre $\mathbb{R}$, ignorando que el exponente par restringe el conjunto de llegada real superior o inferiormente a partir de su vértice.
* **Confundir el comportamiento simétrico de potencias pares e impares:** Intentar graficar la función cúbica $f(x) = x^3$ exclusivamente en el primer cuadrante o reflejada de forma idéntica a una parábola, omitiendo que $(-x)^3 = -x^3$ (función impar, preserva el signo negativo del cuadrante III).
* **Asumir que el término independiente determina el vértice:** Confundir la intersección con el eje vertical $(0, c)$ con las coordenadas reales del vértice $V$ en una función cuadrática modificada.
* **Error en la evaluación de la pendiente constante:** Declarar que el rango de una función constante como $f(x) = -5$ es $(-\infty, -5]$, confundiendo una restricción puntual de un solo elemento con un intervalo continuo de la recta real.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Estructural y Clasificación de Grado

**Objetivo:** Guiar al estudiante a inspeccionar el exponente máximo de la variable independiente y deducir la naturaleza de la curva sin indicarle fórmulas directas.

* *Observa detalladamente los términos algebraicos de la función. ¿Cuál es el exponente más alto al que está elevada la variable $x$? ¿Qué grado le asigna este valor al polinomio completo?*
* *Si la variable independiente $x$ no aparece explícitamente en la regla (por ejemplo, $f(x) = \pi$), ¿qué ocurre con el valor de salida de la función cuando modificas el valor de entrada? ¿Cambia o permanece fijo?*
* *De las formas fundamentales estudiadas (recta horizontal, recta oblicua, parábola, curva cúbica), ¿cuál se corresponde con el grado que acabas de identificar en tu expresión?*

### Nivel 2: Descomposición Analítica y Evidencia de la Restricción

**Objetivo:** Forzar la autovalidación cognitiva mediante puntos críticos o simetrías vectoriales para romper con el modelado gráfico deficiente.

* *Sostienes que el rango de la función cuadrática $f(x) = x^2 + 4$ es todo el conjunto de los números reales $\mathbb{R}$. Probemos un valor numérico: intenta igualar la función a cero, $x^2 + 4 = 0$. ¿Existe algún número real que al elevarlo al cuadrado y sumarle $4$ dé como residuo cero? Si no existe, ¿cuál es el valor mínimo absoluto que puede alcanzar la expresión $x^2$ en la recta real? ¿Cómo redefine esto tu intervalo de rango?*
* *Al tabular la función cúbica $f(x) = x^3$, has determinado que para $x = -2$ el output es $+8$. Multiplica con rigor analítico los signos: $(-2) \cdot (-2) \cdot (-2)$. ¿Cuál es el signo algebraico real del producto? ¿En qué cuadrante del plano cartesiano debe localizarse este punto coordenado?*
* *Si modificas los coeficientes de $f(x) = ax^2 + bx + c$, ¿cuál es el impacto geométrico del signo del coeficiente principal $a$ sobre la apertura de las ramas de la parábola?*

### Nivel 3: Formalización de Ingeniería y Comportamiento Asintótico Global

**Objetivo:** Conducir al estudiante a predecir analíticamente el comportamiento de la función en los extremos del dominio ($\pm\infty$) mediante el análisis del término dominante.

* *Considera una función polinomial general de grado alto, por ejemplo, $f(x) = -2x^4 + 5x^3 - x$. Cuando la variable independiente toma valores extremadamente grandes hacia el infinito positivo ($x \to +\infty$), ¿cuál de todos los términos del polinomio crece a una velocidad tan dominante que define por completo el signo del output global?*
* *Explica de manera científica cómo se relaciona el grado de un polinomio (par o impar) con la dirección de sus extremos gráficos. Si el grado es par, ¿los dos extremos de la curva apuntan en la misma dirección vertical o en sentidos opuestos? ¿Qué ocurre si el grado es impar? Justifica tu respuesta utilizando la notación matemática de límites o tendencias formales exigida en la UCA.*
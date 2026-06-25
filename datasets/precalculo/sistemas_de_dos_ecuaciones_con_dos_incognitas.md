---

## subject: "precalculo"
topic: "sistemas_de_dos_ecuaciones_con_dos_incognitas"
content_type: "base_teorica_socrática"

# Sistemas de dos ecuaciones con dos incógnitas

## Sustento Axiomático y Conceptual

Un sistema lineal de dos ecuaciones con dos incógnitas (sistema $2 \times 2$) representa una conjunción lógica de dos afirmaciones algebraicas de primer grado que deben satisfacerse simultáneamente. Formalmente, dadas las variables $x, y \in \mathbb{R}$, un sistema lineal se define de forma canónica mediante el entorno:

$$\begin{cases} a_1x + b_1y = c_1 \\ a_2x + b_2y = c_2 \end{cases}$$

Donde los coeficientes $a_i, b_i, c_i \in \mathbb{R}$ para todo $i = 1, 2$. Resolver el sistema consiste en hallar el conjunto solución ($S$) compuesto por los pares ordenados $(x, y) \in \mathbb{R}^2$ que transforman ambas ecuaciones en identidades verdaderas.

### 1. Clasificación Algebraica y Teorema de Existencia

El comportamiento y la naturaleza de las soluciones de un sistema lineal están determinados estrictamente por las relaciones de proporcionalidad entre sus coeficientes (analizado a través del determinante del sistema $\det(A) = a_1b_2 - a_2b_1$). Axiomáticamente, los sistemas se clasifican bajo tres categorías unívocas:

* **Sistema Compatible Determinado (SCD):** Ocurre si $\frac{a_1}{a_2} \neq \frac{b_1}{b_2}$ (es decir, $\det(A) \neq 0$). El sistema posee una **única solución**. Geométricamente, representa dos líneas rectas no paralelas que se intersecan en un único punto común del plano cartesiano.
* **Sistema Compatible Indeterminado (SCI):** Ocurre si $\frac{a_1}{a_2} = \frac{b_1}{b_2} = \frac{c_1}{c_2}$. El sistema posee **infinitas soluciones**, dado que ambas ecuaciones son linealmente dependientes. Geométricamente, representa dos rectas coincidentes (la misma línea recta).
* **Sistema Incompatible (SI):** Ocurre si $\frac{a_1}{a_2} = \frac{b_1}{b_2} \neq \frac{c_1}{c_2}$ (donde $\det(A) = 0$ pero los términos independientes no son proporcionales). El sistema **no tiene solución** ($S = \emptyset$). Geométricamente, describe dos líneas rectas paralelas no coincidentes que jamás se cruzan.

### 2. Métodos Algebraicos de Resolución

Los métodos de resolución se basan en las propiedades de sustitución y uniformidad de las operaciones aditivas y multiplicativas en el campo real para desacoplar las variables:

* **Sustitución:** Consiste en aislar analíticamente una variable de una de las ecuaciones para reemplazar su equivalencia en la otra expresión, reduciendo el problema a una ecuación de una sola incógnita.
* **Igualación:** Se despeja la misma variable en ambas ecuaciones y se igualan sus respectivos equivalentes algebraicos basados en la propiedad transitiva de la igualdad ($A = B \ \land \ A = C \implies B = C$).
* **Reducción (Suma y Resta):** Consiste en multiplicar una o ambas ecuaciones por constantes reales estratégicas de modo que los coeficientes de una de las variables sean inversos aditivos, permitiendo la eliminación de dicha incógnita mediante la adición vertical de los sistemas.

## Errores Algebraicos Comunes

El análisis empírico en los cursos preuniversitarios y de pre-cálculo en la UCA evidencia las siguientes desviaciones operativas en los estudiantes:

* **Error de signo al sustituir binomios:** Omitir el uso de paréntesis asociativos al insertar el despeje de una variable en la segunda ecuación, provocando fallos en la distribución de coeficientes negativos:

$$\text{Sustituir } y = (3 - 2x) \text{ en } 5x - 2y = 1 \implies 5x - 2 \cdot 3 - 2x = 1 \quad \text{(Falso, el término } -2x \text{ debió ser } +4x\text{)}$$


* **Multiplicación incompleta al aplicar el método de reducción:** Multiplicar únicamente los coeficientes de las variables de un miembro del sistema por la constante de balanceo, olvidando aplicar dicha amplificación al término independiente ($c_i$).
* **Malinterpretación de resultados singulares:** Confundir las identidades de reducción triviales. Si al eliminar variables se llega a una verdad absoluta como $0 = 0$, el estudiante suele concluir erróneamente que "no hay solución" en lugar de identificar un SCI (infinitas soluciones). Inversamente, si se obtiene una contradicción lógica como $0 = 5$, asumen que el cálculo está equivocado en lugar de diagnosticar un sistema Incompatible.
* **Despejes ilegales con divisiones indeterminadas:** Intentar despejar variables cuyos coeficientes dependen de parámetros sin evaluar si estos pueden anularse, violando la restricción de división por cero.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Estructural y Visualización Geométrica

**Objetivo:** Guiar al estudiante a ordenar el sistema en su estructura canónica y clasificar las relaciones de sus pendientes antes de mecanizar un método algebraico.

* *Antes de ejecutar cualquier manipulación algebraica, observa la alineación de las variables. ¿Se encuentran los términos en $x$, los términos en $y$ y las constantes numéricas ordenados en columnas idénticas?*
* *Examina la proporción entre los coeficientes de $x$ y los de $y$ ($\frac{a_1}{a_2}$ y $\frac{b_1}{b_2}$). ¿Son estas razones numéricas iguales o diferentes? Si las interpretáramos como las pendientes de dos rectas en el plano, ¿qué nos dice esto sobre si las líneas se van a intersecar, son paralelas o son la misma recta?*
* *Si decides aplicar el método de sustitución, ¿cuál de las dos variables en cuál ecuación presenta el coeficiente más simple (por ejemplo, $1$ o $-1$) para facilitar un despeje libre de fracciones complejas?*

### Nivel 2: Descomposición de Operadores e Intervención ante Inconsistencias

**Objetivo:** Forzar al estudiante a identificar fallos en la distribución de signos o errores en la amplificación de ecuaciones mediante el rastreo inverso de pasos.

* *Durante la sustitución del binomio que despejaste, has escrito la línea de cálculo pasando de $-3(4 - x)$ a $-12 - 3x$. Detengámonos ahí: aplica detalladamente la propiedad distributiva del factor $-3$ sobre cada miembro interno. ¿Qué signo real debe adquirir el término variable?*
* *Al utilizar el método de reducción para eliminar $y$, decidiste multiplicar la primera ecuación por $2$. Revisa el miembro derecho de tu nueva ecuación: ¿has multiplicado también el término independiente por ese factor $2$, o conservaste el valor original? ¿Qué ocurre con el equilibrio de la balanza algebraica si solo alteras un lado de la igualdad?*
* *Durante el proceso operativo, las variables desaparecieron por completo y tu última línea afirma que $0 = -8$. Analicemos este resultado de forma lógica: ¿es esa proposición matemática verdadera o falsa en nuestro sistema numérico? Si es una contradicción absoluta, ¿qué tipo de relación geométrica tienen las rectas que impide que compartan un punto común?*

### Nivel 3: Formalización Analítica y Validación Cruzada de Doble Vía

**Objetivo:** Inducir al alumno a implementar el principio socrático de doble vía, forzándolo a validar meta-cognitivamente el par ordenado hallado en ambas ecuaciones originales.

* *Has calculado que el punto de cruce del sistema es el par ordenado $(x, y) = (2, -1)$. Si aplicamos el axioma de sustitución exclusivamente en la primera ecuación, se genera una identidad verdadera. Sin embargo, para garantizar con rigor científico de ingeniería que es la solución unívoca del sistema, ¿qué es necesario que ocurra al evaluar ese mismo par en la segunda ecuación del problema? Realiza la comprobación numérica.*
* *Explica con tus propias palabras cómo el concepto de "simultaneidad" exige que la solución satisfaga ambas restricciones al mismo tiempo. Si un par ordenado funciona para una ecuación pero falla en la otra, ¿pertenece legítimamente al conjunto solución $S$ del sistema o representa simplemente un punto aislado de una sola línea recta?*
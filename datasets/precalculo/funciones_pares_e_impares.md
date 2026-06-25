---

## subject: "precalculo"
topic: "funciones_pares_e_impares"
content_type: "base_teorica_socrática"

# Funciones Pares e Impares

## Sustento Axiomático y Conceptual

La simetría algebraica de una función respecto al origen o a los ejes coordenados en el plano cartesiano $\mathbb{R}^2$ constituye una propiedad fundamental que optimiza el estudio de curvas, el cálculo integral y el análisis de señales en ingeniería. Axiomáticamente, la simetría se clasifica según el comportamiento de la regla de correspondencia cuando se evalúa el inverso aditivo del argumento independiente.

Para que una función $f: X \to Y$ sea candidata a poseer propiedades de paridad, su dominio $X \subset \mathbb{R}$ debe ser estrictamente un **conjunto simétrico respecto al origen**. Esto exige formalmente el cumplimiento del siguiente axioma de existencia de simetría de partida:

$$\forall x \in \text{Dom}(f) \implies -x \in \text{Dom}(f)$$

Si el dominio es simétrico, la función se clasifica bajo los siguientes teoremas formales:

### 1. Función Par (Simetría Reflexiva Axial)

Una función $f$ es par si la evaluación del elemento negativo $-x$ produce un output exactamente idéntico al de la variable original $x$:

$$f(-x) = f(x) \quad \forall x \in \text{Dom}(f)$$

* **Geometría:** Su gráfica presenta **simetría axial respecto al eje vertical $y$**. Si el punto coordenado $(x, y)$ pertenece a la curva, el punto reflejado $(-x, y)$ también formará parte del lugar geométrico con total certeza matemática.

### 2. Función Impar (Simetría Rotacional Central)

Una función $f$ es impar si la evaluación del elemento negativo $-x$ produce el inverso aditivo de la imagen original de $x$:

$$f(-x) = -f(x) \quad \forall x \in \text{Dom}(f)$$

* **Geometría:** Su gráfica presenta **simetría rotacional de $180^\circ$ ($\pi$ radianes) respecto al origen $(0,0)$**. Esto implica que si el punto $(x, y)$ se encuentra sobre la curva, su contraparte del cuadrante opuesto $(-x, -y)$ también pertenece de forma unívoca a la función.

### 3. Teorema de Descomposición Única

Es crucial recalcar que la paridad no es una propiedad dicotómica y exhaustiva; la gran mayoría de funciones en ingeniería no son ni pares ni impares (carecen de paridad). Sin embargo, cualquier función real integrable puede descomponerse de forma unívoca como la adición de una componente par ($f_p$) y una componente impar ($f_i$):

$$f(x) = f_p(x) + f_i(x) \quad \text{donde} \quad f_p(x) = \frac{f(x) + f(x)}{2} \quad \land \quad f_i(x) = \frac{f(x) - f(x)}{2}$$

## Errores Algebraicos Comunes

Las fallas y confusiones analíticas más recurrentes detectadas en la población objetivo de ingeniería inicial en la UCA comprenden:

* **Asumir que la paridad depende exclusivamente de los exponentes visibles:** Clasificar polinomios basados solo en los exponentes de sus variables, ignorando que la presencia de términos independientes ocultiza constantes pares de grado cero ($c \cdot x^0$), lo que rompe la condición si se mezclan (ej. asumir que $f(x) = x^3 - 5$ es impar porque su exponente visible es $3$, omitiendo que $-5$ es un término par).
* **Tratamiento incorrecto de los signos negativos en funciones compuestas:** Errar en la simplificación algebraica de potencias o funciones trascendentes al evaluar $-x$, incurriendo en faltas distributivas del tipo:

$$f(-x) = (-x)^4 - (-x) = x^4 - x \implies \text{concluir erróneamente paridad o neutralidad por confusión de signos}$$


* **Omitir la validación del dominio simétrico:** Intentar clasificar la paridad de una función basándose solo en su regla algebraica, ignorando que si el dominio está acotado asimétricamente (por ejemplo, $f(x) = x^2$ definida únicamente para el intervalo $[0, +\infty)$), la función pierde axiomáticamente toda propiedad de paridad.
* **Confundir el concepto de función impar con reflexiones negativas:** Creer que para que una función sea impar su gráfica debe dar resultados puramente negativos en todo el plano, en lugar de comprender la rotación central de coordenadas.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación y Validación de la Condición de Partida

**Objetivo:** Guiar al estudiante a verificar la simetría del dominio y plantear formalmente la prueba analítica de sustitución del argumento negativo.

* *Antes de realizar cualquier manipulación en los términos de la función, observa su dominio. ¿Si tomas un valor positivo cualquiera del conjunto de partida, su contraparte negativa exacta también se encuentra permitida dentro de las restricciones de la función?*
* *Para evaluar analíticamente si una función posee simetría, ¿qué cambio debes realizar sobre la variable independiente $x$ en cada sección de la regla de correspondencia?*
* *Escribe la estructura inicial sustituyendo cada $x$ por un bloque protegido entre paréntesis $(-x)$. ¿Qué leyes de signos o propiedades de exponentes controlan la simplificación de potencias pares e impares?*

### Nivel 2: Descomposición Algebraica y Evidencia de Contradicciones

**Objetivo:** Forzar al alumno a comparar el polinomio modificado con la función original y su inverso negativo, evidenciando el quiebre de sus hipótesis iniciales mediante contraejemplos tabulares.

* *Considera la función $f(x) = x^3 - 1$. Tu hipótesis te lleva a afirmar que es una función impar. Evaluemos numéricamente la función en el punto $x = 2$: ¿cuánto da $f(2)$? Ahora calcula el output para su inverso aditivo, $f(-2)$. Según la definición de función impar, el resultado de $f(-2)$ debería dar exactamente el negativo de tu primer cálculo ($-1 \cdot f(2)$). ¿Coinciden aritméticamente estos dos valores? ¿Qué término constante rompió la simetría rotacional?*
* *Al evaluar el término $(-x)^2$, has propuesto que el resultado final conserva el signo negativo ($-x^2$). Multipliquemos el bloque por sí mismo aplicando el rigor algebraico: $(-1 \cdot x) \cdot (-1 \cdot x)$. ¿Cuál es el residuo del producto de dos signos negativos según los axiomas de campo? ¿Qué ocurre entonces con los signos de las potencias pares?*
* *Si tras simplificar $f(-x)$ notas que la expresión resultante no es exactamente idéntica a $f(x)$ ni tampoco equivale a multiplicar toda la función original por $-1$, ¿cuál es la conclusión científica legítima sobre la paridad de este objeto matemático?*

### Nivel 3: Formalización Analítica y Demostración Abstracta de Ingeniería

**Objetivo:** Inducir al estudiante a generalizar las propiedades operativas de la paridad mediante modelos abstractos (productos y cocientes de funciones), consolidando el pensamiento científico.

* *Supongamos que en un modelo de ingeniería necesitas multiplicar dos funciones simétricas conocidas: una función par $P(x)$ y una función impar $I(x)$, generando la combinación $h(x) = P(x) \cdot I(x)$. Demuestra de forma totalmente abstracta y analítica, utilizando las definiciones axiomáticas de paridad, cuál será el comportamiento de simetría final de la función producto $h(x)$.*
* *Explica de qué manera la interpretación geométrica de los puntos coordenados $(x, y)$ frente a $(-x, y)$ o $(-x, -y)$ te permite verificar la exactitud de una gráfica utilizando solo la mitad de su plano cartesiano. ¿Cómo aplicarías este principio meta-cognitivo para ahorrar recursos computacionales si estuvieras programando el renderizado de estas curvas en un entorno asíncrono local?*
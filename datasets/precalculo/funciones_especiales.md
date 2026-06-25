---

## subject: "precalculo"
topic: "funciones_especiales"
content_type: "base_teorica_socrática"

# Funciones Especiales (Proporción Inversa, Seccionadas, Valor Absoluto, Parte Entera, Escalón, Signo)

## Sustento Axiomático y Conceptual

Las funciones especiales introducen discontinuidades estructurales, criterios de asignación condicional y comportamientos asintóticos complejos no lineales en el modelado matemático para ingeniería. Su formalización extiende las nociones fundamentales de dominio y rango en el conjunto de los números reales $\mathbb{R}$.

### 1. Función de Proporción Inversa (Racional Base)

Representa la relación de proporcionalidad inversa entre variables, definida analíticamente por la ecuación:

$$f(x) = \frac{k}{x} \quad (k \in \mathbb{R} \setminus \{0\})$$

* **Dominio:** $\text{Dom}(f) = \mathbb{R} \setminus \{0\} = (-\infty, 0) \cup (0, +\infty)$ por la restricción de división por cero.
* **Rango:** $\text{Ran}(f) = \mathbb{R} \setminus \{0\} = (-\infty, 0) \cup (0, +\infty)$.
* **Comportamiento Asintótico:** Presenta una asíntota vertical en $x = 0$ debido a que el límite de la función tiende a infinito ($\lim_{x \to 0^{\pm}} f(x) = \pm\infty$), y una asíntota horizontal en $y = 0$ puesto que la función decae hacia las abscisas en los extremos ($\lim_{x \to \pm\infty} f(x) = 0$). Su lugar geométrico es una hipérbola equilátera.

### 2. Funciones Seccionadas (o a Trozos)

Son funciones cuya regla de correspondencia cambia de forma unívoca según el subintervalo del dominio en el que se encuentre la variable independiente $x$. Se estructuran formalmente mediante el entorno condicional:

$$f(x) = \begin{cases} g_1(x) & \text{si } x \in I_1 \\ g_2(x) & \text{si } x \in I_2 \\ \vdots & \vdots \\ g_n(x) & \text{si } x \in I_n \end{cases}$$

* **Dominio:** Es la unión unificada de todos los subintervalos disjuntos definidos por las restricciones: $\text{Dom}(f) = I_1 \cup I_2 \cup \dots \cup I_n$.
* **Rango:** Es la unión de los rangos individuales de cada función componente evaluada estrictamente bajo su respectivo subintervalo de dominio: $\text{Ran}(f) = \text{Ran}(g_1|_{I_1}) \cup \dots \cup \text{Ran}(g_n|_{I_n})$.

### 3. Función Valor Absoluto

Se define axiomáticamente a partir de la distancia de un punto real al origen. Constituye intrínsecamente la forma base de una función seccionada simétrica:

$$f(x) = |x| = \begin{cases} x & \text{si } x \ge 0 \\ -x & \text{si } x < 0 \end{cases}$$

* **Dominio:** $\text{Dom}(f) = \mathbb{R}$.
* **Rango:** $\text{Ran}(f) = [0, +\infty)$ por la condición de no negatividad de las distancias en $\mathbb{R}$.
* **Propiedad Geométrica:** Su gráfica describe una esquina angular en forma de "V" cuyo vértice representa un punto de continuidad pero no de derivabilidad.

### 4. Función Parte Entera (Función Piso)

Asigna a cada entrada real el mayor entero que sea menor o igual que dicho número, denotada formalmente por el operador $\lfloor x \rfloor$ o $[x]$:

$$f(x) = \lfloor x \rfloor = n \iff n \le x < n + 1 \quad (n \in \mathbb{Z})$$

* **Dominio:** $\text{Dom}(f) = \mathbb{R}$.
* **Rango:** $\text{Ran}(f) = \mathbb{Z}$ (conjunto discreto de los números enteros).
* **Geometría:** Estructura escalonada con infinitas discontinuidades de salto finito en cada valor entero del dominio.

### 5. Función Escalón Unitario (Heaviside)

Utilizada extensamente en la teoría de señales y control automatizado en ingeniería. Modela la activación repentina de un sistema físico:

$$f(x) = H(x) = \begin{cases} 0 & \text{si } x < 0 \\ 1 & \text{si } x \ge 0 \end{cases}$$

* **Dominio:** $\text{Dom}(H) = \mathbb{R}$.
* **Rango:** $\text{Ran}(H) = \{0, 1\}$.

### 6. Función Signo

Extrae el sentido de orientación algebraico de la variable de entrada, anulándose exclusivamente en el origen:

$$f(x) = \text{sgn}(x) = \begin{cases} -1 & \text{si } x < 0 \\ 0 & \text{si } x = 0 \\ 1 & \text{si } x > 0 \end{cases}$$

* **Dominio:** $\text{Dom}(\text{sgn}) = \mathbb{R}$.
* **Rango:** $\text{Ran}(\text{sgn}) = \{-1, 0, 1\}$.
* *Relación axiomática:* Para todo $x \neq 0$, se cumple que $\text{sgn}(x) = \frac{x}{|x|} = \frac{|x|}{x}$.

## Errores Algebraicos Comunes

La recopilación de fallos en el Curso Pre-Universitario de la UCA para estas temáticas muestra las siguientes tendencias erróneas:

* **Asumir linealidad aditiva en el valor absoluto:** Creer equívocamente que las barras actúan como operadores lineales distribuibles sobre sumas algebraicas:

$$|a + b| = |a| + |b| \quad \text{(Falso, viola la desigualdad triangular } |a+b| \le |a| + |b|\text{)}$$


* **Evaluación incorrecta de la parte entera para números negativos:** Calcular erróneamente el valor piso de un número negativo redondeando hacia el entero más cercano al origen, cometiendo fallos del tipo:

$$\lfloor -2.3 \rfloor = -2 \quad \text{(Falso, el entero máximo menor o igual a } -2.3 \text{ es } -3\text{)}$$


* **Unificación ilegal de criterios en funciones seccionadas:** Intentar evaluar un único input variable en todas las ramas de la función seccionada simultáneamente, ignorando las restricciones excluyentes de los subintervalos del dominio.
* **Omitir las asíntotas en la inversión de variables:** Intentar graficar la función de proporción inversa uniendo los trazos hiperbólicos de forma continua a través del origen, ignorando la discontinuidad esencial en $x = 0$.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación y Reconocimiento de Discontinuidad

**Objetivo:** Guiar al estudiante a identificar el tipo de regla de correspondencia especial y la naturaleza condicionada de su dominio sin proveer cálculos aritméticos.

* *Observa la función seccionada de tu problema. Si deseas evaluar el comportamiento de la función en el punto $x = -2$, ¿cuál de los subintervalos condicionales contiene legítimamente a este número? ¿Es correcto procesarlo en las otras ecuaciones de la llave?*
* *En la función de proporción inversa $f(x) = \frac{4}{x}$, ¿qué ocurre con el valor de salida si intentas aproximar la variable $x$ a valores sumamente cercanos a cero, como $0.0001$? ¿Hacia dónde se dispara numéricamente el output?*
* *Al observar las barras de la función $|x - 5|$, ¿cuál es el significado geométrico que tiene este operador en términos de distancias? ¿Puede una distancia pura arrojar un valor final negativo?*

### Nivel 2: Descomposición Analítica y Confrontación de Intervalos

**Objetivo:** Forzar la autovalidación analítica del estudiante rompiendo los sesgos de cálculo de signos en partes enteras y valor absoluto mediante contraejemplos.

* *Afirmas que la parte entera de $-1.5$ es $-1$. Ubiquemos ambos números en la recta numérica real: ¿se encuentra el $-1$ a la izquierda o a la derecha de $-1.5$? Si la definición formal exige un entero que sea estrictamente **menor o igual**, ¿cuál es el primer número entero que aparece a la izquierda de $-1.5$ al recorrer el eje ordenado?*
* *Intentas reescribir la expresión de valor absoluto $|x + 2|$ deshaciéndote de las barras de forma directa. Recuerda que el valor absoluto cambia de comportamiento según el signo de su argumento. ¿Para qué intervalo de $x$ el término interno $(x+2)$ se vuelve negativo, obligando algebraicamente a anteponer un signo menos distributivo ($-1 \cdot (x+2)$) para forzar su positividad?*
* *Al graficar una función seccionada, colocaste dos puntos cerrados sólidos verticalmente alineados en la frontera de cambio $x = 1$. Apliquemos el Criterio de la Línea Vertical: ¿cuántas imágenes reales estás asignando para la entrada $1$? ¿Viola esto el axioma de unicidad de una función? ¿Cómo se representa gráficamente un extremo excluido?*

### Nivel 3: Formalización y Consistencia Estructural en $\mathbb{R}$

**Objetivo:** Conducir al estudiante a la construcción abstracta de la estructura seccionada o asintótica, validando los conjuntos solución según los estándares de ingeniería de la UCA.

* *Considera la función mixta $f(x) = \frac{\text{sgn}(x-3)}{|x-3|}$. Describe de forma analítica cómo se comporta esta expresión para los tres grandes casos del dominio ($x > 3$, $x = 3$ y $x < 3$). Modela los resultados parciales y unifica la respuesta en una estructura de función seccionada limpia libre de operadores especiales. ¿Qué tipo de asíntota o indeterminación formal se genera en la frontera singular?*
* *Explica de manera científica cómo la combinación de funciones escalón o funciones piso permite modelar fenómenos discretos en ingeniería (como pulsos de voltaje o tarifas segmentadas). Justifica de forma meta-cognitiva la asignación de corchetes abiertos y cerrados en el rango resultante.*
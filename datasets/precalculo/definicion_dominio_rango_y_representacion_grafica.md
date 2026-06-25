---

## subject: "precalculo"
topic: "definicion_dominio_rango_y_representacion_grafica"
content_type: "base_teorica_socrática"

# Definición, Dominio, Rango y Representación Gráfica

## Sustento Axiomático y Conceptual

El concepto de función constituye el pilar estructural del análisis matemático moderno y la ingeniería. Axiomáticamente, se fundamenta en la teoría de conjuntos como una relación específica entre elementos de dos colecciones numéricas.

### 1. Definición Formal de una Función

Sean $X$ e $Y$ dos subconjuntos no vacíos de los números reales $\mathbb{R}$. Una función $f$ de $X$ en $Y$ (denotada como $f: X \to Y$) es una regla de correspondencia que asigna a **cada** elemento $x \in X$ un **único** elemento $y \in Y$. El elemento $y$ se denomina la imagen de $x$ bajo $f$ y se denota formalmente mediante la ecuación analítica:

$$y = f(x)$$

Para que una relación matemática califique estrictamente como una función, debe cumplir con dos axiomas fundamentales:

* **Axioma de Existencia:** $\forall x \in X, \exists y \in Y \ | \ (x, y) \in f$
* **Axioma de Unicidad:** Si $(x, y_1) \in f \ \land \ (x, y_2) \in f \implies y_1 = y_2$

### 2. Dominio y Rango

* **Dominio ($\text{Dom}(f)$):** Es el conjunto de partida o de todas las variables independientes $x \in \mathbb{R}$ para las cuales la regla de correspondencia produce un resultado que pertenece legítimamente al campo de los números reales. Analíticamente, se define como:

$$\text{Dom}(f) = \{x \in X \ | \ \exists y \in Y \ \land \ y = f(x)\}$$



*Restricciones de existencia en $\mathbb{R}$:* Está gobernado por la prohibición absoluta de divisiones entre cero ($\frac{k}{0}$) y raíces de índice par con argumentos estrictamente negativos ($\sqrt[2n]{-k}$).
* **Rango o Imagen ($\text{Ran}(f)$ o $\text{Im}(f)$):** Es el conjunto de llegada efectivo, constituido por todas las variables dependientes u outputs $y \in Y$ que son imagen de al menos un elemento del dominio. Se define formalmente como:

$$\text{Ran}(f) = \{y \in Y \ | \ \exists x \in X \ \land \ y = f(x)\}$$



### 3. Representación Gráfica y Criterio de la Línea Vertical

La gráfica de una función representa el lugar geométrico de todos los puntos ordenados en el plano cartesiano $\mathbb{R}^2$ que satisfacen su ecuación matemática:

$$\text{Gráfica}(f) = \{(x, f(x)) \in \mathbb{R}^2 \ | \ x \in \text{Dom}(f)\}$$

Geométricamente, el dominio se visualiza proyectando la curva de forma ortogonal sobre el eje horizontal $x$, mientras que el rango se determina proyectando la curva sobre el eje vertical $y$.

* **Teorema del Criterio de la Línea Vertical:** Una curva en el plano cartesiano representa la gráfica de una función si y solo si ninguna línea recta vertical interseca a la curva en más de un punto. Si una recta vertical corta a la gráfica en dos o más puntos, la relación viola el axioma de unicidad, clasificándose meramente como una ecuación o relación geométrica (como la circunferencia o la elipse).

## Errores Algebraicos Comunes

La cátedra de matemática de la UCA identifica los siguientes vacíos conceptuales recurrentes en los estudiantes de ingeniería inicial:

* **Asumir que toda relación geométrica es una función:** Intentar calcular el dominio de expresiones como $x^2 + y^2 = 9$ sin notar que la presencia del exponente par en la variable dependiente $y$ bifurca el resultado en dos imágenes opuestas ($y = \pm\sqrt{9-x^2}$), violando la unicidad.
* **Confundir el dominio analítico con la evaluación discreta:** Suponer que el dominio de una función se reduce únicamente a los números enteros que el estudiante tabula en una lista pequeña de datos, perdiendo la noción de continuidad de intervalos en $\mathbb{R}$.
* **Cálculo de restricciones incompleto:** Ignorar que las restricciones de un dominio pueden estar acopladas dentro de otras funciones complejas. Por ejemplo, en la expresión $f(x) = \frac{1}{\sqrt{x-2}}$, el estudiante suele evaluar la raíz como $x-2 \ge 0$, olvidando que al encontrarse en el denominador, el valor no puede ser cero, por lo que la desigualdad correcta debe ser estrictamente abierta: $x-2 > 0$.
* **Lectura invertida de intervalos en el rango gráfico:** Leer el rango sobre la gráfica recorriendo el eje vertical de arriba hacia abajo, resultando en intervalos mal estructurados e invertidos respecto al orden axiomático de los números reales (ej. escribir $\text{Ran}(f) = [5, -2]$ en lugar de $[-2, 5]$).

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Conceptual y Escrutinio de Unicidad

**Objetivo:** Guiar al estudiante a validar la definición de función y la existencia de restricciones en el plano sin revelar fórmulas algebraicas ni trazar la solución.

* *Si observas la regla de correspondencia o la gráfica propuesta, elige un valor cualquiera para la variable $x$. ¿Se produce un único valor de salida para $y$ o encuentras la posibilidad de obtener múltiples respuestas reales simultáneas?*
* *Analiza la ecuación de tu ejercicio. ¿Contiene alguna de las dos grandes alertas del campo real: un denominador variable o una raíz de índice par? Si es así, ¿cuál es la condición matemática obligatoria que debe cumplir el argumento interno de estos operadores para no generar una indeterminación?*
* *Si trazas mentalmente líneas verticales que corten la gráfica de izquierda a derecha, ¿existe alguna sección de la curva donde la línea toque dos o más puntos al mismo tiempo? ¿Qué te indica esto sobre la naturaleza de la relación?*

### Nivel 2: Descomposición Algebraica y Proyección de Intervalos

**Objetivo:** Forzar al estudiante a contrastar sus errores en el despeje del dominio o rango mediante contraejemplos o la inversión de variables.

* *Supongamos que afirmas que el dominio de $f(x) = \sqrt{x - 3}$ incluye al número $x = 0$. Sustituyamos ese valor en la regla: ¿cuál es el resultado de procesar $\sqrt{-3}$ dentro del conjunto de los números reales? Si el resultado no es un número real, ¿qué condición de orden debe cumplir el binomio $x - 3$ para asegurar su existencia científica?*
* *Para hallar analíticamente el rango de una función algebraica simple, suele ser muy útil aislar la variable independiente. Si en la ecuación $y = \frac{1}{x}$ realizas un intercambio algebraico para despejar $x$ en términos de $y$, ¿qué nueva restricción aparece ahora sobre la variable $y$ que condicione el rango del sistema?*
* *Observa el comportamiento de la gráfica en sus extremos. ¿La curva continúa expandiéndose indefinidamente hacia los infinitos o se detiene en un punto coordenado sólido o hueco? ¿Cómo afecta esa delimitación a la escritura de tus intervalos?*

### Nivel 3: Formalización y Consistencia Estructural de Ingeniería

**Objetivo:** Conducir al estudiante a la formalización rigurosa de su respuesta final utilizando la notación matemática formal exigida en los niveles superiores de ingeniería en la UCA.

* *Define de forma analítica el dominio de la expresión mixta $f(x) = \frac{2x}{x^2 - 4} + \sqrt{x}$. Si resuelves las restricciones del denominador por un lado y las de la raíz por el otro, ¿qué operación de la teoría de conjuntos (unión o intersección) debes aplicar entre ambos subintervalos para hallar la región real donde ambas condiciones se cumplen simultáneamente?*
* *Escribe formalmente el conjunto solución para el dominio y el rango utilizando la notación de intervalos acotados o abiertos. Asegúrate de justificar de manera meta-cognitiva por qué ciertos puntos críticos llevan un corchete cerrado (inclusión por igualdad) o un paréntesis abierto (exclusión por discontinuidad o asíntotas).*
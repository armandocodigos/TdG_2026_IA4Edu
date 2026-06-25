---

## subject: "precalculo"
topic: "funcion_logaritmica_dominio_rango_y_grafica"
content_type: "base_teorica_socrática"

# Función Logarítmica — Dominio, Rango y Gráfica

## Sustento Axiomático y Conceptual

La función logarítmica es una estructura matemática trascendente que se define axiomáticamente como la **función inversa** de la función exponencial. Su desarrollo analítico es fundamental en las ciencias e ingeniería para modelar fenómenos de compresión de escala (como la escala de pH, la intensidad sísmica de Richter o la atenuación de señales en decibelios).

Formalmente, si $a$ es una constante real positiva diferente de la unidad ($a > 0 \ \land \ a \neq 1$), la función logarítmica con base $a$ se denota como:

$$f(x) = \log_a(x)$$

Y se encuentra gobernada de forma unívoca por la equivalencia de campo respecto a la potencia:

$$y = \log_a(x) \iff a^y = x$$

A partir de esta relación de inversión de conjuntos coordenados, se deducen rigurosamente sus propiedades fundamentales:

### 1. Dominio y Rango

Debido a que el dominio de una función inversa corresponde exactamente al rango de su función original, y viceversa, se establecen los siguientes conjuntos de definición en $\mathbb{R}$:

* **Dominio ($\text{Dom}(f)$):** Puesto que una base positiva elevada a cualquier exponente real siempre arroja un resultado estrictamente mayor que cero ($a^y > 0$), el argumento de un logaritmo está restringido de forma absoluta al semi-eje positivo abierto. Las cantidades negativas o nulas carecen de logaritmo real:

$$\text{Dom}(f) = \mathbb{R}^+ = (0, +\infty)$$


* **Rango ($\text{Ran}(f)$):** El exponente $y$ puede asumir con total certeza matemática cualquier valor continuo a lo largo de la recta real:

$$\text{Ran}(f) = \mathbb{R} = (-\infty, +\infty)$$



### 2. Comportamiento Gráfico y Monotonía

La geometría y el crecimiento de la curva logarítmica dependen de manera estricta del valor numérico de la base $a$, dividiéndose analíticamente en dos grandes casos teóricos homólogos a la exponencial:

* **Caso 1: Crecimiento Logarítmico ($a > 1$)**
La función es estrictamente creciente en todo su dominio. Cuando la variable independiente se aproxima a cero por la derecha ($x \to 0^+$), las imágenes caen asintóticamente hacia el infinito negativo. Al crecer el argumento ($x \to +\infty$), el output aumenta de forma continua pero con una tasa de variación decreciente (crecimiento atenuado).
* **Caso 2: Decaimiento Logarítmico ($0 < a < 1$)**
La función es estrictamente decreciente en todo su dominio. Cuando $x \to 0^+$, las imágenes se disparan hacia el infinito positivo, y decaen cruzando el eje horizontal conforme el argumento se expande.

### 3. Propiedades Geométricas Fundamentales

Todas las funciones logarítmicas de la forma canónica $f(x) = \log_a(x)$ cumplen con los siguientes teoremas de estructura:

* **Intersección Horizontal Unívoca:** La curva interseca obligatoriamente al eje de las abscisas $x$ en el punto $(1, 0)$, dado que $\log_a(1) = 0$ (equivalente a la propiedad exponencial $a^0 = 1$).
* **Ausencia de Intersección Vertical:** La curva jamás corta al eje de las ordenadas $y$, puesto que el valor $x = 0$ se encuentra fuera de su dominio de definición real.
* **Comportamiento Asintótico Vertical:** El eje $y$ (definido analíticamente por la recta línea $x = 0$) actúa como una asíntota vertical por su extremo izquierdo:

$$\lim_{x \to 0^+} \log_a(x) = \begin{cases} -\infty & \text{si } a > 1 \\ +\infty & \text{si } 0 < a < 1 \end{cases}$$



*Nota de Cátedra (Logaritmos Especiales):* En la UCA, los dos sistemas de logaritmos más utilizados en el modelado técnico son el logaritmo común o decimal (base $a=10$, denotado simplemente como $\log(x)$) y el logaritmo natural o neperiano (base el número de Euler $a=e$, denotado formalmente como $\ln(x)$). Ambos pertenecen estrictamente al caso de crecimiento ($10 > 1 \ \land \ e > 1$).

## Errores Algebraicos Comunes

Los principales vicios procedimentales e imprecisiones analíticas detectados en la población estudiantil abarcan:

* **Intentar evaluar argumentos negativos o nulos:** Tratar de resolver inecuaciones o dominios permitiendo valores donde el radicando o argumento interno sea menor o igual a cero (ej. asumir erróneamente que $\log_a(0) = 0$ o que absorbe signos negativos).
* **Confundir las propiedades logarítmicas con la linealidad distributiva:** Cometer aberraciones conceptuales que violan las leyes de los logaritmos, tales como:

$$\log_a(x + y) = \log_a(x) + \log_a(y) \quad \text{(Falso, la suma interna es inoperable; la suma externa viene de un producto)}$$


* **Trazar la curva cruzando la barrera asintótica vertical:** Dibujar la gráfica tocando el eje vertical $y$ o cruzando hacia el segundo cuadrante ($x < 0$), violando la restricción de existencia del dominio real.
* **Inversión errónea en desplazamientos horizontales:** Al evaluar funciones transformadas como $g(x) = \ln(x + c)$, desplazar la asíntota vertical hacia la derecha en lugar de trasladarla hacia la coordenada negativa $x = -c$.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Canónica y Restricción del Argumento

**Objetivo:** Guiar al estudiante a identificar la naturaleza de la función logarítmica y plantear la inecuación de restricción del dominio sin revelar cálculos operativos.

* *Observa detalladamente el argumento dentro del operador logarítmico. Si recordamos que el logaritmo es la operación inversa de la potencia, ¿existe alguna potencia real de una base positiva que pueda dar como resultado un número negativo o exactamente cero?*
* *De acuerdo con esta restricción axiomática, ¿qué tipo de inecuación formal debes plantear sobre el binomio o argumento interno para asegurar que la función exista en el campo real? ¿Debe ser una desigualdad abierta, cerrada, mayor o menor que cero?*
* *Antes de tabular o graficar la expresión transformada, ¿cuál es la ecuación de la recta vertical que limita el avance de la curva por su extremo izquierdo y actúa como asíntota?*

### Nivel 2: Descomposición Algebraica y Desmitificación del Signo

**Objetivo:** Forzar la autovalidación cognitiva confrontando al estudiante con el comportamiento del rango frente a valores fraccionarios del dominio mediante análisis inverso.

* *Sostienes que como el dominio está restringido a valores positivos ($x > 0$), el rango de la función también debe arrojar únicamente resultados positivos ($y > 0$). Evaluemos analíticamente la expresión bajo la forma exponencial equivalente: si consideramos $y = \log_2(x)$, y elegimos un output de rango negativo como $y = -3$, reescribe la igualdad en su formato de potencia. ¿A qué es igual $2^{-3}$? ¿El valor de $x$ resultante es un número real permitido en el dominio? Si la respuesta es afirmativa, ¿por qué tu rango excluía los números negativos?*
* *Al intentar calcular el dominio de la función transformada $f(x) = \log(x - 5)$, has determinado que el dominio empieza desde el origen. Apliquemos la definición de restricción: si introduces el valor $x = 2$, el argumento se convierte en $(2 - 5) = -3$. ¿Es posible procesar el logaritmo de una magnitud negativa? ¿Qué punto crítico equilibra exactamente el argumento en cero y redefine tu asíntota vertical?*
* *Si tu ejercicio presenta la estructura $\frac{\log(x)}{\log(y)}$, tu hipótesis te sugiere simplificarla restando los argumentos como si fuera un cociente. Revisa minuciosamente las leyes de los logaritmos: ¿cuál es la diferencia real entre el logaritmo de una división ($\log\left(\frac{x}{y}\right)$) y la división de dos operaciones logarítmicas independientes? ¿Qué propiedad de cambio de base se aplica en el segundo caso?*

### Nivel 3: Formalización y Consistencia Analítica en Expresiones Compuestas

**Objetivo:** Inducir al estudiante a modelar formalmente dominios complejos que acoplan restricciones logarítmicas y racionales, garantizando el rigor de ingeniería.

* *Modela con total rigor científico el dominio de la función compuesta mixta $g(x) = \log_3(x^2 - 9) + \frac{1}{x - 5}$. Desarrolla el análisis formal separando las restricciones: plantea la inecuación cuadrática que exige el operador logarítmico por un lado y la restricción de división por cero por el otro. ¿Qué operación conjuntista debes aplicar entre ambos subconjuntos para determinar el dominio global de ingeniería?*
* *Explica analíticamente, utilizando el concepto de simetría reflexiva diagonal, cómo la gráfica de la función $y = \ln(x)$ es el espejo exacto de la curva $y = e^x$. Si un ingeniero de sistemas en la UCA deseara comprobar la consistencia geométrica de ambas curvas en un plano cartesiano, ¿qué papel juega la recta identidad $y = x$ en dicha validación meta-cognitiva?*
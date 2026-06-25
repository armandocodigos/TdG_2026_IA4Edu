---

## subject: "precalculo"
topic: "funcion_periodica"
content_type: "base_teorica_socrática"

# Función Periódica

## Sustento Axiomático y Conceptual

En el análisis matemático y las diversas ramas de la ingeniería (como la ingeniería eléctrica, mecánica y en sistemas), el modelado de fenómenos cíclicos o repetitivos —tales como ondas sonoras, señales de corriente alterna, vibraciones estructurales o ciclos térmicos— se fundamenta rigurosamente en el concepto de **Función Periódica**.

Axiomáticamente, una función real $f$ con dominio $\text{Dom}(f) \subset \mathbb{R}$ se clasifica como periódica si existe una constante real no nula $T \neq 0$ tal que, para cualquier valor de la variable independiente $x$ contenido en su conjunto de partida, se satisfacen de forma simultánea las siguientes condiciones de existencia y correspondencia:

1. **Simetría de traslación del dominio:** 
$$\forall x \in \text{Dom}(f) \implies (x + T) \in \text{Dom}(f) \ \land \ (x - T) \in \text{Dom}(f)$$


2. **Invarianza de la imagen:**

$$f(x + T) = f(x) \quad \forall x \in \text{Dom}(f)$$



### El Periodo Fundamental ($T_0$)

Si una función satisface la identidad anterior para una constante $T$, de forma inductiva se demuestra que también la cumple para cualquier múltiplo entero del mismo ($f(x + kT) = f(x)$ para todo $k \in \mathbb{Z}$). Se define formalmente como **Periodo Fundamental** ($T_0$) al menor número real estrictamente positivo ($T_0 > 0$) que valida la igualdad fundamental.

Geométricamente, la gráfica de una función periódica está constituida por la repetición infinita y exacta de un segmento de curva base denominado *ciclo*, el cual se desplaza horizontalmente de manera uniforme a lo largo de intervalos de longitud equivalentes a $T_0$.

Las funciones circulares elementales como la función seno ($f(x) = \sin(x)$) y la función coseno ($f(x) = \cos(x)$) representan los pilares axiomáticos de esta familia de funciones en el espacio continuo reales, poseyendo ambas de manera unívoca un periodo fundamental de:

$$T_0 = 2\pi \text{ rad} \quad (360^\circ)$$

## Errores Algebraicos Comunes

El rastreo didáctico y el análisis de errores en los niveles iniciales de ingeniería en la UCA identifican las siguientes confusiones conceptuales y mecánicas:

* **Asumir linealidad al modificar el argumento (Inversión del periodo):** Creer erróneamente que al multiplicar el argumento interno de la función por una constante angular $\omega$ (por ejemplo, en $f(x) = \sin(\omega x)$), el nuevo periodo fundamental se calcula multiplicando directamente el periodo base por dicha constante ($T = 2\pi \cdot \omega$), omitiendo que la velocidad angular comprime la onda de forma inversamente proporcional:

$$T = \frac{2\pi}{\omega} \quad \text{(Relación inversa de frecuencia-periodo)}$$


* **Confundir la periodicidad con la repetición discontinua aislada:** Catalogar como periódicas a curvas que imitan un patrón visual repetitivo pero cuyos outputs escalares o intervalos de dominio experimentan desfases aditivos variables que rompen la invarianza formal $f(x+T)=f(x)$.
* **Ignorar el impacto de las adiciones externas sobre la periodicidad:** Suponer que al desplazar verticalmente una función periódica (ej. $g(x) = \cos(x) + c$) o modificar su amplitud externamente ($g(x) = A\sin(x)$), el valor del periodo fundamental $T_0$ se altera, confundiendo los cambios de rango geométrico con la frecuencia del dominio.
* **Mal cálculo del periodo en funciones compuestas por sumas:** Intentar hallar el periodo de una función mixta como $h(x) = \sin(2x) + \cos(3x)$ sumando o promediando de manera ilegal los periodos individuales, en lugar de recurrir al cálculo formal del mínimo común múltiplo ($mcm$) de los periodos componentes.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Canónica y Reconocimiento del Patrón Cíclico

**Objetivo:** Guiar al estudiante a identificar si la función exhibe un comportamiento repetitivo y a aislar los puntos homólogos sobre la gráfica sin proveer algoritmos directos.

* *Observa minuciosamente la curva o la regla analítica propuesta en tu problema. Si seleccionas un punto coordenado de control cualquiera $(x, y)$ sobre la gráfica y avanzas horizontalmente hacia la derecha, ¿vuelves a encontrar exactamente el mismo valor de altura $y$? ¿Cada cuánta distancia en el eje $x$ ocurre esta coincidencia exacta?*
* *De acuerdo con las definiciones de la teoría de conjuntos, ¿qué requisitos debe cumplir el dominio de una función para asegurar que podamos sumarle o restarle indefinidamente una constante $T$ sin salirnos de sus restricciones de existencia?*
* *Si la expresión que analizas presenta la estructura $f(x) = \cos(4x)$, ¿qué elemento algebraico ha sido alterado: el valor de salida externo (amplitud) o la velocidad de variación de la variable interna (argumento angular)?*

### Nivel 2: Descomposición Analítica y Evidencia del Contra-Intuitivismo Frecuencial

**Objetivo:** Forzar la autovalidación cognitiva confrontando al estudiante con los errores de amplificación mediante la evaluación analítica de ciclos completos en el plano cartesiano.

* *Sostienes que para la función $f(x) = \sin(2x)$, al duplicar el argumento interno, el periodo debe duplicarse también volviéndose $4\pi$. Evaluemos numéricamente la función en el extremo del periodo base estándar: si calculas el valor de la función en $x = \pi$, el argumento se convierte en $2 \cdot (\pi) = 2\pi$. ¿Cuánto vale $\sin(2\pi)$? Si la función ya completó una revolución total al llegar a la coordenada de abscisa $\pi$, ¿la onda se expandió horizontalmente o experimentó una compresión geométrica? ¿Qué nos dice esto sobre la proporcionalidad de la constante interna?*
* *Al analizar la expresión transformada $g(x) = 3\sin(x) + 5$, has propuesto que el periodo fundamental queda multiplicado por tres y desplazado cinco unidades. Piensa analíticamente: las operaciones de multiplicación por tres y adición de cinco ocurren fuera del operador seno. ¿Modifican estas transformaciones rígidas el tiempo o el ángulo que tarda la variable $x$ en completar una vuelta en el círculo unitario, o alteran únicamente el rango vertical de las ordenadas $y$?*
* *Si te enfrentas a una función constante como $f(x) = 5$, se cumple formalmente que $f(x+T) = f(x) = 5$ para cualquier número real. Sin embargo, recuerda la restricción del Periodo Fundamental: ¿es posible aislar el número real positivo **más pequeño que exista** que actúe como base de repetición? Si no existe un mínimo positivo unívoco en el continuo real, ¿puede catalogarse formalmente como una función periódica en ingeniería inicial?*

### Nivel 3: Formalización Abstracta y Composición de Ondas en Ingeniería

**Objetivo:** Inducir al estudiante a modelar matemáticamente el periodo compuesto y predecir de forma meta-cognitiva el comportamiento global de señales complejas.

* *Modela con total rigor científico el periodo fundamental de la señal compuesta definida por la adición de dos frecuencias: $h(x) = \sin\left(\frac{x}{3}\right) + \cos\left(\frac{x}{4}\right)$. Desarrolla el análisis extrayendo primero de forma unívoca los periodos individuales $T_1$ y $T_2$ mediante la fórmula analítica del radio de compresión. Una vez obtenidos, explica de qué manera el concepto de mínimo común múltiplo ($mcm$) aplicado a fracciones te permite deducir el instante exacto donde ambos ciclos vuelven a acoplarse en el origen.*
* *Explica de qué manera la propiedad de periodicidad optimiza el diseño de algoritmos de simulación física en la UCA. Si un ingeniero conoce a la perfección el comportamiento de un sistema síncrono local durante un solo periodo fundamental $[0, T_0]$, ¿qué justificación matemática axiomática le faculta para predecir con total certeza científica el estado del sistema en cualquier punto remoto del tiempo futuro (por ejemplo, en $t = 1000 \cdot T_0$)?*
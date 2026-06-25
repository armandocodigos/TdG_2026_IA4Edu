---

## subject: "precalculo"
topic: "la_parabola_forma_canonica_y_general"
content_type: "base_teorica_socrática"

# La Parábola — Forma Canónica y General

## Sustento Axiomático y Conceptual

El estudio de la parábola como sección cónica es fundamental en la geometría analítica, el cálculo y el modelado físico en ingeniería y arquitectura (por ejemplo, en el diseño de reflectores parabólicos, antenas satelitales, trayectorias balísticas y puentes colgantes).

### 1. Definición Geométrica como Lugar Geométrico

Axiomáticamente, una parábola se define en el plano cartesiano $\mathbb{R}^2$ como el lugar geométrico de todos los puntos $P(x, y)$ que equidistan de un punto fijo denominado **Foco** ($F$) y de una recta fija denominada **Directriz** ($D$), la cual no contiene al foco. Es decir:

$$d(P, F) = d(P, D)$$

### 2. Elementos Estructurales de la Parábola

A partir de su definición conjuntista, se derivan analíticamente sus componentes clave:

* **Vértice ($V(h, k)$):** Punto medio del segmento perpendicular que une al foco con la recta directriz. Representa el extremo local del sistema coordenado.
* **Eje de Simetría (o Eje Focal):** Recta ortogonal a la directriz que pasa por el vértice y el foco, dividiendo a la curva en dos ramas perfectamente simétricas.
* **Parámetro ($p$):** Distancia dirigida desde el vértice hasta el foco ($d(V, F) = |p|$), que por definición es igual a la distancia desde el vértice hasta la directriz ($d(V, D) = |p|$). El signo de $p$ rige el sentido de apertura de las ramas.
* **Lado Recto ($LR$):** Segmento de recta paralelo a la directriz que pasa por el foco y cuyos extremos cortan a la parábola. Su longitud absoluta está determinada por el teorema de apertura:

$$|LR| = 4|p|$$



### 3. Forma Canónica (u Ordinaria)

La forma canónica desacopla de manera explícita las coordenadas del vértice $V(h, k)$ y la orientación del eje de simetría, dividiéndose analíticamente en dos grandes familias de curvas:

#### Parábolas Verticales (Eje de simetría paralelo al eje $y$)

Su estructura analítica eleva al cuadrado la variable independiente horizontal:

$$(x - h)^2 = 4p(y - k)$$

* Si $p > 0$, las ramas abren hacia **arriba** (cóncava hacia el infinito positivo).
* Si $p < 0$, las ramas abren hacia **abajo** (cóncava hacia el infinito negativo).
* **Foco:** $F(h, k + p) \quad \land \quad$ **Directriz:** $y = k - p$

#### Parábolas Horizontales (Eje de simetría paralelo al eje $x$)

Su estructura analítica eleva al cuadrado la variable dependiente vertical:

$$(y - k)^2 = 4p(x - h)$$

* Si $p > 0$, las ramas abren hacia la **derecha** (dirección positiva de las abscisas).
* Si $p < 0$, las ramas abren hacia la **izquierda** (dirección negativa de las abscisas).
* **Foco:** $F(h + p, k) \quad \land \quad$ **Directriz:** $x = h - p$

### 4. Forma General

La forma general representa la ecuación cuadrática polinomial expandida y homogeneizada, igualada a cero en uno de sus miembros. Dependiendo de cuál variable conserve el término de segundo grado, adopta una de las siguientes ecuaciones:

* **Eje Vertical:** $Ax^2 + Dx + Ey + F = 0 \quad (\text{donde } A \neq 0 \ \land \ E \neq 0)$
* **Eje Horizontal:** $Cy^2 + Dx + Ey + F = 0 \quad (\text{donde } C \neq 0 \ \land \ D \neq 0)$

La transmutación formal entre la forma general y la forma canónica se ejecuta analíticamente mediante el algoritmo algebraico de **completación de cuadrados perfectos** para el trinomio de la variable cuadrática.

## Errores Algebraicos Comunes

El rastreo didáctico en los cursos iniciales de la Facultad de Ingeniería y Arquitectura de la UCA identifica los siguientes sesgos procedimentales recurrentes:

* **Confusión en la asignación de la orientación del eje:** Intentar graficar una parábola horizontal abriendo hacia los infinitos verticales debido a una mala lectura del término cuadrático:

$$(y - 2)^2 = 8(x - 1) \longrightarrow \text{Asumir erróneamente que es vertical porque asocian las funciones estándar con } x^2.$$


* **Inversión de signos al extraer el vértice de la forma canónica:** Errar al identificar las coordenadas $h$ y $k$ debido a fallos con los signos negativos intrínsecos de la fórmula:

$$(x + 3)^2 = 4(y - 5) \longrightarrow \text{Declarar que el vértice se ubica en } V(3, -5) \text{ en lugar del valor real } V(-3, 5).$$


* **Error jerárquico al completar cuadrados con coeficientes principales:** Olvidar factorizar el coeficiente numérico principal antes de añadir el término de balanceo de completación $\left(\frac{b}{2}\right)^2$, rompiendo la uniformidad aditiva de la balanza algebraica.
* **Asignación incorrecta del signo del parámetro $p$:** Determinar la distancia focal omitiendo el sentido vectorial, lo que provoca que una parábola que debe abrir a la izquierda o hacia abajo termine orientada de forma invertida en los trazos finales.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Estructural y Diagnóstico del Eje

**Objetivo:** Guiar al estudiante a inspeccionar las variables de la ecuación, catalogar el eje focal (horizontal o vertical) y predecir el sentido de apertura sin realizar manipulaciones numéricas.

* *Observa detalladamente la ecuación provista en tu ejercicio. ¿Cuál de las dos variables independientes ($x$ o $y$) se encuentra afectada por el exponente de segundo grado?*
* *De acuerdo con los teoremas analíticos de las secciones cónicas, si la variable cuadrática es la $x$, ¿qué tipo de orientación (vertical u horizontal) va a adoptar el eje de simetría de la curva en el plano cartesiano? ¿Qué ocurre si la variable cuadrática es la $y$?*
* *Inspecciona el coeficiente numérico que multiplica al bloque lineal (el término equivalente a $4p$). ¿Esa magnitud posee un signo positivo o negativo? ¿Qué te indica esto sobre la dirección exacta hacia donde deben abrir las ramas elásticas de la parábola?*

### Nivel 2: Descomposición de Operadores de Completación y Evidencia del Desbalance

**Objetivo:** Forzar la autovalidación cognitiva del estudiante confrontándolo con sus errores de signos o fallos al balancear la completación de cuadrados mediante el análisis de identidades de productos notables.

* *Durante la transformación de la ecuación general $x^2 + 6x - 8y + 1 = 0$, decidiste añadir el número $9$ únicamente dentro del miembro izquierdo para agrupar el binomio $(x+3)^2$. Detengámonos ahí: según los axiomas de uniformidad operativa en los campos reales, si alteras una balanza algebraica sumando una cantidad en un miembro, ¿qué estás obligado a realizar de forma simultánea en el miembro opuesto para mantener la igualdad legítima del sistema matemático?*
* *Al extraer el vértice desde la estructura ordinaria $(y - 4)^2 = -12(x + 2)$, has propuesto que las coordenadas corresponden al par ordenado $V(4, -2)$. Comparemos minuciosamente tu propuesta con la fórmula canónica general $(y - k)^2 = 4p(x - h)$. Recuerda que el primer componente del vértice en $\mathbb{R}^2$ debe ser obligatoriamente la abscisa $h$. ¿En qué orden colocaste tus variables? ¿Qué signo real adquiere $h$ si la expresión muestra un $+2$?*
* *Si calculas que la longitud del Lado Recto es igual a $-8$ debido al signo del parámetro, piensa geométricamente: ¿puede una distancia métrica pura o una longitud física de un segmento arrojar una magnitud negativa? ¿Qué operador de contención (como el valor absoluto) debes aplicar a la relación $|LR| = 4|p|$ para asegurar la consistencia científica requerida en ingeniería?*

### Nivel 3: Formalización Analítica e Integridad del Modelo Cónico de Ingeniería

**Objetivo:** Conducir al estudiante a consolidar el modelo abstracto unificando la regla canónica, las coordenadas exactas de los elementos y la comprobación meta-cognitiva de distancias.

* *Modela con total rigor científico la transición de la parábola dada en su formato implícito general $y^2 + Dy + Ex + F = 0$ hacia su formato ordinario. Desarrolla analíticamente los pasos algebraicos de completación de cuadrados utilizando variables simbólicas puras y aísla el bloque lineal del parámetro. Al finalizar, escribe las fórmulas generales resultantes para las coordenadas del vértice y el foco en términos de los coeficientes $D, E$ y $F$.*
* *Una vez calculadas de forma analítica las coordenadas del Foco y la ecuación de la recta Directriz de tu ejercicio, explica detalladamente cómo aplicarías el axioma de distancia entre dos puntos para verificar con total certeza científica que tu gráfica cumple rigurosamente con la definición pura de una parábola en la UCA.*
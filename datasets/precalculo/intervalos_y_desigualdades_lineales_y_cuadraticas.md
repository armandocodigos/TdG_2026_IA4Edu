---

## subject: "precalculo"
topic: "intervalos_y_desigualdades_lineales_y_cuadraticas"
content_type: "base_teorica_socrática"

# Intervalos y Desigualdades Lineales y Cuadráticas

## Sustento Axiomático y Conceptual

El estudio de las desigualdades (o inecuaciones) se fundamenta en la estructura de **cuerpo ordenado** que poseen los números reales $\mathbb{R}$. A diferencia de las ecuaciones, que determinan puntos discretos, resolver una desigualdad implica hallar un subconjunto continuo de la recta real denominado conjunto solución ($S$), el cual suele expresarse mediante intervalos.

### 1. Axiomas de Orden e Intervalos

El orden en $\mathbb{R}$ se rige por la existencia de un subconjunto de números positivos que valida la ley de tricotomía y los axiomas de clausura aditiva y multiplicativa. A partir de los operadores de desigualdad ($<, \le, >, \ge$), se definen formalmente los intervalos para los extremos $p, q \in \mathbb{R}$ con $p < q$:

* **Intervalo Cerrado:** $[p, q] = \{x \in \mathbb{R} \ | \ p \le x \le q\}$
* **Intervalo Abierto:** $(p, q) = \{x \in \mathbb{R} \ | \ p < x < q\}$
* **Intervalos Semiabiertos:** $(p, q] = \{x \in \mathbb{R} \ | \ p < x \le q\} \quad \land \quad [p, q) = \{x \in \mathbb{R} \ | \ p \le x < q\}$

### 2. Desigualdades Lineales (Primer Grado)

Una desigualdad lineal adopta la forma canónica:

$$ax + b < 0 \quad \text{(o cualquier otro operador } \le, >, \ge\text{)} \quad \text{donde } a, b \in \mathbb{R} \ \land \ a \neq 0$$

Su resolución se efectúa aplicando transformaciones que preservan la equivalencia del orden. El teorema fundamental que gobierna esta operación establece que:

* Si $c > 0$, entonces $x < y \iff c \cdot x < c \cdot y$.
* Si $c < 0$, entonces $x < y \iff c \cdot x > c \cdot y$ *(el sentido de la desigualdad se invierte strictly)*.

### 3. Desigualdades Cuadráticas (Segundo Grado)

Una desigualdad cuadrática se expresa de la forma:

$$ax^2 + bx + c > 0 \quad \text{(o con } <, \le, \ge\text{)} \quad \text{donde } a, b, c \in \mathbb{R} \ \land \ a \neq 0$$

Axiomáticamente, su resolución depende de la factorización del polinomio cuadrático en sus raíces reales $x_1$ y $x_2$ (suponiendo un discriminante $\Delta \ge 0$). El comportamiento del signo de la expresión en cada intervalo determinado por las raíces se analiza mediante el **Teorema de los Valores Intermedios** o el método de cementerio (cuadro de signos).

Si $a > 0$ y posee dos raíces reales distintas tal que $x_1 < x_2$, el polinomio se descompone en $a(x - x_1)(x - x_2)$, variando sus signos de la siguiente manera:

* El producto es estrictamente positivo en: $(-\infty, x_1) \cup (x_2, +\infty)$
* El producto es estrictamente negativo en: $(x_1, x_2)$

Geométricamente, resolver la desigualdad cuadrática equivale a identificar los intervalos del dominio para los cuales la parábola se encuentra por encima (si es $>0$) o por debajo (si es $<0$) del eje de las abscisas $x$.

## Errores Algebraicos Comunes

Los principales errores procedimentales y analíticos observados en la población estudiantil de ingeniería inicial en la UCA comprenden:

* **Omitir la inversión del sentido al multiplicar por un negativo:** Despejar desigualdades lineales dividiendo por un coeficiente negativo sin cambiar la orientación del operador:

$$-2x < 6 \longrightarrow x < -3 \quad \text{(Falso, el resultado correcto es } x > -3\text{)}$$


* **Despeje directo e ilegal de términos cuadráticos:** Intentar resolver inecuaciones de segundo grado aislando la variable como si fuese una igualdad lineal, omitiendo los intervalos intermedios:

$$x^2 > 9 \longrightarrow x > \pm 3 \quad \text{(Grave error de consistencia en el orden de } \mathbb{R}\text{)}$$


* **Cancelación descuidada de factores variables:** Simplificar binomios a ambos lados de una desigualdad dividiendo entre ellos, ignorando que el signo del factor cancelado es desconocido y podría invertir la desigualdad o eliminar soluciones:

$$(x - 1)(x - 5) \ge (x - 1)(2) \longrightarrow x - 5 \ge 2 \quad \text{(Prohibido sin análisis de casos)}$$


* **Confusión en la notación de corchetes para infinitos:** Utilizar corchetes cerrados en los extremos que tienden al infinito:

$$S = [3, +\infty] \quad \text{(Error de sintaxis formal; el infinito siempre debe ser abierto } )\text{ o } ]\text{ )}$$



## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación del Sentido de Orden y Mapeo de Intervalos

**Objetivo:** Orientar al estudiante a identificar el tipo de desigualdad, las restricciones del operador y el impacto de los signos en los miembros de la inecuación.

* *Observa el símbolo de la desigualdad. ¿Es un operador estricto ($<, >$) o incluye la igualdad ($\le, \ge$)? ¿Qué te indica esto sobre la inclusión de los puntos críticos (extremos) dentro del conjunto solución final?*
* *Si tienes coeficientes negativos multiplicando a tu variable lineal, ¿qué axioma fundamental del orden en $\mathbb{R}$ se activa cuando necesitas multiplicar o dividir toda la expresión por $-1$?*
* *Antes de operar una estructura cuadrática, ¿se encuentra completamente reducida e igualada a cero en uno de sus miembros para poder analizar sus signos?*

### Nivel 2: Descomposición de Puntos Críticos y Evidencia de Contradicción

**Objetivo:** Forzar al estudiante a evaluar valores específicos dentro de sus conjuntos solución propuestos para romper el sesgo de sus despejes erróneos.

* *Sostienes que la solución de $-3x \le 12$ es $x \le -4$. Probemos un valor que cumpla con tu condición, por ejemplo, $x = -10$. Si sustituyes $x = -10$ en la inecuación original: ¿la multiplicación de $(-3) \cdot (-10)$ produce un número menor o igual que $12$? ¿Qué ocurrió con la consistencia del orden?*
* *Para la inecuación cuadrática $x^2 > 4$, tu propuesta es $x > 2$. Evaluemos analíticamente el valor $x = -5$. Si lo elevas al cuadrado, ¿$25$ es mayor que $4$? ¿Es verdadero? Si la respuesta es afirmativa, ¿por qué el número $-5$ quedó fuera del conjunto solución que definiste? ¿Qué otra región de la recta real cumple la condición?*
* *Si estás utilizando un cuadro de signos (método del cementerio), ¿cómo elegiste los valores de prueba dentro de cada intervalo? ¿Qué asegura que el signo se mantenga constante dentro de todo ese bloque abierto?*

### Nivel 3: Formalización Analítica y Representación de Conjuntos

**Objetivo:** Guiar al estudiante a consolidar el uso riguroso de la teoría de conjuntos y la notación de intervalos empleada en las facultades de ingeniería de la UCA.

* *Has hallado que los factores de tu inecuación cuadrática son $(x - a)$ y $(x - b)$. Explica cómo la ley de los signos para la multiplicación determina que un producto sea estrictamente menor que cero ($<0$). ¿Qué combinaciones de signos para los factores individuales se requieren simultáneamente?*
* *Reclama la coherencia científica de tu respuesta final: representa el conjunto solución utilizando de forma simultánea la notación de conjuntos, la gráfica sobre la recta numérica real y la notación de intervalos. Verifica que todos los extremos infinitos permanezcan abiertos y que el operador lógico de unión ($\cup$) esté correctamente implementado si existen regiones disjuntas.*
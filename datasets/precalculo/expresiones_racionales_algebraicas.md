---

## subject: "precalculo"
topic: "expresiones_racionales_algebraicas"
content_type: "base_teorica_socrática"

# Expresiones Racionales Algebraicas

## Sustento Axiomático y Conceptual

Una expresión racional algebraica representa el cociente formal de dos polinomios dentro del anillo $\mathbb{R}[x]$. Matemáticamente, constituye una extensión hacia el cuerpo de fracciones de los polinomios, de manera análoga a cómo los números racionales ($\mathbb{Q}$) extienden a los enteros ($\mathbb{Z}$).

Formalmente, una expresión racional se define como:

$$W(x) = \frac{P(x)}{Q(x)}$$

Donde $P(x), Q(x) \in \mathbb{R}[x]$. Debido a las restricciones elementales de los axiomas de campo en los números reales $\mathbb{R}$, la división por cero no está definida. Por lo tanto, el dominio de definición de $W(x)$ está restringido exclusivamente a los valores reales de $x$ que no anulan al polinomio denominador:

$$\text{Dom}(W) = \{x \in \mathbb{R} \ | \ Q(x) \neq 0\}$$

### Operaciones Fundamentales e Identidades de Campo

Las operaciones con expresiones racionales algebraicas heredan las propiedades operativas del campo fraccionario:

1. **Simplificación (Reducción a términos mínimos):** Se fundamenta en la propiedad del neutro multiplicativo. Si un factor lineal o irreducible $H(x)$ divide tanto al numerador como al denominador, este puede simplificarse bajo la condición estricta de excluir dichas raíces del dominio real:

$$\frac{P(x) \cdot H(x)}{Q(x) \cdot H(x)} = \frac{P(x)}{Q(x)} \quad \text{para } H(x) \neq 0$$


2. **Adición y Sustracción:** Requiere la homogeneización de los denominadores mediante la determinación del Mínimo Común Múltiplo ($mcm$) de los polinomios denominadores:

$$\frac{A(x)}{B(x)} \pm \frac{C(x)}{D(x)} = \frac{A(x) \cdot \left(\frac{mcm}{B(x)}\right) \pm C(x) \cdot \left(\frac{mcm}{D(x)}\right)}{mcm(B, D)}$$


3. **Multiplicación:** Producto directo de componentes polinomiales:

$$\frac{A(x)}{B(x)} \cdot \frac{C(x)}{D(x)} = \frac{A(x) \cdot C(x)}{B(x) \cdot D(x)}$$


4. **División:** Multiplicación por la expresión recíproca (inverso multiplicativo), añadiendo restricciones al dominio para los ceros de $C(x)$:

$$\frac{A(x)}{B(x)} \div \frac{C(x)}{D(x)} = \frac{A(x)}{B(x)} \cdot \frac{D(x)}{C(x)} = \frac{A(x) \cdot D(x)}{B(x) \cdot C(x)} \quad (C(x) \neq 0)$$



## Errores Algebraicos Comunes

Los sesgos y vicios algebraicos más frecuentes detectados en los estudiantes de ingeniería inicial de la UCA comprenden:

* **Cancelación ilegal de términos aditivos individuales:** Intentar simplificar monomios que forman parte de una suma o resta en lugar de simplificar factores comunes multiplicativos:

$$\frac{x^2 + 5}{x} \longrightarrow x + 5 \quad \text{(Falso, error estructural severo)}$$


* **Omitir las restricciones del dominio antes de simplificar:** Cancelar un factor común en el numerador y denominador sin declarar que el dominio original queda modificado permanentemente en ese punto singular (discontinuidad evitable o "hueco"):

$$f(x) = \frac{x(x-2)}{x-2} \longrightarrow f(x) = x \quad \text{(Omitiendo que } x \neq 2\text{)}$$


* **Suma directa de numeradores con denominadores distintos:** Operar expresiones fraccionarias sumando de forma lineal los numeradores y los denominadores entre sí, violando el axioma del $mcm$:

$$\frac{A}{B} + \frac{C}{D} = \frac{A + C}{B + D} \quad \text{(Falso)}$$


* **Inversión incorrecta de signos en binomios opuestos:** Confundir la factorización del signo negativo en binomios con inversión de orden, asumiendo erróneamente que $(x - 3)$ equivale de forma directa a $(3 - x)$ sin multiplicar por $-1$:

$$\frac{x - 3}{3 - x} = 1 \quad \text{(Falso, el resultado correcto es } -1\text{)}$$



## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Cognitiva y Análisis del Dominio Real

**Objetivo:** Guiar al estudiante a identificar las restricciones del denominador y promover la factorización completa antes de ejecutar cualquier operación o cancelación.

* *Antes de intentar simplificar o cancelar variables, observa detalladamente el denominador. ¿Para qué valores reales de $x$ la expresión matemática completa dejaría de existir o se volvería indeterminada?*
* *Examina tanto el polinomio superior como el inferior de forma independiente. ¿Qué métodos de factoreo (factor común, trinomios, diferencia de cuadrados) puedes aplicar en cada bloque para descomponerlos en sus factores mínimos irreducibles?*
* *Si una expresión presenta una división de fracciones, ¿cuál es la relación algebraica entre el operador de división y la multiplicación por el elemento inverso del divisor?*

### Nivel 2: Descomposición de Operadores y Evidencia del Error

**Objetivo:** Forzar al alumno a comprobar la invalidez de sus cancelaciones aditivas mediante la sustitución aritmética o la redistribución inversa de términos.

* *Supongamos que afirmas que en la expresión $\frac{x + 4}{4}$ es legal cancelar los números cuatro para obtener $x$. Evaluemos numéricamente para verificar la consistencia de tu hipótesis: si asignamos $x = 8$, ¿el valor de $\frac{8 + 4}{4}$ es igual a $8$? ¿Qué regla fundamental del álgebra se infringe cuando cancelas un sumando en lugar de un factor?*
* *Has simplificado el factor $(x - 5)$ de la fracción original. Si graficáramos la función original y la función simplificada, ¿se comportarían exactamente igual en el punto $x = 5$? ¿Cómo debes declarar analíticamente esta restricción de dominio en tu respuesta de ingeniería?*
* *Al restar las fracciones $\frac{A}{x-2} - \frac{B}{2-x}$, notas que los denominadores son casi idénticos salvo por el orden de sus términos. ¿Qué factor común numérico constante te permitiría invertir el binomio $(2-x)$ para homogeneizar el denominador común? ¿Cómo altera eso al signo de la operación central?*

### Nivel 3: Formalización y Consistencia Estructural en el $mcm$

**Objetivo:** Inducir al estudiante a estructurar correctamente el mínimo común múltiplo algebraico y validar de forma científica la solución final.

* *Si los denominadores de tus expresiones algebraicas racionales son $(x+1)^2$ y $(x+1)(x-3)$, ¿cómo construyes formalmente el mínimo común múltiplo ($mcm$)? ¿Debes incluir los factores comunes con su mayor o menor exponente, y qué ocurre con los factores no comunes?*
* *Una vez que has unificado la expresión en una sola fracción fraccionaria compleja, explica cómo la propiedad distributiva te ayuda a expandir y agrupar el numerador final. ¿Cómo puedes comprobar de manera científica que el polinomio resultante en el numerador no posee factores ocultos compartidos con el denominador?*
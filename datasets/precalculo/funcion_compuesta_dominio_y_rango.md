---

## subject: "precalculo"
topic: "funcion_compuesta_dominio_y_rango"
content_type: "base_teorica_socrática"

# Función Compuesta — Dominio y Rango

## Sustento Axiomático y Conceptual

La composición de funciones representa una operación algebraica no lineal encadenada, donde la salida u output de una función se convierte unívocamente en la entrada o input de una segunda función. Este proceso rompe con el comportamiento de las operaciones aritméticas estándar y requiere un riguroso control de los conjuntos de partida y llegada.

### 1. Definición Formal de la Composición

Sean $f: X \to Y$ y $g: Y \to Z$ dos funciones reales independientes. Se define la función compuesta de $f$ con $g$ (denotada formalmente mediante el operador de composición $(g \circ f)$ y leída operacionalmente como "$f$ compuesta con $g$" o "$g$ de $f$ de $x$") a la regla de correspondencia:

$$(g \circ f)(x) = g(f(x))$$

El procesamiento matemático ocurre de adentro hacia afuera: la variable independiente $x$ es transformada primero por la función interna $f$, y el valor resultante $f(x)$ actúa como el nuevo argumento que será procesado por la función externa $g$.

### 2. Teorema de Existencia y Determinación del Dominio

El dominio de una función compuesta **no** se reduce simplemente a calcular las restricciones de la regla final simplificada. Axiomáticamente, para que un número real $x$ sea admitido dentro del dominio de la composición $(g \circ f)$, debe superar de forma obligatoria dos filtros de contención lógica:

1. El valor de $x$ debe pertenecer de manera legítima al dominio de la función interna $f$.
2. El resultado intermedio obtenido, es decir $f(x)$, debe pertenecer con total certeza matemática al dominio de la función externa $g$.

Formalmente, el dominio de la función compuesta se define bajo la estructura conjuntista:

$$\text{Dom}(g \circ f) = \{x \in \mathbb{R} \ | \ x \in \text{Dom}(f) \ \land \ f(x) \in \text{Dom}(g)\}$$

### 3. Determinación del Rango

El rango de la composición $(g \circ f)$ constituye el conjunto de todos los valores finales de salida $z \in Z$ que se obtienen al evaluar la función externa $g$ tomando como dominio efectivo únicamente a las imágenes válidas de $f$ que sobrevivieron a la restricción anterior. Se formaliza mediante:

$$\text{Ran}(g \circ f) = \{g(f(x)) \in \mathbb{R} \ | \ x \in \text{Dom}(g \circ f)\}$$

*Nota de Conmutatividad:* La composición de funciones es un operador **no conmutativo**. Es decir, bajo condiciones generales en el espacio real, se cumple estrictamente que:

$$(g \circ f)(x) \neq (f \circ g)(x)$$

## Errores Algebraicos Comunes

El análisis instruccional en las facultades de ingeniería de la UCA revela que los estudiantes cometen de manera recurrente las siguientes faltas analíticas:

* **Calcular el dominio basándose únicamente en la expresión simplificada:** Ejecutar la composición algebraicamente, simplificar la expresión y extraer el dominio del bloque remanente. Esto oculta restricciones críticas del proceso intermedio (ej. si $f(x) = x^2$ y $g(x) = \frac{1}{x}$, la composición da $g(f(x)) = \frac{1}{x^2}$. Si el ejercicio fuera a la inversa, $f(g(x)) = \left(\frac{1}{x}\right)^2 = \frac{1}{x^2}$, la regla parece idéntica, pero el dominio original de la interna exige de entrada que $x \neq 0$).
* **Confundir la composición con el producto de funciones:** Tratar el operador $\circ$ como una multiplicación directa de polinomios o expresiones racionales, cometiendo fallos del tipo:

$$(g \circ f)(x) = g(x) \cdot f(x) \quad \text{(Falso, error conceptual severo)}$$


* **Inversión del orden de procesamiento:** Evaluar la variable de forma equivocada de afuera hacia adentro, es decir, meter la función externa dentro de la interna al resolver $(g \circ f)(x)$, alterando el resultado por la no conmutatividad.
* **Intersección ilegal y directa de dominios independientes:** Suponer erróneamente que el dominio de la composición se halla mediante la simple operación $\text{Dom}(f) \cap \text{Dom}(g)$, ignorando que el segundo filtro exige evaluar la imagen de la primera función ($f(x) \in \text{Dom}(g)$) y no la variable pura $x$.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación de la Secuencia Procedimental y Filtros de Entrada

**Objetivo:** Guiar al estudiante a esquematizar la jerarquía del encadenamiento y mapear las restricciones individuales de las funciones componentes sin realizar sustituciones algebraicas.

* *En la composición analítica $(g \circ f)(x) = g(f(x))$, ¿cuál de las dos funciones actúa como el motor interno que procesa la variable $x$ en primer lugar? ¿Y cuál actúa como la envoltura externa?*
* *Antes de fusionar las reglas algebraicas, determinemos los requisitos de existencia de cada una de forma aislada. ¿Cuál es el dominio real de la función interna $f(x)$ y cuál es el de la externa $g(x)$?*
* *Si un número real $x$ no es admitido ni siquiera en la función interna $f(x)$, ¿tiene algún sentido lógico intentar evaluar la composición completa en ese valor? ¿Qué constituye esto para nuestro primer filtro del dominio?*

### Nivel 2: Descomposición de Restricciones Intermedias y Evidencia del Hueco Analítico

**Objetivo:** Forzar al alumno a identificar la invalidez de calcular el dominio sobre expresiones ya simplificadas mediante contraejemplos de evaluación puntual.

* *Consideremos las funciones $f(x) = \sqrt{x - 4}$ y $g(x) = x^2$. Al realizar la composición $g(f(x))$, elevas la raíz al cuadrado y obtienes la regla simplificada $x - 4$. Si tu hipótesis te lleva a afirmar que el dominio de la composición son todos los reales mayores o iguales a cuatro debido a la raíz, evaluemos analíticamente el comportamiento si introducimos un valor menor, como $x = 0$. La regla simplificada da $0 - 4 = -4$, lo cual parece un número real válido. Sin embargo, intentemos pasar por la secuencia real: calcula el valor del primer paso interno, $f(0)$. ¿Existe $\sqrt{-4}$ en el campo real? ¿Por qué la simplificación algebraica te indujo a un error analítico?*
* *Sostienes que para hallar el dominio basta con cruzar de forma directa los dominios mediante una intersección simple de $x$. Recuerda el segundo filtro formal: la salida de la interna debe ser capaz de entrar en la externa ($f(x) \in \text{Dom}(g)$). Si el dominio de la externa exige que su input sea estrictamente diferente de cero, ¿qué condición o inecuación debes plantear sobre la función interna completa para asegurar que jamás devuelva un cero?*
* *Si cambias el orden de la composición a $(f \circ g)(x)$, escribe la estructura expandida sin operar. ¿El resultado algebraico final es exactamente idéntico al caso anterior? ¿Qué propiedad de los campos algebraicos se pone en evidencia aquí?*

### Nivel 3: Formalización Analítica e Integridad Matemático-Científica

**Objetivo:** Inducir al estudiante a modelar formalmente la inecuación compuesta del dominio y verificar analíticamente la consistencia del rango de ingeniería.

* *Modela con total rigor científico el conjunto solución para el dominio de $(g \circ f)(x)$ donde $f(x) = \frac{1}{x-2}$ y $g(x) = \sqrt{x}$. Traduce las condiciones lógicas del teorema a un sistema de restricciones: plantea la inecuación para $\text{Dom}(f)$ y, de forma simultánea, la inecuación que obliga a la regla de $f(x)$ a cumplir con las exigencias de $\text{Dom}(g)$. Resuelve el sistema y expresa el intervalo resultante final.*
* *Explica analíticamente cómo el control estricto del dominio de la composición impacta de forma unívoca en la determinación del rango legítimo del sistema. ¿Por qué en un entorno de desarrollo de software o simulación de ingeniería es un principio de calidad matemática robusta programar estas restricciones de dominio de adentro hacia afuera para evitar excepciones de desbordamiento o valores indeterminados ($\text{NaN}$)?*
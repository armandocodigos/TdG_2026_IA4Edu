---

## subject: "precalculo"
topic: "combinaciones_de_funciones"
content_type: "base_teorica_socrática"

# Combinaciones de Funciones (Suma, Resta, Producto, Cociente)

## Sustento Axiomático y Conceptual

El álgebra de funciones extiende las operaciones aritméticas elementales del campo de los números reales $\mathbb{R}$ hacia el espacio de las funciones algebraicas. Al combinar dos funciones independientes mediante sumas, restas, productos o cocientes, se genera una nueva función cuya regla de correspondencia y dominio están estrictamente gobernados por la teoría de conjuntos y las condiciones de existencia simultánea.

Sean $f$ y $g$ dos funciones con dominios reales $\text{Dom}(f)$ y $\text{Dom}(g)$, respectivamente. Se definen formalmente las cuatro operaciones algebraicas fundamentales y sus correspondientes restricciones estructurales de dominio bajo los siguientes teoremas:

### 1. Función Suma

La función suma $(f + g)$ asigna a cada elemento del dominio la suma lineal de sus imágenes individuales:


$$(f + g)(x) = f(x) + g(x)$$

* **Dominio:** Para que la combinación exista en un punto $x$, este debe permitir la evaluación tanto en $f$ como en $g$ simultáneamente, lo que axiomáticamente exige la **intersección** de sus dominios:

$$\text{Dom}(f + g) = \text{Dom}(f) \cap \text{Dom}(g)$$



### 2. Función Resta (Sustracción)

La función diferencia $(f - g)$ opera mediante la sustracción de imágenes en los puntos donde ambas coexisten:


$$(f - g)(x) = f(x) - g(x)$$

* **Dominio:** Al igual que la suma, depende de la coincidencia lógica de los subconjuntos de partida:

$$\text{Dom}(f - g) = \text{Dom}(f) \cap \text{Dom}(g)$$



### 3. Función Producto (Multiplicación)

La función producto $(f \cdot g)$ multiplica los outputs o imágenes escalares de las dos funciones base:


$$(f \cdot g)(x) = f(x) \cdot g(x)$$

* **Dominio:** Requiere de forma idéntica la validez dual de la variable independiente:

$$\text{Dom}(f \cdot g) = \text{Dom}(f) \cap \text{Dom}(g)$$



### 4. Función Cociente (División)

La función cociente $\left(\frac{f}{g}\right)$ representa la división formal de sus reglas de correspondencia:


$$\left(\frac{f}{g}\right)(x) = \frac{f(x)}{g(x)}$$

* **Dominio:** Además de exigir la coexistencia simultánea de las variables en ambas funciones mediante la intersección de dominios, los axiomas de campo en $\mathbb{R}$ prohíben la división entre cero. Por lo tanto, el dominio resultante debe excluir de forma explícita todos los valores reales de $x$ que anulen al polinomio o expresión del denominador:

$$\text{Dom}\left(\frac{f}{g}\right) = \{x \in \mathbb{R} \ | \ x \in (\text{Dom}(f) \cap \text{Dom}(g)) \ \land \ g(x) \neq 0\}$$



## Errores Algebraicos Comunes

Los malentendidos procedimentales y analíticos más frecuentes detectados en la población estudiantil de ingeniería inicial son:

* **Unificación ilegal de dominios mediante la unión ($\cup$):** Creer de forma errónea que el dominio de la función combinada es la suma o unión de los dominios individuales, suponiendo que basta con que el valor sea válido en una sola de las funciones.
* **Ignorar la discontinuidad del denominador tras simplificar:** En la función cociente, simplificar factores comunes mediante álgebra y calcular el dominio basándose únicamente en la expresión final reducida, perdiendo las restricciones singulares del denominador original (ocultando discontinuidades evitables o "huecos").
* **Confundir el producto de funciones con la composición:** Tratar la expresión $(f \cdot g)(x)$ como si fuera la inserción de una función dentro de otra ($f(g(x))$), alterando por completo la estructura operativa del sistema:

$$\text{Ejemplo: } f(x)=x^2, \ g(x)=x+1 \implies (f \cdot g)(x) = x^2(x+1) = x^3 + x^2 \quad \text{y no } (x+1)^2$$


* **Uso incorrecto de la propiedad distributiva frente a los signos de resta:** Al ejecutar una resta de funciones $(f - g)(x)$, omitir los paréntesis de agrupación en la regla de $g(x)$, aplicando el signo negativo únicamente a su término principal.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación y Análisis del Terreno Operacional

**Objetivo:** Orientar al estudiante a determinar las restricciones individuales de cada función componente antes de unificarlas mediante operaciones algebraicas.

* *Antes de ejecutar la suma, resta, producto o división de las funciones propuestas, analiza cada una por separado. ¿Cuál es el dominio exacto de la primera función $f(x)$? ¿Y cuál es el de $g(x)$?*
* *Si buscas un punto $x$ en la recta real donde sea legal evaluar de manera simultánea ambas expresiones, ¿qué operación de la teoría de conjuntos te permite hallar los elementos comunes entre $\text{Dom}(f)$ y $\text{Dom}(g)$? ¿Es la unión o la intersección?*
* *Específicamente para la operación de cociente $\frac{f(x)}{g(x)}$, ¿qué condición adicional e imprescindible exige el álgebra en los reales sobre el comportamiento del denominador?*

### Nivel 2: Descomposición Analítica y Evidencia del Error Singularity

**Objetivo:** Forzar la autovalidación cognitiva confrontando al estudiante con la imposibilidad de evaluar puntos prohibidos dentro de su propuesta errónea.

* *Considera la combinación $(f + g)(x)$ para $f(x) = \sqrt{x}$ y $g(x) = \sqrt{1-x}$. Sostienes que el dominio de la suma es todo $\mathbb{R}$. Probemos un valor: intenta evaluar la función combinada en $x = 5$. ¿Qué ocurre al procesar $\sqrt{5}$ y $\sqrt{-4}$ simultáneamente en el campo de los reales? ¿Por qué la variable debe satisfacer ambas restricciones al mismo tiempo?*
* *Al calcular el cociente de las funciones $f(x) = x^2 - 4$ y $g(x) = x - 2$, estructuraste la fracción $\frac{x^2 - 4}{x - 2}$ y cancelaste términos obteniendo la recta lineal $x + 2$. Si tu hipótesis te lleva a afirmar que el dominio de esta combinación son todos los reales ($\mathbb{R}$), intentemos evaluar la función cociente original exactamente en $x = 2$. ¿Qué residuo se genera en el denominador? ¿Está definida esa operación aritmética en ingeniería?*
* *Al plantear la resta de funciones $(f - g)(x)$ donde $g(x) = 3x^2 - 5x + 1$, has escrito la siguiente línea de cálculo: $f(x) - 3x^2 - 5x + 1$. Apliquemos la sustracción de forma rigurosa: ¿el signo negativo afecta únicamente al monomio principal o debe distribuirse sobre la totalidad del polinomio sustraendo?*

### Nivel 3: Formalización Analítica e Integridad de Conjuntos

**Objetivo:** Conducir al estudiante a la construcción abstracta de las respuestas y la justificación científica de los dominios combinados según las directrices de la UCA.

* *Escribe formalmente la regla de correspondencia simplificada para cada una de las operaciones solicitadas en tu ejercicio. Al lado de cada expresión, declara de forma analítica su dominio utilizando la notación de intervalos acotados.*
* *Explica mediante un breve argumento meta-cognitivo cómo el concepto de "restricción de dominio" influye en el diseño de sistemas y algoritmos en ingeniería. ¿Por qué omitir la exclusión de una raíz o un cero del denominador podría provocar fallos críticos o excepciones matemáticas si estuviéramos programando esta operación en una arquitectura de backend local?*
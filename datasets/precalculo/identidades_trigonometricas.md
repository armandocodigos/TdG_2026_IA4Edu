---

## subject: "precalculo"
topic: "identidades_trigonometricas"
content_type: "base_teorica_socrática"

# Identidades Trigonométricas

## Sustento Axiomático y Conceptual

Una identidad trigonométrica es una igualdad algebraica establecida entre funciones trigonométricas que resulta estrictamente verdadera para **todo** valor de la variable angular (input $\theta \in \mathbb{R}$) donde las funciones se encuentren legítimamente definidas. Su formalización geométrica se deduce a partir de las coordenadas de un punto móvil $P(x,y)$ sobre la circunferencia unitaria o trigonométrica, la cual posee un radio constante $r = 1$.

Axiomáticamente, en el círculo unitario se definen las funciones fundamentales asociadas al ángulo central $\theta$ mediante las proyecciones ortogonales:

$$x = \cos(\theta) \quad \land \quad y = \sin(\theta)$$

A partir de este marco geométrico, las identidades se clasifican axiomáticamente en los siguientes teoremas de composición:

### 1. Identidades Pitagóricas

Derivadas directamente de aplicar la geometría euclidiana y el Teorema de Pitágoras sobre el triángulo rectángulo elemental inscrito en la circunferencia ($x^2 + y^2 = r^2$):

$$\sin^2(\theta) + \cos^2(\theta) = 1$$

Si se divide uniformemente esta identidad fundamental entre $\cos^2(\theta)$ o $\sin^2(\theta)$ (bajo condiciones de existencia donde los denominadores sean no nulos), se deducen analíticamente las identidades pitagóricas complementarias:

$$1 + \tan^2(\theta) = \sec^2(\theta) \quad \left(\theta \neq \frac{\pi}{2} + k\pi, \ k \in \mathbb{Z}\right)$$

$$1 + \cot^2(\theta) = \csc^2(\theta) \quad (\theta \neq k\pi, \ k \in \mathbb{Z})$$

### 2. Identidades Recíprocas y de Cociente

Establecidas a través del álgebra de fracciones algebraicas sobre las definiciones base de las razones trigonométricas:

* **De cociente:** 
$$\tan(\theta) = \frac{\sin(\theta)}{\cos(\theta)} \quad \land \quad \cot(\theta) = \frac{\cos(\theta)}{\sin(\theta)}$$


* **Recíprocas (Inversos multiplicativos):** 
$$\csc(\theta) = \frac{1}{\sin(\theta)}, \quad \sec(\theta) = \frac{1}{\cos(\theta)}, \quad \cot(\theta) = \frac{1}{\tan(\theta)}$$



### 3. Identidades de Suma y Diferencia de Ángulos

Teoremas geométricos fundamentales que gobiernan la rotación de vectores y la composición lineal de frecuencias en ingeniería:

$$\sin(\alpha \pm \beta) = \sin(\alpha)\cos(\beta) \pm \cos(\alpha)\sin(\beta)$$

$$\cos(\alpha \pm \beta) = \cos(\alpha)\cos(\beta) \mp \sin(\alpha)\sin(\beta)$$

A partir de estas estructuras de adición, haciendo el supuesto analítico de simetría angular $\alpha = \beta = \theta$, se deducen de forma unívoca las fórmulas de **Ángulo Doble**:

$$\sin(2\theta) = 2\sin(\theta)\cos(\theta)$$

$$\cos(2\theta) = \cos^2(\theta) - \sin^2(\theta) = 2\cos^2(\theta) - 1 = 1 - 2\sin^2(\theta)$$

## Errores Algebraicos Comunes

El análisis instruccional y de rendimiento en los cursos de pre-cálculo e ingeniería inicial en la UCA revela la persistencia de las siguientes aberraciones procedimentales:

* **Linealización ilegal de los operadores trigonométricos (Falsa propiedad distributiva):** Intentar tratar a la función trigonométrica como un factor multiplicativo distribuible sobre la adición angular:

$$\sin(\alpha + \beta) = \sin(\alpha) + \sin(\beta) \quad \text{(Falso, violación severa de la geometría no lineal)}$$


* **Mal manejo sintáctico de la potencia de un operador:** Confundir la elevación al cuadrado de la función completa con la potencia del argumento angular, asumiendo erróneamente equivalencia entre:

$$\sin^2(\theta) \quad \text{y} \quad \sin(\theta^2) \implies \text{Ejemplo: } [\sin(\pi)]^2 \neq \sin(\pi^2)$$


* **Cancelación ilegal de variables angulares dentro del argumento:** Intentar simplificar términos en fracciones cancelando variables de empaque interno con monomios externos, destruyendo la integridad de la función:

$$\frac{\sin(2x)}{x} \longrightarrow \sin(2) \quad \text{(Error conceptual fatal)}$$


* **Omisión de restricciones de discontinuidad al demostrar identidades:** Cancelar factores como $\cos(\theta)$ en denominadores complejos sin declarar de forma explícita que la validez del modelo matemático resultante excluye a todas las asíntotas verticales del operador tangente o secante.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Canónica y Mapeo de Destinos

**Objetivo:** Guiar al estudiante a identificar las funciones involucradas y plantear una estrategia de simplificación unificando variables hacia senos y cosenos sin alterar el flujo analítico.

* *Observa minuciosamente ambos miembros de la igualdad que buscas demostrar. ¿Cuál de los dos lados presenta la estructura algebraica más compleja o con mayor cantidad de operadores no fundamentales (como $\tan$, $\sec$, $\csc$)? ¿Por cuál miembro convendría iniciar el desarrollo analítico?*
* *Si reescribes todos los operadores especiales del término seleccionado utilizando de forma estricta sus equivalencias fraccionarias de cociente y recíprocas, ¿qué funciones base (senos y cosenos) unificarían el plano completo de la expresión?*
* *Examina los argumentos angulares. ¿Son todos homogéneos (ej. variable única $\theta$) o detectas la presencia de múltiplos como un ángulo doble ($2\theta$)? Si hay multiplicidad, ¿qué teorema permite reducir el orden del argumento?*

### Nivel 2: Descomposición de Operadores y Quiebre de Linealidad

**Objetivo:** Forzar la autovalidación cognitiva confrontando al estudiante con las consecuencias numéricas de aplicar una linealización ilegal mediante evaluación de ángulos notables.

* *Sostienes que para la expresión $\cos(\alpha - \beta)$ basta con distribuir el operador obteniendo $\cos(\alpha) - \cos(\beta)$. Evaluemos analíticamente utilizando ángulos notables de la ingeniería: asignemos $\alpha = \frac{\pi}{2}$ ($90^\circ$) y $\beta = 0$ ($0^\circ$). El miembro izquierdo exige calcular $\cos\left(\frac{\pi}{2} - 0\right) = \cos\left(\frac{\pi}{2}\right) = 0$. Ahora calcula el miembro derecho con tu propuesta: $\cos\left(\frac{\pi}{2}\right) - \cos(0) = 0 - 1 = -1$. ¿Coincide el residuo geométrico $0$ con tu resultado $-1$? ¿Qué nos demuestra este quiebre numérico sobre distribuir funciones trigonométricas?*
* *Durante la simplificación de una fracción con el término central $\sin^2(\theta)$, decidiste sustituirlo por $1 - \cos(\theta)$ omitiendo la potencia. Apliquemos rigurosamente el teorema pitagórico: si despejas la función cuadrática de la igualdad $\sin^2(\theta) + \cos^2(\theta) = 1$, ¿el término remanente queda libre de potencias o conserva una estructura cuadrática?*
* *Al enfrentarte a la suma de fracciones $\frac{1}{\sin(\theta)} + \frac{1}{\cos(\theta)}$, intentas operar sumando directamente los numeradores y los denominadores. Recuerda las reglas algebraicas del campo racional: ¿cómo se ejecuta formalmente la adición de fracciones heterogéneas utilizando el mínimo común múltiplo multiplicativo?*

### Nivel 3: Formalización Analítica y Demostración Rigurosa de Ingeniería

**Objetivo:** Inducir al estudiante a estructurar formalmente el proceso deductivo en una sola dirección lineal, validando la equivalencia científica de la identidad.

* *Explica analíticamente por qué al demostrar una identidad matemática en ingeniería inicial está estrictamente prohibido realizar un "despeje cruzado" trasladando términos de un miembro al otro a través del signo igual. ¿Cómo garantiza el método de reducción unidireccional (partir de un lado $A$ y llegar analíticamente al lado $B$) que estás frente a una demostración científica deductiva e incontestable?*
* *Modela con total rigor analítico la demostración de la expresión $\frac{\sin(2\theta)}{1 + \cos(2\theta)} = \tan(\theta)$. Desarrolla el miembro izquierdo sustituyendo las identidades de ángulo doble exactas. ¿Qué factor de cancelación común se genera en el numerador y denominador que valide de forma unívoca la correspondencia con la función tangente? Justifica meta-cognitivamente tus pasos basados en los axiomas de campo.*
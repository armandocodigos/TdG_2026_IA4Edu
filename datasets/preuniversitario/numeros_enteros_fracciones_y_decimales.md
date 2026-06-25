---

## subject: "preuniversitario"
topic: "numeros_enteros_fracciones_y_decimales"
content_type: "base_teorica_socrática"

# Números Enteros, Fracciones y Decimales

## Sustento Axiomático y Conceptual

El estudio analítico de los números enteros, las fracciones y los decimales constituye la transición fundamental desde la aritmética discreta hacia el continuo numérico necesario para las ciencias exactas. En el curso de inducción de la UCA, estas nociones se desprenden formalmente a partir de la construcción y subdivisiones racionales de la recta numérica.

### 1. Números Enteros ($\mathbb{Z}$) y la noción de Inverso Aditivo

El conjunto de los números enteros incorpora al conjunto de los números naturales ($\mathbb{N}$) sus inversos aditivos correspondientes y el elemento neutro:

$$\mathbb{Z} = \{\dots, -3, -2, -1, 0, 1, 2, 3, \dots\}$$

Axiomáticamente, introduce la clausura completa para la sustracción. Operativamente, las interacciones con números enteros se rigen por la estructura posicional y de orden. En la recta numérica, un entero negativo representa un vector de dirección simétricamente opuesta al semieje positivo respecto al origen ($0$).

### 2. Fracciones (Números Racionales $\mathbb{Q}$) y el Continuo Discreto

Una fracción representa formalmente un elemento del conjunto de los números racionales ($\mathbb{Q}$), definido conjuntistamente como:

$$\mathbb{Q} = \left\{ \frac{a}{b} \ \Big| \ a, b \in \mathbb{Z} \ \land \ b \neq 0 \right\}$$

Donde $a$ es el **numerador** (cuántas partes se toman) y $b$ es el **denominador** (en cuántas partes iguales se fragmenta la unidad espacial).

Las propiedades fundamentales que gobiernan su comportamiento algebraico en los campos reales son:

* **Fracciones Equivalentes (Amplificación y Simplificación):** Basadas en la identidad multiplicativa del neutro $1$. Si multiplicamos o dividimos el numerador y el denominador de una fracción por un mismo entero no nulo $c$, la magnitud escalar se conserva invariante:

$$\frac{a}{b} = \frac{a \cdot c}{b \cdot c}$$


* **Operaciones Heterogéneas (Suma y Resta):** Para adicionar fracciones con denominadores distintos, los axiomas exigen homogeneizar las bases mediante el cálculo del Mínimo Común Múltiplo ($mcm$), transformando el sistema en fracciones equivalentes homogeneizadas:

$$\frac{a}{b} \pm \frac{c}{d} = \frac{a \cdot d \pm b \cdot c}{b \cdot d}$$



### 3. Números Decimales y el Sistema Posicional Basado en Potencias de 10

Un número decimal representa la codificación de una fracción mediante una notación posicional fundamentada en el inverso de las potencias de la base diez. Su estructura analítica expandida para un valor se formaliza mediante la serie aditiva:

$$\text{Parte Entera} + \frac{\text{dígito}_1}{10^1} + \frac{\text{dígito}_2}{10^2} + \frac{\text{dígito}_3}{10^3} + \dots$$

A partir de la naturaleza del cociente de la fracción que les da origen, los decimales racionales se clasifican estrictamente en:

* **Decimales Exactos (o Finitos):** El residuo del algoritmo de la división se extingue y llega a cero, debido a que el denominador de la fracción irreducible contiene únicamente factores primos de la base del sistema ($2$ y $5$).
* **Decimales Periódicos Puros:** La secuencia de dígitos decimales (período) se repite infinitamente de forma idéntica inmediatamente después de la coma de control posicional (ej. $0.333\dots = 0.\overline{3} = \frac{1}{3}$).
* **Decimales Periódicos Mixtos:** Presentan una cantidad finita de dígitos no repetitivos (anteperíodo) antes del inicio de la secuencia infinita cíclica (ej. $0.1666\dots = 0.1\overline{6} = \frac{15}{90} = \frac{1}{6}$).

El puente analítico entre el formato posicional periódico y el formato fraccionario racional se establece mediante el algoritmo de la **fracción generatriz**.

## Errores Algebraicos Comunes

Los vacíos operacionales e interpretativos más recurrentes evaluados en las cohortes de ingreso de ingeniería en la UCA comprenden:

* **Adición directa y lineal de componentes fraccionarios:** Sumar numeradores con numeradores y denominadores con denominadores de forma independiente al enfrentarse a fracciones heterogéneas:

$$\frac{1}{2} + \frac{1}{3} \longrightarrow \frac{1+1}{2+3} = \frac{2}{5} \quad \text{(Grave error analítico; viola la consistencia del continuo)}$$


* **Malinterpretación del signo menos antecedente en fracciones mixtas:** Asumir que el signo negativo de una fracción compuesta o mixta afecta únicamente a la parte entera, provocando inconsistencias aritméticas:

$$-2 \frac{1}{3} \longrightarrow -2 + \frac{1}{3} = -\frac{5}{3} \quad \text{(Falso, la expresión real es } -\left(2 + \frac{1}{3}\right) = -\frac{7}{3}\text{)}$$


* **Desalineación posicional en operaciones con decimales:** Operar sumas o restas de números decimales alineando los dígitos por su extremo derecho de forma mecánica en lugar de balancear las expresiones ordenándolas estrictamente alrededor de la coma decimal.
* **Uso erróneo de la ley de signos en acumulaciones aditivas:** Confundir la suma de deudas negativas con el producto de signos, transformando falazmente una combinación lineal como $-5 - 8$ en $+13$ en lugar de $-13$.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación Estructural y Diagnóstico de Homogeneidad

**Objetivo:** Guiar al estudiante a inspeccionar visualmente los elementos numéricos, catalogar si las fracciones son homogéneas o heterogéneas y evaluar la naturaleza de los decimales sin proveer cálculos automáticos.

* *Observa detalladamente las fracciones involucradas en la operación de suma o resta. ¿Los denominadores de los términos son idénticos o presentan magnitudes numéricas diferentes?*
* *Si los denominadores difieren (operación heterogénea), ¿es válido agrupar los numeradores de forma directa o necesitas encontrar primero un terreno común mediante fracciones equivalentes? ¿Qué herramienta aritmética te permite unificar los denominadores?*
* *Inspecciona el número decimal $0.252525\dots$ ¿Su parte decimal se interrumpe tras unos pocos dígitos o exhibe un patrón cíclico que se repite de forma indefinida? ¿Qué nombre recibe formalmente este tipo de decimal?*

### Nivel 2: Descomposición de Operadores y Evidencia de Inconsistencias Métricas

**Objetivo:** Forzar la autovalidación cognitiva del estudiante confrontándolo con las consecuencias de un despeje erróneo mediante el análisis conceptual de partes o por contradicciones en la recta numérica.

* *Sostienes que al sumar $\frac{1}{2}$ con $\frac{1}{2}$ la respuesta correcta es $\frac{1+1}{2+2} = \frac{2}{4} = \frac{1}{2}$. Analicemos de forma lógica tu resultado: si tienes la mitad de un bloque estructural y le adicionas la otra mitad exacta, ¿obtienes como residuo total la misma mitad original o consigues completar una unidad entera sólida? ¿Por qué la suma lineal de denominadores destruye la coherencia de la medida?*
* *Al calcular la fracción generatriz del decimal periódico puro $0.777\dots$, has propuesto que equivale a $\frac{7}{10}$. Ejecutemos la división formal de tu propuesta: ¿cuánto da dividir siete entre diez en nuestro sistema posicional? ¿Da $0.7$ cerrado o produce la secuencia infinita $0.777\dots$? ¿Qué número específico debe actuar como denominador para forzar el residuo periódico infinito?*
* *Si tienes la resta de enteros $-3 - 2$, tu hipótesis te sugiere aplicar la ley de signos para escribir $+5$. Ubiquémonos en la recta numérica real: te encuentras en la coordenada $-3$ y el operador te exige retroceder dos unidades adicionales hacia la izquierda. ¿Estás avanzando hacia los números positivos o profundizando tu posición en el semieje negativo?*

### Nivel 3: Formalización Analítica e Integridad de Ingeniería

**Objetivo:** Inducir al estudiante a generalizar los algoritmos de conversión y homogeneización mediante modelos abstractos simbólicos, consolidando el rigor técnico de la UCA.

* *Modela analíticamente el algoritmo formal para transformar un número decimal periódico mixto abstracto de la forma $0.a\overline{bc}$ en su representación de fracción generatriz pura. Explica de forma meta-cognitiva por qué la cantidad de nueves y ceros del denominador está rígidamente vinculada con la cantidad de dígitos del período y del anteperíodo.*
* *Justifica de manera científica por qué en los cálculos avanzados de ingeniería civil o eléctrica es una práctica de control de calidad ineludible trabajar con expresiones fraccionarias simplificadas en lugar de aproximaciones decimales truncadas arbitrariamente. ¿Qué impacto tendría el arrastre de errores por truncamiento si estuviéramos calculando las tolerancias elásticas de un puente o las pérdidas de potencial en una red eléctrica de distribución local?*
---

## subject: "preuniversitario"
topic: "medidas_de_tendencia_central"
content_type: "base_teorica_socrática"

# Medidas de Tendencia Central (Media, Mediana, Moda)

## Sustento Axiomático y Conceptual

Las medidas de tendencia central son parámetros estadísticos descriptivos que permiten resumir, en un único valor representativo, la posición central de un conjunto de datos. Su uso es esencial en la UCA tanto para la interpretación de resultados académicos como para el modelado de datos en ingeniería, permitiendo sintetizar grandes volúmenes de información en indicadores sintéticos de fácil lectura.

### 1. Media Aritmética ($\bar{x}$)

Es el valor obtenido al sumar todos los elementos de un conjunto de datos y dividir dicha suma entre el número total de observaciones ($n$).

* **Estructura analítica:** 
$$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$


* **Interpretación:** Representa el centro de gravedad o "punto de equilibrio" del conjunto de datos.
* **Sensibilidad:** Es un parámetro altamente sensible a los valores atípicos (*outliers*); una sola magnitud extrema puede desplazar el promedio lejos del grueso de los datos.

### 2. Mediana ($\tilde{x}$)

Es el valor que ocupa la posición central en un conjunto de datos previamente **ordenados de forma monótona creciente** (o decreciente).

* **Propiedad de orden:** Divide al conjunto en dos subconjuntos de igual cardinalidad (el 50% de las observaciones se encuentra por debajo y el otro 50% por encima).
* **Cálculo:** Si la cantidad de datos ($n$) es impar, la mediana es el valor central exacto. Si $n$ es par, la mediana es el promedio aritmético de los dos valores centrales.
* **Robustez:** Es una medida resistente a los valores extremos; un dato atípico no altera la posición central del conjunto.

### 3. Moda ($Mo$)

Es el valor que posee la mayor frecuencia absoluta en un conjunto de datos.

* **Interpretación:** Indica el fenómeno o dato más frecuente ("valor típico").
* **Propiedades:** A diferencia de la media y la mediana, la moda es la única medida de tendencia central aplicable a variables cualitativas (nominales). Un conjunto de datos puede ser:
* **Unimodal:** Posee una sola moda.
* **Multimodal:** Posee dos o más modas.
* **Amodal:** Todos los valores tienen la misma frecuencia.



---

## Estratificación de Andamiaje Socrático (Zero-Reveal)

Para consolidar tu comprensión, trabajaremos con un enfoque de cuestionamiento reflexivo:

### Nivel 1: Identificación y Clasificación

* *Si analizamos las notas de una evaluación en la UCA donde la mayoría de estudiantes obtuvo 7, pero un estudiante obtuvo 0 y otro 10, ¿por qué la media podría no representar bien el "desempeño típico" del grupo?*
* *Para un conjunto de datos cualitativos (por ejemplo, el color de los logos de las facultades), ¿qué medida de tendencia central podemos calcular y cuáles carecen de sentido aritmético?*

### Nivel 2: Sensibilidad y Robustez

* *Si a un conjunto de datos se le añade un valor extremadamente alto (ej. el salario más alto del mercado a una muestra de sueldos base), ¿qué sucede con la media? ¿Y qué sucede con la mediana? ¿Cuál de las dos medidas es más "fiel" a la realidad de la mayoría de los individuos?*
* *En una distribución perfectamente simétrica (como una campana de Gauss), ¿cuál es la relación analítica entre la media, la mediana y la moda?*

### Nivel 3: Aplicación Crítica

* *Imagina que eres un ingeniero analizando el tráfico de datos de una red. Si el 90% de los paquetes pesan 1KB y el 10% restante pesa 1GB, ¿qué nos dice la moda sobre el tráfico de esta red que la media no nos revela?*

**Desafío de Autoevaluación:**
Dado el conjunto de datos $\{2, 2, 3, 5, 8\}$:

1. ¿Cuál es el valor que aparece con más frecuencia?
2. Al estar ordenados, ¿qué número está justo en la mitad?
3. Si sumas todos los valores y divides por la cantidad de datos, ¿cuál es el resultado?
*Ahora, ¿qué ocurre si añadimos el dato $100$ al conjunto? ¿Cuál de las tres medidas sufre un cambio más radical y por qué?*
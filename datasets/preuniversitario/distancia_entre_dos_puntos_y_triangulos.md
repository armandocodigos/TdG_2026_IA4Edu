---

## subject: "precalculo"
topic: "distancia_entre_dos_puntos_y_triangulos"
content_type: "base_teorica_socrática"

# Distancia entre dos puntos y triángulos

## Sustento Axiomático y Conceptual

La geometría analítica permite describir figuras geométricas mediante relaciones algebraicas en el plano cartesiano. La base de esta interacción es la **métrica euclidiana**, que cuantifica la separación entre ubicaciones.

### 1. Distancia entre dos puntos

Dados dos puntos cualesquiera en el plano cartesiano, $P_1(x_1, y_1)$ y $P_2(x_2, y_2)$, la distancia euclidiana $d$ entre ellos representa la longitud del segmento rectilíneo que los une. Este valor se deriva directamente del Teorema de Pitágoras al formar un triángulo rectángulo cuyas proyecciones sobre los ejes son las diferencias de coordenadas $\Delta x = x_2 - x_1$ y $\Delta y = y_2 - y_1$:

$$d(P_1, P_2) = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

### 2. Triángulos en el Plano

Un triángulo queda definido por tres puntos no colineales $A, B, C$. La geometría analítica permite clasificar triángulos y validar sus propiedades intrínsecas:

* **Clasificación por longitudes:** Utilizando la fórmula de distancia, calculamos la magnitud de los tres lados ($d_{AB}, d_{BC}, d_{CA}$). Si los tres son iguales, el triángulo es equilátero; si dos son iguales, isósceles; si todos difieren, escaleno.
* **Triángulos Rectángulos:** Un triángulo es rectángulo si y solo si las longitudes de sus lados cumplen estrictamente el Teorema de Pitágoras ($a^2 + b^2 = c^2$). Analíticamente, esto también puede verificarse si el producto de las pendientes de dos de sus lados es $-1$ ($m_1 \cdot m_2 = -1$), confirmando que son perpendiculares.

---

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Identificación y Mapeo

* *Si te solicito clasificar un triángulo cuyos vértices están en $(0,0), (3,0)$ y $(0,4)$, ¿cuál es el primer paso analítico necesario para conocer la longitud de sus lados?*
* *¿Qué sucede con los signos de los valores al elevar las diferencias $\Delta x$ y $\Delta y$ al cuadrado en la fórmula de distancia? ¿Afecta el orden en que restas los puntos al resultado final?*

### Nivel 2: Descomposición y Validación

* *Al calcular la distancia entre $(1, 2)$ y $(-2, 6)$, ¿cómo manejas la resta $(1 - (-2))$? ¿Qué sucede con la naturaleza del número resultante antes de elevarlo al cuadrado?*
* *Si afirmas que un triángulo es isósceles, ¿qué condición algebraica mínima sobre sus tres distancias calculadas debes demostrar para sustentar esa afirmación?*

### Nivel 3: Formalización y Rigor Estructural

* *Modela analíticamente la condición necesaria para que tres puntos $A, B$ y $C$ sean colineales, expresándola en términos de las distancias entre ellos. ¿Qué desigualdad debe transformarse en una igualdad para que el "triángulo" pierda su área y se convierta en una línea recta?*
* *Explica por qué, en el diseño de estructuras de ingeniería en la UCA, la verificación de la perpendicularidad mediante pendientes de los lados es preferible o complementaria a la verificación mediante la suma de cuadrados de las distancias.*

---

**Desafío para el estudiante:**
Considera los puntos $A(0,0)$, $B(4,0)$ y $C(2, 3)$.

1. Calcula la longitud de cada lado utilizando la fórmula de distancia.
2. ¿Qué tipo de triángulo es según sus lados?
3. ¿Cómo podrías demostrar, sin usar Pitágoras, que este triángulo no es rectángulo usando solo las pendientes de sus lados?
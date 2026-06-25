---

## subject: "precalculo"
topic: "desplazamiento_y_reflexion_de_funciones"
content_type: "base_teorica_socrática"

# Desplazamiento y Reflexión de Funciones

## Sustento Axiomático y Conceptual

Las transformaciones de funciones permiten modificar la posición y orientación del lugar geométrico de una curva en el plano cartesiano $\mathbb{R}^2$ sin alterar su forma intrínseca o rigidez matemática. Desde una perspectiva analítica, si conocemos la gráfica de una función base o "madre" $y = f(x)$, las operaciones de adición y multiplicación por constantes reales específicas sobre las variables independientes ($x$) o dependientes ($y$) generan nuevas funciones asociadas.

Dada una función base $y = f(x)$ y una constante real positiva $c > 0$, se formalizan axiomáticamente los siguientes dos grupos de transformaciones geométricas rígidas:

### 1. Desplazamientos (Traducciones en el Plano)

Los desplazamientos alteran de forma uniforme las coordenadas de los puntos coordenados de la función original, trasladando la curva de forma vertical u horizontal.

* **Desplazamiento Vertical Hacia Arriba:** Se añade la constante al output completo de la función. Cada punto $(x, y)$ se transforma unívocamente en $(x, y + c)$:

$$h(x) = f(x) + c$$


* **Desplazamiento Vertical Hacia Abajo:** Se sustrae la constante al output de la función, mapeando los puntos hacia $(x, y - c)$:

$$h(x) = f(x) - c$$


* **Desplazamiento Horizontal Hacia la Izquierda:** Se añade la constante directamente al argumento de entrada (variable independiente). El dominio se desplaza hacia valores menores, transformando los puntos $(x, y)$ en $(x - c, y)$:

$$h(x) = f(x + c)$$


* **Desplazamiento Horizontal Hacia la Derecha:** Se sustrae la constante del argumento interno de la función, mapeando geométricamente los puntos originales hacia coordenadas de abscisa $(x + c, y)$:

$$h(x) = f(x - c)$$



*Principio operativo del contra-intuitivismo horizontal:* Note que para los desplazamientos horizontales, la adición interna ($x + c$) genera un movimiento en sentido negativo del eje real $x$, mientras que la sustracción ($x - c$) desplaza la curva hacia la dirección positiva. Esto se debe a que la variable de entrada requiere compensar de forma inversa la alteración para alcanzar el mismo valor del argumento original en la función base.

### 2. Reflexiones (Inversión Geométrica)

Las reflexiones actúan como espejos matemáticos utilizando los ejes coordenados del plano cartesiano como rectas de simetría axial.

* **Reflexión Respecto al Eje Horizontal $x$ (Inversión de Output):** Se multiplica de manera externa la función completa por el factor $-1$. Modifica el signo de todas las ordenadas, transformando los puntos ordenados $(x, y)$ en $(x, -y)$:

$$h(x) = -f(x)$$


* **Reflexión Respecto al Eje Vertical $y$ (Inversión de Input):** Se multiplica de manera interna la variable independiente por $-1$. Cambia el sentido de las abscisas del dominio, transformando los puntos $(x, y)$ en $(-x, y)$:

$$h(x) = f(-x)$$



## Errores Algebraicos Comunes

Los sesgos procedimentales recurrentes en los estudiantes de ingeniería inicial en la UCA comprenden:

* **Inversión de la dirección en desplazamientos horizontales:** Desplazar la gráfica hacia la derecha ante una expresión del tipo $f(x + c)$, confundiendo la suma interna con un avance positivo sobre el eje de las abscisas.
* **Confusión en el orden de aplicación de transformaciones mixtas:** Operar funciones con múltiples transformaciones combinadas (ej. $h(x) = -f(x - 2) + 3$) de forma aleatoria, ignorando que la prioridad algebraica exige resolver primero los desplazamientos horizontales (operaciones de argumento), luego las reflexiones o estiramientos y, por último, los desplazamientos verticales.
* **Alcance incorrecto del signo negativo en reflexiones verticales:** Aplicar la reflexión respecto al eje $x$ únicamente al término principal de la función en lugar de distribuirlo con paréntesis asociativos sobre todo el polinomio:

$$\text{Reflejar } f(x) = x^2 - 3x + 1 \longrightarrow h(x) = -x^2 - 3x + 1 \quad \text{(Falso, el signo menos afecta a cada sumando)}$$


* **Modificación ilegal de la forma base:** Alterar la apertura o curvatura interna de una función elemental al desplazarla, perdiendo la rigidez geométrica del objeto matemático por imprecisiones al tabular los nuevos puntos de control.

## Estratificación de Andamiaje Socrático (Zero-Reveal)

### Nivel 1: Activación y Diagnóstico de Componentes Transmutados

**Objetivo:** Guiar al estudiante a identificar la función madre y catalogar las alteraciones algebraicas según su posición (interna o externa) sin efectuar trazos ni resolver la ecuación.

* *Observa la función modificada $g(x) = (x - 4)^2 + 1$. ¿Cuál es la función elemental o "madre" que está sirviendo como base operativa para esta estructura?*
* *Identifica las constantes numéricas que alteran a la función base. ¿Cuáles de ellas se encuentran operando de forma interna (dentro del argumento que afecta directamente a $x$) y cuáles actúan de forma externa (afectando a todo el output del bloque)?*
* *De acuerdo con los principios algebraicos de traducción de curvas, ¿qué tipo de movimiento geométrico (horizontal o vertical) se asocia unívocamente a las operaciones internas? ¿Y cuál a las externas?*

### Nivel 2: Descomposición Analítica y Evidencia del Sentido Inverso

**Objetivo:** Forzar la autovalidación cognitiva del estudiante rompiendo el sesgo de la dirección horizontal mediante la evaluación numérica de puntos críticos coordenados.

* *Sostienes que para graficar la función $f(x) = \sqrt{x + 3}$ debes mover la curva base $\sqrt{x}$ tres unidades hacia la derecha en dirección positiva. Evaluemos analíticamente el punto crítico del origen: para la función base, la raíz se anula exactamente en $x = 0$. En tu nueva función, ¿qué valor real de $x$ se necesita introducir para que el argumento interno $(x + 3)$ se vuelva cero? ¿Ese valor se localiza a la derecha o a la izquierda del origen en la recta real?*
* *Si necesitas graficar la transformación mixta $h(x) = -(x)^2 + 5$, y tu hipótesis te lleva a aplicar primero la adición externa antes que el signo negativo: calculemos el output para $x = 2$. Según la jerarquía de las operaciones en los campos reales, ¿qué operación tiene prioridad absoluta, la potencia con su signo negativo antecedente o la adición de la constante $+5$? ¿Cómo impacta este orden al orden geométrico en que debes trasladar los puntos?*
* *Para la función $f(x) = x^3 - 2x$, se te pide aplicar una reflexión respecto al eje horizontal $x$. Si tu respuesta actual es $h(x) = -x^3 - 2x$, multipliquemos de forma explícita $-1 \cdot [x^3 - 2x]$ aplicando la propiedad distributiva. ¿Qué ocurre con el signo del segundo monomio? ¿Es consistente tu propuesta inicial?*

### Nivel 3: Formalización Analítica e Integridad de Coordenadas de Ingeniería

**Objetivo:** Conducir al estudiante a generalizar la transformación mediante un modelo analítico de mapeo de puntos coordenados, garantizando el rigor formal de ingeniería.

* *Considera un punto genérico cualquiera $(p, q)$ que pertenezca con total certeza matemática a la gráfica de la función base $y = f(x)$. Si definimos una nueva función transformada bajo la regla $g(x) = -f(x + h) - k$, explica analíticamente cómo se transforman las coordenadas originales del punto. Escribe el nuevo par ordenado en términos de $p, q, h$ y $k$.*
* *Justifica de qué manera este mapeo de puntos te permite verificar científicamente la exactitud de tu nueva gráfica sin necesidad de volver a tabular una cantidad infinita de datos en el dominio. ¿Cómo aplicarías esta técnica al vértice de una parábola o al punto de inflexión de una cúbica para comprobar la consistencia global del sistema transformado?*
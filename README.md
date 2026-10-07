# Fintech Customer Analytics

Proyecto de análisis de datos aplicado a una campaña de marketing del
sector financiero. El objetivo es estudiar el comportamiento de los
clientes, identificar los factores relacionados con la suscripción y
desarrollar una solución que combine análisis exploratorio, análisis
estadístico, visualización de datos y modelización predictiva.

El proyecto cubre el flujo completo de trabajo, desde los datos
originales hasta la construcción de una aplicación web para realizar
predicciones sobre nuevos clientes.

## Objetivos

Los principales objetivos del proyecto son:

-   Explorar y comprender la información disponible sobre clientes y
    campañas comerciales.
-   Detectar patrones, relaciones y variables relevantes mediante
    análisis exploratorio y estadístico.
-   Preparar y transformar los datos para su posterior análisis y
    modelización.
-   Construir visualizaciones y dashboards que faciliten la
    interpretación de los resultados.
-   Desarrollar un modelo predictivo para estimar la probabilidad de
    suscripción de un cliente.
-   Convertir el modelo entrenado en una aplicación sencilla que pueda
    utilizarse fuera del entorno de desarrollo.

## Estructura del proyecto

``` text
Fintech_TFM/
├── 00_data/          # Datos originales y datos procesados
├── 01_notebooks/     # EDA, análisis y modelización
├── 02_scripts/       # Funciones reutilizables de Python
├── 03_reports/       # Informes del proyecto
├── 04_results/       # Resultados y salidas del análisis
├── 05_docs/          # Documentación adicional
├── 06_models/        # Modelo entrenado y metadatos
├── app/              # Aplicación Streamlit
├── requirements.txt  # Dependencias necesarias
├── .gitignore
└── README.md
```

## Metodología

### 1. Análisis exploratorio de datos

El análisis comienza sobre los datos originales, antes de aplicar las
transformaciones definitivas. Se estudian la estructura del dataset, los
tipos de variables, los valores ausentes o categorías especiales, los
duplicados, las distribuciones y el comportamiento de las variables
categóricas y numéricas.

También se analiza la variable objetivo de suscripción para conocer el
equilibrio entre clases y disponer de una referencia antes de construir
el modelo.

### 2. Análisis estadístico y relaciones entre variables

Además del análisis descriptivo, se estudian relaciones entre variables
mediante técnicas estadísticas y visuales.

Entre los análisis realizados se incluyen tablas de contingencia,
pruebas de Chi-cuadrado para variables categóricas y análisis de
correlaciones entre variables numéricas. El objetivo es complementar las
visualizaciones con evidencia cuantitativa y detectar asociaciones
relevantes para la interpretación del problema.

### 3. Limpieza y transformación

La preparación de los datos se realiza mediante funciones reutilizables
en Python. El proceso incluye normalización de nombres de variables,
tratamiento de determinadas categorías, eliminación de duplicados,
creación de variables derivadas y preparación de un dataset procesado.

Entre las variables generadas durante esta fase se encuentran
indicadores relacionados con clientes nuevos en campaña, intensidad de
contacto y agrupaciones de duración de llamadas.

El resultado se guarda como un dataset procesado separado de los datos
originales, manteniendo así la trazabilidad entre la fuente y los datos
utilizados posteriormente.

### 4. Dashboards y visualización

El proyecto incorpora dashboards y visualizaciones orientados a resumir
los principales resultados del análisis y facilitar su interpretación.

Esta parte permite trasladar el análisis técnico a una presentación más
accesible, centrada en distribuciones, comportamiento de clientes,
resultados de campaña y principales indicadores obtenidos durante el
estudio.

### 5. Modelo predictivo

Para la parte predictiva se utiliza una regresión logística integrada en
un `Pipeline` de Scikit-learn.

Las variables categóricas se transforman mediante `OneHotEncoder` y las
variables numéricas se estandarizan mediante `StandardScaler`. El
preprocesamiento se integra con el modelo mediante `ColumnTransformer`,
de forma que las mismas transformaciones utilizadas durante el
entrenamiento puedan aplicarse posteriormente a nuevos clientes.

Los datos se separan en conjuntos de entrenamiento, validación y test
con una distribución aproximada de 60 %, 20 % y 20 %. La separación se
realiza de forma estratificada para conservar la proporción de la
variable objetivo.

El modelo utiliza `class_weight="balanced"` para tener en cuenta el
desequilibrio existente entre las clases.

### 6. Selección del umbral de decisión

En lugar de utilizar únicamente el umbral estándar de 0.50, se analiza
el comportamiento del modelo para diferentes thresholds sobre el
conjunto de validación.

El umbral final se selecciona buscando el mejor F1-score, tratando de
encontrar un equilibrio entre precision y recall para la clase positiva.

El threshold seleccionado es aproximadamente:

``` text
0.69
```

Este valor se guarda de forma independiente en los metadatos del modelo
y se utiliza posteriormente durante la inferencia.

## Resultados del modelo

En el conjunto de validación, utilizando inicialmente un threshold de
0.50, el modelo obtuvo un ROC-AUC aproximado de:

``` text
ROC-AUC: 0.777
```

Después de seleccionar el threshold sobre validación, la evaluación
final se realiza sobre el conjunto de test, que se mantiene aislado
durante el ajuste del modelo y del umbral.

Con un threshold aproximado de 0.69, la matriz de confusión obtenida
sobre test fue:

``` text
TN = 6619
FP = 513
FN = 447
TP = 459
```

Estos resultados permiten evaluar no solo la exactitud global, sino
también el comportamiento del modelo al identificar clientes de la clase
positiva.

El ROC-AUC se interpreta como una medida de capacidad de discriminación
del modelo basada en las probabilidades generadas y no depende de un
único threshold de clasificación.

## Interpretabilidad

Al tratarse de una regresión logística, el proyecto también permite
estudiar los coeficientes del modelo.

Un coeficiente positivo indica una mayor tendencia hacia la clase de
suscripción, mientras que un coeficiente negativo indica una menor
tendencia, manteniendo constantes el resto de variables. En las
variables categóricas, la interpretación se realiza respecto a la
categoría de referencia generada durante el One-Hot Encoding.

Este análisis permite complementar las métricas predictivas con una
interpretación del comportamiento del modelo.

## Modelo preparado para inferencia

Una vez completada la evaluación, el pipeline se entrena para su
utilización posterior y se guarda con `joblib`.

Los artefactos principales son:

``` text
06_models/
├── logistic_regression_pipeline.joblib
└── logistic_regression_metadata.json
```

El archivo `.joblib` contiene el pipeline de preprocesamiento y el
modelo entrenado.

El archivo de metadatos almacena información adicional necesaria para
utilizar y documentar el modelo, como el threshold de decisión, la
versión, las variables esperadas y métricas de referencia.

## Aplicación Streamlit

El proyecto incluye una aplicación desarrollada con Streamlit que
permite utilizar el modelo mediante una interfaz web.

El usuario introduce las características de un cliente mediante campos y
desplegables. La aplicación construye la observación, aplica el pipeline
entrenado, obtiene la probabilidad de suscripción mediante
`predict_proba` y aplica el threshold almacenado en los metadatos.

De esta forma, el modelo puede utilizarse sin necesidad de ejecutar
directamente los notebooks ni escribir código Python.

Para ejecutar la aplicación localmente:

``` bash
streamlit run app/app.py
```

## Instalación

Se recomienda crear y activar un entorno virtual antes de instalar las
dependencias.

Las dependencias principales del proyecto se encuentran en
`requirements.txt` y pueden instalarse con:

``` bash
pip install -r requirements.txt
```

## Tecnologías utilizadas

-   Python
-   Pandas
-   NumPy
-   Matplotlib
-   Seaborn
-   Scikit-learn
-   SciPy
-   Joblib
-   Jupyter Notebook
-   Streamlit
-   Git y GitHub

## Flujo general del proyecto

``` text
Datos originales
      |
      v
Análisis exploratorio y estadístico
      |
      v
Limpieza y transformación
      |
      +--------------------+
      |                    |
      v                    v
Dashboards            Dataset procesado
                           |
                           v
                    Modelo predictivo
                           |
                           v
                 Evaluación y threshold
                           |
                           v
                  Modelo + metadatos
                           |
                           v
                  Aplicación Streamlit
```

## Estado del proyecto

El análisis, el procesamiento de datos, la modelización y la aplicación
local se encuentran implementados. El siguiente paso es publicar el
repositorio y desplegar la aplicación para permitir su acceso mediante
una URL pública.

## Autor

Diego

Proyecto desarrollado como trabajo de análisis de datos y modelización
aplicado al sector Fintech.

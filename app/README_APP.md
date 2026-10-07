# Interfaz Streamlit - Fintech TFM

Esta carpeta contiene una interfaz web sencilla para utilizar el
pipeline de regresión logística del proyecto.

## Estructura esperada

``` text
Fintech_TFM/
├── 03_models/
│   ├── logistic_regression_pipeline.joblib
│   └── logistic_regression_metadata.json
├── app/
│   └── app.py
└── requirements.txt
```

## Ejecución local

Desde la carpeta raíz `Fintech_TFM`:

``` bash
pip install -r requirements.txt
streamlit run app/app.py
```

La aplicación carga el pipeline completo, recupera el threshold desde
los metadatos, calcula `predict_proba()` para un cliente nuevo y aplica
ese threshold para obtener la predicción final.

## GitHub y despliegue

Sube el proyecto a GitHub. Después puedes conectar el repositorio a
Streamlit Community Cloud y seleccionar `app/app.py` como fichero
principal de la aplicación.

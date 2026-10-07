from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Predicción de suscripción Fintech",
    page_icon="📊",
    layout="centered"
)

st.title("Predicción de suscripción Fintech")
st.write(
    "Introduce los datos del cliente y el modelo estimará "
    "la probabilidad de suscripción."
)


# ---------------------------------------------------------
# 2. RUTAS DEL MODELO Y DE LOS METADATOS
# ---------------------------------------------------------
# app.py está dentro de /app, por eso parent.parent apunta
# a la carpeta raíz Fintech_TFM.
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    BASE_DIR
    / "05_models"
    / "logistic_regression_pipeline.joblib"
)

METADATA_FILE = (
    BASE_DIR
    / "05_models"
    / "logistic_regression_metadata.json"
)


# ---------------------------------------------------------
# 3. CARGA DEL PIPELINE Y DE LOS METADATOS
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE)


@st.cache_data
def load_metadata():
    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


try:
    model = load_model()
    metadata = load_metadata()
except FileNotFoundError as error:
    st.error(
        "No se encuentra el modelo o el fichero de metadatos. "
        "Comprueba que ambos estén dentro de 05_models/."
    )
    st.exception(error)
    st.stop()


# Recuperamos el threshold seleccionado durante la validación.
threshold = float(metadata["threshold"])

# Recuperamos las variables y su orden.
expected_features = metadata["features"]


# ---------------------------------------------------------
# 4. FORMULARIO DE ENTRADA
# ---------------------------------------------------------
st.subheader("Datos del cliente")

with st.form("prediction_form"):

    age = st.number_input(
        "Edad",
        min_value=18,
        max_value=100,
        value=40,
        step=1
    )

    job_type = st.selectbox(
        "Tipo de trabajo",
        [
            "admin.",
            "blue-collar",
            "entrepreneur",
            "housemaid",
            "management",
            "retired",
            "self-employed",
            "services",
            "student",
            "technician",
            "unemployed",
            "undisclosed"
        ],
        format_func=lambda x: {
            "admin.": "Administración",
            "blue-collar": "Trabajador manual",
            "entrepreneur": "Emprendedor",
            "housemaid": "Trabajo doméstico",
            "management": "Dirección / gestión",
            "retired": "Jubilado",
            "self-employed": "Autónomo",
            "services": "Servicios",
            "student": "Estudiante",
            "technician": "Técnico",
            "unemployed": "Desempleado",
            "undisclosed": "No informado"
        }[x]
    )

    education_level = st.selectbox(
        "Nivel educativo",
        [
            "basic.4y",
            "basic.6y",
            "basic.9y",
            "high.school",
            "illiterate",
            "professional.course",
            "university.degree",
            "undisclosed"
        ],
        format_func=lambda x: {
            "basic.4y": "Educación básica - 4 años",
            "basic.6y": "Educación básica - 6 años",
            "basic.9y": "Educación básica - 9 años",
            "high.school": "Secundaria",
            "illiterate": "Sin alfabetización",
            "professional.course": "Formación profesional",
            "university.degree": "Universitaria",
            "undisclosed": "No informado"
        }[x]
    )

    credit_default = st.selectbox(
        "¿Tiene impagos de crédito?",
        ["no", "yes", "undisclosed"],
        format_func=lambda x: {
            "no": "No",
            "yes": "Sí",
            "undisclosed": "No informado"
        }[x]
    )

    contact_method = st.selectbox(
        "Método de contacto",
        ["cellular", "telephone"],
        format_func=lambda x: {
            "cellular": "Móvil",
            "telephone": "Teléfono fijo"
        }[x]
    )

    contact_month = st.selectbox(
        "Mes de contacto",
        ["mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"],
        format_func=lambda x: {
            "mar": "Marzo",
            "apr": "Abril",
            "may": "Mayo",
            "jun": "Junio",
            "jul": "Julio",
            "aug": "Agosto",
            "sep": "Septiembre",
            "oct": "Octubre",
            "nov": "Noviembre",
            "dec": "Diciembre"
        }[x]
    )

    previously_contacted = st.number_input(
        "Días desde el último contacto (999 = nunca contactado)",
        min_value=0,
        max_value=999,
        value=999,
        step=1
    )

    previous_campaign_outcome = st.selectbox(
        "Resultado de la campaña anterior",
        ["nonexistent", "failure", "success"],
        format_func=lambda x: {
            "nonexistent": "No hubo campaña anterior",
            "failure": "No tuvo éxito",
            "success": "Tuvo éxito"
        }[x]
    )

    euribor_3m_rate = st.number_input(
        "Euribor a 3 meses",
        min_value=-5.0,
        max_value=10.0,
        value=3.0,
        step=0.001,
        format="%.3f"
    )

    is_new_campaign_client = st.selectbox(
        "¿Es un cliente nuevo para la campaña?",
        ["yes", "no"],
        format_func=lambda x: {
            "yes": "Sí",
            "no": "No"
        }[x]
    )

    submitted = st.form_submit_button(
        "Realizar predicción",
        use_container_width=True
    )


# ---------------------------------------------------------
# 5. PREDICCIÓN
# ---------------------------------------------------------
if submitted:

    # Creamos un DataFrame de una sola fila con el nuevo cliente.
    new_client = pd.DataFrame([{
        "age": age,
        "job_type": job_type,
        "education_level": education_level,
        "credit_default": credit_default,
        "contact_method": contact_method,
        "contact_month": contact_month,
        "previously_contacted": previously_contacted,
        "previous_campaign_outcome": previous_campaign_outcome,
        "euribor_3m_rate": euribor_3m_rate,
        "is_new_campaign_client": is_new_campaign_client
    }])

    # Comprobamos que la aplicación está enviando exactamente
    # las variables que espera el modelo.
    missing_features = [
        feature for feature in expected_features
        if feature not in new_client.columns
    ]

    extra_features = [
        feature for feature in new_client.columns
        if feature not in expected_features
    ]

    if missing_features or extra_features:
        st.error("Las variables de la aplicación no coinciden con las del modelo.")

        if missing_features:
            st.write("Variables que faltan:", missing_features)

        if extra_features:
            st.write("Variables que sobran:", extra_features)

        st.stop()

    # Colocamos las columnas en el mismo orden guardado en los metadatos.
    new_client = new_client[expected_features]

    # El pipeline aplica automáticamente el preprocesamiento
    # y calcula la probabilidad de la clase positiva (suscripción = 1).
    probability = float(
        model.predict_proba(new_client)[:, 1][0]
    )

    # Aplicamos el threshold guardado en los metadatos.
    prediction = int(probability >= threshold)

    # Mostramos el resultado.
    st.subheader("Resultado")

    st.metric(
        "Probabilidad estimada de suscripción",
        f"{probability:.1%}"
    )

    st.caption(
        f"Threshold utilizado por la aplicación: {threshold:.2f}"
    )

    if prediction == 1:
        st.success("Predicción: SÍ es probable que se suscriba.")
    else:
        st.info("Predicción: NO es probable que se suscriba.")

    # Información adicional útil para comprobar qué se envió al pipeline.
    with st.expander("Ver datos enviados al modelo"):
        st.dataframe(new_client, use_container_width=True)

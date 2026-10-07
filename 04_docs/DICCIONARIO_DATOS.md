# Diccionario de datos

Este documento describe las variables del dataset una vez aplicado el proceso de limpieza y transformación utilizado en el proyecto Fintech.

| Variable | Tipo | Descripción | Tratamiento / origen |
|---|---|---|---|
| age | Numérica | Edad del cliente, en años. | Dato original renombrado. |
| job_type | Categórica | Tipo de ocupación o situación laboral del cliente. | Categorías del dataset original; 'unknown' se normaliza cuando corresponde. |
| marital_status | Categórica | Estado civil del cliente. | Dato original renombrado. |
| education_level | Categórica | Nivel educativo declarado por el cliente. | Dato original renombrado; categorías no informadas se tratan de forma explícita. |
| credit_default | Categórica | Indica si el cliente presenta impago de crédito. | Procede de 'default'. |
| has_housing_loan | Categórica | Indica si el cliente tiene un préstamo hipotecario. | Procede de 'housing'; registros con valor 'unknown' se eliminan durante la limpieza. |
| has_personal_loan | Categórica | Indica si el cliente tiene un préstamo personal. | Procede de 'loan'; registros con valor 'unknown' se eliminan durante la limpieza. |
| contact_method | Categórica | Canal utilizado para contactar con el cliente. | Procede de 'contact'. |
| contact_month | Categórica ordinal | Mes en el que se realizó el contacto. | Procede de 'month' y se ordena cronológicamente. |
| contact_day | Categórica ordinal | Día de la semana en el que se realizó el contacto. | Procede de 'day_of_week' y se ordena cronológicamente. |
| call_duration | Numérica | Duración de la última llamada de contacto. | Procede de 'duration'. Variable sensible a leakage si se predice antes de realizar la llamada. |
| contact_attempts | Numérica discreta | Número de contactos realizados durante la campaña actual para ese cliente. | Procede de 'campaign'. |
| previously_contacted | Numérica discreta | Número de días transcurridos desde el último contacto de una campaña anterior. | Procede de 'pdays'; el valor especial del dataset original indica que no hubo contacto previo. |
| previous_contacts | Numérica discreta | Número de contactos realizados antes de la campaña actual. | Procede de 'previous'. |
| previous_campaign_outcome | Categórica | Resultado de la campaña de marketing anterior. | Procede de 'poutcome'. |
| employment_variation_rate | Numérica | Indicador de variación del empleo asociado al contexto económico. | Procede de 'emp.var.rate'. |
| consumer_price_index | Numérica | Índice de precios al consumo asociado al contexto económico. | Procede de 'cons.price.idx'. |
| consumer_confidence_index | Numérica | Índice de confianza del consumidor asociado al contexto económico. | Procede de 'cons.conf.idx'. |
| euribor_3m_rate | Numérica | Tipo Euribor a tres meses. | Procede de 'euribor3m'. |
| total_employment | Numérica | Indicador del nivel total de empleo utilizado en el dataset. | Procede de 'nr.employed'. |
| call_duration_group | Categórica derivada | Agrupación de la duración de la llamada en intervalos o categorías. | Variable creada durante la limpieza a partir de 'call_duration'. |
| is_new_campaign_client | Binaria derivada | Identifica si el cliente no había sido contactado en campañas anteriores. | Variable creada durante la limpieza a partir de la información de contactos previos. |
| high_contact_attempts | Binaria derivada | Identifica clientes con un número elevado de intentos de contacto en la campaña actual. | Variable creada durante la limpieza a partir de 'contact_attempts'. |
| subscribed | Binaria / objetivo | Indica si el cliente se suscribió al producto tras la campaña. | Variable objetivo. Procede de 'y' y se sitúa al final del dataset limpio. |

## Notas

- `subscribed` es la variable objetivo del proyecto.
- `call_duration_group`, `is_new_campaign_client` y `high_contact_attempts` son variables creadas durante el proceso de limpieza.
- `call_duration` debe interpretarse con cautela en modelos cuyo objetivo sea predecir la suscripción antes de que se produzca la llamada, ya que su valor solo se conoce una vez realizada.
- Los nombres del dataset limpio se mantienen en inglés para facilitar su uso en código, mientras que la documentación se presenta en español.

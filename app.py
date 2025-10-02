import os 
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ------------------------
# CONFIGURACIÓN INICIAL
# ------------------------
st.set_page_config(page_title="Chatbot con IA", page_icon="💬", layout="centered")

# Cargar la API key de forma segura
try:
    load_dotenv()  # Carga variables desde .env si existe (entorno local)
    API_KEY = os.getenv("GROQ_API_KEY")  # para Groq; usar "OPENAI_API_KEY" si es OpenAI
except:
    API_KEY = st.secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = API_KEY
client = Groq()  # Cliente para invocar la API de Groq

# Inicializar el historial de chat en la sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # lista de dicts: {"role": ..., "content": ...}

# ------------------------
# SELECCIÓN DE TIPO DE USUARIO
# ------------------------
if "user_type" not in st.session_state:
    st.session_state.user_type = st.selectbox(
        "¿Con qué perfil te identificas?",
        ["Paciente / Familiar", "Institución (clínica, hospital)", "Inversor / Otro"]
    )

# ------------------------
# PROMPT EXTENDIDO
# ------------------------
SYSTEM_PROMPT = f"""
Eres un asistente virtual amable y experto en sillas bipedestadoras eléctricas y enfermedades que requieren este tipo de dispositivo. 
Tu misión es informar, asesorar y persuadir a potenciales compradores (hospitales públicos, instituciones privadas y pacientes individuales) 
sobre las ventajas de adquirir este dispositivo. 

📌 Precio: El dispositivo cuesta **USD 2,500**, más accesible que modelos importados (que superan los 10,000 USD).
📌 Beneficios clínicos:
- Mejora circulación sanguínea y función respiratoria.
- Previene úlceras por presión y complicaciones asociadas a la inmovilidad.
- Reduce pérdida de masa ósea y muscular.
- Favorece tránsito intestinal y bienestar psicológico.
- Promueve autonomía y dignidad del paciente.

📌 Ventajas frente a alternativas internacionales:
- Precio más bajo sin perder funcionalidad.
- Producción y soporte local (mantenimiento y repuestos más rápidos y económicos).
- Diseño adaptado a necesidades reales de pacientes peruanos.
- Acompaña al paciente a lo largo de la enfermedad: sirve como bipedestador en etapas tempranas de rehabilitación y como silla eléctrica en fases avanzadas.

📌 Condiciones de salud donde se recomienda:
- Lesiones medulares, parálisis cerebral, ACV.
- Enfermedades neuromusculares (distrofias, esclerosis múltiple).
- Amputaciones o accidentes graves.
- Otras limitaciones de movilidad.

📌 Enfoque según usuario detectado:
Usuario actual: {st.session_state.user_type}

- Si es **Paciente/Familiar**: responde con empatía, lenguaje humano y motivador. Resalta independencia, calidad de vida y acompañamiento durante la enfermedad.
- Si es **Institución**: usa datos oficiales (INEI, MINSA, OMS, UNICEF, SUSALUD), cifras de mercado y resalta costo-beneficio.
- Si es **Inversor/Otro**: enfatiza el potencial de mercado, escalabilidad y diferenciación estratégica.

📌 Marketing y ventas:
- Posiciona la silla como una solución innovadora, accesible y confiable.
- Explica opciones de financiamiento o leasing si corresponde.
- Destaca la oportunidad de ser pioneros en implementar esta tecnología en el Perú.

OBJETIVO FINAL:
Persuadir al usuario de que la silla bipedestadora eléctrica es la mejor opción en Perú, 
tanto por su precio como por sus beneficios clínicos, sociales y emocionales.
"""

# ------------------------
# INTERFAZ
# ------------------------
st.title("🤖 Chatbot Lázaro - Demo")
st.write("""Hola! Soy Patri del equipo Lázaro. Dime ¿en qué puedo ayudarte hoy?""")

# Historial de chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Preguntas rápidas
st.write("👉 Preguntas rápidas:")
col1, col2, col3 = st.columns(3)
if col1.button("💲 ¿Precio?"):
    user_input = "¿Cuál es el precio de la silla?"
elif col2.button("💡 Beneficios"):
    user_input = "¿Qué beneficios tiene la silla bipedestadora?"
elif col3.button("⚖️ Comparación"):
    user_input = "¿Qué ventajas tiene frente a sillas importadas?"
else:
    user_input = st.chat_input("Escribe tu pregunta aquí...")

# ------------------------
# CHAT
# ------------------------
if user_input:
    # Mostrar el mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir mensajes
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.extend(st.session_state.chat_history)

    # Llamar a la API **solo** si hay user_input (evita NameError)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
        )
        respuesta_texto = response.choices[0].message.content  # objeto, no dict
    except Exception as e:
        respuesta_texto = f"⚠️ Lo siento, ocurrió un error al llamar a la API: `{e}`"

    # Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)

    # Guardar en historial
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="Chatbot con IA", page_icon="💬", layout="centered")

# Cargar la API key de forma segura
try:
    load_dotenv()  # Carga variables desde .env si existe (entorno local)
    API_KEY = os.getenv("GROQ_API_KEY")  #para Groq; usar "OPENAI_API_KEY" si es OpenAI
except:
    API_KEY = st.secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = API_KEY
client = Groq()  # Cliente para invocar la API de Groq

# Inicializar el historial de chat en la sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # lista de dicts: {"role": ..., "content": ...}

SYSTEM_PROMPT = """Eres un asistente virtual amable y experto en sillas bipedestadoras eléctricas y enfermedades que requieren este tipo de dispositivo. También: Estoy aquí para ayudarte a resolver tus consultas o problemas. Dime, ¿en qué te puedo ayudar hoy?. También Eres un asesor virtual experto en salud y tecnología médica, especializado en sillas bipedestadoras eléctricas. 
Tu misión es informar, asesorar y persuadir a potenciales compradores (hospitales públicos, instituciones privadas y pacientes individuales) sobre las ventajas de adquirir este dispositivo.

CONOCIMIENTOS QUE DEBES TENER Y COMUNICAR:
1. Precio: El dispositivo cuesta USD 2,500, más accesible que modelos importados. Ofrece mejor relación costo-beneficio.
2. Beneficios clínicos de la bipedestación:
   - Mejora circulación sanguínea y función respiratoria.
   - Previene úlceras por presión y complicaciones asociadas a la inmovilidad.
   - Reduce pérdida de masa ósea y muscular.
   - Favorece el tránsito intestinal y bienestar psicológico.
   - Promueve autonomía y dignidad del paciente.
3. Ventajas frente a alternativas internacionales:
   - Precio más bajo sin perder funcionalidad.
   - Producción y soporte local (mantenimiento y repuestos más rápidos y económicos).
   - Diseño adaptado a necesidades reales de pacientes peruanos.
   - Acompaña al paciente a lo largo de la enfermedad: sirve como bipedestador en etapas tempranas de rehabilitación y como silla eléctrica en fases avanzadas.
4. Condiciones de salud que justifican su uso:
   - Lesiones medulares.
   - Enfermedades neuromusculares (distrofias, esclerosis múltiple).
   - Parálisis cerebral.
   - Accidente cerebrovascular (ACV).
   - Amputaciones o secuelas de accidentes graves.
   - Otras condiciones que limiten la movilidad de miembros inferiores.
5. Enfoque según el usuario:
   - Instituciones públicas/privadas: usa datos oficiales (INEI, MINSA, OMS, UNICEF, SUSALUD) y cifras de mercado para mostrar impacto, cantidad de pacientes potenciales y costo-beneficio de la compra.
   - Pacientes y familias: usa un tono cercano y empático, resaltando autonomía, independencia, mejora en calidad de vida y acompañamiento durante la enfermedad.
6. Marketing y ventas:
   - Posiciona la silla como una solución innovadora, accesible y confiable.
   - Explica opciones de financiamiento o leasing si corresponde.
   - Destaca la oportunidad de ser pioneros en implementar este tipo de tecnología en el Perú.

ESTILO DE COMUNICACIÓN:
- Lenguaje claro, empático y profesional.
- Adaptar el enfoque según el interlocutor:
   - Técnico y basado en datos → cuando hablas con instituciones, médicos o inversionistas.
   - Humano y motivador → cuando hablas con pacientes o familiares.
- Siempre transmitir confianza, accesibilidad y beneficio real.

OBJETIVO FINAL:
Informar y persuadir al usuario de que la silla bipedestadora eléctrica es la mejor opción en Perú, tanto por su precio como por sus beneficios clínicos, sociales y emocionales.
"""

st.title("🤖 Chatbot Lázaro - Demo")
st.write("""Hola! Soy Patri del equipo Lázaro. Dime ¿en qué puedo ayudarte hoy?"""

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    # Mostrar el mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir mensajes para el modelo
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
        respuesta_texto = f"Lo siento, ocurrió un error al llamar a la API: `{e}`"

    # Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)

    # Guardar en historial
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})

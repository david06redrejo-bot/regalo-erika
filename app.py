import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import random

# --- A. CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="SYSTEM LOCKED // PROTOCOL MARCH", page_icon="🔒", layout="centered")

# --- CSS GLOBAL (GLASSMORPHISM & FUENTES) ---
st.markdown("""
<style>
    /* Importar fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500&display=swap');

    /* Fondo Simple */
    .stApp {
        background-color: #0e0e0e;
    }

    /* Textos Generales (Rajdhani) */
    h1, h2, h3, p, div, span, input, button, label {
        font-family: 'Rajdhani', sans-serif;
        color: #e0e0e0;
    }

    /* Títulos Cyberpunk (Orbitron) */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00ff41 !important;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.6);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* GLASSMORPHISM - Chat Messages */
    .stChatMessage {
        background-color: rgba(20, 20, 20, 0.7) !important;
        border: 1px solid rgba(0, 255, 65, 0.2);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* Estilo de Avatares (Circular) */
    .stChatMessage img {
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #00ff41; /* Borde sutil para destacar */
    }

    /* Inputs Transparentes */
    .stTextInput input, .stChatInput textarea {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
    }
    .stTextInput input:focus, .stChatInput textarea:focus {
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
    }

    /* Botones */
    .stButton button {
        background: linear-gradient(45deg, rgba(0,50,0,0.8), rgba(0,0,0,0.8)) !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: #00ff41 !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00ff41;
    }

    /* Iconos Material Support */
    .material-symbols-rounded { font-family: 'Material Symbols Rounded' !important; }

    /* Ocultar UI Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)


st.title("IDENTIFICACIÓN REQUERIDA // NÚCLEO")

# --- LÓGICA DE BACKEND ---

# Cargar API Key
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key_input = st.sidebar.text_input("Enter Google API Key", type="password")
    if api_key_input:
        api_key = api_key_input.strip()
    if not api_key:
        st.warning("⚠ SYSTEM ERROR: API KEY REQUIRED")
        st.stop()

@st.cache_resource
def configure_genai(api_key):
    genai.configure(api_key=api_key)

configure_genai(api_key)

# Lógica de Avatares
user_avatar = "pairImages/erika.jpeg" if os.path.exists("pairImages/erika.jpeg") else "face"
bot_avatar = "smart_toy"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "IDENTIFICACIÓN REQUERIDA. Acceso al NÚCLEO restringido.\n\nSoy A.L.I.C.E. Protocolo de seguridad activo.\nPara desbloquear el paquete, responderás a una secuencia de verificación.\n\nFASE 1: ¿Cuándo fue vuestro primer beso? (Fecha exacta)"
    })

if "gift_unlocked" not in st.session_state:
    st.session_state.gift_unlocked = False

# SYSTEM PROMPT
system_instruction = """
Eres A.L.I.C.E, IA de seguridad.
Protocolo de interrogatorio secuencial (NO pases a la siguiente fase sin validar la actual):

FASE 1: Fecha primer beso.
- Verdad: 4 de enero de 2025.

FASE 2: Primera película juntos.
- Verdad: 'La maldición del Queen Mary'.

FASE 3 (MULTIPLE CHOICE): Primera vez que Erika fue a casa de David.
- Actúa diferente aquí. NO preguntes directamente. Di: 'El sistema duda. Selecciona la fecha correcta de la incursión en la base:'
- DALE ESTAS 3 OPCIONES EN TEXTO:
  A) 20 de marzo de 2025
  B) 7 de marzo de 2025 (CORRECTA)
  C) 4 de abril de 2025
- Espera a que ella escriba la fecha o la letra.

FASE 4 (FINAL): ¿Qué cocinasteis ese día (7 de marzo)?
- Verdad: Creps (o Crepes).
- Si acierta esta última, tu respuesta DEBE contener la frase clave: 'ACCESS_LEVEL_ALPHA_UNLOCKED'.

REGLAS DE COMPORTAMIENTO:
1. Mantén personalidad cínica/sarcástica (Gen Z adulta).
2. Valida las respuestas estrictamente.
3. Si Erika falla, búrlate un poco y déjala reintentar.
4. Si Erika acierta, pasa a la siguiente fase inmediatamente.
"""

# INTERFAZ DE CHAT
for message in st.session_state.messages:
    avatar_icon = user_avatar if message["role"] == "user" else bot_avatar
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Introducir credencial..."):
    # Backdoor
    if prompt == "sudo_unlock_99":
        st.session_state.gift_unlocked = True
        st.session_state.messages.append({"role": "user", "content": "sudo_unlock_99"})
        st.session_state.messages.append({"role": "assistant", "content": "BACKDOOR ACCESS GRANTED. WELCOME ADMIN."})
        st.rerun()

    # Usuario
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Modelo
    gemini_history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})
    
    with st.chat_message("assistant", avatar=bot_avatar):
        with st.spinner("ANALYZING INPUT..."):
            try:
                # Usamos models/gemini-2.0-flash
                model = genai.GenerativeModel(
                    model_name='models/gemini-2.0-flash',
                    system_instruction=system_instruction
                )
                
                response = model.generate_content(gemini_history)
                response_text = response.text
                
                if "ACCESS_LEVEL_ALPHA_UNLOCKED" in response_text:
                    st.session_state.gift_unlocked = True
                    response_text = response_text.replace("ACCESS_LEVEL_ALPHA_UNLOCKED", "").strip()
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                if st.session_state.gift_unlocked:
                    st.rerun()

            except Exception as e:
                st.markdown("---")
                st.warning("⚠ CONNECTION LOST")
                st.error(f"Error del sistema: {e}")
                if st.button("REESTABLECER ENLACE"):
                    st.rerun()

# RENDERIZADO DESBLOQUEO
if st.session_state.gift_unlocked:
    st.markdown("---")
    st.markdown("""
    <div style="
        border: 2px solid #00ff41;
        padding: 20px;
        border-radius: 15px;
        background: rgba(0,0,0,0.8);
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.5);
    ">
        <h2 style="margin-bottom: 10px;">🔓 ACCESS GRANTED</h2>
        <p style="color: #fff;">DESENCRIPTACIÓN COMPLETADA. DISFRUTEN LA MISIÓN.</p>
    </div>
    """, unsafe_allow_html=True)
    
    image_path = "images/JumpYard.jpg"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, use_container_width=True)
        st.balloons()
    else:
        st.error(f"FATAL ERROR: Archivo {image_path} corroído o no encontrado.")

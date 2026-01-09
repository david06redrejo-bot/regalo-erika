import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import base64
import random

# --- A. CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="SYSTEM LOCKED // PROTOCOL MARCH", page_icon="🔒", layout="centered")

# Función para cargar imágenes y convertirlas a Base64
def get_base64_images(folder_path):
    images_b64 = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                    images_b64.append(f"data:image/{filename.split('.')[-1]};base64,{encoded}")
    return images_b64

# Cargar imágenes de fondo
background_images = get_base64_images("pairImages")

# Generar CSS dinámico para el fondo
if background_images:
    # Creamos una animación simple que cambia el fondo si hay imágenes
    # Si hay muchas, podemos hacer un carrusel. Para v1, usaremos una aleatoria cada vez
    # O un ciclo CSS si queremos ser fancy. Vamos a hacer un ciclo CSS.
    
    keyframes_css = "@keyframes slideShow {\n"
    step = 100 / len(background_images)
    for i, img in enumerate(background_images):
        keyframes_css += f"  {i * step}% {{ background-image: url('{img}'); }}\n"
    keyframes_css += "}\n"
    
    bg_css = f"""
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        {keyframes_css}
        animation: slideShow {len(background_images) * 5}s infinite;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        z-index: -1;
        opacity: 0.8; /* Ajuste de opacidad para que se vea la imagen */
    }}
    .stApp::after {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7); /* Overlay oscuro para legibilidad */
        z-index: -1;
    }}
    """
else:
    # Fallback a negro si no hay imágenes
    bg_css = """
    .stApp {
        background-color: #000000;
    }
    """

# CSS Global (Glassmorphism + Fonts)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');

    /* Fondo Dinámico */
    {bg_css}

    /* Tipografía */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Orbitron', sans-serif !important;
        color: #00ff00 !important;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }}
    
    p, div, span, label, input, textarea, button {{
        font-family: 'Share Tech Mono', monospace !important;
        color: #e0e0e0 !important;
    }}

    /* Glassmorphism Containers */
    .stChatMessage {{
        background: rgba(20, 20, 20, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 0, 0.2);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    
    /* Input Field Glass */
    .stTextInput input {{
        background: rgba(0, 0, 0, 0.5) !important;
        color: #00ff00 !important;
        border: 1px solid rgba(0, 255, 0, 0.4) !important;
        border-radius: 5px;
        backdrop-filter: blur(5px);
    }}
    
    /* Buttons */
    .stButton button {{
        background: rgba(0, 50, 0, 0.6) !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }}
    .stButton button:hover {{
        background: rgba(0, 255, 0, 0.2) !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.4);
    }}

    /* Ocultar elementos extra de Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

</style>
""", unsafe_allow_html=True)

st.title("IDENTIFICACIÓN REQUERIDA // Acceso al NÚCLEO restringido")

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
        st.warning("⚠ SYSTEM ERROR: API KEY REQUIRED FOR INITIALIZATION")
        st.stop()

# Configuración cacheada de Gemini
@st.cache_resource
def configure_genai(api_key):
    genai.configure(api_key=api_key)

configure_genai(api_key)

# --- B. ESTADO DE SESIÓN (STATELESS) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje inicial simulado
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "IDENTIFICACIÓN REQUERIDA. Acceso al NÚCLEO restringido.\n\nSoy A.L.I.C.E. Protocolo de seguridad activo.\nPara desbloquear el paquete, responderás a una secuencia de verificación.\n\nFASE 1: ¿Cuándo fue vuestro primer beso? (Fecha exacta)"
    })

if "gift_unlocked" not in st.session_state:
    st.session_state.gift_unlocked = False

# --- C. SYSTEM PROMPT ---
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

# --- D. INTERFAZ DE CHAT ---
# Renderizar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de usuario
if prompt := st.chat_input("Introducir credencial..."):
    # 0. Backdoor de desarrollador
    if prompt == "sudo_unlock_99":
        st.session_state.gift_unlocked = True
        st.session_state.messages.append({"role": "user", "content": "sudo_unlock_99"})
        st.session_state.messages.append({"role": "assistant", "content": "BACKDOOR ACCESS GRANTED. WELCOME ADMIN."})
        st.rerun()

    # 1. Mostrar mensaje usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Construir historial para Gemini (Stateless format)
    gemini_history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})
    
    # 3. Llamada al modelo con manejo de errores manual
    with st.chat_message("assistant"):
        with st.spinner("ANALYZING INPUT..."):
            try:
                # Usamos models/gemini-2.0-flash (Serie 2.0 requerida por API Key)
                model = genai.GenerativeModel(
                    model_name='models/gemini-2.0-flash',
                    system_instruction=system_instruction
                )
                
                response = model.generate_content(gemini_history)
                response_text = response.text
                
                # --- Lógica de Desbloqueo (Keyword Trigger) ---
                if "ACCESS_LEVEL_ALPHA_UNLOCKED" in response_text:
                    st.session_state.gift_unlocked = True
                    # Limpiamos la clave para que no se vea feo
                    response_text = response_text.replace("ACCESS_LEVEL_ALPHA_UNLOCKED", "").strip()
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                # Forzar rerun si se desbloqueó para mostrar la imagen inmediatamente
                if st.session_state.gift_unlocked:
                    st.rerun()

            except Exception as e:
                st.markdown("---")
                st.warning("⚠ CONNECTION LOST")
                st.error(f"Error del sistema: {e}")
                st.markdown("El servidor ha rechazado la conexión. Por favor reintentar manualmente.")
                if st.button("REESTABLECER ENLACE"):
                    st.rerun()

# --- E. LÓGICA DE RENDERIZADO (DESBLOQUEO) ---
if st.session_state.gift_unlocked:
    st.markdown("---")
    st.success("🔓 SYSTEM OVERRIDE SUCCESSFUL. ARCHIVOS DESENCRIPTADOS.")
    
    image_path = "images/JumpYard.jpg"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption="JUMP YARD ACCESS PASS // TIER 1 AUTHORIZATION", use_container_width=True)
        st.balloons()
    else:
        st.error(f"FATAL ERROR: Archivo {image_path} corroído o no encontrado.")

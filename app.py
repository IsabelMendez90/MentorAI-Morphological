import streamlit as st
from openai import OpenAI
import json
import pandas as pd
import re
from datetime import datetime
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


# Leer la API Key desde Streamlit Secrets
API_KEY = st.secrets["OPENROUTER_API_KEY"]
API_BASE = "https://openrouter.ai/api/v1"
MODEL_NAME = "deepseek/deepseek-r1:free"

# Inicializar cliente
client = OpenAI(api_key=API_KEY, base_url=API_BASE)

# Configuración de la app
st.set_page_config(page_title="Prueba de conexión con LLM", layout="centered")
st.title("🔍 Test de conexión con el modelo")

# Área de input del usuario
user_input = st.text_input("Escribe algo para probar el modelo:")

if st.button("Enviar"):
    if user_input.strip():
        with st.spinner("Consultando al modelo..."):
            try:
                mensajes = [
                    {"role": "system", "content": "Eres un asistente amigable."},
                    {"role": "user", "content": user_input}
                ]
                respuesta = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=mensajes,
                    extra_headers={
                        "HTTP-Referer": "https://tu-app.streamlit.app/",
                        "X-Title": "Prueba de conexión"
                    }
                )
                if respuesta and respuesta.choices:
                    st.success("✅ Respuesta del modelo:")
                    st.write(respuesta.choices[0].message.content)
                else:
                    st.warning("⚠️ El modelo no devolvió ninguna respuesta.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Por favor, escribe algo antes de enviar.")

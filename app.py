import os
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError


# Configuración de la página
st.set_page_config(
    page_title="App Azure + ACR + MongoDB Atlas",
    page_icon="🚀",
    layout="wide"
)


def consultar_hora_mongodb():
    """
    Consulta la hora del servidor de MongoDB Atlas sin crear colecciones
    ni insertar documentos.
    """
    mongo_uri = os.getenv("MONGODB_URI")

    if not mongo_uri:
        return {
            "ok": False,
            "mensaje": "No se encontró la variable de entorno MONGODB_URI en Azure Web App.",
            "hora": None
        }

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

        # El comando hello consulta metadata del servidor.
        # No crea base de datos, no crea colección y no inserta documentos.
        resultado = client.admin.command("hello")

        hora_mongo = resultado.get("localTime")

        return {
            "ok": True,
            "mensaje": "Conexión exitosa a MongoDB Atlas.",
            "hora": hora_mongo
        }

    except ServerSelectionTimeoutError as e:
        return {
            "ok": False,
            "mensaje": f"No se pudo conectar a MongoDB Atlas. Revisa Network Access, usuario, password o URI. Detalle: {e}",
            "hora": None
        }

    except PyMongoError as e:
        return {
            "ok": False,
            "mensaje": f"Error de MongoDB: {e}",
            "hora": None
        }

    except Exception as e:
        return {
            "ok": False,
            "mensaje": f"Error general: {e}",
            "hora": None
        }


# Título principal
st.title("🚀 App Streamlit en Azure Web App + Docker + ACR + MongoDB Atlas")
st.markdown("---")

st.info(
    "Esta aplicación está desplegada en Azure Web App como contenedor desde Azure Container Registry "
    "y consulta la hora del sistema desde MongoDB Atlas usando una variable de entorno."
)

# Sección MongoDB Atlas
st.header("🟢 Validación de conexión a MongoDB Atlas")

st.write(
    "La app no crea colecciones ni inserta registros. Solo ejecuta el comando `hello` "
    "para obtener la hora del servidor MongoDB."
)

if st.button("Consultar hora del servidor MongoDB"):
    respuesta = consultar_hora_mongodb()

    if respuesta["ok"]:
        st.success(respuesta["mensaje"])

        hora = respuesta["hora"]

        if hora:
            st.metric("Hora MongoDB Atlas UTC", hora.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            st.warning("La conexión fue exitosa, pero MongoDB no devolvió localTime.")

    else:
        st.error(respuesta["mensaje"])

st.markdown("---")

# Sidebar
st.sidebar.header("Configuración")
nombre = st.sidebar.text_input("Tu nombre:", "Usuario")
edad = st.sidebar.slider("Tu edad:", 1, 100, 25)

# Contenido principal de demo
col1, col2 = st.columns(2)

with col1:
    st.header(f"¡Hola {nombre}!")
    st.write(f"Tienes {edad} años")

    if st.button("Generar datos aleatorios"):
        st.success("¡Datos generados exitosamente!")

with col2:
    st.header("📊 Gráfico de ejemplo")

    data = pd.DataFrame({
        "x": range(10),
        "y": np.random.randn(10).cumsum(),
        "categoria": np.random.choice(["A", "B", "C"], 10)
    })

    fig = px.line(
        data,
        x="x",
        y="y",
        color="categoria",
        title="Datos Aleatorios"
    )

    st.plotly_chart(fig, use_container_width=True)

# Métricas
st.markdown("---")
st.header("📈 Métricas de ejemplo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Usuarios", "1,234", "12%")

with col2:
    st.metric("Ventas", "$5,678", "-2%")

with col3:
    st.metric("Conversión", "3.4%", "0.5%")

with col4:
    st.metric("Satisfacción", "4.8/5", "0.2")

# Tabla de datos
st.markdown("---")
st.header("📋 Tabla de Datos")
st.dataframe(data, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Aplicación creada con Streamlit, Docker, ACR, Azure Web App y MongoDB Atlas** 🐳")

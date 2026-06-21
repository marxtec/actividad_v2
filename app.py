import streamlit as st

# Título de la app
st.title("Calculadora de IMC 💪")

st.write("Esta aplicación calcula tu Índice de Masa Corporal (IMC) y determina tu nivel de peso.")

# Entradas de usuario
peso = st.number_input("Ingresa tu peso (kg):", min_value=0.0, format="%.2f")
estatura = st.number_input("Ingresa tu estatura (m):", min_value=0.0, format="%.2f")

# Calcular IMC
if st.button("Calcular IMC"):
    if peso > 0 and estatura > 0:
        imc = peso / (estatura ** 2)

        st.write(f"Tu IMC es: **{imc:.2f}**")

        # Clasificación según la OMS
        if imc < 18.5:
            st.info("Bajo peso 🟡")
        elif 18.5 <= imc < 25:
            st.success("Peso normal ✅")
        elif 25 <= imc < 30:
            st.warning("Sobrepeso 🟠")
        else:
            st.error("Obesidad 🔴")
    else:
        st.warning("Por favor, ingresa valores válidos.")

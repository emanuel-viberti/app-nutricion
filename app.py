import streamlit as st
import pandas as pd

st.title("Generador de Planes Nutricionales 🍏")

# --- 1. DATOS DEL PACIENTE ---
st.header("1. Datos del Paciente")
col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre del paciente")
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    edad = st.number_input("Edad", min_value=15, max_value=100, step=1)
with col2:
    peso = st.number_input("Peso Actual (kg)", min_value=30.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", min_value=100.0, step=0.1)
    af = st.selectbox("Nivel de Actividad Física", ["Sedentario", "Leve", "Moderado", "Intenso"])

# --- 2. CÁLCULOS Y DIAGNÓSTICO ---
if st.button("Calcular Diagnóstico y Requerimientos"):
    if peso > 0 and talla_cm > 0:
        talla_m = talla_cm / 100
        imc = peso / (talla_m ** 2)
        
        # Diagnóstico OMS
        if imc < 18.5: diag = "Delgadez"
        elif 18.5 <= imc <= 24.9: diag = "Peso normal, sano o saludable"
        elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
        elif 30.0 <= imc <= 34.9: diag = "Obesidad grado I"
        elif 35.0 <= imc <= 39.9: diag = "Obesidad grado II"
        else: diag = "Obesidad grado III"
        
        st.success(f"**IMC:** {imc:.2f} - **Diagnóstico OMS:** {diag}")
        
        # Objetivos y Prescripción
        st.info("**Objetivos:** Descender el peso, modificar los hábitos alimentarios, incorporar AF, mantener a través del tiempo el peso perdido.\n\n**Prescripción:** Plan de alimentación hipocalórico.")

        # Cálculo de Peso Ideal (Fórmula de Brocca)
        if sexo == "Masculino":
            pi_calc = talla_cm - 100
        else:
            pi_calc = (talla_cm - 100) - ((talla_cm - 100) * 0.10)
            
        st.write("---")
        st.header("2. Pesos y Requerimientos")
        
        # Editables según diagnóstico
        if imc < 25:
            peso_usar = st.number_input("Peso Ideal (Broca) - Editable:", value=float(pi_calc), step=0.5)
        else:
            pic_calc = ((peso - pi_calc) * 0.25) + pi_calc
            peso_usar = st.number_input("Peso Ideal Corregido (Wilkens) - Editable:", value=float(pic_calc), step=0.5)

        # Kcal Diarias (Fórmula de Knox simplificada 22 * Peso)
        kcal_diarias = 22 * peso_usar
        kcal_final = st.number_input("Kcal Diarias recomendadas (Editable):", value=float(kcal_diarias), step=50.0)
        
        # Distribución de Macronutrientes
        st.write("**Distribución sugerida de Macronutrientes:**")
        st.write(f"- Carbohidratos (55%): {(kcal_final * 0.55 / 4):.0f} g")
        st.write(f"- Proteínas (17.5%): {(kcal_final * 0.175 / 4):.0f} g")
        st.write(f"- Grasas (27.5%): {(kcal_final * 0.275 / 9):.0f} g")
        
        st.write("*(En la próxima fase conectaremos esto con tu base de datos de 100 platos para armar el menú y generar el PDF)*")

import streamlit as st

st.set_page_config(page_title="NutriAsistente", layout="wide")

st.title("Generador de Planes Nutricionales 🍏")

# --- 1. DATOS DEL PACIENTE ---
st.header("1. Datos del Paciente")
col1, col2, col3 = st.columns(3)
with col1:
    nombre = st.text_input("Nombre del paciente")
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
with col2:
    peso = st.number_input("Peso Actual (kg)", min_value=30.0, value=70.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", min_value=100.0, value=165.0, step=0.1)
with col3:
    edad = st.number_input("Edad", min_value=15, max_value=100, value=30, step=1)
    af = st.selectbox("Nivel de Actividad Física", ["Sedentario", "Leve", "Moderado", "Intenso"])

# --- 2. CÁLCULOS LÓGICOS ---
talla_m = talla_cm / 100
imc = peso / (talla_m ** 2)

if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Peso normal"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
elif 30.0 <= imc <= 34.9: diag = "Obesidad grado I"
elif 35.0 <= imc <= 39.9: diag = "Obesidad grado II"
else: diag = "Obesidad grado III"

# Lógica de Peso Ideal
if sexo == "Masculino":
    pi_base = talla_cm - 100
else:
    pi_base = (talla_cm - 100) * 0.90

st.divider()

# --- 3. PESO OBJETIVO (EDITABLE) ---
st.header("2. Determinación de Peso Objetivo")
if imc < 25:
    st.info("Diagnóstico: Normopeso o inferior. Se sugiere Peso Ideal (Broca).")
    peso_objetivo = st.number_input("Peso Ideal (Broca) - Editable", value=float(pi_base), step=0.5)
else:
    st.info(f"Diagnóstico: {diag}. Se sugiere Peso Ideal Corregido (Wilkens).")
    pic_base = ((peso - pi_base) * 0.25) + pi_base
    peso_objetivo = st.number_input("Peso Ideal Corregido (Wilkens) - Editable", value=float(pic_base), step=0.5)

# --- 4. RESULTADOS (NO EDITABLES) ---
kcal_final = peso_objetivo * 22
cho_g = (kcal_final * 0.55) / 4
pro_g = (kcal_final * 0.175) / 4
gra_g = (kcal_final * 0.275) / 9

st.divider()
st.header("3. Prescripción y Objetivos")

# Diseño con columnas de texto para que no se corte
res1, res2 = st.columns(2)

with res1:
    st.subheader("🎯 Objetivos")
    st.write("- Descender el peso corporal.")
    st.write("- Modificar hábitos alimentarios.")
    st.write("- Incorporar actividad física regular.")
    st.write("- Mantener el peso perdido a largo plazo.")

with res2:
    st.subheader("📋 Prescripción")
    st.write(f"**Plan de alimentación:** Hipocalórico (basado en {peso_objetivo} kg).")
    st.write(f"**Valor Calórico Total:** {kcal_final:.0f} kcal/día.")
    st.write(f"**Distribución:** CHO 55%, PRO 17.5%, GRA 27.5%.")

st.info("💡 **Macronutrientes en gramos:**")
m1, m2, m3 = st.columns(3)
m1.write(f"🍞 **CHO:** {cho_g:.1f} g")
m2.write(f"🥩 **PRO:** {pro_g:.1f} g")
m3.write(f"🥑 **GRA:** {gra_g:.1f} g")

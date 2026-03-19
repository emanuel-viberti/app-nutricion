import streamlit as st

st.set_page_config(page_title="NutriAsistente - Diagnóstico", layout="centered")

st.title("Generador de Planes Nutricionales 🍏")

# --- 1. DATOS DEL PACIENTE ---
st.header("1. Datos del Paciente")
col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre del paciente")
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    edad = st.number_input("Edad", min_value=15, max_value=100, value=30, step=1)
with col2:
    peso = st.number_input("Peso Actual (kg)", min_value=30.0, value=70.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", min_value=100.0, value=165.0, step=0.1)
    af = st.selectbox("Nivel de Actividad Física", ["Sedentario", "Leve", "Moderado", "Intenso"])

# --- 2. CÁLCULOS AUTOMÁTICOS ---
talla_m = talla_cm / 100
imc = peso / (talla_m ** 2)

# Determinar diagnóstico OMS
if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Peso normal"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
elif 30.0 <= imc <= 34.9: diag = "Obesidad grado I"
elif 35.0 <= imc <= 39.9: diag = "Obesidad grado II"
else: diag = "Obesidad grado III"

st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")

# Lógica de Peso Ideal según documento
if sexo == "Masculino":
    pi_base = talla_cm - 100
else:
    pi_base = (talla_cm - 100) * 0.90

st.write("---")
st.header("2. Prescripción y Requerimientos")

# Selección de Peso para el cálculo (Editable)
if imc < 25:
    peso_objetivo = st.number_input("Peso Ideal (Fórmula de Broca) - Ajustable:", value=float(pi_base), step=0.5)
else:
    pic_base = ((peso - pi_base) * 0.25) + pi_base
    peso_objetivo = st.number_input("Peso Ideal Corregido (Wilkens) - Ajustable:", value=float(pic_base), step=0.5)

# --- CÁLCULOS DERIVADOS (No editables, automáticos) ---
# Usamos 22 kcal/kg como base según el documento para descenso
kcal_final = peso_objetivo * 22

# Distribución de Macros (Rangos del documento)
# CHO: 55%, PRO: 17.5%, GRA: 27.5%
cho_g = (kcal_final * 0.55) / 4
pro_g = (kcal_final * 0.175) / 4
gra_g = (kcal_final * 0.275) / 9

# Mostrar resultados al nutricionista
c1, c2, c3 = st.columns(3)
c1.metric("Calorías Diarias", f"{kcal_final:.0f} kcal")
c2.metric("Objetivo", "Descenso de peso" if imc >= 25 else "Mantenimiento")
c3.metric("Fórmula", "Hipocalórica" if imc >= 25 else "Normocalórica")

st.info("**Distribución de Macronutrientes Sugerida:**")
col_a, col_b, col_c = st.columns(3)
col_a.write(f"🍞 **Carbohidratos (55%):** {cho_g:.1f} g")
col_b.write(f"🥩 **Proteínas (17.5%):** {pro_g:.1f} g")
col_c.write(f"🥑 **Grasas (27.5%):** {gra_g:.1f} g")

st.warning("⚠️ Nota: Al modificar el Peso (PI/PIC) arriba, estos valores se actualizan automáticamente.")

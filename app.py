import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente Pro", layout="wide")

# --- BASE DE DATOS DE PLATOS (MAQUETA) ---
if 'db_platos' not in st.session_state:
    st.session_state.db_platos = [
        {"nombre": "Tostadas integrales con palta y huevo", "tipo": "dym", "kcal": 350, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "Yogur con granola y almendras", "tipo": "dym", "kcal": 320, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "Omelette de queso y espinaca con 1 fruta", "tipo": "dym", "kcal": 310, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "Pechuga al limón con puré de calabaza y gelatina", "tipo": "ayc", "kcal": 550, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "Merluza al horno con ensalada mixta y 1 manzana", "tipo": "ayc", "kcal": 500, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "Wok de vegetales y tofu/pollo con 1 naranja", "tipo": "ayc", "kcal": 520, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "Sandwich integral de atún y tomate (Fácil)", "tipo": "trabajo", "kcal": 450, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "Ensalada de arroz y legumbres en frasco", "tipo": "trabajo", "kcal": 480, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "1 Fruta de estación", "tipo": "colacion", "kcal": 80, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"},
        {"nombre": "Yogur descremado", "tipo": "colacion", "kcal": 90, "macros": "CHO: 55%, PRO: 17%, GRA: 28%"}
    ]

if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {}

def obtener_plato(tipo):
    opciones = [p for p in st.session_state.db_platos if p['tipo'] == tipo]
    return random.choice(opciones) if opciones else {"nombre": "Plato no encontrado", "kcal": 0}

# --- 1. DATOS DEL PACIENTE ---
st.title("Generador de Planes Nutricionales 🍏")
st.header("1. Evaluación y Diagnóstico")

col1, col2, col3 = st.columns(3)
with col1:
    nombre = st.text_input("Nombre del paciente", "Paciente Ejemplo")
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
with col2:
    peso = st.number_input("Peso Actual (kg)", min_value=30.0, value=85.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", min_value=100.0, value=170.0, step=0.1)
with col3:
    edad = st.number_input("Edad", min_value=15, max_value=100, value=35, step=1)
    af = st.selectbox("Nivel de Actividad Física", ["Sedentario", "Leve", "Moderado", "Intenso"])

# Lógica IMC y Diagnóstico
talla_m = talla_cm / 100
imc = peso / (talla_m ** 2)

if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Peso normal"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
elif 30.0 <= imc <= 34.9: diag = "Obesidad grado I"
elif 35.0 <= imc <= 39.9: diag = "Obesidad grado II"
else: diag = "Obesidad grado III"

st.subheader(f"Resultado: {diag} (IMC: {imc:.2f})")
st.divider()

# --- 2. OBJETIVOS Y PESO ---
st.header("2. Peso Objetivo y Requerimientos")
c_obj1, c_obj2 = st.columns(2)

# Cálculo de PI o PIC
pi_broca = (talla_cm - 100) if sexo == "Masculino" else (talla_cm - 100) * 0.90

with c_obj1:
    if imc < 25:
        st.info("Sugerencia: Peso Ideal (Broca)")
        peso_final = st.number_input("Peso Objetivo (Editable):", value=float(pi_broca), step=0.5)
    else:
        pic_wilkens = ((peso - pi_broca) * 0.25) + pi_broca
        st.info("Sugerencia: Peso Ideal Corregido (Wilkens)")
        peso_final = st.number_input("Peso Objetivo (Editable):", value=float(pic_wilkens), step=0.5)

with c_obj2:
    kcal_final = peso_final * 22
    st.write(f"**Prescripción:** Plan Hipocalórico de **{kcal_final:.0f} kcal/día**")
    st.write(f"**Distribución Macros:** CHO 55%, PRO 17.5%, GRA 27.5%")

st.divider()

# --- 3. CONFIGURACIÓN DEL MENÚ ---
st.header("3. Configuración del Plan Semanal")
col_conf1, col_conf2 = st.

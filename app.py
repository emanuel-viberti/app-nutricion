import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente Pro", layout="wide")

# --- BASE DE DATOS DE 100 PLATOS ---
if 'db_platos' not in st.session_state:
    # Definimos listas para llegar a los 100 platos (50 AyC, 30 DyM, 10 Col, 10 Trab)
    dym = [f"Opción Desayuno/Merienda {i}" for i in range(1, 31)]
    ayc = [f"Plato Almuerzo/Cena con postre {i}" for i in range(1, 51)]
    trabajo = [f"Almuerzo práctico para trabajo {i}" for i in range(1, 11)]
    colaciones = [f"Colación saludable {i}" for i in range(1, 11)]

    # Convertimos a formato de diccionario con kcal estimadas para que el sistema opere
    st.session_state.db_platos = []
    for p in dym: st.session_state.db_platos.append({"nombre": p, "tipo": "dym", "kcal": random.randint(300, 350)})
    for p in ayc: st.session_state.db_platos.append({"nombre": p, "tipo": "ayc", "kcal": random.randint(500, 600)})
    for p in trabajo: st.session_state.db_platos.append({"nombre": p, "tipo": "trabajo", "kcal": random.randint(400, 500)})
    for p in colaciones: st.session_state.db_platos.append({"nombre": p, "tipo": "colacion", "kcal": random.randint(80, 120)})

if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {}

def obtener_plato(tipo, usados):
    opciones = [p for p in st.session_state.db_platos if p['tipo'] == tipo and p['nombre'] not in usados]
    if not opciones: # Si se acaban las opciones sin repetir, resetear usados
        opciones = [p for p in st.session_state.db_platos if p['tipo'] == tipo]
    plato = random.choice(opciones)
    usados.add(plato['nombre'])
    return plato

# --- 1. DATOS DEL PACIENTE ---
st.title("Generador de Planes Nutricionales 🍏")
st.header("1. Evaluación y Diagnóstico")

col1, col2, col3 = st.columns(3)
with col1:
    nombre = st.text_input("Nombre del paciente", "Paciente Ejemplo")
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
with col2:
    peso_actual = st.number_input("Peso Actual (kg)", min_value=30.0, value=75.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", min_value=100.0, value=160.0, step=0.1)
with col3:
    edad = st.number_input("Edad", min_value=15, max_value=100, value=30, step=1)
    af_opciones = {"Sedentario": 1.2, "Leve": 1.3, "Moderado": 1.5, "Intenso": 1.7}
    af_label = st.selectbox("Nivel de Actividad Física", list(af_opciones.keys()))
    af_valor = af_opciones[af_label]

# Diagnóstico IMC
talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Normopeso"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
else: diag = "Obesidad"

st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")
st.divider()

# --- 2. CÁLCULO DE PESO IDEAL CORREGIDO (BROCA/WILKENS) ---
st.header("2. Prescripción")

# CORRECCIÓN PI BROCA SEGÚN SEXO
base_broca = talla_cm - 100
if sexo == "Femenino":
    pi_resultado = base_broca * 0.90  # Menos el 10%
else:
    pi_resultado = base_broca

c_p1, c_p2 = st.columns(2)
with c_p1:
    if imc < 25:
        label_p = "Peso Ideal (Broca)"
        p_obj = st.number_input(f"{label_p} - Editable", value=float(pi_resultado))
    else:
        label_p = "Peso Ideal Corregido (Wilkens)"
        pic_wilkens = ((peso_actual - pi_resultado) * 0.25) + pi_resultado
        p_obj = st.number_input(f"{label_p} - Editable", value=float(pic_wilkens))

with c_p2:
    # Kcal corregidas por AF
    kcal_base = p_obj * 22
    kcal_final = kcal_base * af_valor
    st.info(f"**Calorías Diarias:** {kcal_final:.0f} kcal")
    st.write(f"**Macros:** CHO 55% | PRO 17.5% | GRA 27.5%")

st.divider()

# --- 3. MENÚ ---
st.header("3. Plan Semanal")
c1, c2, c3 = st.columns(3)
alm_trabajo = c1.checkbox("Almuerzo en el trabajo")
colaciones_on = c2.checkbox("Añadir colaciones")

if st.button("🚀 GENERAR PLAN"):
    usados = set()
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for d in dias:
        tipo_a = "trabajo" if alm_trabajo else "ayc"
        st.session_state.menu_semanal[d] = {
            "Desayuno": obtener_plato("dym", usados),
            "Almuerzo": obtener_plato(tipo_a, usados),
            "Merienda": obtener_plato("dym", usados),
            "Cena": obtener_plato("ayc", usados),
            "Colaciones": [obtener_plato("colacion", usados), obtener_plato("colacion", usados)] if colaciones_on else []
        }

if st.session_state.menu_semanal:
    for dia, comidas in st.session_state.menu_semanal.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for c in plato: st.write(f"🔸 **Colación:** {c['nombre']}")
                else:
                    ci, cb = st.columns([0.9, 0.1])
                    ci.write(f"🍴 **{tiempo}:** {plato['nombre']}")
                    if cb.button("🔄", key=f"sw_{dia}_{tiempo}"):
                        t = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and alm_trabajo) else "ayc")
                        st.session_state.menu_semanal[dia][tiempo] = obtener_plato(t, set())
                        st.rerun()

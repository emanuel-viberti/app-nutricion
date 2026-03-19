import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente Pro", layout="wide")

# --- BASE DE DATOS DE PLATOS ---
if 'db_platos' not in st.session_state:
    st.session_state.db_platos = [
        {"nombre": "Tostadas integrales con palta y huevo", "tipo": "dym", "kcal": 350},
        {"nombre": "Yogur con granola y almendras", "tipo": "dym", "kcal": 320},
        {"nombre": "Omelette de queso y espinaca con 1 fruta", "tipo": "dym", "kcal": 310},
        {"nombre": "Pechuga al limón con puré de calabaza y gelatina", "tipo": "ayc", "kcal": 550},
        {"nombre": "Merluza al horno con ensalada mixta y 1 manzana", "tipo": "ayc", "kcal": 500},
        {"nombre": "Wok de vegetales y pollo con 1 naranja", "tipo": "ayc", "kcal": 520},
        {"nombre": "Sandwich integral de atún y tomate (Fácil)", "tipo": "trabajo", "kcal": 450},
        {"nombre": "Ensalada de arroz y legumbres en frasco", "tipo": "trabajo", "kcal": 480},
        {"nombre": "1 Fruta de estación", "tipo": "colacion", "kcal": 80},
        {"nombre": "Yogur descremado", "tipo": "colacion", "kcal": 90}
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
    peso_actual = st.number_input("Peso Actual (kg)", min_value=30.0, value=85.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", min_value=100.0, value=170.0, step=0.1)
with col3:
    edad = st.number_input("Edad", min_value=15, max_value=100, value=35, step=1)
    # Definimos los valores de AF
    af_opciones = {"Sedentario": 1.2, "Leve": 1.375, "Moderado": 1.55, "Intenso": 1.725}
    af_label = st.selectbox("Nivel de Actividad Física", list(af_opciones.keys()))
    af_valor = af_opciones[af_label]

# Lógica IMC y Diagnóstico
talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)

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
        st.write("**Sugerencia:** Peso Ideal (Broca)")
        peso_objetivo = st.number_input("Peso Objetivo (Editable):", value=float(pi_broca), key="p_obj")
    else:
        pic_wilkens = ((peso_actual - pi_broca) * 0.25) + pi_broca
        st.write("**Sugerencia:** Peso Ideal Corregido (Wilkens)")
        peso_objetivo = st.number_input("Peso Objetivo (Editable):", value=float(pic_wilkens), key="p_obj")

with c_obj2:
    # NUEVA FÓRMULA: Kcal Base (22) * Peso Objetivo * Factor AF
    kcal_final = (peso_objetivo * 22) * (1 + (af_valor - 1) * 0.5) 
    # Nota: Usamos un ajuste moderado del factor AF para planes de descenso
    
    st.write(f"**Prescripción:** Plan Hipocalórico")
    st.info(f"🔥 **{kcal_final:.0f} kcal/día** (Ajustado por AF {af_label})")
    
    # Cálculo de Macros
    cho_g = (kcal_final * 0.55) / 4
    pro_g = (kcal_final * 0.175) / 4
    gra_g = (kcal_final * 0.275) / 9
    
    st.write(f"**Macros:** CHO: {cho_g:.0f}g | PRO: {pro_g:.0f}g | GRA: {gra_g:.0f}g")

st.divider()

# --- 3. CONFIGURACIÓN Y MENÚ ---
st.header("3. Plan Semanal")
c_conf1, c_conf2, c_conf3 = st.columns([1, 1, 1])
with c_conf1:
    alm_trabajo = st.checkbox("¿Almuerzo en el trabajo?")
with c_conf2:
    colaciones_activas = st.checkbox("Añadir 2 colaciones diarias")
with c_conf3:
    btn_generar = st.button("🚀 GENERAR PLAN")

if btn_generar:
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for dia in dias:
        tipo_alm = "trabajo" if alm_trabajo else "ayc"
        st.session_state.menu_semanal[dia] = {
            "Desayuno": obtener_plato("dym"),
            "Almuerzo": obtener_plato(tipo_alm),
            "Merienda": obtener_plato("dym"),
            "Cena": obtener_plato("ayc"),
            "Colaciones": [obtener_plato("colacion"), obtener_plato("colacion")] if colaciones_activas else []
        }

if st.session_state.menu_semanal:
    for dia, comidas in st.session_state.menu_semanal.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for col in plato:
                        st.write(f"🔸 **Colación:** {col['nombre']} ({col['kcal']} kcal)")
                else:
                    ci, cb = st.columns([0.9, 0.1])
                    ci.write(f"🍴 **{tiempo}:** {plato['nombre']} ({plato['kcal']} kcal)")
                    if cb.button("🔄", key=f"sw_{dia}_{tiempo}"):
                        t = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and alm_trabajo) else "ayc")
                        st.session_state.menu_semanal[dia][tiempo] = obtener_plato(t)
                        st.rerun()

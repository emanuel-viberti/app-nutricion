import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente AR Pro", layout="wide")

# --- 1. CONFIGURACIÓN DEL PROFESIONAL ---
st.sidebar.header("Datos del Profesional")
nombre_nutri = st.sidebar.text_input("Nombre y Apellido", "Lic. en Nutrición")
matricula = st.sidebar.text_input("Matrícula Profesional", "M.P. 1234")
contacto = st.sidebar.text_input("Contacto (Cel/Email)", "contacto@nutri.com")

# --- 2. BASE DE DATOS DETALLADA ---
def cargar_base_datos():
    # Ejemplo de estructura detallada (puedes seguir completando hasta los 100)
    ayc = [
        {
            "nombre": "Milanesa de peceto con puré de calabaza",
            "porcion": "1 unidad mediana y 1 taza de té de puré",
            "preparacion": "Cocinar la milanesa al horno con rocío vegetal. El puré debe ser sin manteca, solo con una pizca de sal y pimienta.",
            "tipo": "ayc"
        },
        {
            "nombre": "Filet de merluza al limón con ensalada",
            "porcion": "1 filet grande y 1 plato playo de ensalada de rúcula/tomate",
            "preparacion": "Cocinar el pescado a la plancha con limón y hierbas. Condimentar la ensalada con 1 cdita de aceite de oliva.",
            "tipo": "ayc"
        },
        {
            "nombre": "Tarta de zapallitos (sin tapa)",
            "porcion": "1 unidad (1/4 de tarta)",
            "preparacion": "Usar solo la base. Relleno: zapallitos salteados, cebolla, 1 huevo y queso magro rallado. Hornear hasta dorar.",
            "tipo": "ayc"
        }
    ]
    
    dym = [
        {
            "nombre": "Infusión con tostadas integrales y queso",
            "porcion": "1 taza de infusión y 2 unidades de pan integral",
            "preparacion": "Untar con 1 cda sopera de queso blanco descremado. Se puede agregar edulcorante a la infusión.",
            "tipo": "dym"
        },
        {
            "nombre": "Yogur con granola y banana",
            "porcion": "1 pote de yogur, 2 cdas de granola y 1/2 unidad de banana",
            "preparacion": "Mezclar en un bowl. Preferir yogur descremado sin azúcar.",
            "tipo": "dym"
        }
    ]

    colaciones = [
        {"nombre": "Fruta de estación", "porcion": "1 unidad mediana", "preparacion": "Lavar bien y consumir con cáscara si es posible.", "tipo": "colacion"},
        {"nombre": "Yogur descremado", "porcion": "1 unidad (pote)", "preparacion": "Consumir preferentemente firme o bebible sin azúcar.", "tipo": "colacion"}
    ]

    return {"dym": dym, "ayc": ayc, "trabajo": ayc, "colacion": colaciones} # "trabajo" usa los mismos por ahora

if 'db_platos' not in st.session_state:
    st.session_state.db_platos = cargar_base_datos()

if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {}

# --- 3. LÓGICA CLÍNICA ---
st.title("Generador de Planes Nutricionales 🍏")
st.header("Evaluación y Diagnóstico")

col1, col2, col3 = st.columns(3)
with col1:
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    nombre_pac = st.text_input("Nombre del Paciente", "Paciente Ejemplo")
with col2:
    peso_actual = st.number_input("Peso Actual (kg)", value=80.0)
    talla_cm = st.number_input("Talla (cm)", value=170.0)
with col3:
    af_label = st.selectbox("Actividad Física", ["Sedentario", "Leve", "Moderado", "Intenso"])
    af_val = {"Sedentario": 1.2, "Leve": 1.3, "Moderado": 1.5, "Intenso": 1.7}[af_label]

# Diagnóstico e IMC
talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Normal"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
else: diag = "Obesidad"

# PI / PIC
pi_base = (talla_cm - 100) * (0.9 if sexo == "Femenino" else 1.0)
peso_final = ((peso_actual - pi_base) * 0.25) + pi_base if imc >= 25 else pi_base
kcal_final = (peso_final * 22) * af_val

st.subheader(f"Diagnóstico OMS: {diag} | IMC: {imc:.1f}")

st.divider()

# --- 4. GENERACIÓN DEL MENÚ ---
if st.button("🚀 GENERAR PLAN SEMANAL DETALLADO"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    nuevo_menu = {}
    for d in dias:
        nuevo_menu[d] = {
            "Desayuno": random.choice(st.session_state.db_platos["dym"]),
            "Almuerzo": random.choice(st.session_state.db_platos["ayc"]),
            "Merienda": random.choice(st.session_state.db_platos["dym"]),
            "Cena": random.choice(st.session_state.db_platos["ayc"]),
            "Colaciones": [random.choice(st.session_state.db_platos["colacion"])]
        }
    st.session_state.menu_semanal = nuevo_menu

# --- 5. VISUALIZACIÓN ---
if st.session_state.menu_semanal:
    st.header(f"Plan Alimentario para {nombre_pac}")
    st.info(f"Prescripción: {kcal_final:.0f} kcal | Objetivo: Descenso de peso")
    
    for dia, comidas in st.session_state.menu_semanal.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for p in plato:
                        st.write(f"🔸 **{tiempo}:** {p['nombre']} ({p['porcion']})")
                else:
                    st.write(f"🍴 **{tiempo}: {plato['nombre']}**")
                    st.write(f"📏 *Medida:* {plato['porcion']}")
                    st.write(f"📝 *Preparación:* {plato['preparacion']}")
                    st.divider()

    # --- BOTÓN DE DESCARGA (SIMULADO) ---
    st.button("💾 DESCARGAR PLAN PROFESIONAL (PDF)")

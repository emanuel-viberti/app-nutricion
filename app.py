import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente AR", layout="wide")

# --- 1. BASE DE DATOS ESTRUCTURADA (Medidas y Prep ocultas para el PDF) ---
def cargar_base_datos():
    ayc = [
        {"nombre": "Milanesa de peceto con puré de calabaza", "mh": "1 unid. med. y 1 taza de puré", "prep": "Al horno con rocío vegetal. Puré sin manteca."},
        {"nombre": "Filet de merluza al limón con ensalada", "mh": "1 filet grande y 1 plato playo de ensalada", "prep": "Pescado a la plancha. Vegetales crudos para más saciedad."},
        {"nombre": "Tarta de zapallitos (sin tapa)", "mh": "1/4 de unidad", "prep": "Masa integral solo base. Relleno con huevo y queso magro."},
        {"nombre": "Wok de pollo y vegetales", "mh": "1 plato playo colmado", "prep": "Saltear con poco aceite. Vegetales al dente."},
        {"nombre": "Fideos integrales con brócoli", "mh": "1 plato hondo cocido", "prep": "Fideos al dente con brócoli salteado en ajo."},
        {"nombre": "Bife de cuadril con ensalada mixta", "mh": "1 bife med. y 1 plato de vegetales", "prep": "Carne sin grasa visible a la plancha."}
    ]
    trabajo = [
        {"nombre": "Sándwich integral de pollo y rúcula", "mh": "2 rodajas de pan y 1 pechuga chica", "prep": "Sin aderezos grasos. Usar mostaza."},
        {"nombre": "Ensalada de arroz, atún y arvejas", "mh": "1 bowl mediano", "prep": "Atún al natural. Arroz integral preferentemente."},
        {"nombre": "Tarta de acelga y queso (vianda)", "mh": "1 porción grande", "prep": "Masa de salvado. Sin frituras previas."},
        {"nombre": "Wrap de carne y vegetales", "mh": "1 unidad grande", "prep": "Tortilla integral. Relleno de lomo y pimientos."}
    ]
    dym = [
        {"nombre": "Infusión con tostadas integrales y queso", "mh": "1 taza y 2 tostadas", "prep": "Queso blanco descremado. Edulcorante."},
        {"nombre": "Yogur descremado con granola y banana", "mh": "1 pote, 2 cdas granola, 1/2 banana", "prep": "Mezclar al momento."},
        {"nombre": "Mate cocido con leche y budín de avena", "mh": "1 taza y 1 rodaja med.", "prep": "Budín casero sin azúcar blanca."},
        {"nombre": "Tostado integral de queso magro", "mh": "2 rodajas de pan y 1 feta queso", "prep": "En sandwichera sin grasa."}
    ]
    col = [
        {"nombre": "Fruta de estación", "mh": "1 unidad med.", "prep": "Lavar bien, comer con cáscara."},
        {"nombre": "Yogur descremado", "mh": "1 pote", "prep": "Preferir sin azúcar."},
        {"nombre": "Huevo duro", "mh": "1 unidad", "prep": "Hervir 10 min."},
        {"nombre": "Gelatina diet", "mh": "1 compotera", "prep": "Sola o con trozos de fruta."}
    ]
    return {"dym": dym, "ayc": ayc, "trabajo": trabajo, "col": col}

if 'db' not in st.session_state: st.session_state.db = cargar_base_datos()
if 'menu' not in st.session_state: st.session_state.menu = {}

# --- 2. VALORACIÓN ANTROPOMÉTRICA ---
st.title("Generador Nutricional Profesional 🍏")
col1, col2, col3 = st.columns(3)
with col1:
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    nombre = st.text_input("Paciente", "Ejemplo")
with col2:
    peso = st.number_input("Peso (kg)", value=75.0)
    talla = st.number_input("Talla (cm)", value=160.0)
with col3:
    af_sel = st.selectbox("Actividad Física", ["Sedentario", "Leve", "Moderado", "Intenso"])
    af_val = {"Sedentario": 1.2, "Leve": 1.3, "Moderado": 1.5, "Intenso": 1.7}[af_sel]

# Lógica de Diagnóstico y Pesos [cite: 27, 67, 81]
imc = peso / ((talla/100)**2)
pi_broca = (talla - 100) * (0.9 if sexo == "Femenino" else 1.0)
if imc >= 25.0:
    p_obj = ((peso - pi_broca) * 0.25) + pi_broca
    diag, tipo_plan = "Sobrepeso/Obesidad", "Plan Hipocalórico"
elif imc < 18.5:
    p_obj = pi_broca
    diag, tipo_plan = "Delgadez", "Plan Hipercalórico"
else:
    p_obj = pi_broca
    diag, tipo_plan = "Normopeso", "Plan Normocalórico"

kcal = (p_obj * 22) * af_val

st.info(f"**Diagnóstico:** {diag} | **Objetivo:** {p_obj:.1f} kg | **Prescripción:** {tipo_plan} de {kcal:.0f} kcal")
st.divider()

# --- 3. GENERACIÓN DE MENÚ ---
c_a, c_b = st.columns(2)
en_trabajo = c_a.checkbox("Almuerzos en el trabajo")
con_col = c_b.checkbox("Incluir colaciones")

if st.button("🚀 GENERAR PLAN SEMANAL"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    tipo_alm = "trabajo" if en_trabajo else "ayc"
    st.session_state.menu = {d: {
        "Desayuno": random.choice(st.session_state.db["dym"]),
        "Almuerzo": random.choice(st.session_state.db[tipo_alm]),
        "Merienda": random.choice(st.session_state.db["dym"]),
        "Cena": random.choice(st.session_state.db["ayc"]),
        "Colaciones": [random.choice(st.session_state.db["col"])] if con_col else []
    } for d in dias}

# --- 4. LISTADO CON BOTONES DE INTERCAMBIO ---
if st.session_state.menu:
    for dia, comidas in st.session_state.menu.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for p in plato: st.write(f"🔸 **Colación:** {p['nombre']}")
                else:
                    cols = st.columns([0.9, 0.1])
                    cols[0].write(f"🍴 **{tiempo}:** {plato['nombre']}")
                    if cols[1].button("🔄", key=f"{dia}_{tiempo}"):
                        tipo = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and en_trabajo) else "ayc")
                        st.session_state.menu[dia][tiempo] = random.choice(st.session_state.db[tipo])
                        st.rerun()

    st.success("Plan listo. Los detalles de preparación se incluirán en la exportación a PDF.")

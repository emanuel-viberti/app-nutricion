import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente AR", layout="wide")

# --- 1. DATOS DEL NUTRICIONISTA (Sidebar) ---
st.sidebar.header("Configuración de Firma")
nombre_nutri = st.sidebar.text_input("Nombre y Apellido", "Lic. en Nutrición")
matricula = st.sidebar.text_input("Matrícula", "M.P. 0000")
contacto = st.sidebar.text_input("Contacto", "Email / Celular")

# --- 2. BASE DE DATOS (Nombres, Medidas y Prep) ---
def cargar_db():
    ayc = [
        {"nombre": "Milanesa de peceto con puré de calabaza", "mh": "1 unid. med. y 1 taza de puré", "prep": "Al horno con rocío vegetal. Puré sin manteca."},
        {"nombre": "Filet de merluza al limón con ensalada", "mh": "1 filet grande y 1 plato playo de vegetales", "prep": "Pescado a la plancha. Ensalada cruda."},
        {"nombre": "Tarta de zapallitos (sin tapa)", "mh": "1/4 de unidad", "prep": "Masa integral solo base. Relleno con huevo y queso magro."},
        {"nombre": "Wok de pollo y vegetales", "mh": "1 plato playo colmado", "prep": "Saltear con poco aceite. Vegetales al dente."},
        {"nombre": "Bife de cuadril con ensalada mixta", "mh": "1 bife med. y 1 plato de vegetales", "prep": "Carne sin grasa visible a la plancha."}
    ]
    trabajo = [
        {"nombre": "Sándwich integral de pollo y rúcula", "mh": "2 rodajas de pan y 1 pechuga chica", "prep": "Sin aderezos grasos."},
        {"nombre": "Ensalada de arroz, atún y arvejas", "mh": "1 bowl mediano", "prep": "Atún al natural."}
    ]
    dym = [
        {"nombre": "Infusión con tostadas integrales y queso", "mh": "1 taza y 2 tostadas", "prep": "Queso blanco descremado."},
        {"nombre": "Yogur descremado con granola y banana", "mh": "1 pote, 2 cdas granola, 1/2 banana", "prep": "Mezclar al momento."}
    ]
    col = [{"nombre": "Fruta de estación", "mh": "1 unidad med.", "prep": "Lavar bien."}, {"nombre": "Yogur descremado", "mh": "1 pote", "prep": "Sin azúcar."}]
    return {"dym": dym, "ayc": ayc, "trabajo": trabajo, "col": col}

if 'db' not in st.session_state: st.session_state.db = cargar_db()
if 'menu' not in st.session_state: st.session_state.menu = {}

# --- 3. EVALUACIÓN Y DIAGNÓSTICO ---
st.title("Generador Nutricional Profesional 🍏")
st.header("1. Evaluación y Diagnóstico")

c1, c2, c3 = st.columns(3)
with c1:
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    nombre_pac = st.text_input("Nombre del Paciente", "Paciente Ejemplo")
    edad = st.number_input("Edad", min_value=1, value=30)
with c2:
    peso_actual = st.number_input("Peso Actual (kg)", value=75.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", value=160.0, step=0.1)
with c3:
    af_sel = st.selectbox("Actividad Física", ["Sedentario", "Leve", "Moderado", "Intenso"])
    af_val = {"Sedentario": 1.2, "Leve": 1.3, "Moderado": 1.5, "Intenso": 1.7}[af_sel]

# Lógica IMC y Diagnóstico
talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag, t_plan = "Delgadez", "Plan Hipercalórico"
elif 18.5 <= imc <= 24.9: diag, t_plan = "Normopeso", "Plan Normocalórico"
elif 25.0 <= imc <= 29.9: diag, t_plan = "Sobrepeso", "Plan Hipocalórico"
else: diag, t_plan = "Obesidad", "Plan Hipocalórico"

st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")
st.divider()

# --- 4. PRESCRIPCIÓN (PI/PIC EDITABLE) ---
st.header("2. Prescripción")
pi_broca = (talla_cm - 100) * (0.9 if sexo == "Femenino" else 1.0)

if imc >= 25.0:
    val_sugerido = ((peso_actual - pi_broca) * 0.25) + pi_broca
    label_peso = "Peso Ideal Corregido (Wilkens)"
else:
    val_sugerido = pi_broca
    label_peso = "Peso Ideal (Broca)"

cp1, cp2 = st.columns(2)
with cp1:
    p_obj = st.number_input(f"{label_peso} - Editable", value=float(val_sugerido), key=f"p_{sexo}_{talla_cm}")

with cp2:
    kcal_final = (p_obj * 22) * af_val
    st.info(f"**Prescripción:** {t_plan} de {kcal_final:.0f} kcal/día")

st.divider()

# --- 5. MENÚ ---
st.header("3. Plan Semanal")
c_a, c_b = st.columns(2)
alm_trabajo = c_a.checkbox("Almuerzo en el trabajo")
colaciones_on = c_b.checkbox("Incluir colaciones")

if st.button("🚀 GENERAR PLAN"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    tipo_a = "trabajo" if alm_trabajo else "ayc"
    st.session_state.menu = {d: {
        "Desayuno": random.choice(st.session_state.db["dym"]),
        "Almuerzo": random.choice(st.session_state.db[tipo_a]),
        "Merienda": random.choice(st.session_state.db["dym"]),
        "Cena": random.choice(st.session_state.db["ayc"]),
        "Colaciones": [random.choice(st.session_state.db["col"])] if colaciones_on else []
    } for d in dias}

if st.session_state.menu:
    for dia, comidas in st.session_state.menu.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for p in plato: st.write(f"🔸 **Colación:** {p['nombre']}")
                else:
                    ci, cb = st.columns([0.9, 0.1])
                    ci.write(f"🍴 **{tiempo}:** {plato['nombre']}")
                    if cb.button("🔄", key=f"sw_{dia}_{tiempo}"):
                        t = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and alm_trabajo) else "ayc")
                        st.session_state.menu[dia][tiempo] = random.choice(st.session_state.db[t])
                        st.rerun()

st.divider()
st.button("💾 DESCARGAR PDF PROFESIONAL")

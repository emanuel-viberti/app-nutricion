import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente AR Pro", layout="wide")

# --- BASE DE DATOS DE 100 PLATOS CON LÓGICA DE PORCIONES ---
def cargar_base_datos():
    dym = [
        "Infusión con tostadas integrales y queso untable", "Yogur descremado con granola y banana",
        "Mate con galletitas de agua y queso por salut light", "Café con leche y macedonia de frutas",
        "Tostado de pan integral con queso y tomate", "Infusión con galletas de arroz y mermelada diet",
        "Yogur con nueces y avena", "Licuado de durazno y tostadas integrales",
        "Mate cocido con leche y budín de avena casero", "Té con limón y vainillas",
        "Omelette de claras con queso y fruta", "Infusión con bizcochos de avena caseros",
        "Yogur con cereales sin azúcar y frutillas", "Leche descremada con copos de maíz",
        "Tostada con huevo revuelto e infusión", "Sándwich de pan negro, queso y pepino",
        "Tostada con ricota descremada y limón", "Batido de proteínas (leche y fruta)",
        "Panqueque de avena con dulce de leche diet", "Ensalada de frutas con yogur"
    ]
    
    ayc = [
        "Milanesa de peceto al horno con puré de calabaza", "Filet de merluza con ensalada de rúcula y tomate",
        "Pollo al horno sin piel con vegetales asados", "Bife de cuadril magro con ensalada mixta",
        "Tarta de zapallitos (sin tapa superior)", "Canelones de verdura con salsa fileto",
        "Wok de pollo y vegetales", "Zapallitos rellenos con carne magra y queso",
        "Ensalada de lentejas, tomate y huevo", "Fideos integrales con brócoli y ajo",
        "Hamburguesa de lentejas con ensalada de repollo", "Cazuela de pollo con calabaza y arvejas",
        "Pastel de papa y carne magra", "Tortilla de espinaca al horno",
        "Arroz integral con atún y vegetales", "Brochetas de carne y verduras",
        "Calabaza rellena con choclo y queso", "Budín de zanahoria con hojas verdes",
        "Suprema a la mostaza con puré mixto", "Salpicón de ave completo",
        "Risotto de vegetales y hongos", "Costillita de cerdo magra con puré de manzana",
        "Guiso de lentejas saludable (sin embutidos)", "Albóndigas de pollo con arroz",
        "Pizza con masa integral y vegetales"
    ]

    trabajo = ["Sándwich integral de pollo", "Ensalada de arroz y atún", "Tarta de acelga", "Empanadas de verdura (2)", "Wrap de carne", "Ensalada de fideos", "Budín de zapallitos", "Milanesa de pollo al pan"]
    colaciones = ["1 Fruta de estación", "1 Yogur descremado", "Nueces/Almendras", "Barrita de cereal diet", "Postre de leche diet", "Queso magro", "Huevo duro", "Gelatina diet con frutas"]
    
    return {"dym": dym, "ayc": ayc, "trabajo": trabajo, "colacion": colaciones}

if 'db_platos' not in st.session_state:
    st.session_state.db_platos = cargar_base_datos()

if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {}

def elegir_plato(tipo, usados_hoy):
    lista = st.session_state.db_platos[tipo]
    opciones = [p for p in lista if p not in usados_hoy]
    elegido = random.choice(opciones if opciones else lista)
    usados_hoy.add(elegido)
    return elegido

# --- 1. DATOS DEL PACIENTE ---
st.title("Generador de Planes Nutricionales 🍏")
st.header("1. Evaluación y Diagnóstico")

c1, c2, c3 = st.columns(3)
with c1:
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    nombre = st.text_input("Nombre", "Paciente")
with c2:
    peso_actual = st.number_input("Peso Actual (kg)", value=75.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", value=160.0, step=0.1)
with c3:
    edad = st.number_input("Edad", value=30, min_value=1)
    af_opciones = {"Sedentario": 1.2, "Leve": 1.3, "Moderado": 1.5, "Intenso": 1.7}
    af_label = st.selectbox("Actividad Física", list(af_opciones.keys()))

talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Normopeso"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
else: diag = "Obesidad"
st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")
st.divider()

# --- 2. OBJETIVOS Y PRESCRIPCIÓN ---
st.header("2. Objetivos y Prescripción")

base_broca = talla_cm - 100
pi_sugerido = base_broca * 0.90 if sexo == "Femenino" else base_broca

if imc >= 25:
    valor_sugerido = ((peso_actual - pi_sugerido) * 0.25) + pi_sugerido
    tipo_peso = "Peso Ideal Corregido (Wilkens)"
else:
    valor_sugerido = pi_sugerido
    tipo_peso = "Peso Ideal (Broca)"

obj_col1, obj_col2 = st.columns(2)
with obj_col1:
    p_obj = st.number_input(f"{tipo_peso} - Sugerido", value=float(valor_sugerido), key=f"p_{sexo}_{talla_cm}")
    st.write("**Objetivos Terapéuticos:**")
    st.write("- Lograr un descenso de peso gradual y sostenible.")
    st.write("- Educación alimentaria y control de porciones.")
    st.write("- Aumento del gasto energético mediante AF.")

with obj_col2:
    kcal_final = (p_obj * 22) * af_opciones[af_label]
    st.success(f"**Prescripción Dietoterápica:**")
    st.write(f"Plan Alimentario Hipocalórico de **{kcal_final:.0f} kcal/día**.")
    st.write(f"Distribución: CHO 55% | PRO 17.5% | GRA 27.5%")
    st.write(f"Fibra: 25-30g/día. Hidratación: 2L de agua mínimo.")

st.divider()

# --- 3. MENÚ SEMANAL ---
st.header("3. Planificación del Menú")
col_c1, col_c2 = st.columns(2)
alm_trabajo = col_c1.checkbox("¿Almuerzos fuera de casa?")
colaciones_on = col_c2.checkbox("Incluir colaciones (Mañana/Tarde)")

if st.button("🚀 GENERAR PLAN SEMANAL INTELIGENTE"):
    usados = set()
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    tipo_a = "trabajo" if alm_trabajo else "ayc"
    
    st.session_state.menu_semanal = {d: {
        "Desayuno": elegir_plato("dym", usados),
        "Almuerzo": elegir_plato(tipo_a, usados),
        "Merienda": elegir_plato("dym", usados),
        "Cena": elegir_plato("ayc", usados),
        "Colaciones": [elegir_plato("colacion", usados), elegir_plato("colacion", usados)] if colaciones_on else []
    } for d in dias}

if st.session_state.menu_semanal:
    # Definir porción según Kcal totales
    if kcal_final < 1600: porcion = "Porción Moderada (Plato chico)"
    elif kcal_final < 2000: porcion = "Porción Estándar (Plato playo)"
    else: porcion = "Porción Abundante (+ Guarnición extra)"

    for dia, comidas in st.session_state.menu_semanal.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for p in plato: st.write(f"🔸 **Colación:** {p} + 1 vaso de agua")
                else:
                    ci, cb = st.columns([0.85, 0.15])
                    # Aquí la "magia" de la porción elástica
                    kcal_tiempo = kcal_final * (0.3 if tiempo in ["Almuerzo", "Cena"] else 0.2)
                    ci.write(f"🍴 **{tiempo}:** {plato}  \n  _({porcion} - Aprox {kcal_tiempo:.0f} kcal)_")
                    if cb.button("🔄", key=f"sw_{dia}_{tiempo}"):
                        t = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and alm_trabajo) else "ayc")
                        st.session_state.menu_semanal[dia][tiempo] = elegir_plato(t, set())
                        st.rerun()

import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente AR Pro", layout="wide")

# --- 1. CONFIGURACIÓN DEL PROFESIONAL (Sidebar) ---
st.sidebar.header("Datos del Profesional")
nombre_nutri = st.sidebar.text_input("Nombre y Apellido", "Lic. en Nutrición")
matricula = st.sidebar.text_input("Matrícula Profesional", "M.P. 1234")
contacto = st.sidebar.text_input("Contacto (Cel/Email)", "contacto@nutri.com")

# --- 2. BASE DE DATOS DE PLATOS DETALLADOS ---
def cargar_base_datos():
    # Estructura: Nombre, Porción (Medida Hogareña), Preparación
    ayc = [
        {"nombre": "Milanesa de peceto con puré de calabaza", "porcion": "1 unidad mediana y 1 taza de té de puré", "preparacion": "Cocinar al horno con rocío vegetal. Puré sin manteca, solo condimentos."},
        {"nombre": "Filet de merluza al limón con ensalada", "porcion": "1 filet grande y 1 plato playo de ensalada", "preparacion": "Pescado a la plancha. Ensalada de hojas verdes y tomate (preferentemente crudos para mayor saciedad)."},
        {"nombre": "Tarta de zapallitos (sin tapa)", "porcion": "1 porción (1/4 de tarta)", "preparacion": "Masa integral solo en la base. Relleno con huevo, cebolla y queso magro."},
        {"nombre": "Wok de pollo y vegetales", "porcion": "1 plato playo colmado", "preparacion": "Saltear tiras de pollo con zanahoria, pimiento y zapallitos. Usar poco aceite."},
        {"nombre": "Bife de cuadril con ensalada mixta", "porcion": "1 bife mediano y 1 plato playo de vegetales", "preparacion": "Carne a la parilla o plancha (quitar grasa visible). Ensalada de lechuga, tomate y cebolla."},
        {"nombre": "Fideos integrales con brócoli", "porcion": "1 plato hondo de fideos ya cocidos", "preparacion": "Cocinar al dente. Saltear el brócoli con ajo y 1 cdita de aceite de oliva."}
    ]
    
    dym = [
        {"nombre": "Infusión con tostadas integrales y queso", "porcion": "1 taza de infusión y 2 tostadas de pan integral", "preparacion": "Untar con 1 cda sopera de queso blanco descremado. Usar edulcorante."},
        {"nombre": "Yogur descremado con granola y banana", "porcion": "1 pote de yogur, 2 cdas de granola y 1/2 banana", "preparacion": "Mezclar en el momento. Elegir cereales sin azúcar."},
        {"nombre": "Mate cocido con leche y budín de avena", "porcion": "1 taza grande y 1 rodaja de budín (2 dedos)", "preparacion": "Budín casero con avena y manzana. Endulzar con estevia."},
        {"nombre": "Tostado de pan integral y queso", "porcion": "2 rodajas de pan integral y 1 feta gruesa de queso magro", "preparacion": "Calentar en sandwichera sin manteca ni aceite."}
    ]

    colaciones = [
        {"nombre": "Fruta de estación", "porcion": "1 unidad mediana", "preparacion": "Consumir con cáscara para mayor aporte de fibra."},
        {"nombre": "Yogur descremado", "porcion": "1 pote (firme o bebible)", "preparacion": "Elegir opciones '0% grasas' y sin azúcar agregado."},
        {"nombre": "Huevo duro", "porcion": "1 unidad", "preparacion": "Hervir 10 minutos. Ideal para aumentar la saciedad entre comidas."},
        {"nombre": "Gelatina diet con frutas", "porcion": "1 compotera", "preparacion": "Preparar según paquete agregando trozos de manzana o pera."}
    ]
    
    return {"dym": dym, "ayc": ayc, "colacion": colaciones}

if 'db_platos' not in st.session_state:
    st.session_state.db_platos = cargar_base_datos()

if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {}

def elegir_plato(tipo):
    return random.choice(st.session_state.db_platos[tipo])

# --- 3. EVALUACIÓN Y DIAGNÓSTICO (FICHA CLÍNICA) ---
st.title("Generador de Planes Nutricionales 🍏")
st.header("1. Evaluación y Diagnóstico")

c1, c2, c3 = st.columns(3)
with c1:
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    nombre_pac = st.text_input("Nombre del Paciente", "Paciente Ejemplo")
with c2:
    peso_actual = st.number_input("Peso Actual (kg)", value=75.0, step=0.1)
    talla_cm = st.number_input("Talla (cm)", value=160.0, step=0.1)
with c3:
    edad = st.number_input("Edad", value=30, min_value=1)
    af_opciones = {"Sedentario": 1.2, "Leve": 1.3, "Moderado": 1.5, "Intenso": 1.7}
    af_label = st.selectbox("Actividad Física", list(af_opciones.keys()))

# Cálculos de Diagnóstico (IMC) [cite: 77, 92]
talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Normopeso (Saludable)"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
else: diag = "Obesidad"

st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")
st.divider()

# --- 4. OBJETIVOS Y PRESCRIPCIÓN (BROCA / WILKENS)  ---
st.header("2. Objetivos y Prescripción")

# Lógica Peso Ideal
pi_broca = (talla_cm - 100) * (0.9 if sexo == "Femenino" else 1.0)

if imc >= 25:
    p_obj_sugerido = ((peso_actual - pi_broca) * 0.25) + pi_broca
    tipo_calculo = "Peso Ideal Corregido (Wilkens)"
else:
    p_obj_sugerido = pi_broca
    tipo_calculo = "Peso Ideal (Broca)"

obj_col1, obj_col2 = st.columns(2)
with obj_col1:
    # Key dinámica para que cambie al modificar sexo/talla
    p_obj = st.number_input(f"{tipo_calculo} - Sugerido", value=float(p_obj_sugerido), key=f"p_{sexo}_{talla_cm}")
    st.markdown("**Objetivos del Tratamiento:**")
    st.write("- Descenso de peso gradual y mantenimiento.")
    st.write("- Modificación de hábitos alimentarios.")
    st.write("- Aumento de la saciedad mediante fibra y masticación.")

with obj_col2:
    # Cálculo Requerimiento (Fórmula de Knox simplificada) 
    kcal_final = (p_obj * 22) * af_opciones[af_label]
    st.success(f"**Prescripción Dietoterápica:**")
    st.write(f"Plan Alimentario Hipocalórico de **{kcal_final:.0f} kcal/día**.")
    st.write("Distribución: CHO 55% | PRO 20% | GR 25%")
    st.caption("Fórmula: VTC = PIC/PI * 22 kcal * Factor AF")

st.divider()

# --- 5. MENÚ SEMANAL DETALLADO ---
st.header("3. Planificación del Menú")
col_c1, col_c2 = st.columns(2)
colaciones_on = col_c2.checkbox("Incluir colaciones diarias (Recomendado)")

if st.button("🚀 GENERAR PLAN SEMANAL PROFESIONAL"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    nuevo_menu = {}
    for d in dias:
        nuevo_menu[d] = {
            "Desayuno": elegir_plato("dym"),
            "Almuerzo": elegir_plato("ayc"),
            "Merienda": elegir_plato("dym"),
            "Cena": elegir_plato("ayc"),
            "Colaciones": [elegir_plato("colacion"), elegir_plato("colacion")] if colaciones_on else []
        }
    st.session_state.menu_semanal = nuevo_menu

if st.session_state.menu_semanal:
    for dia, comidas in st.session_state.menu_semanal.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for p in plato: 
                        st.markdown(f"🔸 **Colación:** {p['nombre']} | *Medida:* {p['porcion']}")
                else:
                    st.markdown(f"🍴 **{tiempo}: {plato['nombre']}**")
                    st.write(f"📏 **Medida Hogareña:** {plato['porcion']}")
                    st.write(f"📝 **Preparación:** {plato['preparacion']}")
                    st.divider()

    st.success("Plan generado correctamente. Listo para exportar.")

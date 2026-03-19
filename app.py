import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente Pro", layout="wide")

# --- BASE DE DATOS INTERNA (Muestra de ejemplo) ---
# En un futuro, aquí sumaremos hasta llegar a los 100 platos.
if 'db_platos' not in st.session_state:
    st.session_state.db_platos = [
        # D/M (Desayunos y Meriendas) - Aprox 300-400 kcal
        {"nombre": "Tostadas integrales con palta y huevo", "tipo": "dym", "kcal": 350, "macros": "CHO: 40g, PRO: 12g, GRA: 15g"},
        {"nombre": "Yogur con granola y frutas secas", "tipo": "dym", "kcal": 320, "macros": "CHO: 45g, PRO: 10g, GRA: 10g"},
        {"nombre": "Panqueque de avena y banana", "tipo": "dym", "kcal": 300, "macros": "CHO: 50g, PRO: 12g, GRA: 5g"},
        {"nombre": "Infusión con galletas de arroz y queso untable", "tipo": "dym", "kcal": 280, "macros": "CHO: 35g, PRO: 8g, GRA: 12g"},
        
        # A/C (Almuerzos y Cenas con Postre) - Aprox 500-700 kcal
        {"nombre": "Pechuga de pollo con puré mixtoy 1 manzana", "tipo": "ayc", "kcal": 550, "macros": "CHO: 60g, PRO: 40g, GRA: 15g"},
        {"nombre": "Merluza al horno con vegetales y gelatina", "tipo": "ayc", "kcal": 500, "macros": "CHO: 45g, PRO: 35g, GRA: 18g"},
        {"nombre": "Fideos integrales con brócoli y 1 naranja", "tipo": "ayc", "kcal": 580, "macros": "CHO: 75g, PRO: 15g, GRA: 20g"},
        {"nombre": "Ensalada completa con atún, legumbres y 1 pera", "tipo": "ayc", "kcal": 520, "macros": "CHO: 55g, PRO: 30g, GRA: 20g"},

        # TRABAJO (Fácil preparación / Microondas)
        {"nombre": "Tarta de zapallitos (fácil transporte)", "tipo": "trabajo", "kcal": 450, "macros": "CHO: 40g, PRO: 15g, GRA: 25g"},
        {"nombre": "Wrap de pollo y vegetales crudos", "tipo": "trabajo", "kcal": 420, "macros": "CHO: 45g, PRO: 25g, GRA: 15g"},
        {"nombre": "Ensalada de arroz, choclo y arvejas", "tipo": "trabajo", "kcal": 480, "macros": "CHO: 65g, PRO: 12g, GRA: 18g"},

        # COLACIONES
        {"nombre": "1 Fruta mediana", "tipo": "colacion", "kcal": 80, "macros": "CHO: 20g, PRO: 1g, GRA: 0g"},
        {"nombre": "Puñado de almendras (10 unidades)", "tipo": "colacion", "kcal": 100, "macros": "CHO: 5g, PRO: 4g, GRA: 9g"},
        {"nombre": "Yogur descremado solo", "tipo": "colacion", "kcal": 90, "macros": "CHO: 12g, PRO: 6g, GRA: 1g"}
    ]

# --- LÓGICA DE INTERCAMBIO ---
if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {}

def obtener_plato(tipo):
    opciones = [p for p in st.session_state.db_platos if p['tipo'] == tipo]
    return random.choice(opciones)

# --- INTERFAZ ---
st.title("Sistema de Prescripción Nutricional 🍏")

with st.sidebar:
    st.header("Configuración del Plan")
    nombre = st.text_input("Paciente", "Juan Perez")
    peso = st.number_input("Peso Actual (kg)", value=85.0)
    talla = st.number_input("Talla (cm)", value=170.0)
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    
    talla_m = talla / 100
    imc = peso / (talla_m**2)
    
    # Lógica de Peso Objetivo según documento
    pi_broca = (talla - 100) if sexo == "Masculino" else (talla - 100) * 0.9
    if imc >= 25:
        peso_sugerido = ((peso - pi_broca) * 0.25) + pi_broca
        label_peso = "PIC (Wilkens)"
    else:
        peso_sugerido = pi_broca
        label_peso = "PI (Broca)"
        
    peso_final = st.number_input(f"{label_peso} - Editable", value=float(peso_sugerido))
    kcal_totales = peso_final * 22
    
    st.metric("Kcal Diarias Recom.", f"{kcal_totales:.0f}")
    almuerzo_trabajo = st.checkbox("Almuerzo en el trabajo")
    colaciones_activas = st.checkbox("Añadir 2 colaciones por día")

# --- GENERACIÓN DE MENÚ ---
if st.button("Generar Plan Semanal"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for dia in dias:
        tipo_alm = "trabajo" if almuerzo_trabajo else "ayc"
        st.session_state.menu_semanal[dia] = {
            "Desayuno": obtener_plato("dym"),
            "Almuerzo": obtener_plato(tipo_alm),
            "Merienda": obtener_plato("dym"),
            "Cena": obtener_plato("ayc"),
            "Colaciones": [obtener_plato("colacion"), obtener_plato("colacion")] if colaciones_activas else []
        }

# --- MOSTRAR MENÚ ---
if st.session_state.menu_semanal:
    st.header("Tu Plan Semanal")
    for dia, comidas in st.session_state.menu_semanal.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for i, col in enumerate(plato):
                        st.write(f"**Colación {i+1}:** {col['nombre']} ({col['kcal']} kcal)")
                else:
                    col_info, col_btn = st.columns([0.8, 0.2])
                    col_info.write(f"**{tiempo}:** {plato['nombre']} - *{plato['kcal']} kcal*")
                    if col_btn.button("🔄", key=f"btn_{dia}_{tiempo}"):
                        tipo_busqueda = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and almuerzo_trabajo) else "ayc")
                        st.session_state.menu_semanal[dia][tiempo] = obtener_plato(tipo_busqueda)
                        st.rerun()

    if st.button("Descargar PDF (Próximamente)"):
        st.write("Estamos configurando la exportación...")

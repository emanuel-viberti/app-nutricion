import streamlit as st
import random
from fpdf import FPDF
import datetime

st.set_page_config(page_title="NutriAsistente AR", layout="wide")

# --- 1. FUNCIÓN TÉCNICA PARA PDF ---
def generar_pdf(datos_nutri, datos_pac, menu, diag_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado del Profesional
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, f"{datos_nutri['nombre']}", ln=True, align='C')
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 5, f"Matrícula: {datos_nutri['matricula']} | Contacto: {datos_nutri['contacto']}", ln=True, align='C')
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Título y Datos del Paciente
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"PLAN ALIMENTARIO: {datos_pac['nombre'].upper()}", ln=True)
    
    # Indicadores Antropométricos (Distribución mejorada)
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 7, " INDICADORES ANTROPOMÉTRICOS Y DIAGNÓSTICO", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    
    # Fila 1: Peso Actual - Talla - Edad
    pdf.cell(63, 6, f"Peso Actual: {datos_pac['peso']} kg", ln=0)
    pdf.cell(63, 6, f"Talla: {int(datos_pac['talla'])} cm", ln=0)
    pdf.cell(63, 6, f"Edad: {datos_pac['edad']} años", ln=1) # Edad ahora al lado de Talla
    
    # Fila 2: IMC - Peso Ideal/Obj - Actividad
    pdf.cell(63, 6, f"IMC: {datos_pac['imc']:.1f}", ln=0)
    pdf.cell(63, 6, f"Peso Ideal/Obj: {datos_pac['p_obj']:.1f} kg", ln=0)
    pdf.cell(63, 6, f"Actividad: {datos_pac['af']}", ln=1)
    
    pdf.set_font("Arial", "B", 9)
    pdf.cell(0, 8, f"Diagnóstico: {diag_info['diag']} | Prescripción: {diag_info['t_plan']} ({diag_info['kcal']:.0f} kcal/día)", ln=1)
    pdf.ln(4)
    
    # Cuerpo del menú
    for dia, comidas in menu.items():
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(235, 235, 235)
        pdf.cell(0, 8, f" {dia.upper()}", ln=True, fill=True)
        pdf.ln(1)
        for tiempo, plato in comidas.items():
            if tiempo == "Colaciones" and plato:
                pdf.set_font("Arial", "B", 9)
                nombres_col = " | ".join([p['nombre'] for p in plato])
                pdf.multi_cell(0, 5, f"COLACIONES: {nombres_col}")
            elif tiempo != "Colaciones":
                pdf.set_font("Arial", "B", 9)
                pdf.cell(25, 5, f"{tiempo.upper()}:", ln=0)
                pdf.set_font("Arial", "", 9)
                pdf.cell(0, 5, f"{plato['nombre']}", ln=1)
                pdf.set_font("Arial", "I", 8)
                pdf.cell(25, 4, "", ln=0)
                pdf.multi_cell(0, 4, f"Medida: {plato['mh']} - {plato['prep']}")
            pdf.ln(1)
        if pdf.get_y() > 260: pdf.add_page()
    
    return pdf.output(dest='S').encode('latin-1') 
# --- 2. DATOS DEL NUTRICIONISTA ---
st.sidebar.header("Configuración de Firma")
nutri_info = {
    "nombre": st.sidebar.text_input("Nombre y Apellido", "Lic. en Nutrición", key="nutri_nom"),
    "matricula": st.sidebar.text_input("Matrícula", "M.P. 0000", key="nutri_mat"),
    "contacto": st.sidebar.text_input("Contacto", "Email / Celular", key="nutri_cont")
}

# --- 3. BASE DE DATOS MEJORADA ---
def cargar_db():
    ayc = [
        {"nombre": "Milanesa de peceto con puré de calabaza", "mh": "1 unid. med. y 1 taza de puré", "prep": "Al horno con rocío vegetal."},
        {"nombre": "Filet de merluza al limón con ensalada", "mh": "1 filet grande y 1 plato playo", "prep": "Pescado a la plancha."},
        {"nombre": "Tarta de zapallitos (sin tapa)", "mh": "1/4 de unidad", "prep": "Masa integral solo base."},
        {"nombre": "Wok de pollo y vegetales", "mh": "1 plato playo colmado", "prep": "Saltear con poco aceite."},
        {"nombre": "Bife de cuadril con ensalada mixta", "mh": "1 bife med. y 1 plato de vegetales", "prep": "Carne a la plancha."},
        {"nombre": "Canelones de verdura con salsa fileto", "mh": "2 unidades", "prep": "Masa liviana."},
        {"nombre": "Zapallitos rellenos con carne magra", "mh": "2 unidades", "prep": "Carne picada especial."},
        {"nombre": "Calabaza rellena con vegetales y queso", "mh": "1/2 unidad chica", "prep": "Al horno con choclo y cebolla."},
        {"nombre": "Pastel de papas (carne magra y puré mixto)", "mh": "1 porción mediana", "prep": "Carne picada especial."},
        {"nombre": "Fideos integrales con brócoli", "mh": "1 plato mediano", "prep": "Fideos al dente."},
        {"nombre": "Medallones de lentejas con ensalada", "mh": "2 unidades", "prep": "Caseros."},
        {"nombre": "Revuelto de zapallitos y huevo", "mh": "1 plato playo colmado", "prep": "Sin fritura."},
        {"nombre": "Pescado al paquete con vegetales", "mh": "1 filet grande", "prep": "Al horno en aluminio."},
        {"nombre": "Guiso de lentejas saludable", "mh": "1 plato hondo", "prep": "Mucha verdura y carne magra."},
        {"nombre": "Ensalada de garbanzos, atún y huevo", "mh": "1 bowl grande", "prep": "Legumbres hervidas."},
        {"nombre": "Brochetas de carne y vegetales", "mh": "3 unidades", "prep": "A la plancha."},
        {"nombre": "Omelette de espinaca y queso magro", "mh": "1 unidad grande", "prep": "2 huevos y espinaca."},
        {"nombre": "Pechuga de pollo a la mostaza con puré", "mh": "1 pechuga chica", "prep": "Mostaza sin azúcar."},
        {"nombre": "Berenjenas a la parmesana (light)", "mh": "2 rodajas grandes", "prep": "Al horno con salsa."},
        {"nombre": "Hamburguesas de mijo y calabaza", "mh": "2 unidades", "prep": "Al horno."},
        {"nombre": "Colita de cuadril al horno con vegetales", "mh": "2 rodajas finas", "prep": "Carne magra asada."},
        {"nombre": "Risotto de cebada perlada y hongos", "mh": "1 plato mediano", "prep": "Cebada bien cocida."},
        {"nombre": "Budín de acelga y zanahoria", "mh": "1 porción grande", "prep": "Con claras de huevo."},
        {"nombre": "Fajitas de carne (tortilla integral)", "mh": "2 unidades", "prep": "Tiras de carne y vegetales."},
        {"nombre": "Albóndigas de pollo con puré de manzana", "mh": "4 unidades chicas", "prep": "Pollo procesado."},
        {"nombre": "Tomates rellenos con arroz y atún", "mh": "2 unidades", "prep": "Arroz integral."},
        {"nombre": "Pizza con masa de alcaucil o coliflor", "mh": "2 porciones", "prep": "Base de vegetal."},
        {"nombre": "Soufflé de calabaza y queso", "mh": "1 porción abundante", "prep": "Claras a nieve."},
        {"nombre": "Lomo a la pimienta con chauchas", "mh": "1 bife mediano", "prep": "Chauchas al vapor."},
        {"nombre": "Croquetas de arroz integral y espinaca", "mh": "3 unidades med.", "prep": "Al horno."},
        {"nombre": "Tarta de choclo y cebolla (sin tapa)", "mh": "1/4 de unidad", "prep": "Relleno cremoso light."},
        {"nombre": "Pollo al horno con vegetales asados", "mh": "1 presa sin piel", "prep": "Hierbas naturales."}
    ]
    trabajo = [
        {"nombre": "Sándwich integral de pollo y rúcula", "mh": "2 rodajas de pan", "prep": "Pollo hervido."},
        {"nombre": "Ensalada de arroz, atún y arvejas", "mh": "1 bowl mediano", "prep": "Atún al natural."},
        {"nombre": "Tarta de acelga y queso (vianda)", "mh": "1 porción grande", "prep": "Masa de salvado."},
        {"nombre": "Wrap de carne y vegetales", "mh": "1 unidad grande", "prep": "Tortilla integral."},
        {"nombre": "Ensalada de fideos fríos y vegetales", "mh": "1 bowl mediano", "prep": "Fideos tirabuzón."},
        {"nombre": "Ensalada de lentejas, tomate y zanahoria", "mh": "1 bowl mediano", "prep": "Lentejas hervidas."},
        {"nombre": "Rollitos de jamón y queso con ensalada", "mh": "3 rollitos", "prep": "Jamón cocido natural."}
    ]
    dym = [
        {"nombre": "Infusión con tostadas integrales y queso", "mh": "1 taza y 2 tostadas", "prep": "Queso descremado."},
        {"nombre": "Yogur descremado con granola y banana", "mh": "1 pote y 1/2 banana", "prep": "Mezclar al momento."},
        {"nombre": "Mate cocido con leche y budín de avena", "mh": "1 taza y 1 rodaja", "prep": "Sin azúcar."},
        {"nombre": "Tostado integral de queso magro", "mh": "2 rodajas de pan", "prep": "En sandwichera."},
        {"nombre": "Leche descremada con copos de maíz", "mh": "1 taza mediana", "prep": "Sin azúcar."},
        {"nombre": "Panqueque de avena con mermelada diet", "mh": "1 unidad", "prep": "Con claras y avena."},
        {"nombre": "Fruta con frutos secos", "mh": "1 bowl chico", "prep": "3 nueces."},
        {"nombre": "Galletitas de arroz con queso y mermelada", "mh": "3 unidades", "prep": "Queso blanco descr."},
        {"nombre": "Licuado de banana con leche descremada", "mh": "1 vaso grande", "prep": "Sin azúcar."},
        {"nombre": "Omelette dulce de claras y manzana", "mh": "1 unidad", "prep": "Manzana rallada."},
        {"nombre": "Yogur con semillas de chía y arándanos", "mh": "1 pote", "prep": "Dejar hidratar."},
        {"nombre": "Bowl de avena cocida con canela", "mh": "1 taza chica", "prep": "Cocida con agua."}
    ]
    col = [
        {"nombre": "Fruta de estación", "mh": "1 unidad", "prep": "Lavar bien."},
        {"nombre": "Yogur descremado", "mh": "1 pote", "prep": "Natural."},
        {"nombre": "Huevo duro", "mh": "1 unidad", "prep": "Hervido."},
        {"nombre": "Gelatina diet", "mh": "1 compotera", "prep": "Con fruta."},
        {"nombre": "Puñado de almendras", "mh": "10 unidades", "prep": "Crudas."},
        {"nombre": "Bastoncitos de zanahoria", "mh": "1 taza", "prep": "Crudos."},
        {"nombre": "Queso magro en cubitos", "mh": "1 feta gruesa", "prep": "Light."},
        {"nombre": "Tomates cherry", "mh": "10 unidades", "prep": "Frescos."}
    ]
    return {"dym": dym, "ayc": ayc, "trabajo": trabajo, "col": col}

if 'db' not in st.session_state: st.session_state.db = cargar_db()
if 'menu' not in st.session_state: st.session_state.menu = {}

# --- 4. EVALUACIÓN Y DIAGNÓSTICO ---
st.title("Generador Nutricional Profesional 🍏")
c1, c2, c3 = st.columns(3)
with c1:
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"], key="sel_sexo")
    nombre_pac = st.text_input("Nombre del Paciente", "Paciente Ejemplo", key="in_nom_pac")
    edad = st.number_input("Edad", min_value=1, value=30, key="in_edad")
with c2:
    peso_actual = st.number_input("Peso Actual (kg)", value=75.0, step=0.1, key="in_peso")
    talla_cm = st.number_input("Talla (cm)", value=160, step=1, format="%d", key="in_talla")
with c3:
    af_sel = st.selectbox("Actividad Física", ["Sedentario", "Leve", "Moderado", "Intenso"], key="sel_af")
    af_val = {"Sedentario": 1.2, "Leve": 1.3, "Moderado": 1.5, "Intenso": 1.7}[af_sel]

talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag, t_plan = "Delgadez", "Plan Hipercalórico"
elif 18.5 <= imc <= 24.9: diag, t_plan = "Normopeso", "Plan Normocalórico"
elif 25.0 <= imc <= 29.9: diag, t_plan = "Sobrepeso", "Plan Hipocalórico"
else: diag, t_plan = "Obesidad Grado I", "Plan Hipocalórico"

st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")

# --- 5. PRESCRIPCIÓN Y CÁLCULO DE PESO OBJETIVO ---
st.divider()
st.subheader("Configuración de la Prescripción")

# Cálculo de PI/PIC (Broca y Wilkens)
if sexo == "Femenino":
    pi_valor = (talla_cm - 100) * 0.9
else:
    pi_valor = (talla_cm - 100) * 1.0

if imc >= 30.0:
    p_obj_calculado = ((peso_actual - pi_valor) * 0.25) + pi_valor
    label_p = "Peso Ideal Corregido (PIC)"
else:
    p_obj_calculado = pi_valor
    label_p = "Peso Ideal (PI)"

col_p1, col_p2 = st.columns(2)
with col_p1:
    p_obj = st.number_input(
        label=label_p,
        value=float(p_obj_calculado),
        step=0.1,
        key=f"p_obj_fix_{sexo}_{talla_cm}_{peso_actual}"
    )

with col_p2:
    kcal_final = (p_obj * 22) * af_val
    st.metric(label="Calorías Objetivo", value=f"{kcal_final:.0f} kcal/día")

# Diccionario consolidado para el PDF (Asegura Edad al lado de Talla)
datos_antropometricos = {
    "nombre": nombre_pac,
    "peso": peso_actual,
    "talla": talla_cm,
    "edad": edad,
    "imc": imc,
    "p_obj": p_obj,
    "af": af_sel
}

# --- 6. GENERACIÓN DEL MENÚ ---
st.divider()
c_a, c_b = st.columns(2)
alm_trabajo = c_a.checkbox("Almuerzo en el trabajo", key="check_trabajo")
colaciones_on = c_b.checkbox("Incluir colaciones", key="check_colaciones")

# BOTÓN RENOMBRADO Y FUNCIONAL
if st.button("🚀 GENERAR PLAN SEMANAL", key="btn_generar_v2"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    st.session_state.menu = {}
    historial_ayc = []
    historial_dym = []

    for d in dias:
        # --- Selección de platos principales (D&M y A&C) ---
        pool_dym = [x for x in st.session_state.db["dym"] if x["nombre"] not in historial_dym]
        dym_hoy = random.sample(pool_dym if len(pool_dym) >= 2 else st.session_state.db["dym"], 2)
        
        if alm_trabajo:
            pool_trab = [x for x in st.session_state.db["trabajo"] if x["nombre"] not in historial_ayc]
            almuerzo = random.choice(pool_trab if pool_trab else st.session_state.db["trabajo"])
            pool_cena = [x for x in st.session_state.db["ayc"] if x["nombre"] not in historial_ayc and x["nombre"] != almuerzo["nombre"]]
            cena = random.choice(pool_cena if pool_cena else st.session_state.db["ayc"])
        else:
            pool_ayc = [x for x in st.session_state.db["ayc"] if x["nombre"] not in historial_ayc]
            ayc_hoy = random.sample(pool_ayc if len(pool_ayc) >= 2 else st.session_state.db["ayc"], 2)
            almuerzo, cena = ayc_hoy[0], ayc_hoy[1]
            
        # --- Lógica de Colaciones ---
        col_m, col_t = None, None
        if colaciones_on:
            c_hoy = random.sample(st.session_state.db["col"], 2)
            col_m, col_t = c_hoy[0], c_hoy[1]

        # Guardado estructurado
        st.session_state.menu[d] = {
            "Desayuno": dym_hoy[0],
            "Colacion_M": col_m,
            "Almuerzo": almuerzo,
            "Merienda": dym_hoy[1],
            "Colacion_T": col_t,
            "Cena": cena
        }
        
        historial_ayc = (historial_ayc + [almuerzo["nombre"], cena["nombre"]])[-6:]
        historial_dym = (historial_dym + [dym_hoy[0]["nombre"], dym_hoy[1]["nombre"]])[-6:]

# --- 7. VISUALIZACIÓN Y DESCARGA ---
if st.session_state.menu:
    for dia, comidas in st.session_state.menu.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo != "Colaciones":
                    st.write(f"🍴 **{tiempo}:** {plato['nombre']}")
    
    st.divider()
    # Aquí llamamos a la función de PDF con el diccionario que tiene la Edad corregida
    pdf_bytes = generar_pdf(
        nutri_info, 
        datos_antropometricos, 
        st.session_state.menu, 
        {"diag": diag, "t_plan": t_plan, "kcal": kcal_final}
    )
    
    st.download_button(
        label="💾 DESCARGAR PLAN PROFESIONAL",
        data=pdf_bytes,
        file_name=f"Plan_{nombre_pac.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

# --- 6. MENÚ ---
st.divider()
c_a, c_b = st.columns(2)
alm_trabajo = c_a.checkbox("Almuerzo en el trabajo", key="check_trabajo")
colaciones_on = c_b.checkbox("Incluir colaciones (Mañana y Tarde)", key="check_colaciones")

if st.button("🚀 GENERAR PLAN SIN REPETICIONES", key="btn_generar"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    st.session_state.menu = {}
    
    # HISTORIAL DE 3 DÍAS PARA EVITAR REPETICIONES CORTAS
    historial_ayc = []
    historial_dym = []
    historial_col = []

    for d in dias:
        # Selección Desayuno/Merienda
        pool_dym = [x for x in st.session_state.db["dym"] if x["nombre"] not in historial_dym]
        dym_hoy = random.sample(pool_dym if len(pool_dym) >= 2 else st.session_state.db["dym"], 2)
        
        # Selección Almuerzo/Cena
        if alm_trabajo:
            pool_trab = [x for x in st.session_state.db["trabajo"] if x["nombre"] not in historial_ayc]
            almuerzo = random.choice(pool_trab if pool_trab else st.session_state.db["trabajo"])
            pool_cena = [x for x in st.session_state.db["ayc"] if x["nombre"] not in historial_ayc and x["nombre"] != almuerzo["nombre"]]
            cena = random.choice(pool_cena if pool_cena else st.session_state.db["ayc"])
        else:
            pool_ayc = [x for x in st.session_state.db["ayc"] if x["nombre"] not in historial_ayc]
            ayc_hoy = random.sample(pool_ayc if len(pool_ayc) >= 2 else st.session_state.db["ayc"], 2)
            almuerzo, cena = ayc_hoy[0], ayc_hoy[1]
            
        # Selección Colaciones
        if colaciones_on:
            pool_col = [x for x in st.session_state.db["col"] if x["nombre"] not in historial_col]
            cols_hoy = random.sample(pool_col if len(pool_col) >= 2 else st.session_state.db["col"], 2)
        else:
            cols_hoy = []

        st.session_state.menu[d] = {
            "Desayuno": dym_hoy[0], "Almuerzo": almuerzo, "Merienda": dym_hoy[1], "Cena": cena, "Colaciones": cols_hoy
        }
        
        # Actualizar historial (mantenemos los últimos 6 platos para cubrir 3 días de almuerzo/cena)
        historial_ayc = (historial_ayc + [almuerzo["nombre"], cena["nombre"]])[-6:]
        historial_dym = (historial_dym + [dym_hoy[0]["nombre"], dym_hoy[1]["nombre"]])[-6:]
        historial_col = (historial_col + [c["nombre"] for c in cols_hoy])[-4:]

if st.session_state.menu:
    # ... (código de los expanders) ...
    
    st.divider()
    # Preparamos el diccionario con todos los datos calculados 
    datos_para_pdf = {
        "nombre": nombre_pac,
        "edad": edad,
        "talla": talla_cm,
        "peso": peso_actual,
        "imc": imc,
        "p_obj": p_obj,
        "af": af_sel
    }
    
    pdf_bytes = generar_pdf(
        nutri_info, 
        datos_para_pdf, 
        st.session_state.menu, 
        {"diag": diag, "t_plan": t_plan, "kcal": kcal_final}
    )
    
    st.download_button(
        label="💾 DESCARGAR PLAN PROFESIONAL (PDF)",
        data=pdf_bytes,
        file_name=f"Plan_{nombre_pac.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

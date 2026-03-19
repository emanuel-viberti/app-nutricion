import streamlit as st
import random
from fpdf import FPDF
import datetime

st.set_page_config(page_title="NutriAsistente AR", layout="wide")

# --- 1. FUNCIÓN TÉCNICA CORREGIDA PARA PDF ---
def generar_pdf(datos_nutri, datos_pac, menu, diag_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)
    
    # Encabezado
    pdf.cell(0, 10, f"{datos_nutri['nombre']}", ln=True, align='C')
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, f"Matrícula: {datos_nutri['matricula']} | Contacto: {datos_nutri['contacto']}", ln=True, align='C')
    pdf.ln(10)
    
    # Datos del Paciente
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"PLAN ALIMENTARIO: {datos_pac['nombre'].upper()}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, f"Fecha: {datetime.date.today().strftime('%d/%m/%Y')} | Edad: {datos_pac['edad']} años", ln=True)
    pdf.cell(0, 5, f"Diagnóstico: {diag_info['diag']} | Prescripción: {diag_info['t_plan']}", ln=True)
    pdf.cell(0, 5, f"Calorías objetivo: {diag_info['kcal']:.0f} kcal/día", ln=True)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Menú Semanal
    for dia, comidas in menu.items():
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, f"--- {dia.upper()} ---", ln=True, fill=True)
        pdf.ln(2)
        
        for tiempo, plato in comidas.items():
            if tiempo == "Colaciones":
                for i, p in enumerate(plato, 1):
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 5, f"Colación {i}: {p['nombre']}", ln=True)
                    pdf.set_font("Arial", "I", 9)
                    pdf.multi_cell(0, 5, f"-> Medida: {p['mh']} | Prep: {p['prep']}")
                    pdf.ln(1)
            else:
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0, 5, f"{tiempo.upper()}: {plato['nombre']}", ln=True)
                pdf.set_font("Arial", "", 9)
                pdf.multi_cell(0, 5, f"-> Medida Hogareña: {plato['mh']}")
                pdf.multi_cell(0, 5, f"-> Preparación: {plato['prep']}")
            pdf.ln(2)
        
        if pdf.get_y() > 250: pdf.add_page()
        else: pdf.ln(3)
            
    return pdf.output(dest='S').encode('latin-1')

# --- 2. DATOS DEL NUTRICIONISTA (Sidebar) ---
st.sidebar.header("Configuración de Firma")
nutri_info = {
    "nombre": st.sidebar.text_input("Nombre y Apellido", "Lic. en Nutrición"),
    "matricula": st.sidebar.text_input("Matrícula", "M.P. 0000"),
    "contacto": st.sidebar.text_input("Contacto", "Email / Celular")
}

# --- 3. BASE DE DATOS ---
def cargar_db():
    ayc = [
        {"nombre": "Milanesa de peceto con puré de calabaza", "mh": "1 unid. med. y 1 taza de puré", "prep": "Al horno con rocío vegetal. Puré sin manteca."},
        {"nombre": "Filet de merluza al limón con ensalada", "mh": "1 filet grande y 1 plato playo de vegetales", "prep": "Pescado a la plancha. Ensalada cruda."},
        {"nombre": "Tarta de zapallitos (sin tapa)", "mh": "1/4 de unidad", "prep": "Masa integral solo base. Relleno con huevo y queso magro."},
        {"nombre": "Wok de pollo y vegetales", "mh": "1 plato playo colmado", "prep": "Saltear con poco aceite. Vegetales al dente."},
        {"nombre": "Bife de cuadril con ensalada mixta", "mh": "1 bife med. y 1 plato de vegetales", "prep": "Carne sin grasa visible a la plancha."},
        {"nombre": "Canelones de verdura con salsa fileto", "mh": "2 unidades", "prep": "Masa de panqueque liviana, salsa sin fritura."},
        {"nombre": "Pollo al horno con vegetales asados", "mh": "1 presa sin piel y 1 taza de vegetales", "prep": "Cocción lenta al horno con hierbas."},
        {"nombre": "Zapallitos rellenos con carne magra", "mh": "2 unidades", "prep": "Relleno de carne picada especial y cebolla."}
    ]
    trabajo = [
        {"nombre": "Sándwich integral de pollo y rúcula", "mh": "2 rodajas de pan y 1 pechuga chica", "prep": "Sin aderezos grasos."},
        {"nombre": "Ensalada de arroz, atún y arvejas", "mh": "1 bowl mediano", "prep": "Atún al natural."},
        {"nombre": "Tarta de acelga y queso (vianda)", "mh": "1 porción grande", "prep": "Masa de salvado."},
        {"nombre": "Wrap de carne y vegetales", "mh": "1 unidad grande", "prep": "Tortilla integral."}
    ]
    dym = [
        {"nombre": "Infusión con tostadas integrales y queso", "mh": "1 taza y 2 tostadas", "prep": "Queso blanco descremado."},
        {"nombre": "Yogur descremado con granola y banana", "mh": "1 pote, 2 cdas granola, 1/2 banana", "prep": "Mezclar al momento."},
        {"nombre": "Mate cocido con leche y budín de avena", "mh": "1 taza y 1 rodaja med.", "prep": "Budín casero sin azúcar."},
        {"nombre": "Tostado integral de queso magro", "mh": "2 rodajas de pan y 1 feta queso", "prep": "En sandwichera."},
        {"nombre": "Leche descremada con copos de maíz", "mh": "1 taza mediana", "prep": "Copos sin azúcar."},
        {"nombre": "Panqueque de avena con mermelada diet", "mh": "1 unidad grande", "prep": "Hecho con claras y avena."}
    ]
    col = [{"nombre": "Fruta de estación", "mh": "1 unidad med.", "prep": "Lavar bien."}, {"nombre": "Yogur descremado", "mh": "1 pote", "prep": "Sin azúcar."}, {"nombre": "Huevo duro", "mh": "1 unidad", "prep": "Hervir 10 min."}, {"nombre": "Gelatina diet", "mh": "1 compotera", "prep": "Con trozos de fruta."}]
    return {"dym": dym, "ayc": ayc, "trabajo": trabajo, "col": col}

if 'db' not in st.session_state: st.session_state.db = cargar_db()
if 'menu' not in st.session_state: st.session_state.menu = {}

# --- 4. EVALUACIÓN Y DIAGNÓSTICO ---
st.title("Generador Nutricional Profesional 🍏")
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

talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag, t_plan = "Delgadez", "Plan Hipercalórico"
elif 18.5 <= imc <= 24.9: diag, t_plan = "Normopeso", "Plan Normocalórico"
elif 25.0 <= imc <= 29.9: diag, t_plan = "Sobrepeso", "Plan Hipocalórico"
elif 30.0 <= imc <= 34.9: diag, t_plan = "Obesidad Grado I", "Plan Hipocalórico"
elif 35.0 <= imc <= 39.9: diag, t_plan = "Obesidad Grado II", "Plan Hipocalórico"
else: diag, t_plan = "Obesidad Grado III", "Plan Hipocalórico"

st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")

# --- 5. PRESCRIPCIÓN ---
pi_broca = (talla_cm - 100) * (0.9 if sexo == "Femenino" else 1.0)
if imc >= 30.0:
    val_sugerido = ((peso_actual - pi_broca) * 0.25) + pi_broca
    label_p = "Peso Ideal Corregido (Wilkens)"
else:
    val_sugerido = pi_broca
    label_p = "Peso Ideal (Broca)"

cp1, cp2 = st.columns(2)
p_obj = cp1.number_input(f"{label_p} - Sugerido", value=float(val_sugerido), key=f"p_{sexo}_{talla_cm}")
kcal_final = (p_obj * 22) * af_val
cp2.info(f"**Prescripción:** {t_plan} de {kcal_final:.0f} kcal/día")

# --- 6. MENÚ (Evitando Repetición) ---
st.divider()
c_a, c_b = st.columns(2)
alm_trabajo = c_a.checkbox("Almuerzo en el trabajo")
colaciones_on = c_b.checkbox("Incluir colaciones (Mañana y Tarde)")

if st.button("🚀 GENERAR PLAN"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    t_a = "trabajo" if alm_trabajo else "ayc"
    
    # Muestreo aleatorio de la base de datos para evitar repeticiones excesivas
    pool_dym = random.sample(st.session_state.db["dym"] * 3, 14) # Multiplicamos por si la lista es corta
    pool_ayc = random.sample(st.session_state.db["ayc"] * 3, 14)
    pool_trab = random.sample(st.session_state.db["trabajo"] * 3, 7)
    pool_col = random.sample(st.session_state.db["col"] * 5, 14)

    st.session_state.menu = {}
    for i, d in enumerate(dias):
        st.session_state.menu[d] = {
            "Desayuno": pool_dym[i],
            "Almuerzo": pool_trab[i] if alm_trabajo else pool_ayc[i],
            "Merienda": pool_dym[i+7],
            "Cena": pool_ayc[i+7],
            "Colaciones": [pool_col[i*2], pool_col[i*2+1]] if colaciones_on else []
        }

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
    pdf_bytes = generar_pdf(nutri_info, {"nombre": nombre_pac, "edad": edad}, st.session_state.menu, {"diag": diag, "t_plan": t_plan, "kcal": kcal_final})
    st.download_button("💾 DESCARGAR PDF PROFESIONAL", data=pdf_bytes, file_name=f"Plan_{nombre_pac.replace(' ', '_')}.pdf", mime="application/pdf")

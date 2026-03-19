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
    pdf.set_font("Arial", "B", 16)
    
    pdf.cell(0, 10, f"{datos_nutri['nombre']}", ln=True, align='C')
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, f"Matrícula: {datos_nutri['matricula']} | Contacto: {datos_nutri['contacto']}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"PLAN ALIMENTARIO: {datos_pac['nombre'].upper()}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, f"Fecha: {datetime.date.today().strftime('%d/%m/%Y')} | Talla: {int(datos_pac['talla'])} cm", ln=True)
    pdf.cell(0, 5, f"Diagnóstico: {diag_info['diag']} | Prescripción: {diag_info['t_plan']}", ln=True)
    pdf.cell(0, 5, f"Calorías objetivo: {diag_info['kcal']:.0f} kcal/día", ln=True)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
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

# --- 2. DATOS DEL NUTRICIONISTA ---
st.sidebar.header("Configuración de Firma")
nutri_info = {
    "nombre": st.sidebar.text_input("Nombre y Apellido", "Lic. en Nutrición", key="nutri_nom"),
    "matricula": st.sidebar.text_input("Matrícula", "M.P. 0000", key="nutri_mat"),
    "contacto": st.sidebar.text_input("Contacto", "Email / Celular", key="nutri_cont")
}

# --- 3. BASE DE DATOS ULTRA AMPLIADA ---
def cargar_db():
    ayc = [
        {"nombre": "Milanesa de peceto con puré de calabaza", "mh": "1 unid. med. y 1 taza de puré", "prep": "Al horno con rocío vegetal."},
        {"nombre": "Filet de merluza al limón con ensalada", "mh": "1 filet grande y 1 plato playo", "prep": "Pescado a la plancha."},
        {"nombre": "Tarta de zapallitos (sin tapa)", "mh": "1/4 de unidad", "prep": "Masa integral solo base."},
        {"nombre": "Wok de pollo y vegetales", "mh": "1 plato playo colmado", "prep": "Saltear con poco aceite."},
        {"nombre": "Bife de cuadril con ensalada mixta", "mh": "1 bife med. y 1 plato de vegetales", "prep": "Carne a la plancha."},
        {"nombre": "Canelones de verdura con salsa fileto", "mh": "2 unidades", "prep": "Masa liviana."},
        {"nombre": "Pollo al horno con vegetales asados", "mh": "1 presa sin piel", "prep": "Hierbas naturales."},
        {"nombre": "Zapallitos rellenos con carne magra", "mh": "2 unidades", "prep": "Carne picada especial."},
        {"nombre": "Calabaza rellena con vegetales y queso", "mh": "1/2 unidad chica", "prep": "Al horno con choclo y cebolla."},
        {"nombre": "Pastel de papas (carne magra y puré mixto)", "mh": "1 porción mediana", "prep": "Carne picada especial y puré mixto."},
        {"nombre": "Fideos integrales con brócoli", "mh": "1 plato mediano", "prep": "Fideos al dente con brócoli al vapor."},
        {"nombre": "Medallones de lentejas con ensalada", "mh": "2 unidades", "prep": "Caseros con condimentos naturales."},
        {"nombre": "Revuelto de zapallitos y huevo", "mh": "1 plato playo colmado", "prep": "Sin fritura, con rocío vegetal."},
        {"nombre": "Pescado al paquete con vegetales", "mh": "1 filet grande", "prep": "Al horno envuelto en aluminio."},
        {"nombre": "Guiso de lentejas saludable", "mh": "1 plato hondo", "prep": "Con mucha verdura y carne magra."},
        {"nombre": "Ensalada de garbanzos, atún y huevo", "mh": "1 bowl grande", "prep": "Legumbres hervidas y atún natural."},
        {"nombre": "Brochetas de carne y vegetales", "mh": "3 unidades", "prep": "A la plancha con morrón y cebolla."},
        {"nombre": "Omelette de espinaca y queso magro", "mh": "1 unidad grande", "prep": "Hecho con 2 huevos y espinaca."},
        {"nombre": "Pechuga de pollo a la mostaza con puré", "mh": "1 pechuga chica", "prep": "Mostaza sin azúcar y puré de papas."},
        {"nombre": "Berenjenas a la parmesana (light)", "mh": "2 rodajas grandes", "prep": "Al horno con salsa y queso magro."},
        {"nombre": "Hamburguesas de mijo y calabaza", "mh": "2 unidades", "prep": "Cereal hervido y puré."},
        {"nombre": "Colita de cuadril al horno con vegetales", "mh": "2 rodajas finas", "prep": "Carne magra asada."},
        {"nombre": "Risotto de cebada perlada y hongos", "mh": "1 plato mediano", "prep": "Cebada bien cocida."},
        {"nombre": "Budín de acelga y zanahoria", "mh": "1 porción grande", "prep": "Con claras de huevo."},
        {"nombre": "Fajitas de carne (tortilla integral)", "mh": "2 unidades", "prep": "Tiras de carne y vegetales."},
        {"nombre": "Albóndigas de pollo con puré de manzana", "mh": "4 unidades chicas", "prep": "Pollo procesado al horno."},
        {"nombre": "Ensalada Rusa Saludable", "mh": "1 bowl mediano", "prep": "Con mayonesa light o yogur natural."},
        {"nombre": "Tomates rellenos con arroz y atún", "mh": "2 unidades", "prep": "Arroz integral y atún al natural."},
        {"nombre": "Pizza con masa de alcaucil o coliflor", "mh": "2 porciones", "prep": "Base de vegetal y queso magro."},
        {"nombre": "Soufflé de calabaza y queso", "mh": "1 porción abundante", "prep": "Con claras batidas a nieve."},
        {"nombre": "Lomo a la pimienta con chauchas", "mh": "1 bife mediano", "prep": "Chauchas al vapor."},
        {"nombre": "Pollo al verdeo con batatas asadas", "mh": "1 presa chica", "prep": "Cebolla de verdeo y poco aceite."},
        {"nombre": "Croquetas de arroz integral y espinaca", "mh": "3 unidades med.", "prep": "Al horno."},
        {"nombre": "Tarta de choclo y cebolla (sin tapa)", "mh": "1/4 de unidad", "prep": "Relleno de choclo cremoso light."},
        {"nombre": "Pescado a la provenzal con ensalada", "mh": "1 filet grande", "prep": "Ajo y perejil fresco."}
    ]
    trabajo = [
        {"nombre": "Sándwich integral de pollo y rúcula", "mh": "2 rodajas de pan", "prep": "Pollo hervido."},
        {"nombre": "Ensalada de arroz, atún y arvejas", "mh": "1 bowl mediano", "prep": "Atún al natural."},
        {"nombre": "Tarta de acelga y queso (vianda)", "mh": "1 porción grande", "prep": "Masa de salvado."},
        {"nombre": "Wrap de carne y vegetales", "mh": "1 unidad grande", "prep": "Tortilla integral."},
        {"nombre": "Ensalada de fideos fríos y vegetales", "mh": "1 bowl mediano", "prep": "Fideos tirabuzón y tomate."},
        {"nombre": "Ensalada de lentejas, tomate y zanahoria", "mh": "1 bowl mediano", "prep": "Lentejas hervidas."},
        {"nombre": "Rollitos de jamón y queso con ensalada", "mh": "3 rollitos", "prep": "Jamón cocido natural."},
        {"nombre": "Arroz con pollo (versión fría)", "mh": "1 bowl mediano", "prep": "Pollo picado y arroz integral."},
        {"nombre": "Salpicón de ave y vegetales", "mh": "1 plato abundante", "prep": "Todo picado con vinagreta liviana."},
        {"nombre": "Empanadas de carne o verdura", "mh": "2 unidades", "prep": "Al horno."}
    ]
    dym = [
        {"nombre": "Infusión con tostadas integrales y queso", "mh": "1 taza y 2 tostadas", "prep": "Queso descremado."},
        {"nombre": "Yogur descremado con granola y banana", "mh": "1 pote y 1/2 banana", "prep": "Mezclar al momento."},
        {"nombre": "Mate cocido con leche y budín de avena", "mh": "1 taza y 1 rodaja", "prep": "Sin azúcar."},
        {"nombre": "Tostado integral de queso magro", "mh": "2 rodajas de pan", "prep": "En sandwichera."},
        {"nombre": "Leche descremada con copos de maíz", "mh": "1 taza mediana", "prep": "Sin azúcar."},
        {"nombre": "Panqueque de avena con mermelada diet", "mh": "1 unidad", "prep": "Con claras y avena."},
        {"nombre": "Fruta con frutos secos", "mh": "1 bowl chico", "prep": "Fruta picada y 3 nueces."},
        {"nombre": "Galletitas de arroz con queso y mermelada", "mh": "3 unidades", "prep": "Queso blanco descremado."},
        {"nombre": "Licuado de banana con leche descremada", "mh": "1 vaso grande", "prep": "Sin azúcar agregada."},
        {"nombre": "Omelette dulce de claras y manzana", "mh": "1 unidad", "prep": "Manzana rallada."},
        {"nombre": "Rebanada de pan integral con palta y huevo", "mh": "1 unidad", "prep": "Huevo poché o revuelto."},
        {"nombre": "Yogur con semillas de chía y arándanos", "mh": "1 pote", "prep": "Dejar hidratar las semillas."},
        {"nombre": "Café con leche y galletas integrales", "mh": "1 taza y 4 galletas", "prep": "Sin azúcar."},
        {"nombre": "Bowl de avena cocida con canela", "mh": "1 taza chica", "prep": "Cocida con agua o leche descr."},
        {"nombre": "Infusión con 1 porción de bizcochuelo casero", "mh": "1 rodaja fina", "prep": "Hecho con aceite y sin azúcar."}
    ]
    col = [
        {"nombre": "Fruta de estación", "mh": "1 unidad", "prep": "Lavar bien."},
        {"nombre": "Yogur descremado", "mh": "1 pote", "prep": "Natural."},
        {"nombre": "Huevo duro", "mh": "1 unidad", "prep": "Hervido."},
        {"nombre": "Gelatina diet", "mh": "1 compotera", "prep": "Con fruta."},
        {"nombre": "Puñado de almendras", "mh": "10 unidades", "prep": "Crudas."},
        {"nombre": "Bastoncitos de zanahoria", "mh": "1 taza", "prep": "Crudos."},
        {"nombre": "Queso magro en cubitos", "mh": "1 feta gruesa", "prep": "Tipo Tybo light."},
        {"nombre": "Tomates cherry", "mh": "10 unidades", "prep": "Frescos."},
        {"nombre": "Pickles caseros", "mh": "1 compotera chica", "prep": "Bajos en sodio."},
        {"nombre": "Media palta chica", "mh": "1/2 unidad", "prep": "Con limón."},
        {"nombre": "Barrita de cereal casera", "mh": "1 unidad", "prep": "Sin azúcar agregada."},
        {"nombre": "Cucharada de semillas de girasol", "mh": "1 cda. sopera", "prep": "Tostadas sin sal."}
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
p_obj = cp1.number_input(f"{label_p} - Sugerido", value=float(val_sugerido), key=f"p_obj_dyn_{sexo}_{talla_cm}_{peso_actual}")
kcal_final = (p_obj * 22) * af_val
cp2.info(f"**Prescripción:** {t_plan} de {kcal_final:.0f} kcal/día")

# --- 6. MENÚ ---
st.divider()
c_a, c_b = st.columns(2)
alm_trabajo = c_a.checkbox("Almuerzo en el trabajo", key="check_trabajo")
colaciones_on = c_b.checkbox("Incluir colaciones (Mañana y Tarde)", key="check_colaciones")

if st.button("🚀 GENERAR PLAN", key="btn_generar"):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    st.session_state.menu = {}
    
    ultimo_dym = []
    ultimo_ayc = []
    ultimo_col = []

    for d in dias:
        pool_dym = [x for x in st.session_state.db["dym"] if x not in ultimo_dym]
        dym_hoy = random.sample(pool_dym if len(pool_dym) >= 2 else st.session_state.db["dym"], 2)
        
        if alm_trabajo:
            pool_trab = [x for x in st.session_state.db["trabajo"] if x not in ultimo_ayc]
            almuerzo = random.choice(pool_trab if pool_trab else st.session_state.db["trabajo"])
            pool_cena = [x for x in st.session_state.db["ayc"] if x not in ultimo_ayc and x != almuerzo]
            cena = random.choice(pool_cena if pool_cena else st.session_state.db["ayc"])
        else:
            pool_ayc = [x for x in st.session_state.db["ayc"] if x not in ultimo_ayc]
            ayc_hoy = random.sample(pool_ayc if len(pool_ayc) >= 2 else st.session_state.db["ayc"], 2)
            almuerzo, cena = ayc_hoy[0], ayc_hoy[1]
            
        if colaciones_on:
            pool_col = [x for x in st.session_state.db["col"] if x not in ultimo_col]
            cols_hoy = random.sample(pool_col if len(pool_col) >= 2 else st.session_state.db["col"], 2)
        else:
            cols_hoy = []

        st.session_state.menu[d] = {
            "Desayuno": dym_hoy[0],
            "Almuerzo": almuerzo,
            "Merienda": dym_hoy[1],
            "Cena": cena,
            "Colaciones": cols_hoy
        }
        
        ultimo_dym = dym_hoy
        ultimo_ayc = [almuerzo, cena]
        ultimo_col = cols_hoy

if st.session_state.menu:
    for dia, comidas in st.session_state.menu.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for p in plato: st.write(f"🔸 **Colación:** {p['nombre']}")
                else:
                    ci, cb = st.columns([0.9, 0.1])
                    ci.write(f"🍴 **{tiempo}:** {plato['nombre']}")
                    if cb.button("🔄", key=f"refresh_{dia}_{tiempo}"):
                        t = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and alm_trabajo) else "ayc")
                        st.session_state.menu[dia][tiempo] = random.choice(st.session_state.db[t])
                        st.rerun()

    st.divider()
    pdf_bytes = generar_pdf(nutri_info, {"nombre": nombre_pac, "edad": edad, "talla": talla_cm}, st.session_state.menu, {"diag": diag, "t_plan": t_plan, "kcal": kcal_final})
    st.download_button("💾 DESCARGAR PDF PROFESIONAL", data=pdf_bytes, file_name=f"Plan_{nombre_pac.replace(' ', '_')}.pdf", mime="application/pdf", key="btn_descarga_pdf")

import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente AR", layout="wide")

# --- BASE DE DATOS DE 100 PLATOS ---
def cargar_base_datos():
    dym = [
        "Infusión con 2 tostadas integrales y queso untable", "Yogur descremado con granola y media banana",
        "Mate con 3 galletitas de agua y queso por salut light", "Café con leche y 1 macedonia de frutas",
        "Tostado de pan integral con queso y tomate", "Infusión con 2 galletas de arroz y mermelada diet",
        "Yogur con 3 nueces y 1 cda de avena", "Licuado de durazno con agua y 2 tostadas integrales",
        "Mate cocido con leche y 1 marquise de manzana saludable", "Té con limón y 3 vainillas",
        "Omelette de claras con queso y 1 kiwi", "Infusión con 1 rodaja de budín de avena",
        "Yogur con cereales sin azúcar y frutillas", "Leche descremada con copos de maíz (1/2 taza)",
        "Café con 1 tostada con huevo revuelto", "Infusión con sándwich de pan negro, queso y pepino",
        "Mate con 2 bizcochos de avena caseros", "Yogur con mix de semillas (lino, chía)",
        "Tostada con ricota descremada y ralladura de limón", "Infusión con 1 pera y 2 nueces",
        "Batido de proteínas casero (leche y fruta)", "Té verde con 2 galletitas de salvado",
        "Panqueque de avena con dulce de leche diet", "Ensalada de frutas con copete de yogur",
        "Mate cocido con 1 bay biscuit", "Infusión con 2 grisines integrales y queso",
        "Café con leche y macedonia de naranja y pomelo", "Yogur descremado firme con almendras",
        "Tostada integral con hummus de garbanzo", "Infusión con 1 manzana asada con canela"
    ]
    
    ayc = [
        "Milanesa de peceto al horno con puré de calabaza + 1 naranja", "Filet de merluza con ensalada de rúcula y tomate + 1 manzana",
        "Pollo al horno sin piel con vegetales asados + Gelatina diet", "Bife de cuadril magro con ensalada mixta + 1 pera",
        "Tarta de zapallitos (sin tapa) + 1 durazno", "Canelones de verdura con salsa fileto + 1 mandarina",
        "Wok de pollo y vegetales + 1 kiwi", "Zapallitos rellenos con carne magra y queso + 1 rodaja de piña",
        "Ensalada de lentejas, tomate y huevo + 1 manzana", "Fideos integrales con brócoli y ajo + Gelatina diet",
        "Hamburguesa de lentejas con ensalada + 1 naranja", "Cazuela de pollo con calabaza y arvejas + 1 ciruela",
        "Pastel de papa y carne magra + 1 mandarina", "Tortilla de espinaca al horno + 1 pera",
        "Arroz integral con atún y vegetales + 1 durazno", "Brochetas de carne y verduras + 1 naranja",
        "Calabaza rellena con choclo y queso + Gelatina diet", "Budín de zanahoria con hojas verdes + 1 banana chica",
        "Suprema a la mostaza con puré mixto + 1 manzana", "Salpicón de ave completo + 1 kiwi",
        "Risotto de vegetales y hongos + 1 pera", "Costillita de cerdo magra con puré de manzana + 1 rodaja de piña",
        "Omelette de espinaca y queso + Gelatina diet", "Guiso de lentejas saludable + 1 mandarina",
        "Albóndigas de pollo con arroz + 1 durazno", "Pizza con masa integral y vegetales + 1 manzana",
        "Rollitos de merluza con puré de berenjena + 1 naranja", "Ensalada de garbanzos y pimiento + 1 pera",
        "Pescado a la vasca con papas + Gelatina diet", "Pollo al verdeo con chauchas + 1 mandarina",
        "Tarta de calabaza y choclo + 1 manzana", "Bife de lomo con remolacha y huevo + 1 naranja",
        "Estofado de ternera con verduras + 1 pera", "Wraps de lechuga con carne y zanahoria + 1 durazno",
        "Revuelto gramajo saludable + 1 kiwi", "Torrejas de acelga al horno + Gelatina diet",
        "Lomito al plato con rúcula + 1 rodaja de piña", "Pimientos rellenos con arroz + 1 naranja",
        "Suprema grillada con chaucha y huevo + 1 manzana", "Colita de cuadril con calabaza asada + 1 pera",
        "Soufflé de zapallitos + Gelatina diet", "Ensalada de pasta fría con queso + 1 durazno",
        "Medallón de merluza con zanahoria + 1 mandarina", "Wok de carne con cebolla y morrón + 1 kiwi",
        "Pollo a la provenzal con papas + 1 manzana", "Zapallo cabutiá con ricota + 1 naranja",
        "Canelones de choclo con salsa blanca light + 1 pera", "Matambre de pollo con ensalada + Gelatina diet",
        "Milanesa de berenjena con queso + 1 mandarina", "Cuscús con vegetales y pollo + 1 durazno"
    ]

    trabajo = ["Sándwich integral de pollo", "Ensalada de arroz y atún", "Tarta de acelga", "Empanadas de verdura (2)", "Wrap de carne", "Ensalada de fideos", "Budín de zapallitos", "Milanesa de pollo al pan", "Ensalada de lentejas", "Rolls de jamón y queso"]
    colaciones = ["1 Fruta", "1 Yogur", "2 Nueces", "1 Barrita", "3 Almendras", "Postre diet", "Queso magro", "1 Huevo duro", "Gelatina con fruta", "2 Orejones"]
    
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

# Diagnóstico IMC
talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Normopeso"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
else: diag = "Obesidad"
st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")
st.divider()

# --- 2. PRESCRIPCIÓN REACTIVA ---
st.header("2. Prescripción")

# Lógica PI Broca (Femenino 0.9 / Masculino 1.0)
base_broca = talla_cm - 100
pi_sugerido = base_broca * 0.90 if sexo == "Femenino" else base_broca

# Lógica Wilkens si hay Sobrepeso
if imc >= 25:
    valor_sugerido = ((peso_actual - pi_sugerido) * 0.25) + pi_sugerido
    tipo_peso = "Peso Ideal Corregido (Wilkens)"
else:
    valor_sugerido = pi_sugerido
    tipo_peso = "Peso Ideal (Broca)"

cp1, cp2 = st.columns(2)
with cp1:
    # Usamos una clave (key) que cambie con el sexo/talla para forzar el refresco del valor
    p_obj = st.number_input(f"{tipo_peso} - Editable", value=float(valor_sugerido), key=f"p_obj_{sexo}_{talla_cm}")

with cp2:
    kcal_final = (p_obj * 22) * af_opciones[af_label]
    st.info(f"**Requerimiento:** {kcal_final:.0f} kcal/día")
    st.write(f"CHO 55% | PRO 17.5% | GRA 27.5%")

st.divider()

# --- 3. MENÚ ---
st.header("3. Plan Semanal")
col_c1, col_c2 = st.columns(2)
alm_trabajo = col_c1.checkbox("Almuerzo en el trabajo")
colaciones_on = col_c2.checkbox("Añadir 2 colaciones diarias")

if st.button("🚀 GENERAR PLAN SEMANAL"):
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
    for dia, comidas in st.session_state.menu_semanal.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for p in plato: st.write(f"🔸 **Colación:** {p}")
                else:
                    ci, cb = st.columns([0.85, 0.15])
                    ci.write(f"🍴 **{tiempo}:** {plato}")
                    if cb.button("🔄", key=f"sw_{dia}_{tiempo}"):
                        t = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and alm_trabajo) else "ayc")
                        st.session_state.menu_semanal[dia][tiempo] = elegir_plato(t, set())
                        st.rerun()

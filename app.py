import streamlit as st
import random

st.set_page_config(page_title="NutriAsistente AR", layout="wide")

# --- BASE DE DATOS DE 100 PLATOS ARGENTINOS ---
if 'db_platos' not in st.session_state:
    # 30 Desayunos y Meriendas (DyM)
    dym = [
        "Infusión con 2 tostadas de pan integral y queso untable", "Yogur descremado con granola y media banana",
        "Mate con 3 galletitas de agua y queso por salut light", "Café con leche y 1 macedonia de frutas",
        "Tostado de pan integral con queso y tomate", "Infusión con 2 galletas de arroz y mermelada diet",
        "Yogur con 3 nueces y 1 cucharada de avena", "Licuado de durazno con agua y 2 tostadas integrales",
        "Mate cocido con leche y 1 marquise de manzana saludable", "Té con limón y 3 vainillas",
        "Omelette de claras con queso y 1 kiwi", "Infusión con 1 rodaja de budín de avena artesanal",
        "Yogur con cereales sin azúcar y frutillas", "Leche descremada con copos de maíz (media taza)",
        "Café con 1 tostada con huevo revuelto", "Infusión con sándwich de pan negro, queso y pepino",
        "Mate con 2 bizcochos de avena caseros", "Yogur con mix de semillas (lino, chía)",
        "Tostada con ricota descremada y ralladura de limón", "Infusión con 1 pera y 2 nueces",
        "Batido de proteínas casero (leche y fruta)", "Té verde con 2 galletitas de salvado",
        "Panqueque de avena con dulce de leche diet", "Ensalada de frutas con copete de yogur",
        "Mate cocido con 1 bay biscuit", "Infusión con 2 grisines integrales y queso",
        "Café con leche y macedonia de naranja y pomelo", "Yogur descremado firme con almendras",
        "Tostada integral con hummus de garbanzo", "Infusión con 1 manzana asada con canela"
    ]
    
    # 50 Almuerzos y Cenas (AyC) - Incluyen postre (Fruta o Gelatina diet)
    ayc = [
        "Milanesa de peceto al horno con puré de calabaza + 1 naranja", "Filet de merluza al limón con ensalada de rúcula y tomate + 1 manzana",
        "Pollo al horno sin piel con vegetales asados + Gelatina diet", "Bife de cuadril magro con ensalada mixta + 1 pera",
        "Tarta de zapallitos (sin tapa superior) + 1 durazno", "Canelones de verdura con salsa fileto + 1 mandarina",
        "Wok de pollo y vegetales (morrón, cebolla, zapallito) + 1 kiwi", "Zapallitos rellenos con carne picada magra y queso + 1 rodaja de piña",
        "Ensalada de lentejas, tomate, cebolla y huevo duro + 1 manzana", "Fideos integrales con brócoli y ajo + Gelatina diet",
        "Hamburguesa de lentejas con ensalada de repollo y zanahoria + 1 naranja", "Cazuela de pollo con calabaza y arvejas + 1 ciruela",
        "Pastel de papa y carne magra (porción moderada) + 1 mandarina", "Tortilla de espinaca al horno con tomate partido + 1 pera",
        "Arroz integral con atún y jardinera de vegetales + 1 durazno", "Brochetas de carne y verduras a la plancha + 1 naranja",
        "Calabaza rellena con choclo y queso + Gelatina diet", "Budín de zanahoria y zapallito con ensalada de hojas verdes + 1 banana chica",
        "Suprema de pollo a la mostaza con puré mixto + 1 manzana", "Salpicón de ave completo (lechuga, tomate, zanahoria, pollo) + 1 kiwi",
        "Risotto de vegetales y hongos + 1 pera", "Costillita de cerdo magra con puré de manzana + 1 rodaja de ananá",
        "Omelette de espinaca y queso con ensalada de tomate + Gelatina diet", "Guiso de lentejas saludable (sin embutidos) + 1 mandarina",
        "Albóndigas de pollo en salsa de tomate con arroz + 1 durazno", "Pizza con masa integral y vegetales + 1 manzana",
        "Rollitos de merluza con puré de berenjena + 1 naranja", "Ensalada de garbanzos, pimiento y cebolla + 1 pera",
        "Pescado a la vasca con papas al natural + Gelatina diet", "Pollo al verdeo con ensalada de chauchas + 1 mandarina",
        "Tarta de calabaza y choclo (sin tapa) + 1 manzana", "Bife de lomo con ensalada de remolacha y huevo + 1 naranja",
        "Estofado de ternera con muchas verduras + 1 pera", "Wraps de lechuga rellenos de carne y zanahoria + 1 durazno",
        "Revuelto gramajo saludable (huevo, jamón cocido, arvejas) + 1 kiwi", "Torrejas de acelga al horno con ensalada + Gelatina diet",
        "Lomito al plato con ensalada de rúcula y parmesano + 1 rodaja de piña", "Pimientos rellenos con arroz y vegetales + 1 naranja",
        "Suprema de pollo grillada con ensalada de chaucha y huevo + 1 manzana", "Colita de cuadril al horno con calabaza asada + 1 pera",
        "Soufflé de zapallitos + Gelatina diet", "Ensalada de pasta fría con tomate, albahaca y queso + 1 durazno",
        "Medallón de merluza con ensalada de zanahoria rallada + 1 mandarina", "Wok de carne con cebolla y morrones + 1 kiwi",
        "Pollo a la provenzal con papas hervidas + 1 manzana", "Zapallo cabutiá relleno con ricota y verdeo + 1 naranja",
        "Canelones de choclo con salsa blanca light + 1 pera", "Matambre de pollo con ensalada mixta + Gelatina diet",
        "Milanesa de berenjena con queso y tomate + 1 mandarina", "Cuscús con vegetales y pollo + 1 durazno"
    ]

    # 10 Almuerzos Trabajo (Apto Microondas / Frío)
    trabajo = [
        "Sándwich integral de pollo, lechuga y tomate", "Ensalada de arroz, atún y choclo",
        "Tarta de acelga y queso", "Empanadas de verdura (2 unidades) con ensalada",
        "Wrap integral de carne y palta", "Ensalada de fideos con arvejas y zanahoria",
        "Budín de zapallitos en porciones", "Milanesa de pollo al pan con lechuga",
        "Ensalada de lentejas y huevo duro", "Rolls de jamón, queso y tomate"
    ]

    # 10 Colaciones
    colaciones = [
        "1 Fruta de estación", "1 Yogur descremado", "2 Mitades de nuez", "1 Barrita de cereal",
        "3 Almendras", "1 Postre de leche diet", "1 Rodaja de queso magro", "1 Huevo duro",
        "Gelatina diet con frutas", "2 Orejones de damasco"
    ]

    # Guardar todo en una lista maestra
    st.session_state.db_platos = []
    for p in dym: st.session_state.db_platos.append({"nombre": p, "tipo": "dym", "kcal": 300})
    for p in ayc: st.session_state.db_platos.append({"nombre": p, "tipo": "ayc", "kcal": 550})
    for p in trabajo: st.session_state.db_platos.append({"nombre": p, "tipo": "trabajo", "kcal": 450})
    for p in colaciones: st.session_state.db_platos.append({"nombre": p, "tipo": "colacion", "kcal": 100})

if 'menu_semanal' not in st.session_state:
    st.session_state.menu_semanal = {}

# --- FUNCIÓN PARA NO REPETIR ---
def obtener_plato_unico(tipo, mazo):
    random.shuffle(mazo)
    for i, plato in enumerate(mazo):
        if plato['tipo'] == tipo:
            return mazo.pop(i)
    return {"nombre": "Consultar lista de intercambios", "kcal": 0}

# --- INTERFAZ ---
st.title("Generador de Planes Nutricionales 🍏")
st.header("1. Evaluación y Diagnóstico")

c1, c2, c3 = st.columns(3)
with c1:
    nombre = st.text_input("Nombre del paciente", "Paciente Ejemplo")
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
with c2:
    peso_actual = st.number_input("Peso Actual (kg)", min_value=30.0, value=75.0)
    talla_cm = st.number_input("Talla (cm)", min_value=100.0, value=160.0)
with c3:
    edad = st.number_input("Edad", min_value=15, value=30)
    af_opciones = {"Sedentario": 1.2, "Leve": 1.3, "Moderado": 1.5, "Intenso": 1.7}
    af_label = st.selectbox("Nivel de Actividad Física", list(af_opciones.keys()))

# Lógica IMC
talla_m = talla_cm / 100
imc = peso_actual / (talla_m ** 2)
if imc < 18.5: diag = "Delgadez"
elif 18.5 <= imc <= 24.9: diag = "Normopeso"
elif 25.0 <= imc <= 29.9: diag = "Sobrepeso"
else: diag = "Obesidad"

st.subheader(f"Diagnóstico: {diag} (IMC: {imc:.2f})")
st.divider()

st.header("2. Prescripción")
col_p1, col_p2 = st.columns(2)

# PI Broca corregido
base_broca = talla_cm - 100
pi_resultado = base_broca * 0.90 if sexo == "Femenino" else base_broca

with col_p1:
    if imc < 25:
        p_obj = st.number_input("Peso Ideal (Broca) - Editable", value=float(pi_resultado))
    else:
        pic_wilkens = ((peso_actual - pi_resultado) * 0.25) + pi_resultado
        p_obj = st.number_input("Peso Ideal Corregido (Wilkens) - Editable", value=float(pic_wilkens))

with col_p2:
    kcal_final = (p_obj * 22) * af_opciones[af_label]
    st.info(f"**Requerimiento:** {kcal_final:.0f} kcal/día")
    st.write(f"**Distribución:** CHO 55% | PRO 17.5% | GRA 27.5%")
    st.write("**Objetivos:** Descenso de peso y educación alimentaria.")

st.divider()

st.header("3. Plan Semanal")
c_conf1, c_conf2, c_conf3 = st.columns(3)
alm_trabajo = c_conf1.checkbox("Almuerzo en el trabajo")
colaciones_on = c_conf2.checkbox("Añadir 2 colaciones")

if c_conf3.button("🚀 GENERAR PLAN"):
    mazo = st.session_state.db_platos.copy()
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for d in dias:
        tipo_a = "trabajo" if alm_trabajo else "ayc"
        st.session_state.menu_semanal[d] = {
            "Desayuno": obtener_plato_unico("dym", mazo),
            "Almuerzo": obtener_plato_unico(tipo_a, mazo),
            "Merienda": obtener_plato_unico("dym", mazo),
            "Cena": obtener_plato_unico("ayc", mazo),
            "Colaciones": [obtener_plato_unico("colacion", mazo), obtener_plato_unico("colacion", mazo)] if colaciones_on else []
        }

if st.session_state.menu_semanal:
    for dia, comidas in st.session_state.menu_semanal.items():
        with st.expander(f"📅 {dia}"):
            for tiempo, plato in comidas.items():
                if tiempo == "Colaciones":
                    for c in plato: st.write(f"🔸 **Colación:** {c['nombre']}")
                else:
                    ci, cb = st.columns([0.9, 0.1])
                    ci.write(f"🍴 **{tiempo}:** {plato['nombre']}")
                    if cb.button("🔄", key=f"sw_{dia}_{tiempo}"):
                        mazo_temp = st.session_state.db_platos.copy()
                        t = "dym" if tiempo in ["Desayuno", "Merienda"] else ("trabajo" if (tiempo == "Almuerzo" and alm_trabajo) else "ayc")
                        st.session_state.menu_semanal[dia][tiempo] = obtener_plato_unico(t, mazo_temp)
                        st.rerun()

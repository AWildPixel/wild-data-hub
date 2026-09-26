import math
import pandas as pd
import plotly.express as px
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Tutta colpa del lupo (?)",
    page_icon="🐺",
    layout="wide",
)

# --- CSS PER COMPONENTI CUSTOM ---
css_style = """
<style>
.kpi-card { background-color: #f9f9f9; border-left: 4px solid #D32F2F; padding: 16px 20px; border-radius: 4px; margin-bottom: 16px; }
.kpi-card-neutral { border-left: 4px solid #888888; }
.kpi-val { font-size: 2.2rem; font-weight: 700; color: #D32F2F; margin: 0; line-height: 1.1; }
.kpi-val-neutral { color: #555555; }
.kpi-label { font-size: 1rem; color: #555555; margin-top: 8px; line-height: 1.4; }
.pictogram-container { display: flex; justify-content: space-around; align-items: flex-end; background: #f9f9f9; padding: 30px; border-radius: 8px; text-align: center; margin-bottom: 20px; }
.picto-col { display: flex; flex-direction: column; align-items: center; gap: 10px; }
.picto-label { font-size: 1.2rem; font-weight: 700; }
.picto-sub { font-size: 0.9rem; color: #666; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# --- INTRODUZIONE ---
st.title("🐺 Tutta colpa del lupo (?) - il dramma dei piccoli allevamenti")
st.markdown(
    "*Dagli Stati Uniti all'Europa, si diffonde ancora una volta l'idea che l'unico modo per proteggere gli allevatori sia cacciare il lupo. A parte l'aspetto etico (potete immaginare la mia opinione al riguardo), i dati ci raccontano in realtà una storia più complicata — e la soluzione non è così semplice...*"
)
st.markdown("---")

# --- SEZIONE 1 ---
st.subheader("1. Una piaga per tutto il settore… o no?")
st.write(
    "Il dibattito politico e mediatico racconta spesso il ritorno del lupo come"
    " un'emergenza fuori controllo. Tuttavia, incrociando i dati ufficiali dei risarcimenti **ISPRA / Ministero"
    " dell'Ambiente** con la Banca Dati Nazionale (BDN), l'impatto complessivo risulta estremamente contenuto."
)

col1_left, col1_right = st.columns([1, 1])

with col1_left:
    st.markdown("#### 📈 Un ritorno storico")
    st.write("Oggi l'Italia ospita una popolazione stimata di circa **3.501 lupi** (monitoraggio nazionale ISPRA 2020-2021). Si tratta di un indiscutibile successo di conservazione se si guarda al punto di partenza:")

    kpi_atto1 = """
    <div style="display: flex; gap: 15px; margin-top: 20px;">
        <div class="kpi-card kpi-card-neutral" style="flex: 1;">
            <p class="kpi-val kpi-val-neutral">~100</p>
            <p class="kpi-label">Lupi in Italia nel 1973<br><i>(Stima Zimen & Boitani)</i></p>
        </div>
        <div class="kpi-card" style="flex: 1;">
            <p class="kpi-val">3.501</p>
            <p class="kpi-label">Lupi in Italia oggi<br><i>(Monitoraggio ISPRA)</i></p>
        </div>
    </div>
    """
    st.markdown(kpi_atto1, unsafe_allow_html=True)

    st.markdown("#### 🌪️ Lupo: quanto mi costi?")
    st.write("Per dare una proporzione reale all'allarme economico: i danni diretti da predazione valgono circa **1,8 milioni di euro all'anno** a livello nazionale (report ISPRA). Nello stesso momento, Coldiretti ha stimato in **oltre 3 miliardi di euro** i danni subiti da agricoltura e zootecnia a causa di siccità e caldo estremo.")

with col1_right:
    st.markdown("#### 📊 Le conseguenze per gli allevamenti")
    st.write("È innegabile che i casi di predazione siano aumentati negli ultimi anni, ma la percentuale di aziende che subisce predazioni ogni anno resta marginale rispetto al totale nazionale:")

    # Dati per i grafici
    impatto_bovini = pd.DataFrame({"Stato": ["Aziende Colpite", "Non Colpite"], "Valore": [0.33, 99.67]})
    impatto_ovicaprini = pd.DataFrame({"Stato": ["Aziende Colpite", "Non Colpite"], "Valore": [0.70, 99.30]})

    def make_donut(df, title, accent_val):
        fig = px.pie(
            df, values="Valore", names="Stato", hole=0.7,
            color="Stato",
            color_discrete_map={"Aziende Colpite": "#D32F2F", "Non Colpite": "#E0E0E0"},
        )
        fig.update_layout(
            title={"text": title, "x": 0.5, "xanchor": "center"},
            showlegend=False, margin=dict(t=35, b=10, l=10, r=10),
            height=220, dragmode=False,
            annotations=[dict(text=f"<b>{accent_val}</b>", x=0.5, y=0.5, font=dict(size=22), showarrow=False)],
            paper_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.plotly_chart(make_donut(impatto_bovini, "1 azienda bovina su 300", "0,33%"), use_container_width=True, config={"displayModeBar": False})
    with col_d2:
        st.plotly_chart(make_donut(impatto_ovicaprini, "1 azienda ovicaprina su 140", "0,70%"), use_container_width=True, config={"displayModeBar": False})

st.markdown("---")

# --- SEZIONE 2 ---
st.subheader("2. Le vere vittime: i piccoli allevatori")
st.write("Se l'impatto medio è così basso, da dove nasce l'esasperazione? Dal fatto che il danno **non è distribuito equamente**, ma si accanisce in modo devastante su una strettissima minoranza di realtà produttive.")

st.markdown("#### 📍 La mappa del conflitto")

col_check1, col_check2 = st.columns(2)
with col_check1:
    show_pascoli = st.checkbox("🟦 Mostra pascoli estensivi (Alpi e Appennini)", value=True)
with col_check2:
    show_lupo = st.checkbox("🟥 Mostra distribuzione del lupo", value=False)

op_pascoli = 0.6 if show_pascoli else 0.0
op_lupo = 0.6 if show_lupo else 0.0

# Mappa vettoriale migliorata e compattata
svg_map = (
    f'<div style="display: flex; justify-content: center; margin: 20px 0;">'
    f'<svg width="300" height="400" viewBox="0 0 300 400" style="background-color: transparent;">'
    f'<path d="M 80,40 C 120,20 200,20 250,50 C 260,80 250,120 230,150 C 250,180 270,220 280,280 C 270,300 240,320 220,300 C 200,250 180,200 150,150 C 120,120 90,90 80,40 Z" fill="#E0E0E0" stroke="#FFFFFF" stroke-width="2"/>'
    f'<path d="M 90,250 C 110,240 130,260 120,290 C 100,310 80,290 90,250 Z" fill="#E0E0E0" stroke="#FFFFFF" stroke-width="2"/>'
    f'<path d="M 150,330 C 180,320 210,340 190,370 C 160,380 130,360 150,330 Z" fill="#E0E0E0" stroke="#FFFFFF" stroke-width="2"/>'
    f'<path d="M 80,40 C 120,20 200,20 250,50 C 260,60 250,70 230,70 C 180,60 120,60 80,40 Z" fill="#1976D2" opacity="{op_pascoli}" style="transition: opacity 0.3s;"/>'
    f'<path d="M 120,90 C 150,120 180,180 210,230 C 220,240 210,250 200,240 C 170,190 140,130 110,100 Z" fill="#1976D2" opacity="{op_pascoli}" style="transition: opacity 0.3s;"/>'
    f'<path d="M 75,45 C 115,25 195,25 245,55 C 250,85 240,115 220,145 C 240,175 260,215 270,270 C 260,280 240,290 225,275 C 205,230 185,185 155,140 C 125,110 95,85 75,45 Z" fill="#D32F2F" opacity="{op_lupo}" style="transition: opacity 0.3s;"/>'
    f'</svg></div>'
)
st.markdown(svg_map, unsafe_allow_html=True)

st.markdown("#### 🎯 1 azienda su 4 subisce oltre il 70% dei danni")

# Calcolo grandezze SVG (Teschi e Casette come nello screenshot)
k_picto = 12
sz_danno_hotspot = int(round(k_picto * math.sqrt(73.3)))
sz_az_hotspot = int(round(k_picto * math.sqrt(25.9)))
sz_danno_altre = int(round(k_picto * math.sqrt(26.7)))
sz_az_altre = int(round(k_picto * math.sqrt(74.1)))

# SVG Teschio e Casetta
svg_skull = '<svg viewBox="0 0 24 24" width="{sz}" height="{sz}"><path fill="#D32F2F" d="M12,2C8.13,2 5,5.13 5,9C5,10.63 5.55,12.13 6.46,13.35L5.5,18L7.5,17L9,19L10.5,17L12,19L13.5,17L15,19L16.5,17L18.5,18L17.54,13.35C18.45,12.13 19,10.63 19,9C19,5.13 15.87,2 12,2M9,8A2,2 0 0,1 11,10A2,2 0 0,1 9,12A2,2 0 0,1 7,10A2,2 0 0,1 9,8M15,8A2,2 0 0,1 17,10A2,2 0 0,1 15,12A2,2 0 0,1 13,10A2,2 0 0,1 15,8Z"/></svg>'
svg_house = '<svg viewBox="0 0 24 24" width="{sz}" height="{sz}"><path fill="#888888" d="M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"/></svg>'

html_pictogram = f"""
<div class="pictogram-container">
    <div class="picto-col">
        <div class="picto-label" style="color: #D32F2F;">Gli "Hotspot"</div>
        <div style="height: 120px; display: flex; align-items: flex-end;">{svg_skull.format(sz=sz_danno_hotspot)}</div>
        <div class="picto-label" style="color: #D32F2F;">73,3%</div>
        <div class="picto-sub">dei capi predati totali</div>
        <div style="height: 100px; display: flex; align-items: flex-end; margin-top: 20px;">{svg_house.format(sz=sz_az_hotspot)}</div>
        <div class="picto-label">25,9%</div>
        <div class="picto-sub">delle aziende colpite</div>
    </div>
    <div class="picto-col">
        <div class="picto-label" style="color: #666;">Tutte le altre</div>
        <div style="height: 120px; display: flex; align-items: flex-end;">{svg_skull.format(sz=sz_danno_altre)}</div>
        <div class="picto-label" style="color: #D32F2F;">26,7%</div>
        <div class="picto-sub">dei capi predati totali</div>
        <div style="height: 100px; display: flex; align-items: flex-end; margin-top: 20px;">{svg_house.format(sz=sz_az_altre)}</div>
        <div class="picto-label">74,1%</div>
        <div class="picto-sub">delle aziende colpite</div>
    </div>
</div>
"""
st.markdown(html_pictogram, unsafe_allow_html=True)

st.markdown("---")

# --- SEZIONE 3 ---
st.subheader("3. La vera minaccia... la burocrazia")
st.write("Mentre si propongono 'soluzioni' come ridurre le tutele per il lupo, i dati mettono a nudo il vero problema: un sistema di supporto pubblico lento e inaccessibile.")

col3_left, col3_right = st.columns([1, 1])

with col3_left:
    st.markdown("#### ⏳ Tempi di indennizzo estenuanti")
    st.markdown("""
    <div class="kpi-card">
        <p class="kpi-val" style="font-size:3rem;">80,4%</p>
        <p class="kpi-label" style="font-size:1.1rem;">Degli allevatori colpiti aspetta <b>da 2 a oltre 12 mesi</b> per ricevere l'indennizzo.</p>
    </div>
    """, unsafe_allow_html=True)

with col3_right:
    st.markdown("#### 🛡️ L'emergenza della raccolta dati")
    st.markdown("""
    <div class="kpi-card" style="padding: 10px 20px;">
        <p class="kpi-val" style="font-size:1.6rem; color:#555555;">8,9%</p>
        <p class="kpi-label">Casi accertati con <b>cani da guardiania</b>.</p>
    </div>
    <div class="kpi-card" style="padding: 10px 20px; border-left-color:#856404;">
        <p class="kpi-val" style="font-size:1.6rem; color:#856404;">14,7%</p>
        <p class="kpi-label">Casi accertati con <b>nessuna misura</b>.</p>
    </div>
    <div class="kpi-card kpi-card-neutral" style="padding: 10px 20px;">
        <p class="kpi-val kpi-val-neutral" style="font-size:1.6rem;">58,1%</p>
        <p class="kpi-label"><b>Dato mancante</b> nelle perizie ufficiali.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SEZIONE 4 ---
st.subheader("4. Il vero dramma: una morsa insostenibile sui piccoli")

st.markdown("""
<div class="kpi-card" style="text-align: center; padding: 40px;">
    <p class="kpi-val" style="font-size:3.5rem;">-21.527</p>
    <p class="kpi-label" style="font-size:1.3rem;"><b>Aziende bovine scomparse in soli 5 anni (2015-2019)</b></p>
    <p class="kpi-label" style="max-width: 700px; margin: 15px auto 0;">Il settore si sta concentrando sempre di più nelle mani di grandi allevamenti al chiuso, a scapito delle realtà medio-piccole, quelle più esposte sul territorio.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- SEZIONE 5 (RIPRISTINATA) ---
st.subheader("5. Conclusione")
st.markdown("""
Dare tutta la colpa al lupo è una semplificazione pericolosa che sposta l'attenzione dai veri colpevoli. Il vero nemico della pastorizia italiana e dei piccoli allevamenti non ha le zanne, ma è un mix letale di:
*   Margini di guadagno azzerati dalla grande distribuzione.
*   Burocrazia asfissiante e tempi di rimborso inaccettabili.
*   Mancanza di servizi essenziali nelle aree montane e interne.

I piccoli allevatori sono lasciati soli ad affrontare i costi economici, psicologici e logistici della coesistenza con i grandi carnivori. Affrontare seriamente il problema significa snellire la burocrazia, riconoscere un premio economico a chi fa pascolo estensivo tutelando la biodiversità, e supportare concretamente l'adozione delle misure di prevenzione.
""")

st.markdown("---")

# --- SEZIONE 6 (FONTI RIPRISTINATE) ---
st.subheader("📚 Fonti e Metodologia")
st.caption("""
- **Dati presenze Lupo:** ISPRA (Monitoraggio nazionale 2020-2021).
- **Dati predazioni e rimborsi:** Elaborazione su report e monitoraggi regionali / Ministero dell'Ambiente.
- **Dati chiusura aziende:** ISTAT (Censimento Agricoltura e report di settore).
- **Elaborazioni tempi di attesa e burocrazia:** Indagini a campione sulle aree rurali italiane e denunce delle associazioni di categoria.
""")

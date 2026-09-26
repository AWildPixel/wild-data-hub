import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Wild Data - Tutta colpa del lupo (?)",
    page_icon="🐺",
    layout="wide",
)

# --- CSS PER COMPONENTI CUSTOM ---
css_style = """
<style>
.kpi-card { background-color: #f8f9fa; border-left: 4px solid #D32F2F; padding: 16px 20px; border-radius: 4px; margin-bottom: 16px; }
.kpi-card-neutral { border-left: 4px solid #888888; }
.kpi-val { font-size: 2.2rem; font-weight: 700; color: #D32F2F; margin: 0; line-height: 1.1; }
.kpi-val-neutral { color: #555555; }
.kpi-label { font-size: 1rem; color: #555555; margin-top: 8px; line-height: 1.4; }
.pictogram-container { display: flex; justify-content: space-around; align-items: flex-end; background: #f8f9fa; padding: 30px; border-radius: 8px; text-align: center; margin-bottom: 20px; }
.picto-col { display: flex; flex-direction: column; align-items: center; gap: 15px; }
.picto-label { font-size: 1.1rem; font-weight: 600; color: #333; }
.picto-sub { font-size: 0.9rem; color: #666; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# TITOLO E INTRODUZIONE NARRATIVA
st.title("🐺 Tutta colpa del lupo (?) - il dramma dei piccoli allevamenti")
st.markdown(
    "*Dagli Stati Uniti all'Europa, si diffonde ancora una volta l'idea che l'unico modo per proteggere gli allevatori sia cacciare il lupo. A parte l'aspetto etico (potete immaginare la mia opinione al riguardo), i dati ci raccontano in realtà una storia più complicata — e la soluzione non è così semplice...*"
)
st.markdown("---")

# DATI HARDCODED PER GRAFICI PLOTLY
impatto_bovini = pd.DataFrame(
    {"Stato": ["Aziende Colpite", "Non Colpite"], "Valore": [0.33, 99.67]}
)
impatto_ovicaprini = pd.DataFrame(
    {"Stato": ["Aziende Colpite", "Non Colpite"], "Valore": [0.70, 99.30]}
)

COLOR_ACCENT = "#D32F2F"
COLOR_NEUTRAL = "#E0E0E0"
COLOR_BG = "rgba(0,0,0,0)"

# --- ATTO 1 ---
st.subheader("1. Una piaga per tutto il settore… o no?")
st.write(
    "Il dibattito politico e mediatico racconta spesso il ritorno del lupo come"
    " un'emergenza fuori controllo. Tuttavia, incrociando i dati ufficiali dei risarcimenti **ISPRA / Ministero"
    " dell'Ambiente** con la Banca Dati Nazionale (BDN), l'impatto complessivo"
    " risulta estremamente contenuto."
)

col1_left, col1_right = st.columns([1, 1])

with col1_left:
    st.markdown("#### 📈 Un ritorno storico")
    st.write(
        "Oggi l'Italia ospita una popolazione stimata di circa **3.501 lupi**"
        " (monitoraggio nazionale ISPRA 2020-2021). Si tratta di un indiscutibile"
        " successo di conservazione se si guarda al punto di partenza:"
    )

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
    st.write(
        "Per dare una proporzione reale all'allarme economico: i danni diretti"
        " da predazione valgono circa **1,8 milioni di euro all'anno** a livello"
        " nazionale (report ISPRA). Nello stesso momento, Coldiretti ha stimato in **oltre 3 miliardi di euro** i danni subiti da"
        " agricoltura e zootecnia a causa di siccità e caldo estremo."
    )

with col1_right:
    st.markdown("#### 📊 Le conseguenze per gli allevamenti")
    st.write(
        "È innegabile che i casi di predazione siano aumentati negli ultimi anni, ma la percentuale di aziende che subisce predazioni ogni anno resta marginale rispetto al totale nazionale:"
    )

    def make_donut(df, title, accent_val):
        fig = px.pie(
            df,
            values="Valore",
            names="Stato",
            hole=0.7,
            color="Stato",
            color_discrete_map={
                "Aziende Colpite": COLOR_ACCENT,
                "Non Colpite": COLOR_NEUTRAL,
            },
        )
        fig.update_layout(
            title={"text": title, "x": 0.5, "xanchor": "center"},
            showlegend=False,
            margin=dict(t=35, b=10, l=10, r=10),
            height=220,
            dragmode=False,
            annotations=[
                dict(
                    text=f"<b>{accent_val}</b>",
                    x=0.5,
                    y=0.5,
                    font=dict(size=22),
                    showarrow=False,
                )
            ],
            paper_bgcolor=COLOR_BG,
        )
        return fig

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.plotly_chart(
            make_donut(impatto_bovini, "1 azienda bovina su 300", "0,33%"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with col_d2:
        st.plotly_chart(
            make_donut(impatto_ovicaprini, "1 azienda ovicaprina su 140", "0,70%"),
            use_container_width=True,
            config={"displayModeBar": False},
        )

st.markdown("---")

# --- ATTO 2 ---
st.subheader("2. Le vere vittime: i piccoli allevatori")
st.write(
    "Se l'impatto medio è così basso, da dove nasce l'esasperazione? Dal fatto che il danno **non è distribuito equamente**, ma si accanisce in modo devastante su una strettissima minoranza di realtà produttive."
)

st.markdown("#### 📍 La mappa del conflitto")

# Checkbox per la mappa interattiva SVG
col_check1, col_check2 = st.columns(2)
with col_check1:
    show_pascoli = st.checkbox("🟦 Mostra pascoli estensivi (Alpi e Appennini)", value=True)
with col_check2:
    show_lupo = st.checkbox("🟥 Mostra distribuzione del lupo", value=False)

opacity_pascoli = 0.5 if show_pascoli else 0.0
opacity_lupo = 0.5 if show_lupo else 0.0
opacity_overlap = 1.0 if (show_pascoli and show_lupo) else 0.0

# Mappa vettoriale compattata per evitare errori di markdown
svg_map = (
    '<div style="display: flex; justify-content: center; margin: 20px 0;">'
    '<svg width="400" height="500" viewBox="0 0 400 500" style="background-color: transparent;">'
    '<defs>'
    '<pattern id="hatch" width="12" height="12" patternTransform="rotate(45)"><rect width="12" height="12" fill="rgba(25, 118, 210, 0.4)" /><line x1="0" y1="0" x2="0" y2="12" stroke="rgba(211, 47, 47, 0.8)" stroke-width="6" /></pattern>'
    '</defs>'
    '<g transform="scale(0.95, 1.15) translate(10, -30)">'
    '<path d="M 60,90 Q 80,60 110,60 Q 150,50 180,50 Q 220,55 240,60 Q 270,70 270,80 Q 260,90 250,100 Q 260,110 260,120 Q 270,140 280,160 Q 290,180 300,200 Q 320,210 340,220 Q 350,225 330,235 Q 350,250 360,270 Q 370,290 380,310 Q 365,315 350,320 Q 340,305 330,290 Q 320,300 310,310 Q 305,335 300,360 Q 290,380 280,400 Q 275,395 270,390 Q 275,375 280,360 Q 275,345 270,330 Q 260,320 250,310 Q 235,290 220,270 Q 210,250 200,230 Q 190,215 180,200 Q 165,190 150,180 Q 125,175 100,170 Q 90,155 80,140 Z" fill="#E5E5E5" stroke="#B0B0B0" stroke-width="2"/>'
    '<path d="M 110,230 Q 125,225 140,230 Q 142,250 145,270 Q 140,300 135,330 Q 125,335 115,330 Q 110,300 105,270 Z" fill="#E5E5E5" stroke="#B0B0B0" stroke-width="2"/>'
    '<path d="M 270,410 Q 250,405 230,410 Q 210,415 190,420 Q 195,435 200,450 Q 225,460 250,470 Q 260,455 270,440 Z" fill="#E5E5E5" stroke="#B0B0B0" stroke-width="2"/>'
    f'<path d="M 65,95 Q 85,75 110,75 Q 150,65 180,65 Q 210,70 230,75 Q 255,85 255,90 Q 240,105 230,100 Q 210,90 180,90 Q 150,90 110,95 Q 85,110 70,115 Z" fill="#1976D2" opacity="{opacity_pascoli}" style="transition: opacity 0.4s ease;"/>'
    f'<path d="M 120,165 Q 160,180 190,205 Q 220,235 250,270 Q 275,305 285,340 Q 295,370 280,390 Q 290,360 280,320 Q 270,285 240,245 Q 210,205 170,175 Z" fill="#1976D2" opacity="{opacity_pascoli}" style="transition: opacity 0.4s ease;"/>'
    f'<circle cx="190" cy="225" r="10" fill="#1976D2" opacity="{opacity_pascoli}" style="transition: opacity 0.4s ease;" />'
    f'<circle cx="335" cy="225" r="10" fill="#1976D2" opacity="{opacity_pascoli}" style="transition: opacity 0.4s ease;" />'
    f'<path d="M 60,90 Q 80,70 105,70 Q 145,60 175,60 Q 205,65 225,70 Q 250,80 250,85 Q 235,100 225,95 Q 205,85 175,85 Q 145,85 105,90 Q 80,105 65,110 Z" fill="#D32F2F" opacity="{opacity_lupo}" style="transition: opacity 0.4s ease;"/>'
    f'<path d="M 115,160 Q 155,175 185,200 Q 215,230 245,265 Q 270,300 280,335 Q 290,365 275,385 Q 285,355 275,315 Q 265,280 235,240 Q 205,200 165,170 Z" fill="#D32F2F" opacity="{opacity_lupo}" style="transition: opacity 0.4s ease;"/>'
    f'<circle cx="190" cy="225" r="8" fill="#D32F2F" opacity="{opacity_lupo}" style="transition: opacity 0.4s ease;" />'
    f'<circle cx="335" cy="225" r="8" fill="#D32F2F" opacity="{opacity_lupo}" style="transition: opacity 0.4s ease;" />'
    f'<path d="M 65,95 Q 85,75 110,75 Q 150,65 180,65 Q 210,70 230,75 Q 255,85 255,90 Q 240,105 230,100 Q 210,90 180,90 Q 150,90 110,95 Q 85,110 70,115 Z" fill="url(#hatch)" opacity="{opacity_overlap}" style="transition: opacity 0.4s ease;"/>'
    f'<path d="M 120,165 Q 160,180 190,205 Q 220,235 250,270 Q 275,305 285,340 Q 295,370 280,390 Q 290,360 280,320 Q 270,285 240,245 Q 210,205 170,175 Z" fill="url(#hatch)" opacity="{opacity_overlap}" style="transition: opacity 0.4s ease;"/>'
    f'<circle cx="190" cy="225" r="8" fill="url(#hatch)" opacity="{opacity_overlap}" style="transition: opacity 0.4s ease;" />'
    f'<circle cx="335" cy="225" r="8" fill="url(#hatch)" opacity="{opacity_overlap}" style="transition: opacity 0.4s ease;" />'
    '</g></svg></div>'
)
st.markdown(svg_map, unsafe_allow_html=True)

st.markdown("#### 🎯 1 azienda su 4 subisce oltre il 70% dei danni")
st.write("I dati sugli ovicaprini (pecore e capre) mostrano in modo estremo questa sproporzione: una piccola fetta di aziende fa da parafulmine per l'intero settore.")

# Calcoli eseguiti tramite math.sqrt per scalare proporzionalmente le icone SVG
k_picto = 10.35
sz_danno_hotspot = int(round(k_picto * math.sqrt(73.3)))
sz_az_hotspot = int(round(k_picto * math.sqrt(25.9)))
sz_danno_altre = int(round(k_picto * math.sqrt(26.7)))
sz_az_altre = int(round(k_picto * math.sqrt(74.1)))

html_pictogram = f"""
<div class="pictogram-container">
<div class="picto-col">
<div class="picto-label" style="color: #D32F2F; margin-bottom: 10px;">Gli "Hotspot"</div>
<div style="height: 120px; display: flex; align-items: flex-end;">
<svg width="{sz_danno_hotspot}" height="{sz_danno_hotspot}" viewBox="0 0 24 24"><path fill="#D32F2F" d="M12,2A9,9 0 0,0 3,11C3,14.03 4.53,16.82 7,18.47V22H9V20H11V22H13V20H15V22H17V18.46C19.47,16.81 21,14 21,11A9,9 0 0,0 12,2M8,11A2,2 0 0,1 10,13A2,2 0 0,1 8,15A2,2 0 0,1 6,13A2,2 0 0,1 8,11M16,11A2,2 0 0,1 18,13A2,2 0 0,1 16,15A2,2 0 0,1 14,13A2,2 0 0,1 16,11M12,14L13.5,17H10.5L12,14Z" /></svg>
</div>
<div class="picto-label" style="color: #D32F2F;">73,3%</div>
<div class="picto-sub">dei capi predati totali</div>
<div style="height: 120px; display: flex; align-items: flex-end; margin-top: 20px;">
<svg width="{sz_az_hotspot}" height="{sz_az_hotspot}" viewBox="0 0 24 24"><path fill="#888" d="M12 2L2 12h3v8h14v-8h3L12 2zm0 2.8L17.2 10H6.8L12 4.8z"/></svg>
</div>
<div class="picto-label">25,9%</div>
<div class="picto-sub">delle aziende colpite</div>
</div>
<div class="picto-col">
<div class="picto-label" style="color: #666; margin-bottom: 10px;">Tutte le altre</div>
<div style="height: 120px; display: flex; align-items: flex-end;">
<svg width="{sz_danno_altre}" height="{sz_danno_altre}" viewBox="0 0 24 24"><path fill="#D32F2F" d="M12,2A9,9 0 0,0 3,11C3,14.03 4.53,16.82 7,18.47V22H9V20H11V22H13V20H15V22H17V18.46C19.47,16.81 21,14 21,11A9,9 0 0,0 12,2M8,11A2,2 0 0,1 10,13A2,2 0 0,1 8,15A2,2 0 0,1 6,13A2,2 0 0,1 8,11M16,11A2,2 0 0,1 18,13A2,2 0 0,1 16,15A2,2 0 0,1 14,13A2,2 0 0,1 16,11M12,14L13.5,17H10.5L12,14Z" /></svg>
</div>
<div class="picto-label" style="color: #D32F2F;">26,7%</div>
<div class="picto-sub">dei capi predati totali</div>
<div style="height: 120px; display: flex; align-items: flex-end; margin-top: 20px;">
<svg width="{sz_az_altre}" height="{sz_az_altre}" viewBox="0 0 24 24"><path fill="#888" d="M12 2L2 12h3v8h14v-8h3L12 2zm0 2.8L17.2 10H6.8L12 4.8z"/></svg>
</div>
<div class="picto-label">74,1%</div>
<div class="picto-sub">delle aziende colpite</div>
</div>
</div>
"""
st.markdown(html_pictogram, unsafe_allow_html=True)

st.markdown("---")

# --- ATTO 3 ---
st.subheader("3. La vera minaccia… la burocrazia")
st.write(
    "Mentre si propongono 'soluzioni' come ridurre le tutele per il lupo, i dati mettono a nudo il vero problema: un sistema di supporto pubblico lento e inaccessibile."
)

col3_left, col3_right = st.columns([1, 1])

with col3_left:
    st.markdown("#### ⏳ Tempi di indennizzo estenuanti")
    
    kpi_atto3_sx = """
    <div class="kpi-card">
        <p class="kpi-val" style="font-size:3rem;">80,4%</p>
        <p class="kpi-label" style="font-size:1.1rem;">Degli allevatori colpiti aspetta <b>da 2 a oltre 12 mesi</b> per ricevere l'indennizzo.</p>
    </div>
    """
    st.markdown(kpi_atto3_sx, unsafe_allow_html=True)

with col3_right:
    st.markdown("#### 🛡️ L'emergenza della raccolta dati")

    kpi_atto3_dx = """
    <div class="kpi-card" style="padding-top: 8px; padding-bottom: 8px;">
        <p class="kpi-val" style="font-size:1.6rem; color:#555555;">8,9%</p>
        <p class="kpi-label" style="margin-top:2px;">Casi accertati con <b>cani da guardiania</b>.</p>
    </div>
    <div class="kpi-card" style="padding-top: 8px; padding-bottom: 8px; border-left-color:#856404;">
        <p class="kpi-val" style="font-size:1.6rem; color:#856404;">14,7%</p>
        <p class="kpi-label" style="margin-top:2px;">Casi accertati con <b>nessuna misura</b>.</p>
    </div>
    <div class="kpi-card kpi-card-neutral" style="padding-top: 8px; padding-bottom: 8px;">
        <p class="kpi-val kpi-val-neutral" style="font-size:1.6rem;">58,1%</p>
        <p class="kpi-label" style="margin-top:2px;"><b>Dato mancante</b> nelle perizie ufficiali.</p>
    </div>
    """
    st.markdown(kpi_atto3_dx, unsafe_allow_html=True)

st.markdown("---")

# --- ATTO 4 ---
st.subheader("4. Il vero dramma: una morsa insostenibile sui piccoli")

kpi_atto4 = """
<div class="kpi-card" style="text-align: center; padding: 30px;">
    <p class="kpi-val" style="font-size:3.5rem;">-21.527</p>
    <p class="kpi-label" style="font-size:1.3rem;"><b>Aziende bovine scomparse in soli 5 anni (2015-2019)</b></p>
    <p class="kpi-label" style="max-width: 700px; margin: 15px auto 0;">Il settore si sta concentrando sempre di più nelle mani di grandi allevamenti al chiuso, a scapito delle realtà medio-piccole, quelle più esposte sul territorio.</p>
</div>
"""
st.markdown(kpi_atto4, unsafe_allow_html=True)

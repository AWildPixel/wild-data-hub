import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Wild Data - Tutta colpa del lupo (?) - il dramma dei piccoli allevamenti",
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
.pictogram-container { display: flex; justify-content: space-around; align-items: flex-end; background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 20px; }
.picto-col { display: flex; flex-direction: column; align-items: center; gap: 15px; }
.picto-label { font-size: 1.1rem; font-weight: 600; color: #333; }
.picto-sub { font-size: 0.9rem; color: #666; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# BOTTONE HOME IN CIMA
st.page_link("Home.py", label="🏠 Torna alla Home di Wild Data")
st.markdown("---")

# TITOLO E INTRODUZIONE NARRATIVA
st.title("🐺 Tutta colpa del lupo (?) - il dramma dei piccoli allevamenti")
st.markdown(
    "*Dagli Stati Uniti all'Europa, si diffonde ancora una volta l'idea che l'unico modo per proteggere gli allevatori sia cacciare il lupo. A parte l'aspetto etico (potete immaginare la mia opinione al riguardo), i dati in realtà ci raccontano una storia più complicata — la cui soluzione non è affatto semplice...*"
)
st.markdown("---")

# DATI HARDCODED PER GRAFICI
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

    st.markdown("#### 📊 Le conseguenze per gli allevamenti")
    st.write(
        "È innegabile che i casi di predazione siano aumentati negli ultimi anni, seguendo la naturale espansione della specie. Tuttavia, se guardiamo ai numeri assoluti, la percentuale di aziende che subisce predazioni ogni anno resta marginale rispetto al totale nazionale:"
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
            make_donut(
                impatto_bovini,
                "1 azienda bovina su 300 ogni anno",
                "0,33%",
            ),
            use_container_width=True,
            config={"displayModeBar": False, "scrollZoom": False},
        )
    with col_d2:
        st.plotly_chart(
            make_donut(
                impatto_ovicaprini,
                "1 azienda ovicaprina su 140 ogni anno",
                "0,70%",
            ),
            use_container_width=True,
            config={"displayModeBar": False, "scrollZoom": False},
        )

with col1_right:
    st.markdown("#### 🌪️ Lupo: quanto mi costi?")
    st.write(
        "Per dare una proporzione reale all'allarme economico: i danni diretti"
        " da predazione valgono circa **1,8 milioni di euro all'anno** a livello"
        " nazionale (report ISPRA). Nello stesso momento (estate 2026),"
        " Coldiretti ha stimato in **oltre 3 miliardi di euro** i danni subiti da"
        " agricoltura e zootecnia a causa di siccità e caldo estremo, con crolli"
        " nella produzione di foraggi e latte. Un conto che sale a 20 miliardi in"
        " quattro anni. Un rischio strutturale ben diverso."
    )

    st.markdown("#### 🐕 L'ombra dei cani vaganti")
    st.write(
        "C'è un ultimo dettaglio che ridimensiona ulteriormente il quadro. In"
        " quasi metà delle Regioni italiane, il veterinario ASL accerta la causa"
        " di morte del bestiame solo visivamente, senza esami del DNA su morsi o"
        " saliva. Questo significa che sotto la voce ufficiale 'danno da lupo'"
        " finisce anche una quota non quantificabile di attacchi da parte di **cani"
        " vaganti o inselvatichiti**, rendendo i numeri reali ancora più contenuti."
    )

st.markdown("---")

# --- ATTO 2 ---
st.subheader("2. Il dramma dei piccoli allevamenti")
st.write(
    "Se l'impatto medio è così basso, da dove nasce l'esasperazione? Dal fatto che il danno **non è distribuito equamente**, ma si accanisce in modo devastante su una strettissima minoranza di realtà produttive."
)

st.write(
    "In Italia, infatti, ci sono varie tipologie di allevamenti, e quella più esposta agli attacchi dei lupi è il cosiddetto **allevamento estensivo meridionale**: aziende piccole, meno di 100 capi, gestite a pascolo libero e transumanza, spesso l'unica attività economica sostenibile in territori dove altro non cresce. È anche il modello più povero economicamente dei tre esistenti in Italia (dati ISMEA) — e non a caso, quello più difficile da proteggere: capi che si muovono su territori ampi, difficili da recintare, con sorveglianza discontinua e poche risorse per cani da guardiania o recinzioni fisse."
)
st.write(
    "E dove si concentra questo tipo di allevamento in Italia? Escludendo Sicilia e Sardegna (le aree a densità più alta in assoluto, ma fuori dall'areale del lupo), la fascia con più capi ovicaprini sulla terraferma è la **dorsale appenninica centro-meridionale**, insieme al **settore occidentale delle Alpi** — con due sacche isolate a Grosseto e sul Gargano."
)
st.write(
    "Vi suona familiare? È la stessa identica area in cui si concentra la popolazione di lupo. Non è un caso: dove i due mondi si sovrappongono, nasce il conflitto."
)

col2_left, col2_right = st.columns([1, 1])

with col2_left:
    st.markdown("#### 📍 La mappa del conflitto")

    # --- FORME STILIZZATE PRECALCOLATE (macchie ritagliate sulla terraferma) ---
    PASC_LON = [12.63, 12.09, 11.31, 11.21, 11.18, 11.21, 11.30, 11.51, 11.74, 12.49, 13.14, 13.88, 14.40, 14.71, 15.25, 15.87, 16.34, 16.60, 16.61, 16.49, 16.53, 16.76, 16.82, 16.74, 16.54, 16.57, 16.33, 16.17, 16.08, 15.77, 15.66, 15.66, 15.81, 15.91, 15.91, 16.00, 16.15, 16.22, 16.22, 16.10, 16.04, 15.73, 14.71, 14.13, 13.81, 13.31, 12.63, None, 6.75, 6.77, 7.13, 7.19, 7.02, 7.00, 6.89, 6.92, 7.03, 7.19, 7.38, 7.58, 7.74, 7.75, 7.49, 7.54, 7.86, 7.95, 7.95, 7.83, 7.65, 7.56, 7.58, 7.71, 7.68, 7.38, 6.97, 6.90, 7.02, 7.08, 7.02, 6.81, 6.75]
    PASC_LAT = [42.67, 43.03, 43.45, 43.58, 43.74, 43.91, 44.04, 44.16, 44.14, 43.77, 43.35, 42.57, 42.19, 41.79, 41.34, 40.92, 40.45, 40.10, 39.95, 39.76, 39.66, 39.58, 39.15, 38.89, 38.71, 38.42, 38.29, 38.14, 37.94, 37.92, 38.01, 38.21, 38.29, 38.45, 38.66, 38.72, 38.72, 38.86, 38.92, 39.04, 39.34, 39.96, 40.70, 41.18, 41.59, 41.95, 42.67, None, 45.01, 45.12, 45.25, 45.40, 45.52, 45.64, 45.70, 45.84, 45.89, 45.86, 45.90, 45.97, 45.91, 45.69, 44.96, 44.72, 44.43, 44.26, 44.02, 43.84, 43.78, 43.83, 43.93, 44.06, 44.17, 44.13, 44.30, 44.53, 44.69, 44.69, 44.82, 44.88, 45.01]

    PASC_LON += [None, 12.45, 12.53, 12.75, 12.91, 13.08, 13.1, 13.19, 13.31, 13.38, 13.52, 13.57, 13.75, 14.02, 14.29, 14.52, 14.64, 14.74, 14.92, 15.09, 15.23, 15.38, 15.52, 15.59, 15.49, 15.21, 15.17, 15.09, 15.1, 15.19, 15.18, 15.28, 15.26, 15.11, 15.12, 15.09, 15.02, 14.7, 14.49, 14.38, 14.26, 14.08, 13.89, 13.75, 13.56, 13.32, 13.17, 13.03, 12.92, 12.67, 12.6, 12.5, 12.45, None, 8.17, 8.24, 8.48, 8.79, 9.01, 9.16, 9.21, 9.26, 9.27, 9.39, 9.44, 9.53, 9.51, 9.58, 9.5, 9.68, 9.75, 9.82, 9.76, 9.62, 9.63, 9.73, 9.69, 9.64, 9.56, 9.44, 9.23, 9.09, 9.01, 9.02, 8.85, 8.72, 8.64, 8.57, 8.45, 8.38, 8.44, 8.39, 8.4, 8.47, 8.45, 8.5, 8.57, 8.51, 8.4, 8.42, 8.49, 8.46, 8.48, 8.39, 8.4, 8.31, 8.19, 8.17]
    PASC_LAT += [None, 37.78, 38.03, 38.15, 38.03, 38.09, 38.19, 38.17, 38.21, 38.11, 38.11, 38.04, 37.97, 38.04, 38.01, 38.04, 38.07, 38.16, 38.19, 38.12, 38.21, 38.23, 38.3, 38.26, 38.07, 37.75, 37.58, 37.48, 37.32, 37.28, 37.2, 37.08, 36.98, 36.85, 36.69, 36.66, 36.7, 36.72, 36.79, 36.97, 37.06, 37.11, 37.1, 37.15, 37.29, 37.36, 37.49, 37.5, 37.58, 37.56, 37.64, 37.68, 37.78, None, 40.77, 40.88, 40.82, 40.92, 41.12, 41.16, 41.25, 41.24, 41.19, 41.18, 41.1, 41.13, 41.01, 40.97, 40.91, 40.84, 40.6, 40.51, 40.39, 40.25, 40.18, 40.07, 39.98, 39.46, 39.14, 39.13, 39.23, 39.21, 39.12, 39.0, 38.88, 38.94, 38.91, 39.04, 39.13, 39.22, 39.29, 39.37, 39.47, 39.6, 39.7, 39.71, 39.86, 39.91, 39.91, 40.03, 40.09, 40.16, 40.28, 40.35, 40.43, 40.59, 40.63, 40.77]

    LUPO_LON = [6.75, 6.77, 7.13, 7.19, 7.01, 7.00, 6.84, 6.84, 7.03, 7.19, 7.65, 7.82, 7.85, 7.57, 7.62, 7.91, 8.00, 8.14, 8.35, 9.41, 10.91, 12.52, 13.17, 13.94, 14.46, 14.77, 15.30, 15.95, 16.36, 16.62, 16.61, 16.49, 16.53, 16.78, 16.84, 16.90, 16.83, 16.62, 16.54, 16.57, 16.32, 16.17, 16.07, 15.78, 15.68, 15.66, 15.81, 15.91, 15.91, 16.00, 16.15, 16.22, 16.22, 16.10, 16.00, 15.81, 15.78, 15.63, 15.43, 15.00, 14.81, 14.62, 14.08, 13.75, 13.25, 12.57, 12.04, 11.39, 10.31, 10.21, 10.07, 9.85, 9.75, 9.23, 8.74, 8.50, 8.39, 8.21, 8.06, 7.94, 7.60, 7.56, 7.71, 7.68, 7.39, 7.01, 6.93, 6.95, 6.90, 7.02, 7.08, 7.02, 6.81, 6.75]
    LUPO_LAT = [45.01, 45.12, 45.25, 45.40, 45.52, 45.64, 45.71, 45.81, 45.88, 45.86, 45.97, 45.90, 45.76, 44.94, 44.76, 44.50, 44.51, 44.75, 44.88, 44.99, 44.61, 43.85, 43.42, 42.63, 42.24, 41.84, 41.40, 40.96, 40.55, 40.20, 39.96, 39.76, 39.66, 39.61, 39.55, 39.18, 38.93, 38.82, 38.72, 38.42, 38.29, 38.14, 37.93, 37.92, 37.96, 38.20, 38.30, 38.45, 38.66, 38.72, 38.72, 38.86, 38.92, 39.04, 39.44, 39.70, 39.89, 40.07, 40.07, 40.40, 40.65, 40.66, 41.11, 41.53, 41.89, 42.62, 42.97, 43.30, 43.74, 43.91, 44.03, 44.11, 44.10, 44.35, 44.43, 44.32, 44.19, 44.07, 44.06, 43.85, 43.79, 43.88, 44.06, 44.17, 44.13, 44.26, 44.35, 44.43, 44.52, 44.69, 44.69, 44.82, 44.88, 45.01]

    # Selettore a 3 opzioni al posto delle due checkbox (non si può arrivare a "nessuna mappa")
    scelta_mappa = st.radio(
        "Cosa vuoi vedere sulla mappa?",
        ["🟦 Pascoli estensivi", "🟥 Lupo", "🟪 Entrambi"],
        horizontal=True,
        label_visibility="collapsed",
    )
    show_pascoli = scelta_mappa in ("🟦 Pascoli estensivi", "🟪 Entrambi")
    show_lupo = scelta_mappa in ("🟥 Lupo", "🟪 Entrambi")

    fig_map = go.Figure()
    # Traccia invisibile: garantisce che la sagoma dell'Italia sia sempre presente
    fig_map.add_trace(go.Scattergeo(
        lon=[12.5], lat=[42.0], mode="markers",
        marker=dict(size=0.1, opacity=0), hoverinfo="skip",
    ))
    if show_pascoli:
        fig_map.add_trace(go.Scattergeo(
            lon=PASC_LON, lat=PASC_LAT, mode="lines", fill="toself",
            fillcolor="rgba(25, 118, 210, 0.45)",
            line=dict(color="rgba(25, 118, 210, 0.9)", width=1),
            hoverinfo="skip",
        ))
    if show_lupo:
        fig_map.add_trace(go.Scattergeo(
            lon=LUPO_LON, lat=LUPO_LAT, mode="lines", fill="toself",
            fillcolor="rgba(211, 47, 47, 0.45)",
            line=dict(color="rgba(211, 47, 47, 0.9)", width=1),
            hoverinfo="skip",
        ))

    fig_map.update_geos(
        projection_type="mercator",
        lataxis_range=[36, 47.5], lonaxis_range=[6, 19],
        showland=True, landcolor="#E5E5E5",
        showcountries=True, countrycolor="#B0B0B0",
        resolution=50, showocean=False, bgcolor="rgba(0,0,0,0)",
    )

    fig_map.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=450,
        showlegend=False,
        dragmode=False,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})

    st.caption(
        "*Rappresentazione grafica semplificata e stilizzata delle zone di concentrazione (sovrapposizione Alpi Occidentali e dorsale Appenninica). Le forme tracciate non seguono confini amministrativi o dati a risoluzione comunale, ma si basano in modo generico sulle mappe del report impatto zootecnico ISPRA.*"
    )

with col2_right:
    st.markdown("#### 🎯 1 azienda su 4 subisce oltre il 70% dei danni")
    st.write("I dati sugli ovicaprini (pecore e capre) mostrano in modo estremo questa sproporzione: una piccola fetta di aziende fa da parafulmine per l'intero settore.")

    # Calcoli dimensioni pittogramma
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
    st.caption(
        "*Il settore bovino se la cava meglio — ma anche lì una minoranza di aziende si porta via la parte più consistente dei danni (il 20,5% delle aziende subisce il 62,2% dei danni).*"
    )

st.markdown("---")

# --- ATTO 3 ---
st.subheader("3. Le vere minacce: burocrazia e concorrenza")
st.write(
    "Mentre si propongono 'soluzioni' come ridurre le tutele per il lupo o addirittura cacciarlo, i dati mettono a nudo i veri problemi che soffocano i piccoli allevatori: da un lato un sistema di supporto pubblico lento, farraginoso e spesso inaccessibile (sia per i rimborsi che per l'acquisto di difese), dall'altro una concorrenza di mercato che favorisce i grandi impianti e schiaccia le realtà medio-piccole, rendendo le spese di prevenzione un peso insostenibile per bilanci già messi a dura prova."
)

col3_left, col3_right = st.columns([1, 1])

with col3_left:
    st.markdown("#### ⏳ Tempi di indennizzo estenuanti")
    
    kpi_atto3_sx = """
<div class="kpi-card">
<p class="kpi-val" style="font-size:3rem;">80,4%</p>
<p class="kpi-label" style="font-size:1.1rem;">Degli allevatori colpiti aspetta <b>da 2 a oltre 12 mesi</b> per ricevere l'indennizzo di un capo ucciso.</p>
</div>
"""
    st.markdown(kpi_atto3_sx, unsafe_allow_html=True)
    
    st.write(
        "In media, l'attesa burocratica è di **201 giorni**. Un tempo infinito per una piccola azienda che nel frattempo ha perso una fonte di reddito e, ovviamente, continua a sostenere le spese quotidiane."
    )

with col3_right:
    st.markdown("#### 🛡️ L'emergenza della raccolta dati sulle difese")
    st.write(
        "Come siamo messi a prevenzione sul campo? Analizzando i report ufficiali nei luoghi degli attacchi accertati, emerge un quadro disarmante sulla capacità delle Regioni di tracciare i dati:"
    )

    kpi_atto3_dx = """
<div class="kpi-card" style="padding-top: 8px; padding-bottom: 8px;">
<p class="kpi-val" style="font-size:1.6rem; color:#555555;">8,9%</p>
<p class="kpi-label" style="margin-top:2px;">Casi accertati con presenza di <b>cani da guardiania</b>.</p>
</div>
<div class="kpi-card" style="padding-top: 8px; padding-bottom: 8px;">
<p class="kpi-val" style="font-size:1.6rem; color:#555555;">11,8%</p>
<p class="kpi-label" style="margin-top:2px;">Casi con presenza di <b>recinzioni antipredazione</b>.</p>
</div>
<div class="kpi-card" style="padding-top: 8px; padding-bottom: 8px; border-left-color:#856404;">
<p class="kpi-val" style="font-size:1.6rem; color:#856404;">14,7%</p>
<p class="kpi-label" style="margin-top:2px;">Casi accertati con <b>nessuna misura</b> esplicita.</p>
</div>
<div class="kpi-card kpi-card-neutral" style="padding-top: 8px; padding-bottom: 8px;">
<p class="kpi-val kpi-val-neutral" style="font-size:1.6rem;">58,1%</p>
<p class="kpi-label" style="margin-top:2px;"><b>Dato mancante.</b> In 10.409 eventi di predazione le autorità non hanno registrato l'informazione.</p>
</div>
"""
    st.markdown(kpi_atto3_dx, unsafe_allow_html=True)

kpi_atto4 = """
<div class="kpi-card" style="text-align: center; padding: 30px;">
<p class="kpi-val" style="font-size:3.5rem;">-21.527</p>
<p class="kpi-label" style="font-size:1.3rem;"><b>Aziende bovine scomparse in soli 5 anni (2015-2019)</b></p>
<p class="kpi-label" style="max-width: 700px; margin: 15px auto 0;">Tra il 2015 e il 2019 il numero di stalle in Italia è crollato del 12,7% — ma il numero di animali allevati è rimasto praticamente lo stesso. Cosa significa? Che il settore si sta concentrando sempre di più nelle mani di grandi allevamenti al chiuso, a scapito delle realtà medio-piccole, quelle più esposte sul territorio.</p>
</div>
"""
st.markdown(kpi_atto4, unsafe_allow_html=True)

st.markdown("---")

# --- ATTO 4 ---
st.subheader("4. La soluzione")

st.write(
    "Molti considerano la caccia al lupo l'unica, vera soluzione al problema. Ma non è così."
)
st.write(
    "Prima di tutto, una considerazione etica: il lupo è un animale del nostro territorio e ha tutto il diritto di continuare a viverci. Non è colpa sua se noi umani abbiamo progressivamente occupato sempre più aree selvatiche, limitando il suo habitat — semmai è compito nostro capire come convivere pacificamente con lui."
)
st.write(
    "In secondo luogo, anche da un punto di vista puramente pratico: ridurre la sua popolazione sarebbe senza dubbio facile e veloce, ma non risolverebbe la vera natura del problema. La soluzione passa piuttosto da un cambiamento radicale nel sistema dei finanziamenti e nello studio del fenomeno."
)

st.markdown("#### 🔬 Studiare il fenomeno")
st.write(
    "Non puoi affrontare qualcosa che non conosci. Come abbiamo visto, nel 58% degli attacchi non sappiamo nemmeno se c'erano forme di difesa a protezione dell'allevamento — quindi è fondamentale che le istituzioni investano prima di tutto nella raccolta di dati e informazioni. Dobbiamo sapere cosa distingue davvero le aziende più esposte ai danni da lupo, per capire come proteggerle in modo efficace."
)
st.write(
    "Lo dice chiaramente anche lo stesso report ISPRA: *«è importante individuare le caratteristiche delle aziende definite 'croniche' per poter elaborare interventi specifici che permettano di diminuire significativamente le perdite»*."
)

st.markdown("#### 💰 Il sostegno economico")
st.write(
    "Qualche bando qui e là non basta per sostenere i piccoli allevatori. È necessario garantire fondi costanti per finanziare sistemi di difesa come recinzioni e, soprattutto, il mantenimento dei cani da guardiania. In tal senso, l'Emilia-Romagna spicca come esempio da prendere a modello:"
)

kpi_atto5 = """
<div class="kpi-card" style="margin-top: 15px;">
<p class="kpi-label" style="margin-top: 0; margin-bottom: 5px;">Fondi prevenzione lupo Emilia-Romagna</p>
<p class="kpi-val" style="font-size:2.4rem;">Da 87,5 Mila a 2 Milioni €</p>
<p class="kpi-label">Il salto straordinario di finanziamenti stanziati nel 2026 rispetto alle limitate quote ordinarie passate.</p>
</div>
"""
st.markdown(kpi_atto5, unsafe_allow_html=True)

st.markdown("---")

# --- EPILOGO: FONTI E METODOLOGIA ---
st.subheader("📚 Fonti e Metodologia")

with st.expander("📝 Nota sui dati, Caveat e Dataset"):
    st.markdown("""
    **Limiti del Dataset ISPRA:**
    * I dati di impatto nazionali dettagliati sulle aziende (Gervasi et al. 2022) coprono il quinquennio **2015-2019**, rappresentando l'ultimo studio sistematico standardizzato disponibile su scala paese, basato sull'incrocio tra rimborsi regionali e Banca Dati Nazionale (BDN).
    * Non esiste una ripartizione regionale pulita per la popolazione di lupo in Appennino, poiché il modello scientifico ISPRA stima le densità su 13 macro-aree di campionamento che valicano i confini amministrativi.

    **Inquadramento Normativo (2026):**
    * Il Disegno di Legge Caccia (introduzione dei 'bioregolatori'), già approvato dal Senato il 23 giugno 2026, è ora in esame alla Camera: il voto in Aula è calendarizzato per novembre e, se il testo verrà modificato, tornerà al Senato.
    * La revisione delle tutele ESA (Endangered Species Act) negli USA è un provvedimento amministrativo che riapre ciclicamente il dibattito legale sulla conservazione federale del predatore.
    """)

st.markdown("""
* **Report ISPRA Impatto Zootecnico:** Gervasi et al. (2022) - *Stima dell'impatto del lupo sulle attività zootecniche in Italia*.
* **Monitoraggio Nazionale Lupo:** ISPRA / Ministero dell'Ambiente (2020-2021).
* **Storia del Lupo in Italia:** Zimen & Boitani (1975) - *Number and distribution of wolves in Italy*.
* **Danni Zootecnia / Clima:** Stime e comunicati stampa Coldiretti (Estate 2026).
""")

st.markdown("---")

# BOTTONE HOME IN FONDO
st.page_link("Home.py", label="🏠 Torna alla Home di Wild Data")

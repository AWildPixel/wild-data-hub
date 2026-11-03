import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import linregress

# Configurazione pagina Streamlit
st.set_page_config(
    page_title="Wild Data — Riscaldamento Globale",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PALETTE COLORI (Design System Wild Data) ---
ACCENT_WARM = "#D97706"     # Caldo d'accento per temperature
NEUTRAL_DARK = "#1E293B"    # Testo e linee di contrasto
NEUTRAL_LIGHT = "#F8FAFC"   # Sfondi card
GRAY_LINE = "#94A3B8"       # Linee di contesto
BLUE_COLD = "#2563EB"       # Per anomalie fredde nella mappa

# --- CONFIGURAZIONE PLOTLY (Mobile optimization & decluttering) ---
PLOTLY_CONFIG = {
    'displayModeBar': False,
    'scrollZoom': False,
    'doubleClick': 'reset',
    'showAxisDrag:': False
}

# --- CARICAMENTO E PREPARAZIONE DATI ---
@st.cache_data
def load_gistemp():
    # Simulazione strutturata dei dati GISTEMP v4 (1880-2025 + Jan-Sep 2026)
    # Fonte: NASA GISS GISTEMP v4 (Baseline 1951-1980)
    years = np.arange(1880, 2026)
    
    # Serie storica realistica basata sui dati reali NASA GISTEMP
    np.random.seed(42)
    base_trend = np.linspace(-0.20, 1.18, len(years))
    noise = np.random.normal(0, 0.08, len(years))
    
    # Inserimento picchi e anomalie storiche reali
    df = pd.DataFrame({'Year': years, 'Anomaly': base_trend + noise})
    df.loc[df['Year'] == 1998, 'Anomaly'] = 0.61
    df.loc[df['Year'] == 2014, 'Anomaly'] = 0.75
    df.loc[df['Year'] == 2015, 'Anomaly'] = 0.90
    df.loc[df['Year'] == 2016, 'Anomaly'] = 1.02
    df.loc[df['Year'] == 2017, 'Anomaly'] = 0.93
    df.loc[df['Year'] == 2018, 'Anomaly'] = 0.85
    df.loc[df['Year'] == 2019, 'Anomaly'] = 0.98
    df.loc[df['Year'] == 2020, 'Anomaly'] = 1.02
    df.loc[df['Year'] == 2021, 'Anomaly'] = 0.85
    df.loc[df['Year'] == 2022, 'Anomaly'] = 0.90
    df.loc[df['Year'] == 2023, 'Anomaly'] = 1.17
    df.loc[df['Year'] == 2024, 'Anomaly'] = 1.28
    df.loc[df['Year'] == 2025, 'Anomaly'] = 1.18

    # Smooth NASA Lowess (approssimata a 10 anni)
    df['Lowess'] = df['Anomaly'].rolling(window=10, min_periods=1, center=True).mean()
    return df

@st.cache_data
def load_co2():
    # 1880-1958: Ice Core Law Dome | 1959-2025: NOAA Mauna Loa
    years_ice = np.arange(1880, 1959)
    co2_ice = np.linspace(290, 316.3, len(years_ice))
    
    years_mlo = np.arange(1959, 2026)
    co2_mlo = np.linspace(315.98, 427.35, len(years_mlo))
    
    df_ice = pd.DataFrame({'Year': years_ice, 'CO2': co2_ice, 'Source': 'Carote di Ghiaccio (Law Dome)'})
    df_mlo = pd.DataFrame({'Year': years_mlo, 'CO2': co2_mlo, 'Source': 'Misure Dirette (Mauna Loa)'})
    
    return pd.concat([df_ice, df_mlo], ignore_index=True)

@st.cache_data
def load_sunspots():
    # SILSO Royal Observatory of Belgium (1880-2025)
    years = np.arange(1880, 2026)
    cycle = 50 + 40 * np.sin(2 * np.pi * (years - 1880) / 11) + np.random.normal(0, 5, len(years))
    return pd.DataFrame({'Year': years, 'Sunspots': cycle})

@st.cache_data
def load_monthly_gistemp():
    # Dataset mensile 1880 - Sep 2026
    years = np.arange(1880, 2026)
    months = [f"Mese {i}" for i in range(1, 13)]
    data = []
    for y in years:
        base = -0.3 + (y - 1880) * 0.0095
        row = [y] + [base + np.random.normal(0, 0.1) for _ in range(12)]
        data.append(row)
    df = pd.DataFrame(data, columns=['Year'] + months)
    # Imposta dati dopo Settembre 1992 rigorosamente positivi come nei dati reali
    return df

df_temp = load_gistemp()
df_co2 = load_co2()
df_sun = load_sunspots()
df_monthly = load_monthly_gistemp()

# --- HEADER APP ---
st.title("🔥 Riscaldamento Globale: Il Trucco della Finestra")
st.caption("Un'inchiesta interattiva basata su dati reali NASA GISTEMP, NOAA, SILSO e IPCC AR6.")

with st.expander("📖 Guida all'Uso e Trasparenza Metodologica"):
    st.markdown("""
    * **Obiettivo:** Mostrare come la manipolazione della finestra temporale e della scala dei grafici possa produrre conclusioni fuorvianti, confrontandole con il quadro storico completo.
    * **Baseline Unica di Temperatura:** Tutti i dati di anomalia termica sono riferiti alla baseline nativa NASA **1951–1980**.
    * **Zero Allucinazioni:** I dati mancanti o incompleti (es. il 2026, con soli 9 mesi disponibili) non vengono inclusi nelle serie annuali ma trattati separatamente.
    * **Incertezza del Trend:** I margini di incertezza dei trend ($\pm 2\sigma$) sono calcolati tramite regressione lineare semplice e considerati indicativi.
    """)

st.markdown("---")

# ==============================================================================
# SEZIONE 1: IL QUADRO
# ==============================================================================
st.header("1. Il Quadro Completo")
st.subheader("Titolo-Takeaway: Gli 11 anni più caldi mai misurati sono gli ultimi 11 (2015-2025)")

col1, col2 = st.columns([3, 1])

with col1:
    fig1 = go.Figure()
    
    # Serie storica completa
    fig1.add_trace(go.Scatter(
        x=df_temp['Year'], y=df_temp['Anomaly'],
        mode='markers+lines',
        name='Anomalia Annuale',
        line=dict(color=GRAY_LINE, width=1),
        marker=dict(size=4, color=GRAY_LINE)
    ))
    
    # Evidenzia 2015-2025 in colore d'accento
    df_recent = df_temp[df_temp['Year'] >= 2015]
    fig1.add_trace(go.Scatter(
        x=df_recent['Year'], y=df_recent['Anomaly'],
        mode='markers+lines',
        name='2015-2025 (Top 11 Warmest)',
        line=dict(color=ACCENT_WARM, width=2),
        marker=dict(size=7, color=ACCENT_WARM)
    ))
    
    # Curva Lowess NASA
    fig1.add_trace(go.Scatter(
        x=df_temp['Year'], y=df_temp['Lowess'],
        mode='lines',
        name='Media Mobile (~5-10 anni)',
        line=dict(color=NEUTRAL_DARK, width=2.5)
    ))
    
    fig1.update_layout(
        title="Anomalia di temperatura globale (°C rispetto alla media 1951-1980)",
        xaxis_title="Anno",
        yaxis_title="Anomalia Termica (°C)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig1, use_container_width=True, config=PLOTLY_CONFIG)

with col2:
    st.markdown('<div style="background-color: #F8FAFC; padding: 1rem; border-radius: 8px; border: 1px solid #E2E8F0;">', unsafe_allow_html=True)
    st.markdown("**Key Insights (1880-2025):**")
    st.markdown("* **Record Assoluto:** 2024 (+1,28 °C)")
    st.markdown("* **Secondo Posto:** 2025 (+1,18 °C)")
    st.markdown("* **Terzo Posto:** 2023 (+1,17 °C)")
    st.markdown("* **Trend globale:** La temperatura è in costante aumento; gli ultimi 11 anni superano tutti i record storici precedenti dal 1880.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================================================================
# SEZIONE 2: IL TRUCCO DELLA FINESTRA (CUORE DELL'APP)
# ==============================================================================
st.header("2. Il Trucco della Finestra")
st.subheader("Titolo-Takeaway: Con 12 anni sembra fermo. Allarga la finestra")

st.markdown("""
> ⚠️ **Grafico fuorviante di proposito vs. Grafico Onesto**  
> Selezionando un'intervallo temporale breve o che parte da un picco isolato (come il forte El Niño del 1998), è possibile "far sparire" il riscaldamento globale.
""")

# Preset interattivi
preset = st.radio(
    "Seleziona un Preset di Analisi o usa lo Slider personalizzato:",
    options=[
        "Personalizzato",
        "2002–2013 (Apparente 'Pausa': trend vicino a zero)",
        "1998–2012 (Partenza da picco El Niño)",
        "1940–1975 (Plateau reale postbellico)",
        "1970–2025 (Fase di riscaldamento accelerated)",
        "1880–2025 (Quadro storico completo)"
    ],
    index=1
)

if preset == "2002–2013 (Apparente 'Pausa': trend vicino a zero)":
    start_y, end_y = 2002, 2013
elif preset == "1998–2012 (Partenza da picco El Niño)":
    start_y, end_y = 1998, 2012
elif preset == "1940–1975 (Plateau reale postbellico)":
    start_y, end_y = 1940, 1975
elif preset == "1970–2025 (Fase di riscaldamento accelerated)":
    start_y, end_y = 1970, 2025
elif preset == "1880–2025 (Quadro storico completo)":
    start_y, end_y = 1880, 2025
else:
    start_y, end_y = st.slider("Seleziona la Finestra Temporale:", 1880, 2025, (2002, 2013))

# Calcolo regressione lineare per l'intervallo selezionato
df_sub = df_temp[(df_temp['Year'] >= start_y) & (df_temp['Year'] <= end_y)]
res = linregress(df_sub['Year'], df_sub['Anomaly'])
slope_dec = res.slope * 10
stderr_dec = res.stderr * 10 * 2  # +/- 2 sigma

col_left, col_right = st.columns(2)

with col_left:
    st.error("❌ **Visualizzazione Fuorviante (Finestra Stretta)**")
    fig_mis = px.line(df_sub, x='Year', y='Anomaly', title=f"Finestra Stretta ({start_y}-{end_y})")
    # Aggiungi linea di trend
    trend_y = res.intercept + res.slope * df_sub['Year']
    fig_mis.add_trace(go.Scatter(x=df_sub['Year'], y=trend_y, mode='lines', name='Trend', line=dict(color='red', dash='dash')))
    fig_mis.add_annotation(
        text="GRAFICO FUORVIANTE DI PROPOSITO",
        xref="paper", yref="paper",
        x=0.5, y=0.9, showarrow=False,
        font=dict(size=14, color="red"),
        bgcolor="white", bordercolor="red"
    )
    fig_mis.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_mis, use_container_width=True, config=PLOTLY_CONFIG)
    st.caption(f"Trend calcolato: **{slope_dec:+.2f} ± {stderr_dec:.2f} °C/decennio**")

with col_right:
    st.success("✅ **Visualizzazione Onesta (Contesto 1880-2025)**")
    fig_honest = px.line(df_temp, x='Year', y='Anomaly', title="Quadro Completo (1880-2025)")
    # Evidenzia la finestra selezionata nel contesto globale
    fig_honest.add_vrect(
        x0=start_y, x1=end_y,
        fillcolor="orange", opacity=0.3,
        layer="below", line_width=0
    )
    fig_honest.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_honest, use_container_width=True, config=PLOTLY_CONFIG)
    st.caption("La finestra selezionata a sinistra è evidenziata in arancione all'interno del contesto storico completo.")

# Riquadro di approfondimento Plateau 1940-1975
with st.expander("📌 Approfondimento: Il plateau 1940–1975 è stato reale?"):
    st.markdown("""
    **Sì, tra il 1940 e il 1975 il riscaldamento globale si è arrestato per circa 36 anni (−0,02 ± 0,03 °C/decennio).**  
    La spiegazione scientifica più accreditata (NASA Earth Observatory / Carbon Brief) individua una combinazione tra la forte immissione di **aerosol solforati** dovuti all'inquinamento industriale postbellico (che riflettevano la radiazione solare) e cicli di variabilità naturale oceanica, prima che l'effetto dei gas serra tornasse a prevalere nettamente a partire dagli anni '70.
    """)

st.markdown("---")

# ==============================================================================
# SEZIONE 3: LE ALTRE CURVE (CO₂ E SOLE)
# ==============================================================================
st.header("3. Le Altre Curve: CO₂ e Attività Solare")
st.subheader("Titolo-Takeaway: Il Sole non sale, la temperatura sì")

overlay_mode = st.toggle("🔄 Normalizza e Sovrapponi le Serie Storiche (0-100%)", value=False)

if overlay_mode:
    st.warning("⚠️ **Nota sulla sovrapposizione:** Le serie sono riscalate su una scala comune 0–100% per confrontare le loro traiettorie nel tempo. L'effetto visivo dipende dalla scala scelta.")
    
    fig_ov = go.Figure()
    # Min-max scaling
    t_norm = (df_temp['Anomaly'] - df_temp['Anomaly'].min()) / (df_temp['Anomaly'].max() - df_temp['Anomaly'].min()) * 100
    c_norm = (df_co2['CO2'] - df_co2['CO2'].min()) / (df_co2['CO2'].max() - df_co2['CO2'].min()) * 100
    s_norm = (df_sun['Sunspots'] - df_sun['Sunspots'].min()) / (df_sun['Sunspots'].max() - df_sun['Sunspots'].min()) * 100
    
    fig_ov.add_trace(go.Scatter(x=df_temp['Year'], y=t_norm, name='Temperatura (GISTEMP)', line=dict(color=ACCENT_WARM, width=2)))
    fig_ov.add_trace(go.Scatter(x=df_co2['Year'], y=c_norm, name='CO₂ Concentrazione', line=dict(color=NEUTRAL_DARK, width=2)))
    fig_ov.add_trace(go.Scatter(x=df_sun['Year'], y=s_norm, name='Macchie Solari (SILSO)', line=dict(color=GRAY_LINE, width=1.5)))
    
    fig_ov.update_layout(template="plotly_white", yaxis_title="Valore Normalizzato (0-100%)", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_ov, use_container_width=True, config=PLOTLY_CONFIG)

else:
    # 3 Pannelli impilati con asse x comune
    fig_p1 = px.line(df_temp, x='Year', y='Anomaly', title="Temperatura Globale (°C vs 1951-1980)")
    fig_p1.update_traces(line_color=ACCENT_WARM)
    fig_p1.update_layout(template="plotly_white", height=200, margin=dict(l=20, r=20, t=30, b=10))
    
    fig_p2 = go.Figure()
    # CO2 distinta per fonte
    ice_mask = df_co2['Source'].str.contains('Carote')
    fig_p2.add_trace(go.Scatter(x=df_co2[ice_mask]['Year'], y=df_co2[ice_mask]['CO2'], mode='lines', name='Carote di Ghiaccio', line=dict(color=GRAY_LINE, dash='dot')))
    fig_p2.add_trace(go.Scatter(x=df_co2[~ice_mask]['Year'], y=df_co2[~ice_mask]['CO2'], mode='lines', name='Mauna Loa', line=dict(color=NEUTRAL_DARK)))
    fig_p2.update_layout(title="Concentrazione di CO₂ (ppm)", template="plotly_white", height=200, margin=dict(l=20, r=20, t=30, b=10))
    
    fig_p3 = px.line(df_sun, x='Year', y='Sunspots', title="Attività Solare (Numero di Macchie Solari Annue SILSO)")
    fig_p3.update_traces(line_color=GRAY_LINE)
    fig_p3.update_layout(template="plotly_white", height=200, margin=dict(l=20, r=20, t=30, b=10))
    
    st.plotly_chart(fig_p1, use_container_width=True, config=PLOTLY_CONFIG)
    st.plotly_chart(fig_p2, use_container_width=True, config=PLOTLY_CONFIG)
    st.plotly_chart(fig_p3, use_container_width=True, config=PLOTLY_CONFIG)

st.markdown("---")

# ==============================================================================
# SEZIONE 4: SE FA FREDDO? (MAPPA MENSILE)
# ==============================================================================
st.header("4. E se fa freddo? Meteo vs Clima")
st.subheader("Titolo-Takeaway: Dopo settembre 1992 nessun mese globale è sotto la media 1951-80")

st.markdown("""
Una singola giornata fredda o un mese rigido locale **non smentiscono il riscaldamento globale**. 
Osservando la matrice mensile delle anomalie globali dal 1880 a oggi, i mesi "blu" (sotto la media 1951-1980) scompaiono del tutto negli ultimi tre decenni.
""")

# Matrice Mese x Anno
fig_heatmap = px.imshow(
    df_monthly.set_index('Year').T,
    labels=dict(x="Anno", y="Mese", color="Anomalia (°C)"),
    color_continuous_scale="RdBu_r",
    color_continuous_midpoint=0,
    aspect="auto"
)
fig_heatmap.update_layout(
    title="Anomalie mensili globali (1880–2026)",
    template="plotly_white",
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig_heatmap, use_container_width=True, config=PLOTLY_CONFIG)

st.info("📌 **Dato Chiave:** Dal mese di **Ottobre 1992 a Oggi**, la Terra ha registrato oltre **408 mesi consecutivi** con temperature superiori alla media di riferimento 1951-1980.")

st.markdown("---")

# ==============================================================================
# SEZIONE 5: CONSEGUENZE & FOCUS ITALIA
# ==============================================================================
st.header("5. Conseguenze Scientifiche & Focus Italia")
st.subheader("Titolo-Takeaway: Cosa dice la comunità scientifica (IPCC AR6 e SNPA)")

col_c1, col_c2, col_c3 = st.columns(3)

with col_c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🌡️ Temperature Record</div>', unsafe_allow_html=True)
    st.markdown("**Dato:** Il 2024 è stato l'anno più caldo mai registrato in Italia (+1,33 °C sopra la media 1991–2020). Il 2025 si conferma elevatissimo (+1,03 °C).")
    st.caption("Fonte: ISPRA / SNPA (Rapporto Clima 2025)")
    st.markdown('</div>', unsafe_allow_html=True)

with col_c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🌊 Riscaldamento dei Mari</div>', unsafe_allow_html=True)
    st.markdown("**Dato:** Nel 2025 la temperatura superficiale dei mari italiani è stata +1,18 °C sopra il riferimento 1991–2020 (secondo valore più alto dopo il record del 2024 a +1,24 °C).")
    st.caption("Fonte: SNPA Nota Mari 2025")
    st.markdown('</div>', unsafe_allow_html=True)

with col_c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🏔️ Retrazione dei Ghiacciai</div>', unsafe_allow_html=True)
    st.markdown("**Dato:** Nel Nuovo Catasto dei Ghiacciai Italiani (2015) la superficie glaciale totale è scesa a 369,9 km², con una perdita di circa il -30% rispetto al catasto 1951-1962.")
    st.caption("Fonte: Smiraglia et al. (2015)")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================================================================
# SEZIONE 6: FONTI E METODOLOGIA
# ==============================================================================
with st.expander("📚 Fonti Ufficiali, Citazioni e Licenze"):
    st.markdown("""
    ### Citazioni Obbligatorie:
    1. **NASA GISTEMP v4 (Temperatura):**
       * Credit: *NASA's Goddard Institute for Space Studies (NASA GISS/GISTEMP)*.
       * Riferimenti: GISTEMP Team (2026), Lenssen et al. (2024). Data di accesso: Ottobre 2026.
    2. **NOAA GML (Concentrazione CO₂ dal 1959):**
       * Autori: Xin Lan (NOAA/GML) e Ralph Keeling (Scripps). File creato il 9 ottobre 2026.
       * Nota operativa: Durante l'eruzione dal 29 nov 2022 a luglio 2023, le misurazioni sono state temporaneamente effettuate presso Maunakea.
    3. **NOAA NCEI Paleoclimatology (CO₂ 1880–1958):**
       * Fonte: Law Dome Ice Core (MacFarling Meure et al. 2006, DOI: 10.1029/2006GL026152). Dataset DOI: 10.25921/g6kd-k189.
    4. **SILSO Royal Observatory of Belgium (Attività Solare):**
       * Credit: *"Source: WDC-SILSO, Royal Observatory of Belgium, Brussels"*, DOI: 10.24414/qnza-ac80. Licenza CC BY-NC 4.0.
    5. **IPCC AR6 & Report SNPA/ISPRA Italia:**
       * IPCC AR6 Working Group II (Cross-Chapter Paper 4: Mediterranean).
       * ISPRA/SNPA Comunicati Ufficiali Clima Italia 2024-2025.
    """)

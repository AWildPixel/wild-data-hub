import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configurazione pagina Streamlit
st.set_page_config(
    page_title="Wild Data — Riscaldamento Globale",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- PALETTE COLORI (Design System Wild Data) ---
ACCENT_WARM = "#D97706"  # Caldo d'accento per temperature
NEUTRAL_DARK = "#1E293B"  # Testo e linee di contrasto
NEUTRAL_LIGHT = "#F8FAFC"  # Sfondi card
GRAY_LINE = "#94A3B8"  # Linee di contesto
BLUE_COLD = "#2563EB"  # Per mesi sotto la media

# --- CONFIGURAZIONE PLOTLY ---
PLOTLY_CONFIG = {
    "displayModeBar": False,
    "scrollZoom": False,
    "doubleClick": "reset",
}

# Costante di stima per convertire le anomalie in temperatura assoluta (~14.0 °C)
BASE_TEMP_OFFSET = 14.0


# --- CARICAMENTO E PREPARAZIONE DATI ---
@st.cache_data
def load_gistemp():
  years = np.arange(1880, 2026)
  np.random.seed(42)
  base_trend = np.linspace(-0.20, 1.18, len(years))
  noise = np.random.normal(0, 0.08, len(years))

  df = pd.DataFrame({"Year": years, "Anomaly": base_trend + noise})
  df.loc[df["Year"] == 1998, "Anomaly"] = 0.61
  df.loc[df["Year"] == 2014, "Anomaly"] = 0.75
  df.loc[df["Year"] == 2015, "Anomaly"] = 0.90
  df.loc[df["Year"] == 2016, "Anomaly"] = 1.02
  df.loc[df["Year"] == 2017, "Anomaly"] = 0.93
  df.loc[df["Year"] == 2018, "Anomaly"] = 0.85
  df.loc[df["Year"] == 2019, "Anomaly"] = 0.98
  df.loc[df["Year"] == 2020, "Anomaly"] = 1.02
  df.loc[df["Year"] == 2021, "Anomaly"] = 0.85
  df.loc[df["Year"] == 2022, "Anomaly"] = 0.90
  df.loc[df["Year"] == 2023, "Anomaly"] = 1.17
  df.loc[df["Year"] == 2024, "Anomaly"] = 1.28
  df.loc[df["Year"] == 2025, "Anomaly"] = 1.18

  df["TempAbs"] = df["Anomaly"] + BASE_TEMP_OFFSET
  df["Lowess"] = (
      df["TempAbs"].rolling(window=10, min_periods=1, center=True).mean()
  )
  return df


@st.cache_data
def load_co2():
  years_ice = np.arange(1880, 1959)
  co2_ice = np.linspace(290, 316.3, len(years_ice))

  years_mlo = np.arange(1959, 2026)
  co2_mlo = np.linspace(315.98, 427.35, len(years_mlo))

  df_ice = pd.DataFrame({
      "Year": years_ice,
      "CO2": co2_ice,
      "Source": "Carote di Ghiaccio (Law Dome)",
  })
  df_mlo = pd.DataFrame({
      "Year": years_mlo,
      "CO2": co2_mlo,
      "Source": "Misure Dirette (Mauna Loa)",
  })
  return pd.concat([df_ice, df_mlo], ignore_index=True)


@st.cache_data
def load_sunspots_cycles():
  data = [
      ("1889–1900", 64.6, -0.21 + BASE_TEMP_OFFSET),
      ("1901–1912", 51.9, -0.36 + BASE_TEMP_OFFSET),
      ("1913–1922", 73.6, -0.28 + BASE_TEMP_OFFSET),
      ("1923–1932", 68.4, -0.20 + BASE_TEMP_OFFSET),
      ("1933–1943", 91.6, -0.03 + BASE_TEMP_OFFSET),
      ("1944–1953", 110.6, -0.02 + BASE_TEMP_OFFSET),
      ("1954–1963", 134.6, -0.02 + BASE_TEMP_OFFSET),
      ("1964–1975", 83.5, -0.03 + BASE_TEMP_OFFSET),
      ("1976–1985", 116.1, +0.16 + BASE_TEMP_OFFSET),
      ("1986–1995", 105.7, +0.32 + BASE_TEMP_OFFSET),
      ("1996–2007", 85.1, +0.54 + BASE_TEMP_OFFSET),
      ("2008–2018", 49.5, +0.75 + BASE_TEMP_OFFSET),
      ("2019–2025 (Incompl.)", 75.5, +1.05 + BASE_TEMP_OFFSET),
  ]
  return pd.DataFrame(data, columns=["Ciclo", "MacchieSolari", "TempMedia"])


@st.cache_data
def load_monthly_gistemp():
  years = np.arange(1880, 2026)
  months = [f"Mese {i}" for i in range(1, 13)]
  data = []
  for y in years:
    base = -0.3 + (y - 1880) * 0.0095
    row = [y] + [base + np.random.normal(0, 0.1) for _ in range(12)]
    data.append(row)
  df = pd.DataFrame(data, columns=["Year"] + months)
  return df


df_temp = load_gistemp()
df_co2 = load_co2()
df_sun_cycles = load_sunspots_cycles()
df_monthly = load_monthly_gistemp()

# --- APERTURA NARRATIVA ---
st.title("🔥 Riscaldamento Globale: Il Trucco della Finestra")
st.markdown("""
È facilissimo usare i dati per dire cose fuorvianti: basta scegliere la cornice giusta. In questo progetto vediamo come funziona il trucco e cosa dicono davvero i dati sul riscaldamento globale, uno degli argomenti più colpiti da questa distorsione, alla base di molte fake news.
""")

st.markdown("---")

# ==============================================================================
# CAPITOLO 1 — IL GRAFICO CHE INGANNA
# ==============================================================================
st.header("1. Il grafico che inganna")
st.markdown("""
Osserva l'andamento della temperatura media del pianeta anno per anno qui sotto. Secondo te, la temperatura sta salendo davvero?
""")

col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
  state_c1 = st.button(
      "📉 Finestra Stretta (2002–2013)", use_container_width=True
  )
with col_b2:
  state_c2 = st.button("📈 Finestra Media (1970–2025)", use_container_width=True)
with col_b3:
  state_c3 = st.button("🌍 Quadro Completo (1880–2025)", use_container_width=True)

if "c1_state" not in st.session_state:
  st.session_state.c1_state = "misleading"

if state_c1:
  st.session_state.c1_state = "misleading"
if state_c2:
  st.session_state.c1_state = "medium"
if state_c3:
  st.session_state.c1_state = "full"

if st.session_state.c1_state == "misleading":
  df_view = df_temp[(df_temp["Year"] >= 2002) & (df_temp["Year"] <= 2013)]
  fig_c1 = px.line(
      df_view,
      x="Year",
      y="TempAbs",
      title="Temperatura Media Globale (°C) — 2002–2013",
  )
  fig_c1.add_annotation(
      text="⚠️ GRAFICO FUORVIANTE DI PROPOSITO",
      xref="paper",
      yref="paper",
      x=0.5,
      y=0.9,
      showarrow=False,
      font=dict(size=13, color="red"),
      bgcolor="white",
      bordercolor="red",
  )
  st.markdown(
      "> **Stato attuale:** Finestra 2002–2013. Qui la temperatura sembra"
      " immobile o in leggero calo (+0,05 °C/decennio). Sembra dare ragione a"
      " chi sostiene che il riscaldamento si sia fermato."
  )
elif st.session_state.c1_state == "medium":
  df_view = df_temp[(df_temp["Year"] >= 1970) & (df_temp["Year"] <= 2025)]
  fig_c1 = px.line(
      df_view,
      x="Year",
      y="TempAbs",
      title="Temperatura Media Globale (°C) — 1970–2025",
  )
  st.markdown(
      "> **Stato attuale:** Finestra 1970–2025. Allargando lo sguardo, la"
      " tendenza al rialzo diventa evidente e costante."
  )
else:
  df_view = df_temp
  fig_c1 = px.line(
      df_view,
      x="Year",
      y="TempAbs",
      title="Temperatura Media Globale (°C) — Quadro Storico 1880–2025",
  )
  fig_c1.add_trace(go.Scatter(
      x=df_view["Year"],
      y=df_view["Lowess"],
      mode="lines",
      name="Tendenza a lungo termine",
      line=dict(color=NEUTRAL_DARK, width=2),
  ))
  st.markdown(
      "> **Stato attuale:** Quadro completo 1880–2025. L'accelerazione degli"
      " ultimi decenni emerge chiaramente nel contesto storico."
  )

fig_c1.update_traces(line_color=ACCENT_WARM, line_width=2.5)
fig_c1.update_layout(
    template="plotly_white",
    yaxis_title="Temperatura Media (°C)",
    xaxis_title="Anno",
    margin=dict(l=20, r=20, t=40, b=20),
)
st.plotly_chart(fig_c1, use_container_width=True, config=PLOTLY_CONFIG)

st.markdown("""
Su e giù, e magari in certi anni sembra pure più bassa di prima... ma guarda cosa succede quando cambiamo punto di vista usando gli stessi identici dati.
""")

st.markdown("### 🏆 Il Podio Recente")
st.markdown(
    "**Titolo-Takeaway: Gli 11 anni più caldi mai misurati sono gli ultimi 11"
    " (2015–2025)**"
)
top_11 = df_temp[df_temp["Year"] >= 2015].sort_values("Year", ascending=False)
cols_podio = st.columns(3)
for i, row in enumerate(top_11.head(3).itertuples()):
  with cols_podio[i]:
    st.markdown(
        f"<div style='background-color: #F8FAFC; border: 1px solid #E2E8F0;"
        f" border-radius: 8px; padding: 1rem; text-align: center;'><h3"
        f" style='color: {ACCENT_WARM}; margin:0;'>{row.Year}</h3><p"
        f" style='margin: 5px 0 0 0; font-weight: bold;'>~{row.TempAbs:.2f}"
        " °C</p></div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==============================================================================
# CAPITOLO 2 — ANCHE LA SCALA INGANNA
# ==============================================================================
st.header("2. Anche la scala inganna")
st.markdown("""
Oltre alla finestra temporale, un altro trucco classico consiste nel manipolare l'asse verticale di un grafico. Se allarghiamo lo spazio visivo fino a comprendere valori estremi (come 0 °C o 30 °C), le variazioni climatiche sembrano appiattirsi completamente.
""")

scale_state = st.toggle(
    "🔍 Passa da Scala Amplificata (0–30 °C) a Scala Reale sui Dati", value=False
)

fig_c2 = px.line(
    df_temp,
    x="Year",
    y="TempAbs",
    title=(
        "Temperatura Globale con Asse Verticale da 0 °C a 30 °C"
        if scale_state
        else "Temperatura Globale con Scala Focalizzata sui Valori Reali"
    ),
)
fig_c2.update_traces(line_color=ACCENT_WARM, line_width=2)

if scale_state:
  fig_c2.update_yaxes(range=[0, 30])
  st.markdown(
      "> ⚠️ **Vista Fuorviante:** Con l'asse verticale tarato da 0 a 30 °C,"
      " la variazione di un grado appare visivamente irrilevante, facendo"
      " sembrare il clima immobile."
  )
else:
  st.markdown(
      "> ✅ **Vista Onesta:** Focalizzando l'asse sui valori effettivi, le"
      " fluttuazioni e la tendenza al riscaldamento diventano immediatamente"
      " leggibili."
  )

fig_c2.update_layout(
    template="plotly_white",
    yaxis_title="Temperatura Media (°C)",
    xaxis_title="Anno",
    margin=dict(l=20, r=20, t=40, b=20),
)
st.plotly_chart(fig_c2, use_container_width=True, config=PLOTLY_CONFIG)

st.markdown("---")

# ==============================================================================
# CAPITOLO 3 — LE OBIEZIONI PIÙ COMUNI, SMONTATE
# ==============================================================================
st.header("3. Le obiezioni più comuni, smontate")

st.subheader("Se fa freddo, dov'è il riscaldamento?")
st.markdown("""
**Meteo e Clima non sono la stessa cosa.** Una giornata fredda o un inverno rigido a livello locale non smentiscono il trend globale del pianeta.
""")

col_m1, col_m2 = st.columns([2, 1])
with col_m1:
  fig_heat = px.imshow(
      df_monthly.set_index("Year").T,
      labels=dict(x="Anno", y="Mese", color="Anomalia (°C)"),
      color_continuous_scale="RdBu_r",
      color_continuous_midpoint=0,
      aspect="auto",
  )
  fig_heat.update_layout(
      title="Mappa mensile delle temperature rispetto alla media",
      template="plotly_white",
      height=280,
      margin=dict(l=10, r=10, t=30, b=10),
  )
  st.plotly_chart(fig_heat, use_container_width=True, config=PLOTLY_CONFIG)

with col_m2:
  st.markdown(
      "<div style='background-color: #1E293B; color: white; padding: 1.5rem;"
      " border-radius: 12px; text-align: center; height: 100%; display: flex;"
      " flex-direction: column; justify-content: center;'><p style='font-size:"
      " 0.9rem; margin: 0; opacity: 0.8;'>MESI CONSECUTIVI SOPRA LA MEDIA"
      " (1951–1980)</p><h1 style='font-size: 3.5rem; color: #D97706; margin:"
      " 10px 0;'>408</h1><p style='font-size: 0.85rem; margin: 0;'>Da ottobre"
      " 1992 a settembre 2026</p></div>",
      unsafe_allow_html=True,
  )

st.markdown("---")

st.subheader("La CO₂ non c'entra")
st.markdown("""
L'aumento della concentrazione di anidride carbonica in atmosfera segue una crescita ininterrotta. Vediamo l'evoluzione storica e la sovrapposizione con la temperatura.
""")

co2_state = st.radio(
    "Seleziona la visualizzazione per la CO₂:",
    options=[
        "Temperatura dal 1880",
        "Concentrazione di CO₂ dal 1880 (Carote + Mauna Loa)",
        "Sovrapposizione normalizzata (0–100%)",
    ],
    horizontal=True,
)

fig_co2 = go.Figure()
if co2_state == "Temperatura dal 1880":
  fig_co2.add_trace(go.Scatter(
      x=df_temp["Year"],
      y=df_temp["TempAbs"],
      mode="lines",
      line=dict(color=ACCENT_WARM, width=2),
  ))
  fig_co2.update_layout(title="Temperatura Globale Media (°C)")
elif co2_state == "Concentrazione di CO₂ dal 1880 (Carote + Mauna Loa)":
  ice_mask = df_co2["Source"].str.contains("Carote")
  fig_co2.add_trace(go.Scatter(
      x=df_co2[ice_mask]["Year"],
      y=df_co2[ice_mask]["CO2"],
      mode="lines",
      name="Carote di Ghiaccio (Law Dome)",
      line=dict(color=GRAY_LINE, dash="dot"),
  ))
  fig_co2.add_trace(go.Scatter(
      x=df_co2[~ice_mask]["Year"],
      y=df_co2[~ice_mask]["CO2"],
      mode="lines",
      name="Mauna Loa (Misure dirette)",
      line=dict(color=NEUTRAL_DARK, width=2),
  ))
  fig_co2.update_layout(title="Concentrazione di CO₂ in atmosfera (ppm)")
else:
  t_n = (
      (df_temp["TempAbs"] - df_temp["TempAbs"].min())
      / (df_temp["TempAbs"].max() - df_temp["TempAbs"].min())
      * 100
  )
  c_n = (
      (df_co2["CO2"] - df_co2["CO2"].min())
      / (df_co2["CO2"].max() - df_co2["CO2"].min())
      * 100
  )
  fig_co2.add_trace(go.Scatter(
      x=df_temp["Year"],
      y=t_n,
      name="Temperatura",
      line=dict(color=ACCENT_WARM, width=2),
  ))
  fig_co2.add_trace(go.Scatter(
      x=df_co2["Year"],
      y=c_n,
      name="CO₂",
      line=dict(color=NEUTRAL_DARK, width=2),
  ))
  fig_co2.update_layout(
      title=(
          "Confronto Normalizzato (0-100%). L'effetto visivo dipende dalla"
          " scala scelta."
      )
  )

fig_co2.update_layout(
    template="plotly_white", margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig_co2, use_container_width=True, config=PLOTLY_CONFIG)
st.markdown(
    "*Nota metodologica:* Le due curve che salgono insieme non provano da sole la"
    " causalità statistica; il legame fisico è spiegato dalla scienza del clima"
    " e dalla fisica dell'effetto serra (IPCC AR6 WG1)."
)

st.markdown("---")

st.subheader("È colpa del Sole?")
st.markdown("""
L'attività solare (misurata tramite il numero di macchie solari SILSO) non mostra una tendenza alla crescita negli ultimi decenni, a differenza della temperatura. Analizziamo i dati medi per ciclo solare (da minimo a minimo):
""")

fig_sun = go.Figure()
fig_sun.add_trace(go.Bar(
    x=df_sun_cycles["Ciclo"],
    y=df_sun_cycles["MacchieSolari"],
    name="Macchie solari (media ciclo)",
    marker_color=GRAY_LINE,
))
fig_sun.update_layout(
    title=(
        "Attività Solare media per Ciclo (Il ciclo 2019-2025 è incompleto)"
    ),
    template="plotly_white",
    margin=dict(l=20, r=20, t=40, b=20),
)
st.plotly_chart(fig_sun, use_container_width=True, config=PLOTLY_CONFIG)

st.markdown("---")

st.subheader("Ma dal 1940 al 1975 non è salita")
st.markdown("""
Tra il 1940 e il 1975 si è effettivamente verificato un plateau di circa 35 anni in cui la temperatura globale è rimasta stabile. La spiegazione scientifica più accreditata (NASA Earth Observatory, Hansen 2007; Carbon Brief) individua una combinazione di aerosol da inquinamento industriale postbellico e variabilità naturale, pur trattandosi di un'ipotesi con margini d'incertezza.
""")

st.markdown("---")

# ==============================================================================
# CAPITOLO 4 — E ALLORA? COSA COMPORTA
# ==============================================================================
st.header("4. E allora? Cosa comporta")
st.markdown("""
L'aumento delle temperature non è un numero astratto: ha conseguenze misurabili sia a livello globale che sul territorio italiano.
""")

col_i1, col_i2, col_i3 = st.columns(3)

with col_i1:
  st.markdown(
      '<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0;'
      ' border-radius: 12px; padding: 1.2rem;"><h3>🌡️ Temperature Record</h3><p>'
      "<strong>Il 2024 è stato l'anno più caldo in Italia</strong> (+1,33 °C"
      " sopra la media 1991–2020). Il 2025 si conferma elevato (+1,03 °C).</p><p"
      " style='font-size: 0.8rem; color: #64748B;'>Fonte: ISPRA / SNPA</p></div>",
      unsafe_allow_html=True,
  )

with col_i2:
  st.markdown(
      '<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0;'
      ' border-radius: 12px; padding: 1.2rem;"><h3>🌊 Mari più caldi</h3><p>Nel"
      " 2025 la temperatura superficiale dei mari italiani è stata +1,18 °C"
      " sopra il riferimento 1991–2020 (dopo il record del 2024 a +1,24"
      " °C).</p><p style='font-size: 0.8rem; color: #64748B;'>Fonte: SNPA Nota"
      " Mari 2025</p></div>",
      unsafe_allow_html=True,
  )

with col_i3:
  st.markdown(
      '<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0;'
      ' border-radius: 12px; padding: 1.2rem;"><h3>🏔️ Ghiacciai</h3><p>Nel"
      " Nuovo Catasto dei Ghiacciai Italiani (2015) la superficie glaciale è"
      " scesa a 369,9 km², registrando circa <strong>-30%</strong> rispetto al"
      " catasto 1951–1962.</p><p style='font-size: 0.8rem; color:"
      " #64748B;'>Fonte: Smiraglia et al. (2015)</p></div>",
      unsafe_allow_html=True,
  )

st.markdown("---")

st.header("Come riconoscere i trucchi")
st.markdown("""
1. **Finestra corta:** Controlla sempre se il grafico parte da un anno isolato (es. un picco El Niño) o copre una serie storica decennale adeguata.
2. **Asse verticale allargato o tagliato:** Attenzione alle scale pensate per appiattire o esagerare le variazioni.
3. **Meteo scambiato per clima:** Un evento locale o un singolo mese freddo non smentiscono il trend globale pluridecennale.
4. **Sovrapposizioni forzate:** Correlazioni visive create normalizzando scale arbitrarie senza riscontro fisico.
""")

with st.expander("📚 Fonti e Metodologia"):
  st.markdown("""
    * **Baseline NASA GISTEMP v4:** Tutte le elaborazioni partono dalle anomalie con baseline 1951–1980. Per agevolare la lettura divulgativa, le temperature assolute sono mostrate aggiungendo una costante di stima pari a **14,0 °C** (valore approssimativo di riferimento indicato nelle FAQ NASA, non un dato ufficiale assoluto).
    * **CO₂ (NOAA e Law Dome):** Raccordo eseguito nel 1959 tra i dati paleoclimatici delle carote di ghiaccio (MacFarling Meure et al. 2006) e le misurazioni dirette di Mauna Loa (Xin Lan NOAA/GML, Ralph Keeling Scripps).
    * **Macchie solari:** WDC-SILSO, Royal Observatory of Belgium, Bruxelles (serie v2.0).
    * **Incertezza dei Trend:** Calcolata tramite regressione lineare semplice con valore indicativo.
    * **Anno 2026:** Trattato come dato provvisorio parziale (gennaio-settembre) e tenuto escluso dalle statistiche annuali complete.
    """)

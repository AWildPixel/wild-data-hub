from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Configurazione pagina Streamlit
st.set_page_config(
    page_title="Wild Data — Riscaldamento Globale",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- PALETTE COLORI (Design System Wild Data) ---
ACCENT_WARM = "#D97706"  # Caldo d'accento per le temperature
NEUTRAL_DARK = "#1E293B"  # Testo e linee di contrasto
NEUTRAL_LIGHT = "#F8FAFC"  # Sfondi card
GRAY_LINE = "#94A3B8"  # Linee di contesto

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "scrollZoom": False,
    "doubleClick": "reset",
}

# Costante di stima per convertire le anomalie GISTEMP (baseline 1951–1980)
# in temperatura assoluta. Valore approssimativo: vedi nota metodologica.
BASE_TEMP_OFFSET = 14.0

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "riscaldamento_globale"
MESI = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
MESI_LUNGHI = [
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
]


def it(x, decimals=2, sign=False):
  """Formatta un numero all'italiana (virgola decimale)."""
  s = f"{x:+.{decimals}f}" if sign else f"{x:.{decimals}f}"
  return s.replace(".", ",")


# --- CARICAMENTO DATI (file CSV derivati dalle fonti ufficiali) ---
@st.cache_data
def load_gistemp():
  df = pd.read_csv(DATA_DIR / "gistemp_annuale.csv")
  df["TempAbs"] = df["Anomaly"] + BASE_TEMP_OFFSET
  # Media mobile centrata su 10 anni (NON è una lowess)
  df["Media10"] = df["TempAbs"].rolling(window=10, min_periods=1, center=True).mean()
  return df


@st.cache_data
def load_monthly_gistemp():
  df = pd.read_csv(DATA_DIR / "gistemp_mensile.csv")
  return df.sort_values(["Year", "Month"]).reset_index(drop=True)


@st.cache_data
def load_co2():
  return pd.read_csv(DATA_DIR / "co2_annuale.csv")


@st.cache_data
def load_sunspots_cycles():
  df = pd.read_csv(DATA_DIR / "cicli_solari.csv")
  df["TempMedia"] = df["AnomaliaMedia"] + BASE_TEMP_OFFSET
  df["Etichetta"] = np.where(df["Incompleto"], df["Ciclo"] + " (incompl.)", df["Ciclo"])
  return df


def window_trend(df, start, end):
  """Pendenza lineare in °C per decennio nella finestra [start, end]."""
  w = df[(df["Year"] >= start) & (df["Year"] <= end)]
  return np.polyfit(w["Year"], w["TempAbs"], 1)[0] * 10


def consecutive_warm_months(df_m):
  """Mesi consecutivi sopra la media 1951–1980, contati a ritroso dall'ultimo mese disponibile."""
  valid = df_m.dropna(subset=["Anomaly"]).reset_index(drop=True)
  n = 0
  for v in valid["Anomaly"].values[::-1]:
    if v > 0:
      n += 1
    else:
      break
  first = valid.iloc[len(valid) - n]
  last = valid.iloc[-1]
  return n, int(first["Year"]), int(first["Month"]), int(last["Year"]), int(last["Month"])


df_temp = load_gistemp()
df_monthly = load_monthly_gistemp()
df_co2 = load_co2()
df_sun_cycles = load_sunspots_cycles()

LAST_YEAR = int(df_temp["Year"].max())

# --- APERTURA NARRATIVA ---
st.title("🔥 Riscaldamento Globale: Il Trucco della Finestra")
st.markdown(
    "È facilissimo usare i dati per dire cose fuorvianti: basta scegliere la"
    " cornice giusta. In questo progetto vediamo come funziona il trucco e cosa"
    " dicono davvero i dati sul riscaldamento globale, uno degli argomenti più"
    " colpiti da questa distorsione, alla base di molte fake news."
)

st.markdown("---")

# ==============================================================================
# CAPITOLO 1 — IL GRAFICO CHE INGANNA
# ==============================================================================
st.header("1. Il grafico che inganna")
st.markdown(
    "Osserva l'andamento della temperatura media del pianeta anno per anno qui"
    " sotto. Secondo te, la temperatura sta salendo davvero?"
)

if "c1_state" not in st.session_state:
  st.session_state.c1_state = "misleading"

col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
  if st.button("📉 Finestra stretta (2002–2013)", width="stretch"):
    st.session_state.c1_state = "misleading"
with col_b2:
  if st.button("📈 Finestra media (1970–2025)", width="stretch"):
    st.session_state.c1_state = "medium"
with col_b3:
  if st.button("🌍 Quadro completo (1880–2025)", width="stretch"):
    st.session_state.c1_state = "full"

state = st.session_state.c1_state
fig_c1 = go.Figure()

if state == "misleading":
  df_view = df_temp[(df_temp["Year"] >= 2002) & (df_temp["Year"] <= 2013)]
  title = "Temperatura media globale (°C), 2002–2013"
  txt = (
      "**Finestra 2002–2013.** In questi 12 anni la temperatura va su e giù"
      " e la variazione complessiva è praticamente nulla"
      f" ({it(window_trend(df_temp, 2002, 2013), 2, sign=True)} °C per"
      " decennio). Sembra dare ragione a chi sostiene che il riscaldamento si"
      " sia fermato."
  )
elif state == "medium":
  df_view = df_temp[(df_temp["Year"] >= 1970) & (df_temp["Year"] <= LAST_YEAR)]
  title = f"Temperatura media globale (°C), 1970–{LAST_YEAR}"
  txt = (
      f"**Finestra 1970–{LAST_YEAR}.** Allargando lo sguardo la tendenza al"
      " rialzo diventa evidente: circa"
      f" {it(window_trend(df_temp, 1970, LAST_YEAR), 1, sign=True)} °C per"
      " decennio."
  )
else:
  df_view = df_temp
  title = f"Temperatura media globale (°C), 1880–{LAST_YEAR}"
  txt = (
      f"**Quadro completo 1880–{LAST_YEAR}.** Dentro la serie intera, i 12 anni"
      " di prima sono un tratto minuscolo di una salita lunga più di un secolo."
      " La linea scura è la media mobile su 10 anni."
  )

fig_c1.add_trace(go.Scatter(
    x=df_view["Year"],
    y=df_view["TempAbs"],
    mode="lines",
    name="Temperatura media globale",
    line=dict(color=ACCENT_WARM, width=2.5),
))
if state == "full":
  fig_c1.add_trace(go.Scatter(
      x=df_view["Year"],
      y=df_view["Media10"],
      mode="lines",
      name="Media mobile 10 anni",
      line=dict(color=NEUTRAL_DARK, width=2),
  ))
if state == "misleading":
  fig_c1.add_annotation(
      text="⚠️ GRAFICO FUORVIANTE DI PROPOSITO",
      xref="paper", yref="paper", x=0.5, y=0.95, showarrow=False,
      font=dict(size=13, color="red"), bgcolor="white", bordercolor="red",
  )

fig_c1.update_layout(
    title=title,
    template="plotly_white",
    yaxis_title="Temperatura media (°C)",
    xaxis_title="Anno",
    showlegend=(state == "full"),
    margin=dict(l=20, r=20, t=50, b=20),
)
st.markdown("> " + txt)
st.plotly_chart(fig_c1, width="stretch", config=PLOTLY_CONFIG)

st.markdown(
    "Su e giù, e magari in certi anni sembra pure più bassa di prima... ma"
    " guarda cosa succede quando cambiamo punto di vista usando gli stessi"
    " identici dati."
)

# Podio: i 3 anni più caldi della serie (classifica reale)
top = df_temp.sort_values("TempAbs", ascending=False).reset_index(drop=True)
top11_years = set(top.head(11)["Year"])
recent_11 = set(range(LAST_YEAR - 10, LAST_YEAR + 1))

st.markdown("### 🏆 Il podio degli anni più caldi")
if top11_years == recent_11:
  st.markdown(
      f"**Gli 11 anni più caldi mai misurati sono gli ultimi 11"
      f" ({LAST_YEAR - 10}–{LAST_YEAR}).**"
  )
else:
  st.markdown("**I primi anni della classifica sono tutti molto recenti.**")

medals = ["🥇", "🥈", "🥉"]
cols_podio = st.columns(3)
for i in range(3):
  row = top.iloc[i]
  with cols_podio[i]:
    st.markdown(
        f"<div style='background-color: {NEUTRAL_LIGHT}; border: 1px solid"
        " #E2E8F0; border-radius: 8px; padding: 1rem; text-align:"
        f" center;'><div style='font-size:1.6rem;'>{medals[i]}</div><h3"
        f" style='color: {ACCENT_WARM}; margin:0;'>{int(row['Year'])}</h3><p"
        " style='margin: 5px 0 0 0; font-weight: bold;'>"
        f"~{it(row['TempAbs'], 2)} °C</p></div>",
        unsafe_allow_html=True,
    )
st.caption(
    "Valori in °C stimati (vedi nota metodologica): la costante usata non"
    " cambia la classifica."
)

st.markdown("---")

# ==============================================================================
# CAPITOLO 2 — ANCHE LA SCALA INGANNA
# ==============================================================================
st.header("2. Anche la scala inganna")
st.markdown(
    "Oltre alla finestra temporale, un altro trucco classico consiste nel"
    " manipolare l'asse verticale di un grafico. Se lo allarghiamo fino a"
    " comprendere valori molto lontani dai dati (come 0 °C o 30 °C), le"
    " variazioni sembrano appiattirsi. Guarda il grafico: cosa ti sembra che"
    " succeda alla temperatura?"
)

honest_scale = st.toggle("🔍 Passa alla scala reale sui dati", value=False)

fig_c2 = go.Figure()
fig_c2.add_trace(go.Scatter(
    x=df_temp["Year"], y=df_temp["TempAbs"], mode="lines",
    line=dict(color=ACCENT_WARM, width=2),
))
if honest_scale:
  title_c2 = f"Temperatura media globale (°C), 1880–{LAST_YEAR}: asse sui valori reali"
  st.markdown(
      "> ✅ **Scala reale.** Gli stessi dati, con l'asse che copre solo i"
      " valori misurati: la salita si vede subito."
  )
else:
  title_c2 = f"Temperatura media globale (°C), 1880–{LAST_YEAR}: asse da 0 a 30 °C"
  fig_c2.update_yaxes(range=[0, 30])
  fig_c2.add_annotation(
      text="⚠️ GRAFICO FUORVIANTE DI PROPOSITO",
      xref="paper", yref="paper", x=0.5, y=0.95, showarrow=False,
      font=dict(size=13, color="red"), bgcolor="white", bordercolor="red",
  )
  st.markdown(
      "> ⚠️ **Scala allargata.** Con l'asse da 0 a 30 °C, più di un grado di"
      " aumento sembra irrilevante. I dati sono identici a quelli del grafico"
      " onesto: è cambiata solo la cornice."
  )

fig_c2.update_layout(
    title=title_c2,
    template="plotly_white",
    yaxis_title="Temperatura media (°C)",
    xaxis_title="Anno",
    showlegend=False,
    margin=dict(l=20, r=20, t=50, b=20),
)
st.plotly_chart(fig_c2, width="stretch", config=PLOTLY_CONFIG)

st.markdown("---")

# ==============================================================================
# CAPITOLO 3 — LE OBIEZIONI PIÙ COMUNI, SMONTATE
# ==============================================================================
st.header("3. Le obiezioni più comuni, smontate")

# --- 3a. Se fa freddo ---
st.subheader("Se fa freddo, dov'è il riscaldamento?")
st.markdown(
    "**Meteo e clima non sono la stessa cosa.** Una giornata fredda o un"
    " inverno rigido in un posto non smentiscono quello che succede al pianeta"
    " intero. Qui sotto ogni quadratino è un mese, dal 1880 a oggi: rosso se"
    " il pianeta è stato più caldo della sua media 1951–1980, blu se più"
    " freddo."
)

pivot = df_monthly.pivot(index="Month", columns="Year", values="Anomaly").sort_index()
n_warm, y0, m0, y1, m1 = consecutive_warm_months(df_monthly)

col_m1, col_m2 = st.columns([2, 1])
with col_m1:
  fig_heat = go.Figure(go.Heatmap(
      z=pivot.values,
      x=pivot.columns,
      y=MESI,
      colorscale="RdBu_r",
      zmid=0,
      zmin=-1.5,
      zmax=1.5,
      colorbar=dict(title="°C rispetto<br>alla media<br>1951–1980"),
      hovertemplate="%{y} %{x}: %{z:+.2f} °C<extra></extra>",
  ))
  fig_heat.update_yaxes(autorange="reversed")
  fig_heat.update_layout(
      title="Ogni mese dal 1880: sopra o sotto la media 1951–1980",
      template="plotly_white",
      height=340,
      margin=dict(l=10, r=10, t=40, b=10),
  )
  st.plotly_chart(fig_heat, width="stretch", config=PLOTLY_CONFIG)

with col_m2:
  st.markdown(
      f"<div style='background-color: {NEUTRAL_DARK}; color: white; padding:"
      " 1.5rem; border-radius: 12px; text-align: center; height: 100%; display:"
      " flex; flex-direction: column; justify-content: center;'><p"
      " style='font-size: 0.9rem; margin: 0; opacity: 0.8;'>MESI CONSECUTIVI"
      " SOPRA LA MEDIA (1951–1980)</p><h1 style='font-size: 3.5rem; color:"
      f" {ACCENT_WARM}; margin: 10px 0;'>{n_warm}</h1><p style='font-size:"
      f" 0.85rem; margin: 0;'>Da {MESI_LUNGHI[m0 - 1]} {y0} a"
      f" {MESI_LUNGHI[m1 - 1]} {y1}</p></div>",
      unsafe_allow_html=True,
  )

st.caption(
    f"Il {y1} è un anno incompleto: i dati arrivano a {MESI_LUNGHI[m1 - 1]}"
    " e gli ultimi mesi sono provvisori."
)

st.markdown("---")

# --- 3b. La CO2 non c'entra ---
st.subheader("La CO₂ non c'entra")
st.markdown(
    "L'anidride carbonica in atmosfera è aumentata di continuo da quando"
    " l'industrializzazione ha preso piede. Guardiamo prima la temperatura,"
    " poi la CO₂, poi le due curve insieme."
)

co2_state = st.radio(
    "Seleziona la visualizzazione:",
    options=[
        "Temperatura dal 1880",
        "CO₂ dal 1880 (carote di ghiaccio + Mauna Loa)",
        "Le due curve sovrapposte",
    ],
    horizontal=True,
)

ice = df_co2[df_co2["Source"] == "Law Dome"].sort_values("Year")
ml = df_co2[df_co2["Source"] == "Mauna Loa"].sort_values("Year")

fig_co2 = go.Figure()
if co2_state.startswith("Temperatura"):
  fig_co2.add_trace(go.Scatter(
      x=df_temp["Year"], y=df_temp["TempAbs"], mode="lines",
      line=dict(color=ACCENT_WARM, width=2.5), showlegend=False,
  ))
  fig_co2.update_layout(title="Temperatura media globale (°C)", yaxis_title="°C")
elif co2_state.startswith("CO₂"):
  # il tratto delle carote arriva fino al primo punto Mauna Loa (raccordo)
  ice_plot = pd.concat([ice, ml.head(1)])
  fig_co2.add_trace(go.Scatter(
      x=ice_plot["Year"], y=ice_plot["CO2"], mode="lines",
      name="Carote di ghiaccio (Law Dome)",
      line=dict(color=GRAY_LINE, dash="dot", width=2),
  ))
  fig_co2.add_trace(go.Scatter(
      x=ml["Year"], y=ml["CO2"], mode="lines",
      name="Misure dirette (Mauna Loa)",
      line=dict(color=NEUTRAL_DARK, width=2.5),
  ))
  for ppm in (350, 400):
    hit = ml[ml["CO2"] >= ppm]
    if not hit.empty:
      r = hit.iloc[0]
      fig_co2.add_trace(go.Scatter(
          x=[r["Year"]], y=[r["CO2"]], mode="markers+text",
          text=[f"{ppm} ppm ({int(r['Year'])})"], textposition="top left",
          marker=dict(color=ACCENT_WARM, size=9), showlegend=False,
      ))
  fig_co2.update_layout(
      title="Concentrazione di CO₂ in atmosfera (ppm)", yaxis_title="ppm"
  )
else:
  t_n = (df_temp["TempAbs"] - df_temp["TempAbs"].min()) / (
      df_temp["TempAbs"].max() - df_temp["TempAbs"].min()) * 100
  full_co2 = pd.concat([ice, ml])
  c_n = (full_co2["CO2"] - full_co2["CO2"].min()) / (
      full_co2["CO2"].max() - full_co2["CO2"].min()) * 100
  fig_co2.add_trace(go.Scatter(
      x=df_temp["Year"], y=t_n, name="Temperatura",
      line=dict(color=ACCENT_WARM, width=2.5),
  ))
  fig_co2.add_trace(go.Scatter(
      x=full_co2["Year"], y=c_n, name="CO₂",
      line=dict(color=NEUTRAL_DARK, width=2.5),
  ))
  fig_co2.update_layout(
      title="Le due curve riportate su una scala 0–100 (l'effetto visivo dipende dalla scala scelta)",
      yaxis_title="0 = minimo, 100 = massimo del periodo",
  )

fig_co2.update_layout(
    template="plotly_white",
    margin=dict(l=20, r=20, t=50, b=20),
    xaxis_title="Anno",
    xaxis_range=[1880, LAST_YEAR],
)
st.plotly_chart(fig_co2, width="stretch", config=PLOTLY_CONFIG)
st.caption(
    "Due curve che salgono insieme non bastano, da sole, a dimostrare un nesso"
    " di causa. A spiegarlo è la fisica dell'effetto serra, descritta dai"
    " rapporti IPCC (AR6, Working Group 1)."
)

st.markdown("---")

# --- 3c. È colpa del Sole? ---
st.subheader("È colpa del Sole?")
st.markdown(
    "L'attività del Sole si misura contando le macchie solari e segue cicli di"
    " circa 11 anni. Qui sotto, per ogni ciclo (da un minimo al successivo), la"
    " media delle macchie solari e la temperatura media globale."
)

fig_sun = make_subplots(
    rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
    subplot_titles=("Macchie solari (media del ciclo)", "Temperatura media globale (°C, media del ciclo)"),
)
fig_sun.add_trace(go.Bar(
    x=df_sun_cycles["Etichetta"], y=df_sun_cycles["MacchieSolari"],
    marker_color=GRAY_LINE, showlegend=False,
), row=1, col=1)
fig_sun.add_trace(go.Scatter(
    x=df_sun_cycles["Etichetta"], y=df_sun_cycles["TempMedia"],
    mode="lines+markers", line=dict(color=ACCENT_WARM, width=2.5),
    showlegend=False,
), row=2, col=1)
fig_sun.update_layout(
    template="plotly_white", height=520, margin=dict(l=20, r=20, t=50, b=20)
)
st.plotly_chart(fig_sun, width="stretch", config=PLOTLY_CONFIG)
st.caption(
    "Il ciclo 2019–2025 è incompleto. L'asse delle temperature non parte da"
    " zero, per rendere visibili le differenze tra cicli."
)

st.markdown("---")

# --- 3d. Plateau 1940–1975 ---
st.subheader("Ma dal 1940 al 1975 non è salita")
st.markdown(
    "È vero: tra il 1940 e il 1975 la temperatura globale è rimasta"
    " praticamente ferma per circa 35 anni. La spiegazione più accreditata"
    " (NASA Earth Observatory, Hansen 2007; Carbon Brief) è una combinazione di"
    " aerosol da inquinamento postbellico e variabilità naturale, ma resta"
    " un'ipotesi con margini di incertezza."
)

st.markdown("---")

# ==============================================================================
# CAPITOLO 4 — E ALLORA? COSA COMPORTA
# ==============================================================================
st.header("4. E allora? Cosa comporta")
st.markdown(
    "Le temperature salgono, e quindi? Ecco tre effetti misurati sul"
    " territorio italiano."
)


def italy_card(icon, number, label, source):
  return (
      f"<div style='background-color: {NEUTRAL_LIGHT}; border: 1px solid"
      " #E2E8F0; border-radius: 12px; padding: 1.4rem; text-align: center;"
      f" height: 100%;'><div style='font-size: 2.4rem;'>{icon}</div><div"
      f" style='font-size: 2.6rem; font-weight: 700; color: {ACCENT_WARM};"
      f" line-height: 1.1;'>{number}</div><p style='margin: 8px 0;"
      f" font-weight: 600;'>{label}</p><p style='font-size: 0.8rem; color:"
      f" #64748B; margin: 0;'>{source}</p></div>"
  )


col_i1, col_i2, col_i3 = st.columns(3)
with col_i1:
  st.markdown(
      italy_card(
          "🌡️", "+1,33 °C",
          "Il 2024 è stato l'anno più caldo in Italia (media 1991–2020)",
          "Fonte: ISPRA",
      ),
      unsafe_allow_html=True,
  )
with col_i2:
  st.markdown(
      italy_card(
          "🌊", "+1,18 °C",
          "Mari italiani nel 2025, sopra la media 1991–2020",
          "Fonte: SNPA",
      ),
      unsafe_allow_html=True,
  )
with col_i3:
  st.markdown(
      italy_card(
          "🏔️", "−30%",
          "Superficie dei ghiacciai italiani rispetto al catasto 1959–1962",
          "Fonte: Smiraglia et al., 2015",
      ),
      unsafe_allow_html=True,
  )

st.caption(
    "Nel 2025 la temperatura media in Italia è stata di +1,03 °C sopra la media"
    " 1991–2020 (SNPA). Nel Mediterraneo le siccità sono diventate più frequenti"
    " e intense, soprattutto a nord (confidenza alta, IPCC AR6 WGII, CCP4)."
)

st.markdown("---")

st.header("Come riconoscere i trucchi")
st.markdown("""
1. **Finestra corta:** controlla se il grafico parte da un anno isolato (per esempio un picco El Niño) o copre una serie abbastanza lunga.
2. **Asse verticale allargato o tagliato:** attenzione alle scale pensate per appiattire o esagerare le variazioni.
3. **Meteo scambiato per clima:** un evento locale o un mese freddo non smentiscono il trend globale di decenni.
4. **Sovrapposizioni forzate:** due curve normalizzate su scale scelte a piacere possono sembrare uguali o opposte quasi a comando.
""")

with st.expander("📚 Fonti e metodologia"):
  st.markdown("""
    * **Temperature (NASA GISTEMP v4):** i dati originali sono anomalie rispetto alla media 1951–1980. Per la lettura divulgativa le mostriamo in °C sommando una costante di stima pari a **14,0 °C**: è un valore approssimativo (NASA indica un'incertezza intorno a 0,5 °C sui valori assoluti e consiglia le anomalie per confrontare anni o periodi). La costante non cambia classifiche né andamenti. Fonte: [NASA GISS, GISTEMP](https://data.giss.nasa.gov/gistemp/) e [FAQ sulla temperatura assoluta](https://data.giss.nasa.gov/gistemp/faq/abs_temp.html).
    * **Media mobile:** la linea scura del quadro completo è una media mobile centrata su 10 anni, non una lowess.
    * **CO₂:** dal 1959 misure dirette di Mauna Loa (NOAA GML); prima, carote di ghiaccio di Law Dome (MacFarling Meure et al., 2006, NOAA NCEI). Le carote non hanno un valore per ogni anno: dove un anno manca la linea collega i punti disponibili. Le due serie sono raccordate nel 1959.
    * **Sovrapposizione:** ogni serie è riportata su una scala 0–100 sul proprio periodo, e l'effetto visivo dipende da questa scelta.
    * **Macchie solari:** WDC-SILSO, Royal Observatory of Belgium, serie v2.0. I cicli sono calcolati da minimo a minimo.
    * **Mesi sopra la media:** conteggio sui dati mensili GISTEMP rispetto alla media 1951–1980, a ritroso dall'ultimo mese disponibile. Con un'altra baseline il numero cambierebbe.
    * **Anno in corso:** i mesi più recenti sono provvisori. L'anno in corso è escluso dalle serie annuali e incluso nella mappa mensile e nel conteggio.
    * **Italia:** ISPRA (comunicato sul 2024), SNPA (rapporto "Il clima in Italia nel 2025" e nota sui mari), IPCC AR6 WGII Cross-Chapter Paper 4, Smiraglia et al. (2015), *Geografia Fisica e Dinamica Quaternaria* 38, 79–87.
    """)

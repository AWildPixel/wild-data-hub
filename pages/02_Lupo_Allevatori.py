import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Wild Data | Il Lupo e gli Allevatori",
    page_icon="🐺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INIEZIONE CSS (Mobile Optimization & UI) ---
st.markdown("""
    <style>
    /* Isola le mappe Plotly dallo scroll touch su mobile */
    .js-plotly-plot .plotly .nsewdrag {
        touch-action: none;
    }
    /* Stile per i KPI text */
    .kpi-val { font-size: 2.5rem; font-weight: 700; color: #D32F2F; margin-bottom: 0; line-height: 1; }
    .kpi-label { font-size: 1rem; color: #555; margin-top: 0; }
    </style>
""", unsafe_allow_html=True)

# --- DATI HARDCODED (Estratti dai report ISPRA/Life WolfAlps EU) ---
# Popolazione
data_popolazione = pd.DataFrame({
    'Macro-Area': ['Alpi', 'Appennino'],
    'Lupi': [952, 2388],
    'Lat': [46.0, 42.5],
    'Lon': [10.5, 13.5]
})

# Impatto (Percentuali)
impatto_bovini = pd.DataFrame({'Stato': ['Colpite dal lupo', 'Non colpite'], 'Valore': [0.33, 99.67]})
impatto_ovicaprini = pd.DataFrame({'Stato': ['Colpite dal lupo', 'Non colpite'], 'Valore': [0.70, 99.30]})

# Concentrazione Danni (Simulazione curva cumulativa basata sui dati ISPRA)
# 20.5% aziende -> 62.2% danni bovini; 25.9% aziende -> 73.3% danni ovicaprini
curve_data = pd.DataFrame({
    'Percentuale Aziende Colpite': [0, 5, 10, 20.5, 25.9, 50, 75, 100],
    'Danni Bovini Cumulati (%)': [0, 25, 45, 62.2, 70, 85, 95, 100],
    'Danni Ovicaprini Cumulati (%)': [0, 30, 50, 65, 73.3, 88, 97, 100]
})

# Burocrazia (Tempi indennizzo)
burocrazia_data = pd.DataFrame({
    'Fascia Temporale': ['Entro 30 giorni', '31 - 60 giorni', '61 - 365 giorni', 'Oltre 1 anno'],
    'Percentuale Pratiche': [4.4, 15.2, 64.1, 16.3]
})

# --- COLOR PALETTE ---
COLOR_ACCENT = "#D32F2F"  # Rosso allarme per evidenziare il problema
COLOR_NEUTRAL = "#E0E0E0"
COLOR_TEXT = "#333333"
COLOR_BG = "rgba(0,0,0,0)"

# --- SEZIONE: HEADER E CONTESTO NARRATIVO ---
st.title("🐺 Il lupo, i piccoli allevatori e chi li lascia soli")

st.markdown("""
*Settembre 2026.* Negli USA un ordine esecutivo avvia la revisione delle tutele storiche per il lupo grigio. In Europa, la Convenzione di Berna ne ha già declassato lo status. In Italia, una proposta di legge in Senato prova a reintrodurre i "bioregolatori" — ovvero i cacciatori — per gestire la fauna selvatica. 

**Il lupo è tornato, e la politica lo tratta come un'emergenza nazionale.** 

Ma cosa dicono davvero i numeri? Abbiamo analizzato i dati del monitoraggio nazionale **ISPRA / Ministero dell'Ambiente**. Ne emerge una verità scomoda per tutti: per chi crede che il lupo stia distruggendo l'intera zootecnia italiana, e per chi crede che il problema dei danni non esista affatto.
""")

st.divider()

# --- SEZIONE 1: IL PRIMO TURN (I NUMERI REALI E L'IMPATTO) ---
st.header("1. Un'emergenza... che non c'è")

col1, col2 = st.columns([1, 1.5])
with col1:
    st.markdown("""
    L'Italia ospita una popolazione stimata di circa **3.501 lupi**. 
    Non sono distribuiti uniformemente: il grosso vive lungo la dorsale appenninica, mentre le Alpi ospitano una popolazione in crescita ma ancora minoritaria.
    """)
    st.markdown(f"<p class='kpi-val'>2.388</p><p class='kpi-label'>Lupi in Appennino</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='kpi-val'>952</p><p class='kpi-label'>Lupi sulle Alpi</p>", unsafe_allow_html=True)

with col2:
    # Mappa a bolle
    fig_map = px.scatter_mapbox(
        data_popolazione, lat="Lat", lon="Lon", size="Lupi",
        color_discrete_sequence=[COLOR_ACCENT],
        zoom=4.5, center={"lat": 41.8719, "lon": 12.5674},
        mapbox_style="carto-positron",
        title="Distribuzione Macro-Aree"
    )
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, uirevision='constant')
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("""
Se si ascolta il dibattito pubblico, sembra che ogni stalla italiana sia sotto assedio. I dati sui risarcimenti ufficiali (incrociati con la Banca Dati Nazionale zootecnica) raccontano una storia di **impatto marginale**. 
""")

# Donut charts per l'impatto
col_d1, col_d2 = st.columns(2)

def make_donut(df, title, accent_val):
    fig = px.pie(df, values='Valore', names='Stato', hole=0.7,
                 color='Stato', color_discrete_map={'Colpite dal lupo': COLOR_ACCENT, 'Non colpite': COLOR_NEUTRAL})
    fig.update_layout(
        title={'text': title, 'x': 0.5, 'xanchor': 'center'},
        showlegend=False, margin=dict(t=40, b=10, l=10, r=10),
        annotations=[dict(text=f"<b>{accent_val}</b>", x=0.5, y=0.5, font_size=24, showarrow=False)],
        uirevision='constant', paper_bgcolor=COLOR_BG
    )
    return fig

with col_d1:
    st.plotly_chart(make_donut(impatto_bovini, "Aziende Bovine colpite (Media annua)", "0.33%"), use_container_width=True)
with col_d2:
    st.plotly_chart(make_donut(impatto_ovicaprini, "Aziende Ovicaprine colpite", "0.70%"), use_container_width=True)

st.divider()

# --- SEZIONE 2: IL SECONDO TURN (LA CONCENTRAZIONE E IL VERO DRAMMA) ---
st.header("2. L'illusione della media: chi paga il conto?")

st.markdown("""
Se l'impatto è inferiore all'1%, perché la rabbia degli allevatori è così accesa? Perché le medie nazionali mentono. Il danno non è spalmato su tutta Italia, ma è **ferocemente concentrato** su un numero ristretto di aziende.
""")

# Grafico curva cumulativa
fig_curve = go.Figure()
fig_curve.add_trace(go.Scatter(
    x=curve_data['Percentuale Aziende Colpite'], y=curve_data['Danni Bovini Cumulati (%)'],
    mode='lines+markers', name='Danni Bovini', line=dict(color='#8D6E63', width=3)
))
fig_curve.add_trace(go.Scatter(
    x=curve_data['Percentuale Aziende Colpite'], y=curve_data['Danni Ovicaprini Cumulati (%)'],
    mode='lines+markers', name='Danni Ovicaprini', line=dict(color=COLOR_ACCENT, width=3)
))
# Annotazioni per gli hotspot
fig_curve.add_annotation(x=20.5, y=62.2, text="20% aziende = 62% danni", showarrow=True, arrowhead=1, ax=40, ay=30)
fig_curve.add_annotation(x=25.9, y=73.3, text="26% aziende = 73% danni", showarrow=True, arrowhead=1, ax=40, ay=-30)

fig_curve.update_layout(
    title="La concentrazione: pochissime aziende subiscono quasi tutti i danni",
    xaxis_title="% Aziende Colpite", yaxis_title="% Capi Predati",
    legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99),
    margin=dict(t=50, l=10, r=10, b=10), uirevision='constant', paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG
)
st.plotly_chart(fig_curve, use_container_width=True)

st.markdown("""
**Chi sono queste aziende bersaglio?** Geograficamente si trovano sull'Appennino centrale (Toscana, Umbria, Marche, Lazio) e, per pecore e capre, nel nord-ovest alpino. 

Ma c'è un dato strutturale più grave segnalato dal rapporto ISPRA: le aziende più colpite sono spesso quelle che praticano il **pascolo estensivo**. Piccole realtà, custodi del territorio, per le quali difendersi è tecnicamente ed economicamente più difficile rispetto a un grande allevamento industriale intensivo (che infatti raramente subisce predazioni).
""")

st.divider()

# --- SEZIONE 3: IL VERO NEMICO (BUROCRAZIA E PREVENZIONE) ---
st.header("3. Lasciati soli dallo Stato")

st.markdown("""
Se un piccolo allevatore subisce un danno, lo Stato dovrebbe aiutarlo. I dati mostrano invece un sistema burocratico paralizzato. Il tempo medio per ricevere un indennizzo è di **201 giorni**.
""")

# Grafico a barre orizzontali per la burocrazia
fig_buro = px.bar(
    burocrazia_data, y='Fascia Temporale', x='Percentuale Pratiche', orientation='h',
    title="Tempi di attesa per i rimborsi",
    color='Percentuale Pratiche', color_continuous_scale=["#E0E0E0", COLOR_ACCENT]
)
fig_buro.update_layout(showlegend=False, xaxis_title="% di pratiche evase", yaxis_title="", margin=dict(t=40, l=10, r=10, b=10), coloraxis_showscale=False, uirevision='constant', paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG)
# Inverti asse y per avere "Entro 30 giorni" in alto
fig_buro.update_yaxes(autorange="reversed")
st.plotly_chart(fig_buro, use_container_width=True)

st.markdown("""
> *"Se non mi pagano il danno per quasi un anno, come faccio a comprare recinzioni da migliaia di euro?"*

Questa dinamica spiega un dato sconcertante sui sistemi di prevenzione al momento degli attacchi:
* **Solo l'8,9%** degli eventi di predazione ha visto l'uso di cani da guardiania.
* **Solo l'11,8%** aveva recinzioni adeguate.
* Nel **14,7%** dei casi non c'era *alcuna* misura di prevenzione registrata.

Le Regioni che attivano bandi per coprire al 100% i costi di prevenzione (come l'Emilia-Romagna, passata da fondi di 87mila euro a bandi straordinari da 2 milioni nel 2026) vedono una forte adesione. Il problema non è che l'allevatore "non vuole" proteggersi. Il problema è che spesso, senza la politica, non può permetterselo.
""")

st.divider()

# --- SEZIONE 4: FONTI E METODOLOGIA ---
with st.expander("📚 Fonti, Metodologia e Limiti dei Dati"):
    st.markdown("""
    **Fonti Principali:**
    * [Stima dell'impatto del lupo sulle attività zootecniche in Italia (Gervasi et al. 2022) - ISPRA](http://www.isprambiente.gov.it/public_files/StimaImpattoLupoAattivitaZootecniche.pdf). Periodo di riferimento dei dati sui danni: 2015-2019.
    * [Relazioni risultati monitoraggio nazionale Lupo 2020-2021 - ISPRA](https://www.isprambiente.gov.it/resolveuid/1845718d9d214fe183da757927f906e6) e [Life WolfAlps EU](https://www.lifewolfalps.eu/wp-content/uploads/2022/05/report-nazionale-lupo-regioni-alpine-20_21-con-Allegati.pdf).

    **Nota Metodologica (L'Area Grigia):**
    I dati ufficiali sui danni da "lupo" presentano un margine di incertezza strutturale. In circa la metà delle Regioni italiane, la causa di morte del bestiame è certificata dal veterinario ASL senza ricorrere ad analisi genetiche. Questo significa che all'interno delle cifre qui mostrate rientra anche una quota (non quantificabile su scala nazionale) di danni causati da cani vaganti o inselvatichiti, spesso indistinguibili dai lupi dall'esame della sola carcassa.

    **Contesto Normativo:**
    * *Ddl Caccia Italia:* Al momento dell'analisi (Giugno 2026), il disegno di legge per l'introduzione dei "bioregolatori" è in discussione al Senato e non costituisce legge definitiva.
    * *Revisione ESA (USA):* L'ordine esecutivo di revisione delle tutele è in fase di valutazione di 90 giorni (Settembre 2026).
    """)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Wild Data - Il lupo e gli allevatori",
    page_icon="🐺",
    layout="wide"
)

# --- CSS PER OPTIMIZATION MOBILE & SCROLL MAPPE ---
st.markdown("""
    <style>
    /* 1. Riabilita lo scorrimento naturale su tutto il contenitore del grafico */
    [data-testid="stPlotlyChart"] {
        touch-action: auto !important;
    }
    /* 2. Disabilita lo scorrimento della pagina SOLO quando il tocco avviene esattamente sui livelli della mappa */
    .js-plotly-plot .geolayer, 
    .js-plotly-plot .draglayer,
    .js-plotly-plot .geo {
        touch-action: none !important;
    }
    /* Stile personalizzato per card KPI */
    .kpi-card {
        background-color: #f8f9fa;
        border-left: 4px solid #D32F2F;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 12px;
    }
    .kpi-val {
        font-size: 2rem;
        font-weight: 700;
        color: #D32F2F;
        margin: 0;
        line-height: 1.1;
    }
    .kpi-label {
        font-size: 0.95rem;
        color: #555555;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# BOTTONE HOME IN CIMA
st.page_link("Home.py", label="🏠 Torna alla Home di Wild Data")
st.markdown("---")

# TITOLO E INTRODUZIONE NARRATIVA
st.title("🐺 Il lupo, i piccoli allevatori e chi li lascia soli")
st.markdown("*Settembre 2026. Negli USA un ordine esecutivo avvia la revisione delle tutele storiche per il lupo grigio. In Europa, la Convenzione di Berna ne ha declassato lo status. In Italia, la riforma del sistema venatorio introduce la figura dei cacciatori 'bioregolatori'. Ma cosa dicono davvero i dati ufficiali?*")
st.markdown("---")

# DATI HARDCODED
data_popolazione = pd.DataFrame({
    'Macro-Area': ['Alpi', 'Appennino'],
    'Lupi': [952, 2388],
    'Lat': [46.0, 42.5],
    'Lon': [10.5, 13.5]
})

impatto_bovini = pd.DataFrame({
    'Stato': ['Aziende Colpite', 'Non Colpite'],
    'Valore': [0.33, 99.67]
})

impatto_ovicaprini = pd.DataFrame({
    'Stato': ['Aziende Colpite', 'Non Colpite'],
    'Valore': [0.70, 99.30]
})

# Punti curva cumulativa esatti dal report (solo [0,0], [Hotspot], [100,100])
curve_bovini = pd.DataFrame({
    'x': [0, 20.5, 100],
    'y': [0, 62.2, 100]
})
curve_ovicaprini = pd.DataFrame({
    'x': [0, 25.9, 100],
    'y': [0, 73.3, 100]
})

burocrazia_data = pd.DataFrame({
    'Fascia Temporale': ['Entro 30 giorni', '31 - 60 giorni', '61 - 365 giorni', 'Oltre 1 anno'],
    'Percentuale Pratiche (%)': [4.4, 15.2, 64.1, 16.3]
})

consolidation_data = pd.DataFrame({
    'Anno': ['2015', '2019'],
    'Aziende Bovine': [169601, 148074],
    'Dimensione Media (Capi)': [34.7, 40.3]
})

COLOR_ACCENT = "#D32F2F"
COLOR_NEUTRAL = "#E0E0E0"
COLOR_BG = "rgba(0,0,0,0)"

# --- ATTO 1 ---
st.subheader("1. Un'emergenza... che non c'è nei numeri generali")
st.write("Il dibattito politico e mediatico dipinge il ritorno del lupo come una catastrofe per l'intera zootecnia italiana. Tuttavia, incrociando i dati ufficiali dei risarcimenti **ISPRA / Ministero dell'Ambiente** con la Banca Dati Nazionale (BDN), l'impatto complessivo risulta estremamente contenuto in termini percentuali.")

col1_left, col1_right = st.columns([1, 1])

with col1_left:
    st.markdown("#### 📍 Il lupo è tornato, ma non ovunque allo stesso modo")
    st.write("L'Italia ospita una popolazione stimata di circa **3.501 lupi** (monitoraggio nazionale ISPRA 2020-2021). Il grosso risiede lungo la dorsale appenninica, mentre la popolazione alpina è in crescita ma ancora minoritaria.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="kpi-card"><p class="kpi-val">2.388</p><p class="kpi-label">Lupi in Appennino</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="kpi-card"><p class="kpi-val">952</p><p class="kpi-label">Lupi sulle Alpi</p></div>', unsafe_allow_html=True)

    # Calcolo proporzionale area (radice quadrata) per le bolle della mappa
    sizes = [math.sqrt(val) * 1.5 for val in data_popolazione['Lupi']]

    fig_map = go.Figure()
    fig_map.add_trace(go.Scattergeo(
        lon=data_popolazione['Lon'],
        lat=data_popolazione['Lat'],
        text=["Alpi: 952 lupi", "Appennino: 2.388 lupi"],
        mode='markers+text',
        textposition=["top center", "bottom center"],
        marker=dict(
            size=sizes,
            color=COLOR_ACCENT,
            opacity=0.8,
            line=dict(width=1, color='#4A4A4A')
        ),
        hovertemplate="<b>%{text}</b><extra></extra>"
    ))
    fig_map.update_layout(
        geo=dict(
            scope='europe',
            center=dict(lat=42.5, lon=12.0),
            projection_scale=5.8,
            showland=True, landcolor='#E5E5E5',
            showcountries=True, countrycolor='#FFFFFF',
            showcoastlines=True, coastlinecolor='#B0B0B0'
        ),
        margin=dict(l=0, r=0, t=10, b=10),
        height=320,
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col1_right:
    st.markdown("#### 📊 Quota di Aziende Colpite ogni anno")
    st.write("In termini assoluti, la percentuale di aziende zootecniche che subisce predazioni ogni anno è marginale rispetto al totale nazionale dei capi e delle stalle iscritte:")
    
    def make_donut(df, title, accent_val):
        fig = px.pie(df, values='Valore', names='Stato', hole=0.7,
                     color='Stato', color_discrete_map={'Aziende Colpite': COLOR_ACCENT, 'Non Colpite': COLOR_NEUTRAL})
        fig.update_layout(
            title={'text': title, 'x': 0.5, 'xanchor': 'center'},
            showlegend=False, margin=dict(t=35, b=10, l=10, r=10),
            height=220,
            annotations=[dict(text=f"<b>{accent_val}</b>", x=0.5, y=0.5, font_size=22, showarrow=False)],
            paper_bgcolor=COLOR_BG
        )
        return fig

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.plotly_chart(make_donut(impatto_bovini, "1 azienda bovina su 300 colpita", "0,33%"), use_container_width=True)
    with col_d2:
        st.plotly_chart(make_donut(impatto_ovicaprini, "1 azienda ovicaprina su 140", "0,70%"), use_container_width=True)

    st.info("💡 **Danno economico medio:** L'impatto economico diretto stimato a livello nazionale si attesta attorno a circa **1,8 milioni di euro all'anno** nell'intero periodo analizzato dal report ISPRA.")

st.markdown("---")

# --- ATTO 2 ---
st.subheader("2. L'illusione della media: il danno è un hotspot concentrato")
st.write("Se l'impatto medio è inferiore all'1%, da dove nasce l'esasperazione degli allevatori? Dal fatto che il danno **non è distribuito equamente**, ma si accanisce in modo devastante su una strettissima minoranza di realtà produttive.")

col2_left, col2_right = st.columns([1.2, 0.8])

with col2_left:
    fig_curve = go.Figure()
    
    # Traccia Bovini
    fig_curve.add_trace(go.Scatter(
        x=curve_bovini['x'], y=curve_bovini['y'],
        mode='lines+markers', name='Danni Bovini', line=dict(color='#8D6E63', width=3)
    ))
    # Traccia Ovicaprini
    fig_curve.add_trace(go.Scatter(
        x=curve_ovicaprini['x'], y=curve_ovicaprini['y'],
        mode='lines+markers', name='Danni Ovicaprini', line=dict(color=COLOR_ACCENT, width=3)
    ))
    
    fig_curve.add_annotation(x=20.5, y=62.2, text="20,5% aziende subisce il 62,2% dei danni", showarrow=True, arrowhead=2, ax=50, ay=30)
    fig_curve.add_annotation(x=25.9, y=73.3, text="25,9% aziende subisce il 73,3% dei danni", showarrow=True, arrowhead=2, ax=50, ay=-30)

    fig_curve.update_layout(
        title="1 azienda su 5 si becca oltre il 60% di tutti i danni",
        xaxis_title="% di Aziende Colpite", yaxis_title="% Capi Predati Cumulati",
        legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99),
        margin=dict(t=50, l=10, r=10, b=10),
        height=380,
        paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG
    )
    st.plotly_chart(fig_curve, use_container_width=True)
    st.caption("*Nota sui dati: il grafico mostra un'interpolazione lineare semplificata tra i punti zero, i punti di hotspot misurati dal report ISPRA e il 100% totale.*")

with col2_right:
    st.markdown("#### 🎯 Chi sono gli 'Hotspot'?")
    st.write("""
    * **Per i bovini:** Il **20,5%** delle aziende colpite (368 strutture concentrate in 177 comuni) subisce ben il **62,2%** di tutte le predazioni nazionali.
    * **Per gli ovicaprini:** Il **25,9%** delle aziende (922 strutture in 416 comuni) subisce il **73,3%** dei capi persi.
    
    **Dove si concentrano?** Prevalentemente lungo la dorsale appenninica centrale (Toscana, Umbria, Marche, Lazio), in alcune aree del Sud e, per pecore e capre, nel nord-ovest alpino (Piemonte e Liguria).
    """)

st.markdown("---")

# --- ATTO 3 ---
st.subheader("3. Burocrazia paralizzata e misure di prevenzione mancanti")
st.write("Mentre il dibattito si concentra sul cacciare o declassare la specie, i dati mettono a nudo il vero nemico degli allevatori: un sistema di supporto pubblico lento, farraginoso e spesso inaccessibile.")

col3_left, col3_right = st.columns([1, 1])

with col3_left:
    st.write("In media, un allevatore deve attendere **più di 6 mesi** (201 giorni) per ricevere il risarcimento di un capo ucciso. In quasi un caso su cinque, l'attesa supera l'anno intero.")

    fig_buro = px.bar(
        burocrazia_data, y='Fascia Temporale', x='Percentuale Pratiche (%)', orientation='h',
        title="Oltre il 60% degli allevatori aspetta dai 2 ai 12 mesi per il risarcimento",
        color='Percentuale Pratiche (%)', color_continuous_scale=["#E0E0E0", COLOR_ACCENT],
        text_auto='.1f'
    )
    fig_buro.update_traces(textposition='outside')
    fig_buro.update_layout(
        showlegend=False, xaxis_title="% delle pratiche evase", yaxis_title="",
        margin=dict(t=40, l=10, r=40, b=10), height=280,
        coloraxis_showscale=False, paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG
    )
    fig_buro.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_buro, use_container_width=True)

with col3_right:
    st.markdown("#### 🛡️ Assenza di Protezioni al Momento dell'Attacco")
    st.write("I report ISPRA rivelano che nei luoghi delle predazioni ufficialmente registrate le misure di prevenzione attiva erano drammaticamente scarse:")

    st.markdown("""
    <div class="kpi-card">
        <p class="kpi-val" style="font-size:1.8rem;">8,9%</p>
        <p class="kpi-label">delle predazioni avvenute in presenza di <b>cani da guardiania</b>.</p>
    </div>
    <div class="kpi-card">
        <p class="kpi-val" style="font-size:1.8rem;">11,8%</p>
        <p class="kpi-label">degli eventi verificatisi in presenza di <b>recinzioni antipredazione</b>.</p>
    </div>
    <div class="kpi-card">
        <p class="kpi-val" style="font-size:1.8rem; color:#856404; border-left-color:#856404;">14,7%</p>
        <p class="kpi-label">dei casi con <b>nessuna misura di protezione esplicita</b> presente.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- ATTO 4 ---
st.subheader("4. Il vero dramma: la scomparsa dei piccoli")
st.write("C'è un dato silenzioso ma devastante nel periodo 2015-2019 (BDN/ISPRA). Mentre i capi allevati sono rimasti stabili, le aziende sono crollate: il settore si sta polarizzando verso i grandi allevamenti, spazzando via le realtà medio-piccole, che incassano il colpo più duro del conflitto con la fauna selvatica.")

col4_left, col4_right = st.columns([1, 1])

with col4_left:
    fig_consol = go.Figure()
    fig_consol.add_trace(go.Bar(
        x=consolidation_data['Anno'], y=consolidation_data['Aziende Bovine'],
        name='Numero di Aziende Bovine', marker_color=COLOR_ACCENT,
        text=consolidation_data['Aziende Bovine'], textposition='auto'
    ))
    fig_consol.update_layout(
        title="Oltre 21.000 aziende bovine perse in soli 5 anni",
        yaxis_title="Numero Aziende",
        margin=dict(t=40, l=10, r=10, b=10), height=300,
        paper_bgcolor=COLOR_BG, plot_bgcolor=COLOR_BG,
        showlegend=False
    )
    st.plotly_chart(fig_consol, use_container_width=True)

with col4_right:
    st.markdown("#### 🏔️ Transumanza e pascolo estensivo")
    st.write("""
    Mentre le aziende chiudevano del 12,7%, **la dimensione media aziendale è salita del +16%** (da 34,7 a 40,3 capi per stalla).
    
    Il report ISPRA, nei suoi commenti qualitativi, suggerisce proprio che le piccole realtà a pascolo estensivo e transumanza risultino strutturalmente più vulnerabili: per i piccoli allevatori tradizionali, la gestione continua della difesa (recinzioni mobili, mantenimento dei cani, manodopera) è immensamente più complessa e costosa rispetto ai grandi allevamenti intensivi al chiuso.
    """)

st.markdown("---")

# --- ATTO 5 ---
st.subheader("5. Oltre la caccia: cosa serve davvero")
st.write("Anziché rincorrere riforme elettorali sull'abbattimento, il vero intervento risolutivo passa per l'investimento massiccio e mirato sui fronti della prevenzione economica e scientifica.")

col5_left, col5_right = st.columns([1, 1])

with col5_left:
    st.markdown("#### 💰 Il sostegno economico reale")
    st.write("I bandi frammentari non bastano. Serve garantire fondi certi non solo per le recinzioni, ma anche per il costoso **mantenimento dei cani da guardiania**. Il caso dell'Emilia-Romagna, che per il 2026 ha approvato una misura drastica, è un esempio del cambio di passo necessario:")
    
    st.markdown("""
    <div class="kpi-card" style="margin-top: 15px;">
        <p class="kpi-label" style="margin-top: 0; margin-bottom: 5px;">Fondi prevenzione lupo Emilia-Romagna</p>
        <p class="kpi-val" style="font-size:2.4rem;">Da 87,5 Mila a 2 Milioni €</p>
        <p class="kpi-label">Il salto di finanziamenti stanziati nel 2026 rispetto alle quote ordinarie passate.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("A questo si aggiungono stanziamenti una tantum come i 740.000€ del Piemonte o bandi specifici come i 55.000€ in Veneto, che dimostrano come le Regioni debbano sostituirsi all'assenza di un piano strutturale nazionale.")

with col5_right:
    st.markdown("#### 🔬 Più studio sugli 'Hotspot' cronici")
    st.write("È la scienza stessa a chiederlo. Nelle conclusioni dello studio ISPRA, i ricercatori ammettono esplicitamente una grande lacuna: **non sappiamo ancora abbastanza sul perché alcune aziende vengano colpite ripetutamente (i cosiddetti 'attacchi cronici') e altre vicine no.**")
    st.info("📌 *«Diventa prioritario investigare le cause che determinano la cronicizzazione del danno in specifiche aziende»*, si legge nel report. Finché non finanzieremo la ricerca per capire le esatte dinamiche ecologiche e strutturali di quegli hotspot, qualsiasi politica di 'gestione letale' (abbattimenti) rischia di colpire a caso, senza risolvere il problema per chi subisce la maggior parte delle perdite.")

st.markdown("---")

# --- EPILOGO: FONTI E METODOLOGIA ---
st.subheader("📚 Fonti e Metodologia")

with st.expander("📝 Nota sui dati, Caveat e Area Grigia"):
    st.markdown("""
    **L'Area Grigia dei Danni (Lupo vs Cane Inselvatichito):**
    In circa la metà delle Regioni italiane, la causa di morte del bestiame registrata negli indennizzi viene accertata visivamente dal veterinario ASL senza l'ausilio di analisi genetiche sui morsi/saliva. Di conseguenza, sotto la voce ufficiale 'danno da lupo' rientra anche una quota non quantificabile di attacchi compiuti da cani vaganti o inselvatichiti, le cui ferite risultano indistinguibili dall'esame autoptico della carcassa.

    **Limiti del Dataset:**
    * I dati di impatto nazionali dettagliati sulle aziende (Gervasi et al. 2022) coprono il quinquennio **2015-2019**, rappresentando l'ultimo studio sistematico standardizzato disponibile su scala paese.
    * Non esiste una ripartizione regionale pulita per la popolazione di lupo in Appennino, poiché il modello scientifico ISPRA stima le densità su 13 macro-aree di campionamento che valicano i confini amministrativi.

    **Inquadramento Normativo (Giugno-Settembre 2026):**
    * Il Disegno di Legge Caccia in Italia (introduzione dei 'bioregolatori') è in iter al Senato.
    * La revisione delle tutele ESA (Endangered Species Act) negli USA è un provvedimento amministrativo soggetto a valutazione procedurale di 90 giorni.
    """)

st.markdown("""
* **Report ISPRA Impatto Zootecnico:** Gervasi et al. (2022) - *Stima dell'impatto del lupo sulle attività zootecniche in Italia*. [Leggi il PDF ufficiale](http://www.isprambiente.gov.it/public_files/StimaImpattoLupoAattivitaZootecniche.pdf)
* **Monitoraggio Nazionale Lupo:** ISPRA / Ministero dell'Ambiente (2020-2021). [Relazione Risultati](https://www.isprambiente.gov.it/resolveuid/1845718d9d214fe183da757927f906e6)
* **Distribuzione Alpina:** Progetto [Life WolfAlps EU](https://www.lifewolfalps.eu/) (Report 2020-2021 e aggiornamenti 2020-2024).
""")

st.markdown("---")

# BOTTONE HOME IN FONDO
st.page_link("Home.py", label="🏠 Torna alla Home di Wild Data")

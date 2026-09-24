import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Wild Data - Il lupo e gli allevatori",
    page_icon="🐺",
    layout="wide",
)

# --- CSS PER OPTIMIZATION MOBILE & SCROLL MAPPE E COMPONENTI CUSTOM ---
st.markdown(
    """
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
    /* Stili personalizzati per KPI e Pittogrammi */
    .kpi-card {
        background-color: #f8f9fa;
        border-left: 4px solid #D32F2F;
        padding: 16px 20px;
        border-radius: 4px;
        margin-bottom: 16px;
    }
    .kpi-card-neutral {
        border-left: 4px solid #888888;
    }
    .kpi-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #D32F2F;
        margin: 0;
        line-height: 1.1;
    }
    .kpi-val-neutral {
        color: #555555;
    }
    .kpi-label {
        font-size: 1rem;
        color: #555555;
        margin-top: 8px;
        line-height: 1.4;
    }
    .pictogram-container {
        display: flex;
        justify-content: space-around;
        align-items: flex-end;
        background: #f8f9fa;
        padding: 30px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
    }
    .picto-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
    }
    .picto-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
    }
    .picto-sub {
        font-size: 0.9rem;
        color: #666;
    }
    .ethical-callout {
        background-color: #fff3cd;
        border-left: 5px solid #f1c40f;
        padding: 18px 24px;
        border-radius: 4px;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
        margin-bottom: 25px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# BOTTONE HOME IN CIMA
st.page_link("Home.py", label="🏠 Torna alla Home di Wild Data")
st.markdown("---")

# TITOLO E INTRODUZIONE NARRATIVA
st.title("🐺 Il lupo, i piccoli allevatori e chi li lascia soli")
st.markdown(
    "*Settembre 2026. Negli USA un ordine esecutivo avvia la revisione delle"
    " tutele storiche per il lupo grigio. In Europa, la Convenzione di Berna ne"
    " ha declassato lo status. In Italia, la riforma del sistema venatorio"
    " introduce la figura dei cacciatori 'bioregolatori'. Ma cosa dicono davvero"
    " i dati ufficiali?*"
)
st.markdown("---")

# DATI HARDCODED
data_popolazione = pd.DataFrame({
    "Macro-Area": ["Alpi", "Appennino"],
    "Lupi": [952, 2388],
    "Lat": [46.0, 42.5],
    "Lon": [10.5, 13.5],
})

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
st.subheader("1. Un'emergenza... che non c'è nei numeri generali")
st.write(
    "Il dibattito politico e mediatico racconta spesso il ritorno del lupo come"
    " un'emergenza fuori controllo per l'intera zootecnia italiana. Tuttavia,"
    " incrociando i dati ufficiali dei risarcimenti **ISPRA / Ministero"
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

  st.markdown(
      """
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
    """,
      unsafe_allow_html=True,
  )

  st.markdown("#### 🌪️ Il vero peso sui bilanci: il clima")
  st.write(
      "Per dare una proporzione reale all'allarme economico: i danni diretti"
      " da predazione valgono circa **1,8 milioni di euro all'anno** a livello"
      " nazionale (report ISPRA). Nello stesso momento (estate 2026),"
      " Coldiretti ha stimato in **oltre 3 miliardi di euro** i danni subiti da"
      " agricoltura e zootecnia a causa di siccità e caldo estremo, con crolli"
      " nella produzione di foraggi e latte. Un conto che sale a 20 miliardi in"
      " quattro anni. Un rischio strutturale ben diverso."
  )

with col1_right:
  st.markdown("#### 📊 Quota di Aziende Colpite ogni anno")
  st.write(
      "In termini assoluti, la percentuale di aziende zootecniche che subisce"
      " predazioni ogni anno è marginale rispetto al totale nazionale dei capi"
      " e delle stalle iscritte:"
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
        dragmode=False,  # Disattiva interazioni fastidiose su mobile
        annotations=[
            dict(
                text=f"<b>{accent_val}</b>",
                x=0.5,
                y=0.5,
                font_size=22,
                showarrow=False,
            )
        ],
        paper_bgcolor=COLOR_BG,
    )
    return fig

  col_d1, col_d2 = st.columns(2)
  with col_d1:
    st.plotly_chart(
        make_donut(impatto_bovini, "1 azienda bovina su 300 colpita", "0,33%"),
        use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": False},
    )
  with col_d2:
    st.plotly_chart(
        make_donut(
            impatto_ovicaprini, "1 azienda ovicaprina su 140", "0,70%"
        ),
        use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": False},
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
st.subheader("2. L'illusione della media: il danno è un hotspot concentrato")
st.write(
    "Se l'impatto medio è inferiore all'1%, da dove nasce l'esasperazione degli"
    " allevatori? Dal fatto che il danno **non è distribuito equamente**, ma si"
    " accanisce in modo devastante su una strettissima minoranza di realtà"
    " produttive."
)

col2_left, col2_right = st.columns([1, 1])

with col2_left:
  st.markdown("#### 📍 Il lupo è tornato, ma non ovunque allo stesso modo")
  # Calcolo proporzionale area (radice quadrata) per le bolle della mappa
  sizes = [math.sqrt(val) * 1.5 for val in data_popolazione["Lupi"]]

  fig_map = go.Figure()
  fig_map.add_trace(
      go.Scattergeo(
          lon=data_popolazione["Lon"],
          lat=data_popolazione["Lat"],
          text=["Alpi: 952 lupi", "Appennino: 2.388 lupi"],
          mode="markers+text",
          textposition=["top center", "bottom center"],
          marker=dict(
              size=sizes,
              color=COLOR_ACCENT,
              opacity=0.8,
              line=dict(width=1, color="#4A4A4A"),
          ),
          hovertemplate="<b>%{text}</b><extra></extra>",
      )
  )
  fig_map.update_layout(
      geo=dict(
          scope="europe",
          center=dict(lat=42.5, lon=12.0),
          projection_scale=5.8,
          showland=True,
          landcolor="#E5E5E5",
          showcountries=True,
          countrycolor="#FFFFFF",
          showcoastlines=True,
          coastlinecolor="#B0B0B0",
      ),
      margin=dict(l=0, r=0, t=10, b=10),
      height=320,
      paper_bgcolor=COLOR_BG,
      plot_bgcolor=COLOR_BG,
      # Mappa resa nuovamente interattiva (rimosso dragmode=False)
  )
  # Rimosse le restrizioni di config per ripristinare l'interattività piena della mappa
  st.plotly_chart(fig_map, use_container_width=True)

  st.write(
      "Gli hotspot dei danni si concentrano lungo la dorsale appenninica"
      " centrale, in alcune aree del Sud e, per le pecore, nel nord-ovest"
      " alpino. Questa mappa del conflitto non è una 'scelta' del lupo: è la"
      " semplice **sovrapposizione geografica** tra le aree ad alta densità di"
      " lupi e le zone in cui si concentra la maggior parte degli allevamenti a"
      " pascolo estensivo in Italia."
  )

with col2_right:
  st.markdown("#### 🎯 1 azienda su 5 subisce oltre il 60% dei danni")

  html_pictogram = """
    <div class="pictogram-container">
        <div class="picto-col">
            <div class="picto-label" style="color: #D32F2F;">Gli "Hotspot"</div>
            <div style="height: 120px; display: flex; align-items: flex-end;">
                <svg width="45" height="45" viewBox="0 0 24 24"><path fill="#888" d="M12 2L2 12h3v8h14v-8h3L12 2zm0 2.8L17.2 10H6.8L12 4.8z"/></svg>
            </div>
            <div class="picto-label">20,5%</div>
            <div class="picto-sub">delle aziende colpite</div>
            
            <div style="height: 120px; display: flex; align-items: flex-end; margin-top: 20px;">
                <svg width="79" height="79" viewBox="0 0 24 24"><path fill="#D32F2F" d="M12 2L1 21h22L12 2zm0 3.8l7.5 13.2H4.5L12 5.8zM11 10v4h2v-4h-2zm0 6v2h2v-2h-2z"/></svg>
            </div>
            <div class="picto-label" style="color: #D32F2F;">62,2%</div>
            <div class="picto-sub">dei bovini predati totali</div>
        </div>
        
        <div class="picto-col">
            <div class="picto-label" style="color: #666;">Tutte le altre</div>
            <div style="height: 120px; display: flex; align-items: flex-end;">
                <svg width="89" height="89" viewBox="0 0 24 24"><path fill="#888" d="M12 2L2 12h3v8h14v-8h3L12 2zm0 2.8L17.2 10H6.8L12 4.8z"/></svg>
            </div>
            <div class="picto-label">79,5%</div>
            <div class="picto-sub">delle aziende colpite</div>
            
            <div style="height: 120px; display: flex; align-items: flex-end; margin-top: 20px;">
                <svg width="61" height="61" viewBox="0 0 24 24"><path fill="#D32F2F" d="M12 2L1 21h22L12 2zm0 3.8l7.5 13.2H4.5L12 5.8zM11 10v4h2v-4h-2zm0 6v2h2v-2h-2z"/></svg>
            </div>
            <div class="picto-label" style="color: #D32F2F;">37,8%</div>
            <div class="picto-sub">dei bovini predati totali</div>
        </div>
    </div>
    """
  st.markdown(html_pictogram, unsafe_allow_html=True)
  st.caption(
      "*Dati di concentrazione del danno per la filiera bovina. Il rapporto è"
      " ancora più estremo per il settore ovicaprino (il 25,9% delle stalle"
      " subisce il 73,3% dei danni).*"
  )

st.markdown("---")

# --- ATTO 3 ---
st.subheader("3. Burocrazia paralizzata e fondi di prevenzione insufficienti")
st.write(
    "Mentre il dibattito si concentra sul cacciare o declassare la specie, i"
    " dati mettono a nudo il vero problema odierno: un sistema di supporto"
    " pubblico lento, farraginoso e spesso inaccessibile, sia per i rimborsi"
    " che per l'acquisto di difese."
)

col3_left, col3_right = st.columns([1, 1])

with col3_left:
  st.markdown("#### ⏳ Tempi di indennizzo estenuanti")
  st.markdown(
      """
    <div class="kpi-card">
        <p class="kpi-val" style="font-size:3rem;">80,4%</p>
        <p class="kpi-label" style="font-size:1.1rem;">Degli allevatori colpiti aspetta <b>da 2 a oltre 12 mesi</b> per ricevere l'indennizzo di un capo ucciso.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )
  st.write(
      "In media, l'attesa burocratica è di **201 giorni**. Un tempo infinito"
      " per una piccola azienda che nel frattempo ha perso capitale produttivo"
      " e continua a sostenere le spese vive quotidiane."
  )

with col3_right:
  st.markdown("#### 🛡️ L'emergenza della raccolta dati sulle difese")
  st.write(
      "Come siamo messi a prevenzione sul campo? Analizzando i report"
      " ufficiali nei luoghi degli attacchi accertati, emerge un quadro"
      " disarmante non solo sulla mancanza di difese, ma sulla stessa"
      " capacità delle Regioni di tracciarle:"
  )

  st.markdown(
      """
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
        <p class="kpi-label" style="margin-top:2px;"><b>Dato mancante.</b> In 10.409 eventi di predazione le autorità non hanno semplicemente registrato l'informazione.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # Integrazione del collegamento sui fondi ordinari esigui
  st.write(
      "E quando le Regioni stanziano fondi per finanziare cani e recinzioni, gli"
      " importi ordinari sono storicamente esigui — un problema che"
      " affronteremo più avanti."
  )

st.markdown("---")

# --- ATTO 4 ---
st.subheader("4. Il vero dramma: una morsa insostenibile sui piccoli")
st.write(
    "Tutti questi numeri assumono il loro peso reale se inseriti nel contesto di"
    " mercato. Chi subisce più danni da lupo (spesso piccoli allevatori a"
    " pascolo estensivo e transumanza in zone montane) deve **anche** affrontare"
    " la concorrenza di aziende che diventano sempre più grandi, abbassando i"
    " prezzi."
)
st.write(
    "La spesa per difendersi dal predatore (recinzioni, mantenimento cani,"
    " manodopera) non è una voce di costo isolata, ma un peso che affonda"
    " bilanci già erosi dalle logiche dell'allevamento intensivo. È un cerchio"
    " che si stringe sulle piccole realtà."
)

st.markdown(
    """
<div class="kpi-card" style="text-align: center; padding: 30px;">
    <p class="kpi-val" style="font-size:3.5rem;">-21.527</p>
    <p class="kpi-label" style="font-size:1.3rem;"><b>Aziende bovine scomparse in soli 5 anni (2015-2019)</b></p>
    <p class="kpi-label" style="max-width: 700px; margin: 15px auto 0;">I dati BDN citati da ISPRA mostrano che, mentre le stalle sono crollate del 12,7% (da 169.601 a 148.074), il numero di capi nazionali è rimasto stabile. La dimensione media aziendale è salita del +16%: <b>il settore si consolida accentrandosi nelle mani dei grandi allevamenti al chiuso, spazzando via le realtà medio-piccole più esposte sul territorio.</b></p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# --- ATTO 5 ---
st.subheader("5. Oltre la caccia: cosa serve davvero")

# Presa di posizione etica esplicita
st.markdown(
    """
<div class="ethical-callout">
    <b>Prima ancora dei numeri, per noi vale un principio semplice:</b> il lupo è una specie protetta e ha lo stesso diritto di esistere nel nostro ecosistema. Sterminarlo perché è la scorciatoia più comoda, invece di affrontare le vere cause del conflitto, non è una soluzione — è solo il modo più rapido per evitare di risolvere il problema.
</div>
""",
    unsafe_allow_html=True,
)

st.write(
    "Abbattere i lupi non risolve la natura strutturale del problema, che come"
    " abbiamo visto è iper-concentrato su poche realtà (gli hotspot) spesso"
    " prive di supporti efficaci. Le soluzioni passano piuttosto per un"
    " radicale cambio di passo nei finanziamenti e nello studio del fenomeno."
)

col5_left, col5_right = st.columns([1, 1])

with col5_left:
  st.markdown("#### 💰 Il sostegno economico reale")
  st.write(
      "I bandi frammentari non bastano. Serve garantire fondi certi non solo"
      " per le recinzioni, ma per coprire stabilmente i costosi **mantenimenti"
      " dei cani da guardiania** e il lavoro extra degli allevatori. Il caso"
      " dell'Emilia-Romagna traccia un modello per il futuro:"
  )

  st.markdown(
      """
    <div class="kpi-card" style="margin-top: 15px;">
        <p class="kpi-label" style="margin-top: 0; margin-bottom: 5px;">Fondi prevenzione lupo Emilia-Romagna</p>
        <p class="kpi-val" style="font-size:2.4rem;">Da 87,5 Mila a 2 Milioni €</p>
        <p class="kpi-label">Il salto straordinario di finanziamenti stanziati nel 2026 rispetto alle limitate quote ordinarie passate.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with col5_right:
  st.markdown("#### 🔬 Studiare gli 'Hotspot' (e raccogliere i dati)")
  st.write(
      "Non si può gestire ciò che non si conosce. Quel buco nero del"
      " **58,1%** di attacchi senza dati sulle recinzioni è l'esempio plastico"
      " di come le istituzioni debbano investire prima di tutto nel capire cosa"
      " succede sul campo."
  )
  st.write(
      "Nelle sue conclusioni, l'ISPRA ammette esplicitamente la necessità di"
      " fare luce su queste dinamiche:"
  )

  # Citazione testuale verbatim ripristinata dal report Gervasi et al. 2022
  st.info(
      "📌 *«è importante individuare le caratteristiche delle aziende definite"
      " 'croniche' per poter elaborare interventi specifici che permettano di"
      " diminuire significativamente le perdite»*, si legge nel report ISPRA"
      " (Gervasi et al. 2022). Finché non finanzieremo la ricerca ecologica su"
      " questi hotspot circoscritti, qualsiasi politica di abbattimento sparerà"
      " letteralmente nel mucchio, senza difendere i pochi pastori che portano"
      " il vero peso economico della biodiversità."
  )

st.markdown("---")

# --- EPILOGO: FONTI E METODOLOGIA ---
st.subheader("📚 Fonti e Metodologia")

with st.expander("📝 Nota sui dati, Caveat e Dataset"):
  st.markdown("""
    **Limiti del Dataset ISPRA:**
    * I dati di impatto nazionali dettagliati sulle aziende (Gervasi et al. 2022) coprono il quinquennio **2015-2019**, rappresentando l'ultimo studio sistematico standardizzato disponibile su scala paese, basato sull'incrocio tra rimborsi regionali e Banca Dati Nazionale (BDN).
    * Non esiste una ripartizione regionale pulita per la popolazione di lupo in Appennino, poiché il modello scientifico ISPRA stima le densità su 13 macro-aree di campionamento che valicani i confini amministrativi.

    **Inquadramento Normativo (2026):**
    * Il Disegno di Legge Caccia in Italia (introduzione dei 'bioregolatori') è in iter al Senato.
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

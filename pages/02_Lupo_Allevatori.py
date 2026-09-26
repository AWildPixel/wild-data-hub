import math
import textwrap
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Funzione helper per impedire a Markdown di creare blocchi di codice
def clean_html(html_str: str) -> str:
    return textwrap.dedent(html_str).strip()

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Wild Data - Tutta colpa del lupo (?)",
    page_icon="🐺",
    layout="wide",
)

# --- CSS PER COMPONENTI CUSTOM ---
st.markdown(
    clean_html("""
    <style>
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
    </style>
    """),
    unsafe_allow_html=True,
)

# BOTTONE HOME IN CIMA
st.page_link("Home.py", label="🏠 Torna alla Home di Wild Data")
st.markdown("---")

# TITOLO E INTRODUZIONE NARRATIVA
st.title("🐺 Tutta colpa del lupo (?)")
st.markdown(
    "*Dagli Stati Uniti all'Europa, si diffonde ancora una volta l'idea che l'unico modo per proteggere gli allevatori sia cacciare il lupo. A parte l'aspetto etico (potete immaginare la mia opinione al riguardo), i dati ci raccontano in realtà una storia più complicata — e la soluzione non è così semplice...*"
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

    st.markdown(
        clean_html("""
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
        """),
        unsafe_allow_html=True,
    )

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

with col1_right:
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
            make_donut(impatto_bovini, "1 azienda bovina su 300 colpita ogni anno", "0,33%"),
            use_container_width=True,
            config={"displayModeBar": False, "scrollZoom": False},
        )
    with col_d2:
        st.plotly_chart(
            make_donut(impatto_ovicaprini, "1 azienda ovicaprina su 140 colpita ogni anno", "0,70%"),
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
st.subheader("2. Le vere vittime: i piccoli allevatori")
st.write(
    "Se l'impatto medio è così basso, da dove nasce l'esasperazione? Dal fatto che il danno **non è distribuito equamente**, ma si accanisce in modo devastante su una strettissima minoranza di realtà produttive."
)

st.write(
    "Per capire chi rischia davvero di più, bisogna prima sapere come si alleva in Italia — e in particolare chi lo fa nel modo più esposto. Si tratta del cosiddetto **allevamento estensivo meridionale**: aziende piccole, meno di 100 capi, gestite a pascolo libero e transumanza, spesso l'unica attività economica sostenibile in territori dove altro non cresce. È anche il modello più povero economicamente dei tre esistenti in Italia (dati ISMEA) — e non a caso, quello più difficile da proteggere: capi che si muovono su territori ampi, difficili da recintare, con sorveglianza discontinua e poche risorse per cani da guardiania o recinzioni fisse."
)
st.write(
    "E dove si concentra questo tipo di allevamento in Italia? Escludendo Sicilia e Sardegna (le aree a densità più alta in assoluto, ma fuori dall'areale del lupo), la fascia con più capi ovicaprini sulla terraferma è la **dorsale appenninica centro-meridionale**, insieme al **settore occidentale delle Alpi** — con due sacche isolate a Grosseto e sul Gargano."
)
st.write(
    "Vi suona familiare? È la stessa identica area in cui si concentra la popolazione di lupo. Non è un caso: dove i due mondi si sovrappongono, nasce il conflitto."
)

st.markdown("#### 📍 La mappa del conflitto")

# Checkbox per la mappa interattiva SVG ("Pascoli estensivi" attiva di default)
col_check1, col_check2 = st.columns(2)
with col_check1:
    show_pascoli = st.checkbox("🟦 Mostra pascoli estensivi (Alpi Occidentali e Appennini)", value=True)
with col_check2:
    show_lupo = st.checkbox("🟥 Mostra distribuzione del lupo", value=False)

# Logica per mostrare i livelli SVG
opacity_pascoli = 0.5 if show_pascoli else 0.0
opacity_lupo = 0.5 if show_lupo else 0.0
opacity_overlap = 1.0 if (show_pascoli and show_lupo) else 0.0

# Illustrazione SVG Statica dell'Italia con i livelli (semplificata)
svg_map = f"""
<div style="display: flex; justify-content: center; margin: 20px 0;">
    <svg width="400" height="500" viewBox="0 0 400 500" style="background-color: transparent;">
        <defs>
            <!-- Pattern di sovrapposizione -->
            <pattern id="hatch" width="12" height="12" patternTransform="rotate(45)">
                <rect width="12" height="12" fill="rgba(25, 118, 210, 0.4)" />
                <line x1="0" y1="0" x2="0" y2="12" stroke="rgba(211, 47, 47, 0.8)" stroke-width="6" />
            </pattern>
            <!-- Maschera per l'intersezione perfetta -->
            <clipPath id="lupo-clip">
                <path d="M 60 120 C 80 80, 160 90, 180 130 C 200 170, 240 250, 280 340 C 310 400, 270 420, 240 370 C 200 300, 150 200, 90 180 C 70 170, 50 140, 60 120 Z" />
            </clipPath>
        </defs>
        
        <!-- Base Italia (Stilizzata e Semplificata) -->
        <path d="M 50 100 Q 150 50, 230 100 Q 250 150, 280 250 Q 320 380, 280 430 Q 250 450, 230 380 Q 200 320, 150 220 Q 90 180, 50 150 Z" 
              fill="#E5E5E5" stroke="#B0B0B0" stroke-width="2"/>
        <!-- Isole Semplificate -->
        <circle cx="120" cy="350" r="25" fill="#E5E5E5" stroke="#B0B0B0" stroke-width="2"/> <!-- Sardegna -->
        <ellipse cx="190" cy="450" rx="35" ry="20" fill="#E5E5E5" stroke="#B0B0B0" stroke-width="2"/> <!-- Sicilia -->

        <!-- Livello Pascoli Estensivi (Blu) -->
        <path d="M 50 110 C 70 70, 150 80, 190 120 C 220 160, 260 260, 290 350 C 320 410, 280 430, 250 380 C 210 310, 160 210, 80 190 C 60 180, 40 140, 50 110 Z" 
              fill="#1976D2" opacity="{opacity_pascoli}" style="transition: opacity 0.4s ease;" />

        <!-- Livello Lupo (Rosso) -->
        <path d="M 60 120 C 80 80, 160 90, 180 130 C 200 170, 240 250, 280 340 C 310 400, 270 420, 240 370 C 200 300, 150 200, 90 180 C 70 170, 50 140, 60 120 Z" 
              fill="#D32F2F" opacity="{opacity_lupo}" style="transition: opacity 0.4s ease;" />

        <!-- Sovrapposizione (Tratteggio visibile solo se entrambi attivi) -->
        <path d="M 50 110 C 70 70, 150 80, 190 120 C 220 160, 260 260, 290 350 C 320 410, 280 430, 250 380 C 210 310, 160 210, 80 190 C 60 180, 40 140, 50 110 Z" 
              fill="url(#hatch)" clip-path="url(#lupo-clip)" opacity="{opacity_overlap}" style="transition: opacity 0.4s ease;"/>
    </svg>
</div>
"""
st.markdown(svg_map, unsafe_allow_html=True)
st.caption(
    "*Rappresentazione grafica semplificata delle zone di concentrazione, basata sulle mappe del report impatto zootecnico ISPRA (Fig. 4) e sulla mappa di distribuzione nazionale del lupo. Non costituisce una mappa di precisione con confini amministrativi calcolati.*"
)

st.markdown("#### 🎯 1 azienda su 4 subisce oltre il 70% dei danni")
st.write("I dati sugli ovicaprini (pecore e capre) mostrano in modo estremo questa sproporzione: una piccola fetta di aziende fa da parafulmine per l'intero settore.")

# Calcolo programmatico dimensioni icone pittogramma: size = k * sqrt(valore)
k_picto = 10.35  # costante k per ottenere dimensione massima ~89px sul valore max (74.1%)
sz_danno_hotspot = int(round(k_picto * math.sqrt(73.3)))  # ~89px
sz_az_hotspot = int(round(k_picto * math.sqrt(25.9)))     # ~53px
sz_danno_altre = int(round(k_picto * math.sqrt(26.7)))     # ~53px
sz_az_altre = int(round(k_picto * math.sqrt(74.1)))        # ~89px

# L'errore nel path SVG era nel ciclo M8,11... che si chiudeva su 16,11. È stato corretto in 8,11 in entrambe le occorrenze.
html_pictogram = clean_html(f"""
    <div class="pictogram-container">
        <!-- COLONNA 1: HOTSPOT (POCHE AZIENDE, TANTI DANNI) -->
        <div class="picto-col">
            <div class="picto-label" style="color: #D32F2F; margin-bottom: 10px;">Gli "Hotspot"</div>
            
            <!-- DANNO (Sopra - Teschio) -->
            <div style="height: 120px; display: flex; align-items: flex-end;">
                <svg width="{sz_danno_hotspot}" height="{sz_danno_hotspot}" viewBox="0 0 24 24"><path fill="#D32F2F" d="M12,2A9,9 0 0,0 3,11C3,14.03 4.53,16.82 7,18.47V22H9V20H11V22H13V20H15V22H17V18.46C19.47,16.81 21,14 21,11A9,9 0 0,0 12,2M8,11A2,2 0 0,1 10,13A2,2 0 0,1 8,15A2,2 0 0,1 6,13A2,2 0 0,1 8,11M16,11A2,2 0 0,1 18,13A2,2 0 0,1 16,15A2,2 0 0,1 14,13A2,2 0 0,1 16,11M12,14L13.5,17H10.5L12,14Z" /></svg>
            </div>
            <div class="picto-label" style="color: #D32F2F;">73,3%</div>
            <div class="picto-sub">dei capi predati totali</div>
            
            <!-- AZIENDA (Sotto - Fabbrica) -->
            <div style="height: 120px; display: flex; align-items: flex-end; margin-top: 20px;">
                <svg width="{sz_az_hotspot}" height="{sz_az_hotspot}" viewBox="0 0 24 24"><path fill="#888" d="M12 2L2 12h3v8h14v-8h3L12 2zm0 2.8L17.2 10H6.8L12 4.8z"/></svg>
            </div>
            <div class="picto-label">25,9%</div>
            <div class="picto-sub">delle aziende colpite</div>
        </div>
        
        <!-- COLONNA 2: TUTTE LE ALTRE (TANTE AZIENDE, POCHI DANNI) -->
        <div class="picto-col">
            <div class="picto-label" style="color: #666; margin-bottom: 10px;">Tutte le altre</div>
            
            <!-- DANNO (Sopra - Teschio) -->
            <div style="height: 120px; display: flex; align-items: flex-end;">
                <svg width="{sz_danno_altre}" height="{sz_danno_altre}" viewBox="0 0 24 24"><path fill="#D32F2F" d="M12,2A9,9 0 0,0 3,11C3,14.03 4.53,16.82 7,18.47V22H9V20H11V22H13V20H15V22H17V18.46C19.47,16.81 21,14 21,11A9,9 0 0,0 12,2M8,11A2,2 0 0,1 10,13A2,2 0 0,1 8,15A2,2 0 0,1 6,13A2,2 0 0,1 8,11M16,11A2,2 0 0,1 18,13A2,2 0 0,1 16,15A2,2 0 0,1 14,13A2,2 0 0,1 16,11M12,14L13.5,17H10.5L12,14Z" /></svg>
            </div>
            <div class="picto-label" style="color: #D32F2F;">26,7%</div>
            <div class="picto-sub">dei capi predati totali</div>
            
            <!-- AZIENDA (Sotto - Fabbrica) -->
            <div style="height: 120px; display: flex; align-items: flex-end; margin-top: 20px;">
                <svg width="{sz_az_altre}" height="{sz_az_altre}" viewBox="0 0 24 24"><path fill="#888" d="M12 2L2 12h3v8h14v-8h3L12 2zm0 2.8L17.2 10H6.8L12 4.8z"/></svg>
            </div>
            <div class="picto-label">74,1%</div>
            <div class="picto-sub">delle aziende colpite</div>
        </div>
    </div>
""")
st.markdown(html_pictogram, unsafe_allow_html=True)
st.caption(
    "*Il settore bovino se la cava meglio — ma anche lì una minoranza di aziende si porta via la parte più consistente dei danni (il 20,5% delle aziende subisce il 62,2% dei danni).*"
)

st.markdown("---")

# --- ATTO 3 ---
st.subheader("3. La vera minaccia… la burocrazia")
st.write(
    "Mentre si propongono 'soluzioni' come ridurre le tutele per il lupo o addirittura cacciarlo, i dati mettono a nudo il vero problema odierno: un sistema di supporto pubblico lento, farraginoso e spesso inaccessibile, sia per i rimborsi che per l'acquisto di difese."
)

col3_left, col3_right = st.columns([1, 1])

with col3_left:
    st.markdown("#### ⏳ Tempi di indennizzo estenuanti")
    st.markdown(
        clean_html("""
        <div class="kpi-card">
            <p class="kpi-val" style="font-size:3rem;">80,4%</p>
            <p class="kpi-label" style="font-size:1.1rem;">Degli allevatori colpiti aspetta <b>da 2 a oltre 12 mesi</b> per ricevere l'indennizzo di un capo ucciso.</p>
        </div>
        """),
        unsafe_allow_html=True,
    )
    st.write(
        "In media, l'attesa burocratica è di **201 giorni**. Un tempo infinito per una piccola azienda che nel frattempo ha perso una fonte di reddito e, ovviamente, continua a sostenere le spese quotidiane."
    )

with col3_right:
    st.markdown("#### 🛡️ L'emergenza della raccolta dati sulle difese")
    st.write(
        "Come siamo messi a prevenzione sul campo? Analizzando i report ufficiali nei luoghi degli attacchi accertati, emerge un quadro disarmante sulla capacità delle Regioni di tracciare i dati:"
    )

    st.markdown(
        clean_html("""
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
        """),
        unsafe_allow_html=True,
    )

st.markdown("---")

# --- ATTO 4 ---
st.subheader("4. Il vero dramma: una morsa insostenibile sui piccoli")
st.write(
    "Chi subisce più danni da lupo deve anche affrontare la concorrenza di aziende sempre più grandi, che spingono i prezzi verso il basso. E le spese per difendersi dal predatore — recinzioni, mantenimento dei cani, manodopera — non sono un costo isolato, ma un peso che si aggiunge a bilanci già messi sotto pressione. È un cerchio che si stringe da più lati sulle stesse realtà."
)

st.markdown(
    clean_html("""
    <div class="kpi-card" style="text-align: center; padding: 30px;">
        <p class="kpi-val" style="font-size:3.5rem;">-21.527</p>
        <p class="kpi-label" style="font-size:1.3rem;"><b>Aziende bovine scomparse in soli 5 anni (2015-2019)</b></p>
        <p class="kpi-label" style="max-width: 700px; margin: 15px auto 0;">Tra il 2015 e il 2019 il numero di stalle in Italia è crollato del 12,7% — ma il numero di animali allevati è rimasto praticamente lo stesso. Cosa significa? Che il settore si sta concentrando sempre di più nelle mani di grandi allevamenti al chiuso, a scapito delle realtà medio-piccole, quelle più esposte sul territorio.</p>
    </div>
    """),
    unsafe_allow_html=True,
)

st.markdown("---")

# --- ATTO 5 ---
st.subheader("5. La soluzione")

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

st.markdown(
    clean_html("""
    <div class="kpi-card" style="margin-top: 15px;">
        <p class="kpi-label" style="margin-top: 0; margin-bottom: 5px;">Fondi prevenzione lupo Emilia-Romagna</p>
        <p class="kpi-val" style="font-size:2.4rem;">Da 87,5 Mila a 2 Milioni €</p>
        <p class="kpi-label">Il salto straordinario di finanziamenti stanziati nel 2026 rispetto alle limitate quote ordinarie passate.</p>
    </div>
    """),
    unsafe_allow_html=True,
)

st.markdown("---")

# --- EPILOGO: FONTI E METODOLOGIA ---
st.subheader("📚 Fonti e Metodologia")

with st.expander("📝 Nota sui dati, Caveat e Dataset"):
    st.markdown("""
    **Limiti del Dataset ISPRA:**
    * I dati di impatto nazionali dettagliati sulle aziende (Gervasi et al. 2022) coprono il quinquennio **2015-2019**, rappresentando l'ultimo studio sistematico standardizzato disponibile su scala paese, basato sull'incrocio tra rimborsi regionali e Banca Dati Nazionale (BDN).
    * Non esiste una ripartizione regionale pulita per la popolazione di lupo in Appennino, poiché il modello scientifico ISPRA stima le densità su 13 macro-aree di campionamento che valicano i confini amministrativi.

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

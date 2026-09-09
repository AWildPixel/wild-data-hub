import pandas as pd
import plotly.graph_objects as go
import country_converter as coco
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Wild Data - Traffico di animali in Italia", layout="wide")

# CSS: FORZA IL BROWSER MOBILE A PASSARE I GESTI SOLO ALLA MAPPA, LASCIANDO LIBERI I MARGINI E LA LEGENDA
st.markdown("""
    <style>
    /* 1. Riabilita lo scorrimento naturale su tutto il contenitore del grafico (legenda e spazi neri) */
    [data-testid="stPlotlyChart"] {
        touch-action: auto !important;
    }
    /* 2. Disabilita lo scorrimento della pagina SOLO quando il tocco avviene esattamente sui livelli della mappa */
    .js-plotly-plot .geolayer, 
    .js-plotly-plot .draglayer,
    .js-plotly-plot .geo {
        touch-action: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# BOTTONE HOME MOBILE-FRIENDLY IN CIMA
st.page_link("Home.py", label="🏠 Torna alla Home di Wild Data")
st.markdown("---")

# TITOLO GIORNALISTICO E SPECIFICO PER IL PUBBLICO
st.title("🐾 Il traffico di animali esotici in Italia")
st.markdown("*Esplora le rotte dell'importazione di specie protette verso il nostro Paese. Passa dal mercato legale ai sequestri doganali per scoprire i veri protagonisti e smontare i falsi miti.*")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('cites.csv', low_memory=False)
    # Rimuoviamo solo se manca l'esportatore, ma manteniamo i record senza Classe tassonomica
    df = df.dropna(subset=['Exporter'])
    df['iso3'] = coco.convert(names=df['Exporter'].tolist(), to='ISO3', not_found=None)
    df = df.dropna(subset=['iso3'])

    def elabora(sub_df):
        # 1. Conteggio totale (tutte le righe)
        v_tot = sub_df.groupby('iso3').size().reset_index(name='Conteggio_Totale')
        
        # 2. Conteggio identificato (solo righe con Class)
        df_id = sub_df.dropna(subset=['Class'])
        v_id = df_id.groupby('iso3').size().reset_index(name='Conteggio_Identificato')
        
        # 3. Classe dominante (calcolata solo sui dati identificati)
        c = df_id.groupby(['iso3', 'Class']).size().reset_index(name='Count')
        c = c.sort_values(['iso3', 'Count'], ascending=[True, False]).drop_duplicates(subset=['iso3'])
        
        # Unione dei dataframe
        res = pd.merge(v_tot, v_id, on='iso3', how='left')
        res['Conteggio_Identificato'] = res['Conteggio_Identificato'].fillna(0).astype(int)
        
        res = pd.merge(res, c[['iso3', 'Class']], on='iso3', how='left')
        res = res.rename(columns={'Class': 'Classe_Dominante'})
        
        # Se un paese ha solo record senza classe, mostriamo "Sconosciuta"
        res['Classe_Dominante'] = res['Classe_Dominante'].fillna('Sconosciuta')
        
        return res

    return elabora(df[df['Source'] != 'I']), elabora(df[df['Source'] == 'I'])

try:
    df_legale, df_illegale = load_data()

    # SELETTORE MAPPA
    scelta = st.radio(
        "Seleziona i dati da visualizzare:",
        ["🌿 Mercato Legale", "🚨 Sequestri"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if scelta == "🌿 Mercato Legale":
        st.markdown("### 🌍 Mercato legale: un traffico da 15.750 registrazioni")
        st.write("La rete delle importazioni autorizzate copre quasi tutto il globo. Non si tratta di commercio illecito, ma di un sistema strettamente monitorato che serve principalmente le filiere produttive e gli scambi tra parchi e istituti europei.")
    else:
        st.markdown("### 🚨 USA: il protagonista del mercato illegale")
        st.write("Guardando ai sequestri, forse vi immaginerete che si tratta di animali catturati dai bracconieri, strappati alle foreste tropicali di paesi esotici. Ma i dati ci raccontano un'altra storia: il Nord America domina nettamente le statistiche delle irregolarità doganali verso l'Italia.")

    # COSTRUZIONE MAPPA
    fig = go.Figure()

    # Legenda ancorata al centro e spinta verso il basso
    colorbar_orizzontale = dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        thickness=12,
        len=0.7,
        title=dict(text="Totale Spedizioni", side="top")
    )

    if scelta == "🌿 Mercato Legale":
        fig.add_trace(go.Choropleth(
            locations=df_legale['iso3'], 
            z=df_legale['Conteggio_Totale'], 
            customdata=df_legale['Conteggio_Identificato'],
            text=df_legale['Classe_Dominante'],
            hovertemplate="<b>%{location}</b><br>Totale spedizioni: %{z}<br>Di cui identificate: %{customdata}<br>Gruppo prevalente: <b>%{text}</b><extra></extra>",
            colorscale='Greens', name='Legale',
            colorbar=colorbar_orizzontale,
            marker_line_color='#4A4A4A', marker_line_width=0.5
        ))
    else:
        fig.add_trace(go.Choropleth(
            locations=df_illegale['iso3'], 
            z=df_illegale['Conteggio_Totale'], 
            customdata=df_illegale['Conteggio_Identificato'],
            text=df_illegale['Classe_Dominante'],
            hovertemplate="<b>%{location}</b><br>Totale sequestri: %{z}<br>Di cui identificati: %{customdata}<br>Gruppo prevalente: <b>%{text}</b><extra></extra>",
            colorscale='Reds', name='Sequestri',
            colorbar=colorbar_orizzontale,
            marker_line_color='#4A4A4A', marker_line_width=0.5
        ))

    # Ripristiniamo il margine inferiore (b=60) per fare spazio alla legenda senza sovrapposizioni
    fig.update_layout(
        geo=dict(
            showframe=False, 
            showcoastlines=True, coastlinecolor='#4A4A4A',
            showland=True, landcolor='#E5E5E5',
            projection_type='natural earth'
        ),
        margin=dict(l=0, r=0, t=10, b=60)
    )

    # OUTPUT CON CONFIGURAZIONE ESPLICITA PER INTERAZIONI MOBILE/DESKTOP
    st.plotly_chart(
        fig, 
        use_container_width=True, 
        config={
            'scrollZoom': True,         
            'displayModeBar': True,     
            'displaylogo': False        
        }
    )
    st.markdown("---")

    # ATTO 1 (AGGIORNATO CON NUOVO INCIPIT)
    st.subheader("🔍 Oltre i numeri: l'anomalia degli Stati Uniti")
    st.write("La nostra indagine mostra che gli USA non sono soltanto il principale esportatore di spedizioni legali in Italia ma anche di quelle illegali, perché? Più che a una rete di contrabbando tradizionale, questo primato viene ricondotto dagli analisti a un mix di dinamiche commerciali, burocrazia e snodi logistici:")
    
    col1_1, col1_2, col1_3 = st.columns(3)
    with col1_1:
        st.markdown("**1. Burocrazia e cavilli normativi**\n\nIl database CITES registra il sequestro, ma non la causa specifica della confisca. Tuttavia, come evidenziato dai report di **TRAFFIC** (la rete internazionale di monitoraggio del commercio di specie selvatiche), la burocrazia dei permessi CITES è complessa e soggetta a frequenti irregolarità o errori documentali. Le norme europee sono estremamente severe: la minima difformità nei certificati fa scattare il blocco alla dogana, trasformando una svista formale in un sequestro ufficiale.")
    with col1_2:
        st.markdown("**2. La spinta degli allevamenti commerciali**\n\nGli USA ospitano un'imponente industria di allevamento di rettili esotici (con forte concentrazione in stati come Florida e Texas). Muovendo volumi d'esportazione sterminati, è statisticamente inevitabile che da questa filiera si generi un numero maggiore di contestazioni e fermi doganali.")
    with col1_3:
        st.markdown("**3. Tutte le rotte passano dagli USA**\n\nPer molte specie esotiche (come pitoni o caimani), gli USA fungono da grande hub intermedio: i grossisti americani acquistano pelli dall'Asia o dal Sud America per rivenderle alle filiere del lusso italiane, moltiplicando i passaggi di confine e i rischi di errori nei documenti. L'eccezione principale è l'**alligatore americano** — la specie in assoluto più intercettata nei sequestri dagli USA — per la quale il territorio statunitense rappresenta sia il luogo d'origine che d'esportazione.")

    st.markdown("---")

    # ATTO 2
    st.subheader("🎯 Moda, lusso e collezionismo: cosa muove davvero la domanda?")
    st.write("Quando si parla di traffico di fauna, l'istinto porta a immaginare animali vivi destinati al mercato dei pets esotici. Ma i dati raccontano un'altra storia: la stragrande maggioranza dei sequestri e delle transazioni riguarda parti e derivati lavorati, e a trainare i volumi maggiori verso l'Italia sono le filiere del lusso e il turismo.")
    
    col2_1, col2_2, col2_3 = st.columns(3)
    with col2_1:
        st.markdown("**🦎 Rettili (Alta Moda e Pelletteria)**\n\nL'Italia importa enormi quantità di pelli lavorate, cinturini, borse e calzature (Alligatore, Pitone, Caimano) destinate al settore fashion.")
    with col2_2:
        st.markdown("**🐘 Mammiferi (Tessile e Trofei)**\n\nImportazioni dominate da filati pregiati (come la lana di Vigogna) e trofei di caccia. Una quota minore riguarda la ricerca scientifica.")
    with col2_3:
        st.markdown("**🪸 Coralli e Altri (Souvenir e Arredamento)**\n\nScheletri di madrepora e conchiglie usati come oggetti d'arredo o portati illegalmente dai turisti come souvenir di viaggio.")

    st.markdown("---")

    # ATTO 3
    st.subheader("🕵️‍♂️ I grandi assenti: i giganti della biodiversità")
    st.write("Guardando la mappa dei sequestri, una cosa balza subito all'occhio: paesi con un patrimonio naturale immenso — come il Brasile, le nazioni del Bacino del Congo o l'Indonesia — non hanno praticamente alcun episodio di sequestro registrato verso l'Italia.")
    st.write("Questo fenomeno rivela in realtà un profondo bias di tracciamento. La mappa, infatti, non fotografa necessariamente il luogo d'origine dell'animale (o del prodotto da esso ricavato), ma il punto in cui le autorità doganali riescono a intercettare la spedizione.")
    st.write("Quindi anche se, ad esempio, si trattasse di un animale catturato da bracconieri, potrebbe comunque uscire dal paese inosservato a causa di controlli poco stringenti da parte delle autorità locali. A quel punto, la spedizione illegale emerge e viene registrata come \"sequestro\" ufficiale solo quando sbatte contro le più rigide ispezioni degli hub intermediari o delle dogane d'arrivo in Europa.")
    st.write("Ma anche qui, diverse spedizioni riescono inevitabilmente a passare sotto i radar... i dati CITES ci parlano di appena **61 sequestri ufficiali** dal 2013 al 2023, ma chissà quanto del traffico illegale resta sommerso, lasciandoci intravedere giusto la punta dell'iceberg.")

    st.markdown("---")

    # ATTO 4
    st.subheader("🧬 Identikit delle specie coinvolte")
    st.write("Le registrazioni CITES ci permettono di scendere fino alla singola specie. I **rettili** costituiscono il gruppo di gran lunga più rappresentato e frequente nelle confisce doganali italiane, affiancati da alcuni casi emblematici relativi ad altre classi animali evidenziate in mappa:")
    
    col4_1, col4_2, col4_3 = st.columns(3)
    with col4_1:
        st.markdown("**Rettili (Reptilia - le specie più frequenti):**\n* *Alligator mississippiensis* (Alligatore americano)\n* *Malayopython reticulatus* (Pitone reticolato)\n* *Caiman crocodilus fuscus* (Caimano bruno)")
    with col4_2:
        st.markdown("**Mammiferi (Mammalia - casi emblematici):**\n* *Vicugna vicugna* (Vigogna)\n* *Loxodonta africana* (Elefante africano)\n* *Macaca mulatta* (Macaco rhesus)")
    with col4_3:
        st.markdown("**Altre Classi (casi emblematici):**\n* **Coralli (Anthozoa):** *Scleractinia spp.* (Madrepore)\n* **Molluschi (Bivalvia/Gastropoda):** *Strombus gigas* (Strombo gigante)\n* **Uccelli (Aves):** *Pavo cristatus* (Pavone indiano)")

    st.markdown("---")

    # EPILOGO
    st.subheader("📚 Fonti e Metodologia")
    
    # NOTA METODOLOGICA CON DETTAGLI SUL PERCHÈ MANCANO I DATI
    with st.expander("📝 Nota sui dati: l'area grigia delle specie sconosciute"):
        st.markdown("""
        Analizzando i registri doganali originali, è emersa un'importante anomalia: in quasi 3.000 spedizioni manca un'informazione fondamentale, ovvero la "Classe" o la specie esatta dell'animale. Sappiamo che c'è stato un transito o un sequestro, ma non sappiamo di che animale si tratti.
        
        **Perché succede?** Principalmente per tre motivi: transito di prodotti ultra-lavorati (estratti, cosmetici, pillole per la medicina tradizionale in cui è impossibile risalire alla specie senza test del DNA), compilazioni doganali affrettate ("pelle di rettile" invece del taxon esatto), o raggruppamenti generici applicati spesso a coralli e piante.
        
        Per garantire la totale trasparenza e mostrarvi la reale dimensione del traffico verso l'Italia, **abbiamo scelto di non nascondere questi dati incompleti**. 
        
        Ecco perché, passando il cursore sui vari Paesi nella mappa, noterete un doppio conteggio: il volume totale delle spedizioni (che include l'area grigia dei registri incompleti) e il numero esatto delle spedizioni in cui l'animale è stato correttamente identificato. Questa scelta ci permette di mantenere la precisione sulla classe dominante per ogni nazione, senza però sminuire i numeri reali del mercato legale (15.750 registrazioni) e dei sequestri ufficiali (61 casi).
        """)
        
    st.markdown("""
    * **La Banca Dati CITES:** I dati utilizzati provengono dal **CITES Trade Database**, gestito dallo UNEP-WCMC (UN Environment Programme World Conservation Monitoring Centre). È il registro ufficiale globale di tutte le transazioni commerciali, le esportazioni autorizzate e i sequestri doganali di fauna e flora selvatiche minacciate.
    * **Analisi sull'enforcement:** I riferimenti sulle dinamiche di ispezione doganale e sull'uso improprio della documentazione CITES fanno riferimento ai report di ricerca della rete **TRAFFIC**.
    * **Periodo di riferimento:** 2013–2023.
    * Puoi esplorare e scaricare i dati grezzi direttamente sul sito ufficiale: [CITES Trade Database](https://trade.cites.org/).
    """)

except Exception as e:
    st.error(f"Errore nel caricamento dei dati: {e}")

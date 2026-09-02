import pandas as pd
import plotly.graph_objects as go
import country_converter as coco
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Wild Data #01 - Sequestri CITES", layout="wide")

st.title("Wild Data 🐾 | #01 - Sequestri CITES Italia")
st.write("Esplora le rotte dell'importazione di specie esotiche verso l'Italia. Passa dal mercato legale ai sequestri doganali.")

with st.expander("ℹ️ Come leggere la mappa e i dati"):
    st.markdown("""
    * **Mercato Legale vs Sequestri:** Usa i pulsanti sopra la mappa per passare dai dati sul commercio autorizzato alle registrazioni delle confische doganali.
    * **Intensità del colore:** Più il colore del Paese d'origine è scuro, maggiore è il numero di transazioni e spedizioni registrate verso l'Italia nel decennio 2013-2023.
    * **Gruppo di animali prevalente:** Passa il cursore (o tocca da mobile) sui singoli Paesi per vedere il numero totale di registrazioni e il gruppo di animali più rappresentato.
    """)

@st.cache_data
def load_data():
    df = pd.read_csv('cites.csv', low_memory=False)
    df = df.dropna(subset=['Exporter', 'Class'])
    df['iso3'] = coco.convert(names=df['Exporter'].tolist(), to='ISO3', not_found=None)
    df = df.dropna(subset=['iso3'])

    def elabora(sub_df):
        v = sub_df.groupby('iso3').size().reset_index(name='Conteggio')
        c = sub_df.groupby(['iso3', 'Class']).size().reset_index(name='Count')
        c = c.sort_values(['iso3', 'Count'], ascending=[True, False]).drop_duplicates(subset=['iso3'])
        return pd.merge(v, c[['iso3', 'Class']], on='iso3').rename(columns={'Class': 'Classe_Dominante'})

    return elabora(df[df['Source'] != 'I']), elabora(df[df['Source'] == 'I'])

try:
    df_legale, df_illegale = load_data()

    st.write("") 
    scelta = st.radio(
        "Seleziona i dati da visualizzare:",
        ["🌿 Mercato Legale", "🚨 Sequestri"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if scelta == "🌿 Mercato Legale":
        totale_legale = df_legale['Conteggio'].sum()
        st.markdown(f"### 🌍 Mercato legale: un traffico da {totale_legale:,} registrazioni".replace(",", "."))
        st.write("La rete delle importazioni autorizzate copre quasi tutto il globo. Non si tratta di commercio illecito, ma di un sistema strettamente monitorato che serve principalmente le filiere produttive e gli scambi tra parchi e istituti europei.")
    else:
        st.markdown("### 🚨 Il caso USA: da dove arriva la maggior parte dei sequestri")
        st.write("Perché proprio gli USA? Il Nord America è un centro nevralgico per l'allevamento di specie esotiche e l'esportazione di pelli lavorate. L'alta concentrazione di fiere di settore e collezionisti genera un volume di spedizioni irregolari superiore a quello di Africa e Asia verso l'Italia.")

    fig = go.Figure()

    colorbar_orizzontale = dict(
        orientation="h",
        y=-0.15,
        thickness=12,
        len=0.8,
        title=dict(
            text="Volume registrazioni",
            side="top"
        )
    )

    if scelta == "🌿 Mercato Legale":
        fig.add_trace(go.Choropleth(
            locations=df_legale['iso3'], z=df_legale['Conteggio'], text=df_legale['Classe_Dominante'],
            hovertemplate="<b>%{location}</b><br>Importazioni: %{z}<br>Gruppo prevalente: <b>%{text}</b><extra></extra>",
            colorscale='Greens', name='Legale',
            colorbar=colorbar_orizzontale,
            marker_line_color='#4A4A4A', marker_line_width=0.5
        ))
    else:
        fig.add_trace(go.Choropleth(
            locations=df_illegale['iso3'], z=df_illegale['Conteggio'], text=df_illegale['Classe_Dominante'],
            hovertemplate="<b>%{location}</b><br>Sequestri: %{z}<br>Gruppo prevalente: <b>%{text}</b><extra></extra>",
            colorscale='Reds', name='Sequestri',
            colorbar=colorbar_orizzontale,
            marker_line_color='#4A4A4A', marker_line_width=0.5
        ))

    fig.update_layout(
        geo=dict(
            showframe=False, 
            showcoastlines=True,
            coastlinecolor='#4A4A4A',
            showland=True, 
            landcolor='#E5E5E5',
            projection_type='natural earth'
        ),
        margin=dict(l=0, r=0, t=10, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📌 Key Insights dell'Analisi")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🦎 Gruppo di animali prevalente:**  
        Il gruppo di animali più spesso intercettato dalle dogane italiane è quello dei rettili! I mammiferi invece si piazzano al secondo posto.
        """)
        
    with col2:
        st.markdown("""
        **🇺🇸 Origine dei Sequestri:**  
        Il maggior volume di confische ufficialmente registrate verso l'Italia proviene dagli **Stati Uniti**, principale hub commerciale mondiale per l'allevamento e il collezionismo esotico.
        """)

    st.markdown("---")
    
    st.subheader("🎯 Moda e Trofei di lusso guidano la domanda")
    st.write("I dati rivelano che il traffico (sia legale che illecito) non è trainato solo dal collezionismo privato. A muovere i volumi maggiori sono le catene di approvvigionamento per il settore del lusso e il turismo irresponsabile.")
    
    col_u1, col_u2, col_u3 = st.columns(3)
    
    with col_u1:
        st.markdown("""
        **🦎 Rettili**
        * **Principale utilizzo:** Alta Moda e Pelletteria
        * **Dettaglio:** Pelli lavorate, cinturini, borse e calzature (in particolare pelli di Alligatore, Pitone e Caimano) destinate alla filiera del lusso.
        """)
        
    with col_u2:
        st.markdown("""
        **🐘 Mammiferi**
        * **Principale utilizzo:** Tessile di Lusso e Trofei
        * **Dettaglio:** Lana di Vigogna e trofei di caccia. Una quota minore riguarda il collezionismo privato e la ricerca scientifica.
        """)
        
    with col_u3:
        st.markdown("""
        **🪸 Coralli e Altri Gruppi**
        * **Principale utilizzo:** Souvenir e Arredamento
        * **Dettaglio:** Scheletri di madrepora e conchiglie usati come oggetti d'arredo o souvenir turistici non dichiarati.
        """)

    st.markdown("---")
    st.markdown("### 🧬 Il bersaglio: dai piccoli coralli ai grandi mammiferi")
    st.write("Le dogane non intercettano solo animali vivi. Gran parte dei sequestri riguarda parti o derivati lavorati di queste specie specifiche.")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("""
        **Rettili (Reptilia)**
        * *Alligator mississippiensis* (Alligatore americano)
        * *Malayopython reticulatus* (Pitone reticolato)
        * *Caiman crocodilus fuscus* (Caimano bruno)
        """)
        
    with col_b:
        st.markdown("""
        **Mammiferi (Mammalia)**
        * *Vicugna vicugna* (Vigogna)
        * *Loxodonta africana* (Elefante africano)
        * *Macaca mulatta* (Macaco rhesus)
        """)
        
    with col_c:
        st.markdown("""
        **Altre Classi**
        * **Coralli:** *Scleractinia spp.* (Madrepore)
        * **Molluschi:** *Strombus gigas* (Strombo gigante)
        * **Uccelli:** *Pavo cristatus* (Pavone indiano)
        """)

    st.markdown("---")
    st.subheader("📚 Fonti e Metodologia")
    st.markdown("""
    * **La Banca Dati CITES:** I dati utilizzati in questa analisi provengono dalla **CITES Trade Database**, gestita dallo UNEP-WCMC (UN Environment Programme World Conservation Monitoring Centre) per conto del Segretariato CITES. Si tratta del registro ufficiale globale che raccoglie tutte le transazioni commerciali, le esportazioni autorizzate e i sequestri doganali di specie della fauna e della flora selvatiche minacciate di estinzione.
    * **Periodo di riferimento:** 2013–2023.
    * Puoi esplorare e scaricare i dati grezzi originali direttamente sul sito ufficiale: [CITES Trade Database](https://trade.cites.org/).
    """)

except Exception as e:
    st.error(f"Errore nel caricamento del grafico: {e}")

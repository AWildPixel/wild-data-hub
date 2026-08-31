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
    * **Mercato Legale vs Sequestri:** Usa i pulsanti in alto sopra la mappa per passare dai dati sul commercio autorizzato alle registrazioni delle confische doganali (Source = I).
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

    fig = go.Figure()

    fig.add_trace(go.Choropleth(
        locations=df_legale['iso3'], z=df_legale['Conteggio'], text=df_legale['Classe_Dominante'],
        hovertemplate="<b>%{location}</b><br>Importazioni: %{z}<br>Prevalenza: <b>%{text}</b><extra></extra>",
        colorscale='Greens', name='Legale', visible=True
    ))

    fig.add_trace(go.Choropleth(
        locations=df_illegale['iso3'], z=df_illegale['Conteggio'], text=df_illegale['Classe_Dominante'],
        hovertemplate="<b>%{location}</b><br>Sequestri: %{z}<br>Prevalenza: <b>%{text}</b><extra></extra>",
        colorscale='Reds', name='Sequestri', visible=False
    ))

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
        updatemenus=[dict(
            type='buttons', direction='right', x=0.5, y=1.1, xanchor='center',
            bgcolor='#1A1C23',
            bordercolor='#333333',
            font=dict(color='#FFFFFF', size=13),
            buttons=[
                dict(
                    label='🌿 Mercato Legale', 
                    method='update', 
                    args=[{'visible': [True, False]}],
                    execute=True
                ),
                dict(
                    label='🚨 Sequestri', 
                    method='update', 
                    args=[{'visible': [False, True]}],
                    execute=True
                )
            ]
        )]
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
    st.markdown("### 🧬 Le Specie più Confiscate (Dati Reali Dogane)")
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

except Exception as e:
    st.error(f"Errore nel caricamento del grafico: {e}")

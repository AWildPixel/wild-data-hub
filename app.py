import streamlit as st

# Configurazione pagina e sidebar visibile
st.set_page_config(
    page_title="Wild Data Hub | A Wild Pixel", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Registrazione delle pagine per il menu laterale e la navigazione
home_page = st.Page("app.py", title="Home Hub", icon="🏠")
project_1 = st.Page("pages/01_Sequestri_CITES.py", title="#01 Sequestri CITES", icon="📊")

# Attivazione della navigazione native di Streamlit
pg = st.navigation([home_page, project_1])

st.title("Wild Data 🐾 | Data Journalism & Visual Inquiries")
st.write("Benvenuto nel repository interattivo di **Wild Data**, la serie di analisi dati e inchieste visuali curate da **A Wild Pixel**.")

st.markdown("---")

st.subheader("📂 Naviga tra le analisi disponibili")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 #01 — Sequestri Esotici CITES Italia (2013-2023)")
    st.write("""
    Mappa interattiva e analisi sui flussi di commercio esotico verso l'Italia. Confronta le importazioni ufficialmente autorizzate con i volumi delle confisce effettuate alle dogane.
    """)
    st.caption("Status: **Completato** | Tematica: *Biodiversità e Traffico Illecito*")
    
    # Pulsante di navigazione sicura con il nuovo sistema di pagine
    if st.button("🚀 Apri l'Analisi #01", type="primary"):
        st.switch_page(project_1)

with col2:
    st.markdown("### 🔄 Prossime Inchieste (In Arrivo)")
    st.write("""
    I nuovi capitoli e dataset di *Wild Data* verranno integrati direttamente in questa piattaforma e saranno selezionabili dal menu laterale.
    """)
    st.caption("Status: **In Sviluppo**")

st.markdown("---")
st.markdown("💡 *Progetto ideato e realizzato da **A Wild Pixel**.*")

# Esecuzione della pagina selezionata
pg.run()

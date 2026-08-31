import streamlit as st

# Configurazione pagina
st.set_page_config(
    page_title="Wild Data Hub | A Wild Pixel", 
    layout="wide"
)

# 1. Registro delle Pagine (Per aggiungere un nuovo progetto in futuro, basterà aggiungere una riga qui!)
home_page = st.Page("app.py", title="Home Hub", icon="🏠", default=True)
progetto_1 = st.Page("pages/01_Sequestri_CITES.py", title="#01 Sequestri CITES", icon="📊")

# 2. Configurazione Menu e Navigazione
pg = st.navigation(
    {"Home": [home_page], "Inchieste": [progetto_1]}, 
    position="top"
)

# 3. Contenuto della Home Page
if pg.selected == home_page:
    st.title("Wild Data 🐾 | Data Journalism & Visual Inquiries")
    st.write("Benvenuto nel repository interattivo di **Wild Data**, la serie di analisi dati e inchieste visuali curate da **A Wild Pixel**.")

    st.markdown("---")
    st.subheader("📂 Naviga tra le analisi disponibili")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 #01 — Sequestri Esotici CITES Italia (2013-2023)")
        st.write("Mappa interattiva e analisi sui flussi di commercio esotico verso l'Italia. Confronta le importazioni ufficialmente autorizzate con i volumi delle confisce effettuate alle dogane.")
        st.caption("Status: **Completato** | Tematica: *Biodiversità e Traffico Illecito*")
        
        # Pulsante diretto che sblocca l'accesso al progetto
        if st.button("🚀 Apri Analisi #01", use_container_width=True):
            st.switch_page(progetto_1)

    with col2:
        st.markdown("### 🔄 Prossime Inchieste (In Arrivo)")
        st.write("I nuovi capitoli e dataset di *Wild Data* verranno integrati direttamente in questa piattaforma.")
        st.caption("Status: **In Sviluppo**")

    st.markdown("---")
    st.markdown("💡 *Progetto ideato e realizzato da **A Wild Pixel**.*")

# 4. Esecuzione
pg.run()

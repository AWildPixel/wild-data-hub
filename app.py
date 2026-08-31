import streamlit as st

st.set_page_config(
    page_title="Wild Data Hub | A Wild Pixel", 
    layout="wide"
)

# 1. Racchiudiamo il contenuto della Home in una funzione
def mostra_home():
    st.title("Wild Data 🐾 | Data Journalism & Visual Inquiries")
    st.write("Benvenuto nel repository interattivo di **Wild Data**, la serie di analisi dati e inchieste visuali curate da **A Wild Pixel**.")

    st.markdown("---")
    st.subheader("📂 Naviga tra le analisi disponibili")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 #01 — Sequestri Esotici CITES Italia (2013-2023)")
        st.write("Mappa interattiva e analisi sui flussi di commercio esotico verso l'Italia. Confronta le importazioni ufficialmente autorizzate con i volumi delle confisce effettuate alle dogane.")
        st.caption("Status: **Completato** | Tematica: *Biodiversità e Traffico Illecito*")
        st.info("👆 Clicca su **#01 Sequestri CITES** nel menu in alto per visualizzare l'analisi.")

    with col2:
        st.markdown("### 🔄 Prossime Inchieste (In Arrivo)")
        st.write("I nuovi capitoli e dataset di *Wild Data* verranno integrati direttamente in questa piattaforma.")
        st.caption("Status: **In Sviluppo**")

    st.markdown("---")
    st.markdown("💡 *Progetto ideato e realizzato da **A Wild Pixel**.*")

# 2. Definiamo le pagine (la Home ora punta alla funzione, non al file)
home_page = st.Page(mostra_home, title="Home Hub", icon="🏠", default=True)
progetto_1 = st.Page("pages/01_Sequestri_CITES.py", title="#01 Sequestri CITES", icon="📊")

# 3. Creiamo e avviamo la navigazione in alto
pg = st.navigation(
    {"Home": [home_page], "Inchieste": [progetto_1]}, 
    position="top"
)
pg.run()

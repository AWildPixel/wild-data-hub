import streamlit as st

st.set_page_config(page_title="Wild Data Hub | A Wild Pixel", layout="wide", initial_sidebar_state="expanded")

st.title("Wild Data 🐾 | Data Journalism & Visual Inquiries")
st.write("Benvenuto nel repository interattivo di **Wild Data**, la serie di analisi dati e inchieste visuali curate da **A Wild Pixel**.")

st.markdown("---")
st.subheader("📂 Naviga tra le analisi disponibili")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 #01 — Sequestri Esotici CITES Italia (2013-2023)")
    st.write("Mappa interattiva e analisi sui flussi di commercio esotico verso l'Italia. Confronta le importazioni ufficialmente autorizzate con i volumi delle confisce effettuate alle dogane.")
    st.caption("Status: **Completato** | Tematica: *Biodiversità e Traffico Illecito*")
    
    # Questo è il nuovo pulsante nativo e sicuro
    st.page_link("pages/01_Sequestri_CITES.py", label="Apri l'Analisi #01", icon="🚀")

with col2:
    st.markdown("### 🔄 Prossime Inchieste (In Arrivo)")
    st.write("I nuovi capitoli e dataset di *Wild Data* verranno integrati direttamente in questa piattaforma e saranno selezionabili dal menu laterale.")
    st.caption("Status: **In Sviluppo**")

st.markdown("---")
st.markdown("💡 *Progetto ideato e realizzato da **A Wild Pixel**.*")

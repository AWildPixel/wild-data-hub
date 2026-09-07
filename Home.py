import streamlit as st

st.set_page_config(page_title="Wild Data 🐾 | Hub", layout="centered")

st.title("Wild Data 🐾")
st.markdown("### Il data journalism applicato alla natura e alla conservazione.")
st.markdown("---")

st.write("Benvenuto nell'archivio interattivo di **A Wild Pixel**.")
st.write("Qui trasformiamo i dati scientifici e i database ufficiali in inchieste visive per comprendere meglio i fenomeni che minacciano la biodiversità globale.")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📂 Inchieste")

# Pulsante grande e visibile che punta direttamente al file del progetto
st.page_link(
    "pages/01_Il_Traffico_Di_Animali_Esotici_In_Italia.py", 
    label="Scopri l'inchiesta: Il traffico di animali esotici in Italia", 
    icon="👉"
)

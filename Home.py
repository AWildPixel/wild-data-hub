import streamlit as st

st.set_page_config(page_title="Wild Data 🐾 | Hub", layout="centered")

# BARRA DI NAVIGAZIONE SUPERIORE
st.page_link("Home.py", label="🏠 Home")
st.markdown("---")

st.title("Wild Data 🐾")
st.markdown("### Il data journalism applicato alla natura e alla conservazione.")
st.markdown("---")

st.write("Benvenuto nell'archivio interattivo di **A Wild Pixel**.")
st.write("Qui trasformiamo i dati scientifici e i database ufficiali in inchieste visive per comprendere meglio i fenomeni che minacciano la biodiversità globale.")

st.info("👈 **Usa il menu laterale o la barra di navigazione** per esplorare le inchieste pubblicate.")

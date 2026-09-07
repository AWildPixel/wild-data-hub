import streamlit as st
import base64

# Impostiamo il layout a schermo largo
st.set_page_config(page_title="Wild Data 🐾 | Hub", layout="wide")

# Funzione per creare l'immagine rotonda stile IG
def render_logo(img_path):
    try:
        with open(img_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        
        # HTML e CSS per il tondino allineato a destra
        html = f"""
        <div style="display: flex; justify-content: right; padding-top: 15px;">
            <img src="data:image/png;base64,{encoded}" 
                 style="border-radius: 50%; width: 130px; height: 130px; object-fit: cover; border: 2px solid #f0f2f6;">
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.write(" ") # Nasconde errori se l'immagine sta ancora caricando su GitHub

# Creiamo le due colonne
col_main, col_logo = st.columns([3, 1])

with col_main:
    st.title("Wild Data 🐾")
    st.markdown("### Il data journalism applicato alla natura e alla conservazione.")

with col_logo:
    # Richiama la funzione usando il nome esatto del file caricato su GitHub
    render_logo("logo.png")

st.markdown("---")

# Sezione di benvenuto
st.write("Benvenuto nell'archivio interattivo di **A Wild Pixel**.")
st.write("Qui trasformiamo i dati scientifici e i database ufficiali in inchieste visive per comprendere meglio i fenomeni che minacciano la biodiversità globale.")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🔍 Inchieste")

# Pulsante per l'inchiesta
st.page_link(
    "pages/01_Il_Traffico_Di_Animali_Esotici_In_Italia.py", 
    label="Scopri l'inchiesta: Il traffico di animali esotici in Italia", 
    icon="👉"
)

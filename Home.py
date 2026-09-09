import base64
import streamlit as st

st.set_page_config(page_title="Wild Data 🐾 | Hub", layout="wide")


# Funzione per generare l'intestazione responsive
def render_header(img_path):
    encoded = ""
    try:
        with open(img_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        img_html = f'<img src="data:image/png;base64,{encoded}" style="border-radius: 50%; width: 75px; height: 75px; object-fit: cover; border: 2px solid #f0f2f6; flex-shrink: 0;">'
    except FileNotFoundError:
        img_html = ""

    html = f"""
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 15px; margin-bottom: 10px;">
        <div>
            <h1 style="margin:0; padding:0; font-size: 2.2rem; line-height: 1.2;">Wild Data 🐾</h1>
            <p style="margin: 5px 0 0 0; font-size: 1.1rem; opacity: 0.85;">Il data journalism applicato alla natura e alla conservazione.</p>
        </div>
        {img_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# Renderizza l'intestazione unica
render_header("logo.png")
st.markdown("---")

# Contenuto di benvenuto
st.write("Benvenuto nell'archivio interattivo di **A Wild Pixel**.")
st.write(
    "Qui trasformiamo i dati scientifici e i database ufficiali in inchieste visive per comprendere meglio i fenomeni che minacciano la biodiversità globale."
)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🔍 Inchieste")

# Elenco degli episodi
st.page_link(
    "pages/01_Il_Traffico_Di_Animali_Esotici_In_Italia.py",
    label="EPISODIO #01: Il traffico di animali esotici in Italia",
    icon="👉",
)

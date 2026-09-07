import base64
import streamlit as st

st.set_page_config(page_title="Wild Data 🐾 | Hub", layout="wide")

def render_header(img_path):
    encoded = ""
    try:
        with open(img_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        pass

    # Usiamo il CSS per rendere il logo adattabile alle dimensioni dello schermo
    html = f"""
    <style>
        .responsive-logo {{
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #f0f2f6;
            flex-shrink: 0;
            width: 75px; 
            height: 75px;
        }}
        @media (min-width: 768px) {{
            .responsive-logo {{
                width: 120px; 
                height: 120px;
            }}
        }}
        .header-container {{
            display: flex; 
            align-items: center; 
            justify-content: space-between; 
            gap: 15px; 
            margin-bottom: 10px;
        }}
    </style>
    
    <div class="header-container">
        <div>
            <h1 style="margin:0; padding:0; font-size: 2.2rem; line-height: 1.2;">Wild Data 🐾</h1>
            <p style="margin: 5px 0 0 0; font-size: 1.1rem; opacity: 0.85;">Il data journalism applicato alla natura e alla conservazione.</p>
        </div>
        <img class="responsive-logo" src="data:image/png;base64,{encoded}">
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

render_header("logo.png")
st.markdown("---")

st.write("Benvenuto nell'archivio interattivo di **A Wild Pixel**.")
st.write("Qui trasformiamo i dati scientifici e i database ufficiali in inchieste visive per comprendere meglio i fenomeni che minacciano la biodiversità globale.")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🔍 Inchieste")

st.page_link(
    "pages/01_Il_Traffico_Di_Animali_Esotici_In_Italia.py",
    label="Scopri l'inchiesta: Il traffico di animali esotici in Italia",
    icon="👉",
)

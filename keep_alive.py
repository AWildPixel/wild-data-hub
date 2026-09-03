from playwright.sync_api import sync_playwright
import time

def run():
    # Il tuo indirizzo pubblico attuale
    url = "https://wild-data.streamlit.app" 
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Visita la pagina e attende il caricamento completo (innescando il WebSocket)
        page.goto(url, wait_until="networkidle")
        time.sleep(10) 
        print(f"Ping eseguito con successo su: {url}")
        browser.close()

if __name__ == "__main__":
    run()

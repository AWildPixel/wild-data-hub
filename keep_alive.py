import re
import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

URL = "https://wild-data.streamlit.app"
TENTATIVI = 3


def ping(p):
    browser = p.chromium.launch()
    try:
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)

        # Il bottone può comparire con un po' di ritardo (rendering JS)
        wake = page.get_by_role(
            "button", name=re.compile("get this app back up", re.I)
        )
        try:
            wake.wait_for(state="visible", timeout=15000)
            print("App addormentata: clicco il bottone di risveglio.")
            wake.click()
            # Il bottone deve sparire, altrimenti il risveglio non è partito
            wake.wait_for(state="hidden", timeout=60000)
        except PWTimeout:
            print("Nessun bottone di risveglio: l'app era già sveglia.")

        # L'app (anche dopo il risveglio) deve caricarsi davvero
        page.wait_for_selector('[data-testid="stApp"]', timeout=180000)

        # Se è ancora visibile la schermata di sospensione, è un fallimento
        if page.get_by_text("gone to sleep", exact=False).count() > 0:
            raise RuntimeError("La schermata di sospensione è ancora visibile.")

        # Tiene aperta la sessione per far registrare il traffico
        page.wait_for_timeout(15000)
        print(f"Ping eseguito con successo su: {URL}")
    finally:
        browser.close()


def run():
    with sync_playwright() as p:
        for n in range(1, TENTATIVI + 1):
            try:
                ping(p)
                return
            except Exception as e:
                print(f"Tentativo {n}/{TENTATIVI} fallito: {e}")
                if n < TENTATIVI:
                    time.sleep(20)
    sys.exit(1)


if __name__ == "__main__":
    run()

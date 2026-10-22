import re
import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

URL = "https://wild-data.streamlit.app"
TENTATIVI = 2


def stato(page, etichetta, n):
    """Stampa cosa vede il browser e salva uno screenshot per il debug."""
    try:
        page.screenshot(path=f"debug_{n}_{etichetta}.png", full_page=True)
    except Exception as e:
        print(f"  (screenshot fallito: {e})", flush=True)
    try:
        testo = page.inner_text("body", timeout=5000)[:400].replace("\n", " | ")
    except Exception:
        testo = "(testo non leggibile)"
    print(f"[{etichetta}] url={page.url}\n  testo: {testo}", flush=True)


def ping(p, n):
    browser = p.chromium.launch()
    try:
        page = browser.new_page()
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            stato(page, "dopo_goto", n)

            wake = page.get_by_role(
                "button", name=re.compile("get this app back up", re.I)
            )
            try:
                wake.wait_for(state="visible", timeout=15000)
                trovato = True
            except PWTimeout:
                trovato = False

            if trovato:
                print("Bottone trovato: clicco.", flush=True)
                wake.click()
                wake.wait_for(state="hidden", timeout=60000)
                print("Bottone sparito.", flush=True)
                stato(page, "dopo_click", n)
            else:
                print("Nessun bottone di risveglio.", flush=True)

            page.wait_for_selector('[data-testid="stApp"]', timeout=120000)

            if page.get_by_text("gone to sleep", exact=False).count() > 0:
                raise RuntimeError("Schermata di sospensione ancora visibile.")

            page.wait_for_timeout(15000)
            stato(page, "finale", n)
            print(f"Ping eseguito con successo su: {URL}", flush=True)
        except Exception:
            stato(page, "errore", n)
            raise
    finally:
        browser.close()


def run():
    with sync_playwright() as p:
        for n in range(1, TENTATIVI + 1):
            try:
                ping(p, n)
                return
            except Exception as e:
                print(f"Tentativo {n}/{TENTATIVI} fallito: {e}", flush=True)
                if n < TENTATIVI:
                    time.sleep(20)
    sys.exit(1)


if __name__ == "__main__":
    run()

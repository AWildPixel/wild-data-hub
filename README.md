# 🐾 Wild Data #01 — Sequestri Esotici CITES Italia

Analisi dati e dashboard interattiva sulle rotte di importazione di specie esotiche CITES verso l'Italia (2013-2023). 

🌐 **Web App Interattiva:** [Accedi alla Dashboard](https://wilddata-sequestri-esotici-cites-italia.streamlit.app)

---

## 📌 Context & Scope
Il progetto nasce per verificare empiricamente i flussi di commercio esotico verso l'Italia, mettendo a confronto i dati ufficiali delle importazioni autorizzate con le registrazioni dei sequestri e delle confische doganali.

### Key Insights
* **Dominanza Tassonomica:** A fronte di una forte attenzione mediatica sui mammiferi, il sommerso intercettato alle dogane italiane riguarda in larga prevalenza la classe dei **Rettili**.
* **Provenienza dei Sequestri:** Il maggior volume di confische ufficialmente registrate verso l'Italia proviene dagli **Stati Uniti**, principale hub mondiale di allevamento e collezionismo esotico.

---

## 📊 Data Source & Methodology
* **Fonte Dati:** [CITES Trade Database](https://trade.cites.org/) (2013-2023).
* **Filtri applicati:** Paese importatore = Italia (`IT`).
* **Segregazione:** Classificazione delle transazioni in *Legali* (tutti i codici di provenienza standard) vs *Sequestri/Confische* (`Source == 'I'`).

---

## 🛠️ Tech Stack
* **Python** (Pandas, Plotly, Country Converter)
* **Streamlit** (Messa in produzione della Web App)

---

## 👤 Credits & Author
Progetto ideato e sviluppato per **A Wild Pixel** nell'ambito del format **Wild Data**.


import pandas as pd

# Carica il dataset
df = pd.read_csv('cites.csv', low_memory=False)

# Filtra solo le righe relative ai sequestri
df_illegale = df[df['Source'] == 'I']

# Raggruppa e conta per Classe e Specie (Taxon)
conteggio = df_illegale.groupby(['Class', 'Taxon']).size().reset_index(name='Count')

# Ordina dal più grande al più piccolo e prendi le prime 3 specie per classe
top_specie = conteggio.sort_values(['Class', 'Count'], ascending=[True, False])
top_3_per_classe = top_specie.groupby('Class').head(3)

# Stampa il risultato
print(top_3_per_classe.to_string(index=False))

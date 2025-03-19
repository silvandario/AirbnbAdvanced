# Die Dateien airbnb_listings_oa_clean.csv und airbnb_listings_oa_clean.csv aneinanderhängen. 
# Spalten Name, Preis, Links und neu bezeichnung Open Air für oa oder Olma für olm   

import pandas as pd

# Dateien einlesen
df_oa = pd.read_csv("airbnb_listings_oa_clean.csv")
df_olm = pd.read_csv("airbnb_listings_olm_clean.csv")

# Event Spalte
df_oa["Event"] = "Open Air"
df_olm["Event"] = "OLMA"

# Neues concat df
df = pd.concat([df_oa, df_olm], ignore_index=True)

#§ Bereinigte Datei speichern
df.to_csv("airbnb_listings_concat.csv", index=False)
print("Aneinanderhängen abgeschlossen. Datei gespeichert als airbnb_listings_concat.csv")



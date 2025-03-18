import pandas as pd
import re

# Datei einlesen
df = pd.read_csv("airbnb_listings.csv", names=["Name", "Preis", "Links"], skiprows=1)

# Funktion zur Bereinigung der Preisangaben
def clean_price(price):
    if isinstance(price, str):
        return re.sub(r'<.*?>', '', price).strip()
    return price

# "Preis" Spalte bereinigen
df["Preis"] = df["Preis"].apply(clean_price)

# Bereinigte Datei speichern
df.to_csv("airbnb_clean.csv", index=False)

print("Bereinigung abgeschlossen. Datei gespeichert als airbnb_clean.csv")

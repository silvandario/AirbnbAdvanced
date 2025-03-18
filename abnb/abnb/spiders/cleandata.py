import pandas as pd
import re

# Datei einlesen
df = pd.read_csv("airbnb_listings_oa.csv", names=["Name", "Preis", "Links"], skiprows=1)

# Funktion zur Bereinigung der Preisangaben
def clean_price(price):
    if isinstance(price, str):
        # Entferne HTML-Tags
        clean_text = re.sub(r'<.*?>', '', price).strip()
        # Extrahiere den reinen Preiswert vor dem "x"
        match = re.search(r'(\d+\s*CHF)', clean_text)
        if match:
            return match.group(1)  # Gibt nur den Preis mit "CHF" zurück
    return price

# "Preis" Spalte bereinigen
df["Preis"] = df["Preis"].apply(clean_price)

# Bereinigte Datei speichern
df.to_csv("airbnb_listings_oa_celan_test.csv", index=False)

print("Bereinigung abgeschlossen. Datei gespeichert als airbnb_clean.csv")
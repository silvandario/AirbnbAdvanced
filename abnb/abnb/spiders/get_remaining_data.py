import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Datei einlesen
df = pd.read_csv("airbnb_listings.csv", names=["Name", "Preis", "Links"], skiprows=1)

# Funktion zur Bereinigung der Preisangaben
def clean_price(price):
    if isinstance(price, str):
        cleaned = re.sub(r'<.*?>', '', price).strip()
        if cleaned == "" or "button" in cleaned or "span" in cleaned:
            return None  # Mark as missing to be re-fetched
        return cleaned
    return price

# "Preis" Spalte bereinigen
df["Preis"] = df["Preis"].apply(clean_price)

# Konfiguration für den Selenium Webdriver
options = Options()
options.add_argument("--headless")  # Browser im Hintergrund laufen lassen
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Webdriver initialisieren
driver = webdriver.Chrome(options=options)

def fetch_price(url):
    try:
        driver.get(url)
        time.sleep(5)  # Wartezeit für das Laden der Seite
        
        # Versuche, den Preis auszulesen
        price_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "(//span[contains(@class,'_18x3iiu')])[1]"))
        )
        
        price = price_element.get_attribute("innerHTML").replace("&nbsp;", " ").strip()
        price = price.split("x")[0].replace("CHF", "CHF").strip()
        return price if "button" not in price else None
    except Exception:
        return None

# Fehlende oder fehlerhafte Preise ergänzen
for index, row in df.iterrows():
    if not isinstance(row["Preis"], str) or not row["Preis"].strip():
        print(f"Preis fehlt oder fehlerhaft für {row['Name']}, hole nach...")
        df.at[index, "Preis"] = fetch_price(row["Links"])

# "Preis" Spalte erneut bereinigen
df["Preis"] = df["Preis"].apply(clean_price)

# Datei speichern
df.to_csv("final.csv", index=False)

# Browser schließen
driver.quit()

print("Datenbereinigung abgeschlossen. Datei gespeichert als final.csv")

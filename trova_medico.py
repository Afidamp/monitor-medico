# Test per attivare GitHub Actions

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib
from email.mime.text import MIMEText

# Configurazione Email (MODIFICA QUESTI DATI)
EMAIL_SENDER = "lorenzo.divita@gmail.com"
EMAIL_PASSWORD = "aimm rgxb vsjn mjli"
EMAIL_RECEIVER = "lorenzo.divita@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# URL della pagina ATS Milano
URL = "https://www.ats-milano.it/trova-medico"
CODICE_REGIONALE = "34019"

# Imposta il WebDriver per Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configura Chrome per girare in modalità headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Modalità senza interfaccia grafica
chrome_options.add_argument("--no-sandbox")  # Necessario per eseguire in ambienti remoti
chrome_options.add_argument("--disable-dev-shm-usage")  # Evita problemi di memoria
chrome_options.add_argument("--disable-gpu")  # Non serve in modalità headless

# Inizializza il driver con le nuove opzioni
driver = webdriver.Chrome(service=Service(), options=chrome_options)


def invia_email():
    """Invia una notifica via email quando il medico ha posti disponibili"""
    try:
        msg = MIMEText(f"✅ La Dott.ssa Laura Forsali ha posti disponibili!\n\nControlla il sito ATS: {URL}")
        msg["Subject"] = "⚠️ Disponibilità Medico Trovata!"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("📧 Email inviata con successo!")
    except Exception as e:
        print(f"❌ Errore nell'invio dell'email: {e}")

def check_disponibilita():
    """Controlla se il medico ha disponibilità leggendo il semaforo con Selenium"""
    
    # Apri il sito ATS
    driver.get(URL)
    
    # Aspetta che il campo di ricerca sia visibile
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "codice_medico"))
    )

    # Inserisce il codice medico e avvia la ricerca
    search_box.send_keys(CODICE_REGIONALE)
    search_box.send_keys(Keys.RETURN)

    # Aspetta il caricamento del risultato
    time.sleep(5)

    try:
        # Controlla se esiste un semaforo verde
        semaforo_verde = driver.find_element(By.XPATH, "//img[contains(@src, 'verde')]")
        print("🟢 La Dott.ssa Laura Forsali ha posti disponibili!")
        invia_email()  # Invia l'email
    except:
        print("🔴 Nessuna disponibilità trovata.")

    # Chiudi il browser
    driver.quit()

# Esegui il controllo
check_disponibilita()

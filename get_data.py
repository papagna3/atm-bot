import selenium
from selenium import webdriver
import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def alert_dx(driver):
    # Scraping alert in alto a dx
    global txt_alert
    # inizializzo txt_alert
    txt_alert = {"alert_title": None, "alert_ctext": None}
    try:
        # Attendo che l'alert sia visualizzabile e cliccabile
        alert_main = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Alert_MainDiv')))
        alert_main.click()

        # Attendo che il contenuto dell'alert sia visibile
        alert_content = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'Alert_m_contenuto')))

        # Estrae il titolo
        alert_title = driver.find_element(By.CLASS_NAME, 'Alert_m_Titolo').text
        txt_alert['alert_title'] = alert_title

        # Estrae i paragrafi nel contenuto dell'alert
        alert_content = driver.find_element(By.CLASS_NAME, 'content').text
        txt_alert['alert_ctext'] = alert_content

        # close the alert window
        alert_close = driver.find_element(By.ID, 'Alert_m_chiudi')
        alert_close.click()

    except selenium.common.TimeoutException:
        pass
    finally:
        return txt_alert

def M_status(driver):
    # Scraping Stato Metro a dx
    global metro_status, general_message

    try:
        # Attendo che la tabella sia visibile
        status_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'StatusLinee')))

        # Trova tutte le righe della tabella che contengono le informazioni delle linee
        rows = status_table.find_elements(By.TAG_NAME, 'tr')
		
        metro_status = {
            "M1": None,
            "M2": None,
            "M3": None,
            "M4": None,
            "M5": None,
            "general_message": None
        }
        
        # Per ogni riga ottengo nome e stato
        for row in rows:
            try:
                # Estrai il nome della linea dal tag 'img' (ad esempio, M1, M2, ecc.)
                line_img = row.find_element(By.CLASS_NAME, 'StatusLinee_img')
                line_name = line_img.get_attribute('alt')  # Nome della linea (M1, M2, etc.)

                # Estrai lo stato della linea
                line_status = row.find_element(By.CLASS_NAME, 'StatusLinee_StatoScritta').text

                # Aggiungi il risultato alla dict
                metro_status[line_name] = line_status
            except:
                # Passa la riga se non contiene lo stato della linea (ad esempio, messaggio generale)
                continue

        # Cerca il messaggio generale (se presente)
        try:
            general_message = driver.find_element(By.CLASS_NAME, 'StatusLinee_Mex_Testo').text
            metro_status["general_message"] = general_message
        except selenium.common.TimeoutException:
            metro_status["general_message"] = None

    finally:
        return metro_status

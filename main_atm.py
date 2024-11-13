#!/usr/bin/env python3

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import get_data, check_update, telegram_sender
import json
import os
import datetime

last_update_path = "last_update.json"
Private_id = ADD HERE YOUR PRIVATE TG ID 


options = Options()
options.add_argument('--headless')  
options.add_argument('--no-sandbox')



while True:
    # Force data reset
    reset_data = False
    # Initialize log file
    with open("log_out.txt", "w") as text_file:
        text_file.write("Log Message:\n")

    # check last update
    reset_data = check_update.check_last_update(last_update_path, reset_data)

    # AGGIUNGI service=service
    driver = webdriver.Firefox(options=options)
    url = 'https://www.atm.it/it/Pagine/default.aspx'
    driver.get(url)

    # get data from alert
    alert_txt = get_data.alert_dx(driver)

    # get data from M status
    metro_status = get_data.M_status(driver)
    driver.close()

    if alert_txt and metro_status:
        check_update.append_log("Data received correctly...")

    # check if there's an update
    time.sleep(3)
    updated = check_update.check_if_update(alert_txt, metro_status, reset_data)

    if updated:
        # write last update
        print("Running Update Procedure")
        check_update.append_log("Update Procedure Running...")
        write_update = {
            "year": int(datetime.datetime.now().year),
            "month": int(datetime.datetime.now().month),
            "day": int(datetime.datetime.now().day),
            "hour": int(datetime.datetime.now().hour),
            "minute": int(datetime.datetime.now().minute)
        }
        check_update.initialize_file(last_update_path)
        ok_write_update = check_update.check_procedure(write_update, last_update_path, reset=True)

        print(f'UPDATED - {write_update["day"]}/{write_update["month"]}/{write_update["year"]} - {write_update["hour"]}:{write_update["minute"]}')
        check_update.append_log(f'UPDATED - {write_update["day"]}/{write_update["month"]}/{write_update["year"]} - {write_update["hour"]}:{write_update["minute"]}')

        time.sleep(2)
        # Calling Message Handler
        telegram_sender.message_handler()

    # Sending logs to private chat
    if Private_id:
        with open("log_out.txt", "r") as text_file:
            mex = text_file.read()
        telegram_sender.send_to_telegram(mex, Private_id)
    print("")
    time.sleep(10)








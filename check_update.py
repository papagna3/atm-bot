import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import datetime

path_alert = "Alert_status.json"
path_metro = "M_status.json"


def append_log(log_text):
    with open("log_out.txt", "a") as text_file:
        text_file.write(log_text + "\n")

def initialize_file(path):
    # Se il file esiste, inizializzalo con un dizionario vuoto
    if os.path.exists(path):
        with open(path, 'w') as f:
            json.dump({}, f)

def load_prev_status(filepath):
    # Load previous status
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            initialize_file(filepath)
            return {}

def load_json(filepath):
    # Load json
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}


def save_current_status(data, filepath):
    # Save new status in JSON file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def compare_status(prev, new):
    # Cfr new and old status
    return new != prev

def check_procedure(data, path, reset):
    if reset:
        initialize_file(path)
    current_status = data
    prev_status = load_prev_status(path)
    if compare_status(current_status, prev_status):
        append_log("Change detected... Updating...")
        save_current_status(data, path)
        return True
    else:
        append_log("No change detected...")


def check_if_update(alert_data, metro_data, reset):
    # checking if needs update
    update1 = False
    update2 = False
    update1 = check_procedure(alert_data, path_alert, reset)
    update2 = check_procedure(metro_data, path_metro, reset)
    update = update1 or update2
    return update

def check_last_update(path, reset):
    # If reset True -> no check needed
    if reset:
        print("check_last_update: Forced Reset detected... Updating...")
        append_log("check_last_update: Forced Reset detected... Updating...")
        return True
    if os.path.exists(path) and os.path.getsize(path) < 1:
        print("check_last_update: Update file empty... Updating...")
        append_log("check_last_update: Update file empty... Updating...")
        return True

    prev = load_prev_status(path)
    dt_prec = datetime.datetime(year=prev['year'], month=prev['month'], day=prev['day'], hour=prev['hour'], minute=prev['minute'])
    dt_now = datetime.datetime.now()
    dt_diff = dt_now - dt_prec

    if dt_diff.seconds >= 3600:
        print("check_last_update: More than 1H passed - Updating...")
        append_log("check_last_update: More than 1H passed - Updating...")
        return True
    return False
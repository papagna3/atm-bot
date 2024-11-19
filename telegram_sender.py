import requests
import check_update
import re


path_alert = "Alert_status.json"
path_metro = "M_status.json"
path_update = "last_update.json"

apiToken = YOUR API TOKEN (TG BOT)
Private_id =  ADD HERE YOUR PRIVATE TG ID 
Channel_ID =  ADD HERE YOUR CHANNEL TG ID 

apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

def send_to_telegram(message, chatID):
    try:
        check_update.append_log("send_to_telegram: sending...")
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

def format_alert(alert):
    if alert.get("alert_title") or alert.get("alert_ctext"):
        alert_message = "⚠️ UPDATE ⚠️\n"
        if alert.get("alert_title"):
            alert_message += f"{alert['alert_title']}\n"
        if alert.get("alert_ctext"):
            alert_message += f"{alert['alert_ctext']}\n"

        # Aggiungi un '\n' se c'è solo uno alla volta
        alert_message = re.sub(r'(?<!\n)\n(?!\n)', '\n\n', alert_message)

        # Aggiungi '\t•' se una riga inizia con un numero dopo un '\n'
        alert_message = re.sub(r'\n(\d)', r'\n\t• \1', alert_message)

        # Aggiungi '\t•' se una riga inizia con tram, Tram, bus o Bus dopo un '\n'
        alert_message = re.sub(r'\n(tram|Tram|bus|Bus)', r'\n\t• \1', alert_message)
        
        return alert_message
    return ""


def format_metro_status(metro):
    """Crea la sezione dello stato della metro."""
    status_message = "🚇 Metro Status:\n\n"
    status_icons = {"Regolare": "🟢", "Rallentata": "🟡", "Chiusa": "🔴", "Tratta sospesa":"🟠"}

    for i in range(1, 6):
        line_status = metro.get(f"M{i}")
        if line_status:
            icon = status_icons.get(line_status, "")
            status_message += f"M{i} - {line_status} {icon}\n"

    if metro.get("general_message"):
        status_message += f"\nMetro Info:\n{metro['general_message']}\n"

    return status_message


def message_generator(alert, metro):
    """Genera il messaggio completo combinando alert e stato della metro."""
    message = format_alert(alert) + format_metro_status(metro)
    return message


def message_handler():
    check_update.append_log("--- Message Handler ---")
    # get data from json
    alert = check_update.load_json(path_alert)
    metro = check_update.load_json(path_metro)
    log_update = check_update.load_json(path_update)

    # generate message for channel
    check_update.append_log("Generating messages...")
    message = message_generator(alert, metro)

    # Send message to channel
    send_to_telegram(message, Channel_ID)

    # Adding message logs
    check_update.append_log(f"Message sent! \n{log_update['day']}/{log_update['month']}/{log_update['year']} - {log_update['hour']}:{log_update['minute']}")








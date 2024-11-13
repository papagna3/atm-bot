Here's an example of a README in English for your project:

---

# ATM Bot - Public Transport Updates Monitoring

This project implements a bot to monitor real-time notifications related to public transportation service updates, disruptions, and schedule changes. It sends alerts on issues affecting metro and bus lines via Telegram.

## Features

- **Live Notifications Monitoring**: Retrieves real-time service notifications regarding disruptions, closures, and other advisories for public transport lines.
- **Telegram Notifications**: Automatically sends notifications via a Telegram bot to keep users informed about delays or other service issues.
- **Update Logging**: Saves each update to a JSON file to create a historical log and track the frequency of alerts.

## Project Structure

- `main_atm.py`: Main script to run the bot.
- `get_data.py`: Retrieves and formats current updates for the notifications.
- `check_update.py`: Checks update frequency to avoid duplicate notifications.
- `telegram_sender.py`: Manages sending notifications through the Telegram bot.
- `log_update.json`: JSON file used to store the date and time of the last update.

## Setup

### Prerequisites

Ensure you have the following Python libraries installed:
- `selenium`
- `datetime`
- `json`

Install dependencies with:
```bash
pip install selenium
```

### Telegram Setup

1. Create a bot on Telegram using [BotFather](https://core.telegram.org/bots).
2. Obtain the bot API token.
3. Add this token to `telegram_sender.py` to allow the bot to send notifications.

### JSON Configuration Example

The `log_update.json` file is used to store the date and time of the last update. Initialize it as follows:

```json
{
  "date": null,
  "hour": null,
  "minute": null,
  "second": null
}
```

When a new update is detected, the bot will automatically update this file with the current date and time.

## Running the Bot

To run the bot:

```bash
python main_atm.py
```

### Example Output

The bot will send Telegram notifications similar to the following:

```
⚠️ UPDATE ⚠️
Tram 12. Service interrupted between Piazza Emilia and Viale Molise (vehicle accident). Please use bus 66 as an alternative.

Expect longer wait times for the following lines:
84, 85, 94, and B12 (traffic and roadworks)
321 and 352 (private vehicle accident)
🅿️ Park-and-Ride: Maciachini, Abbiategrasso, and Bovio parking lots are currently full.
```

## Customization

Modify `check_update.py` to adjust the time interval between update checks. You can also edit the `message_generator` function in `telegram_sender.py` to change the format of the messages sent.

## Contributing

Feel free to fork this repository, open issues, or submit pull requests to improve the project. Contributions are always welcome!

---

### License

This project is licensed under the MIT License.

---

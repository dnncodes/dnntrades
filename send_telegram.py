import requests

TELEGRAM_TOKEN = "7054861876:AAFYYltoxKjwogz9zQ5IoQdGeyC5ZKS9pDY"
CHAT_ID = "6901249827"

def send_telegram_message(signal_data):
    # Message format for the Telegram channel
    message = f"""
    <b>A 3 to 5-Minutes Scalping Trade-Shot</b>

    <b>Signal:</b> {signal_data['signal']}
    <b>Market Asset:</b> {signal_data['market_asset']}
    <b>Price:</b> {signal_data['price']}
    <b>Time:</b> {signal_data['time']}

    <i>In-depth Price Action Technical Analysis with Smart Money Concept</i>
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Message sent to Telegram successfully.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while sending message to Telegram: {e}")

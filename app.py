from flask import Flask, jsonify, render_template
import asyncio
import threading
import datetime
from deriv_api import DerivAPI
from send_telegram import send_telegram_message  # Assuming you have this module for Telegram messaging

app = Flask(__name__)

# List of volatility markets
volatility_markets = [
    "R_10", "R_25", "R_50", "R_75", "R_100",  
    "R_10S", "R_25S", "R_50S", "R_75S", "R_100S"
]

# Signal data to be sent to the frontend and Telegram
signal_data = {
    "signal": "Loading...",
    "market_asset": "Loading...",
    "price": "Loading...",
    "time": "Loading..."
}

async def subscribe_to_markets(api):
    try:
        for market in volatility_markets:
            # Subscribing to ticks for the market
            source_tick = await api.subscribe({'ticks': market})
            # Using RxPy to handle the ticks
            source_tick.subscribe(lambda tick: handle_tick_data(tick, market))
    except Exception as e:
        print(f"Error subscribing to market ticks: {e}")

def handle_tick_data(tick, market):
    global signal_data

    # Processing the tick data and checking signal conditions
    # Replace this with your logic to check for trading signals
    signal = check_signal_conditions(tick, market)
    
    if signal:
        signal_data = {
            "signal": signal,
            "market_asset": market,
            "price": tick['tick']['quote'],
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Send signal to Telegram
        send_telegram_message(signal_data)
        print(f"Signal sent: {signal_data}")

def check_signal_conditions(tick, market):
    # Add your conditions to check for signals here
    # For now, this is just a placeholder that always returns "buy"
    return "buy"

async def connect_deriv():
    try:
        # Initialize the Deriv API with endpoint and app_id
        api = DerivAPI(endpoint='wss://ws.binaryws.com/websockets/v3', app_id=1234)
        
        # Subscribe to the markets
        await subscribe_to_markets(api)

    except Exception as e:
        print(f"An error occurred: {e}")

def start_websocket_thread():
    asyncio.run(connect_deriv())

# Start the websocket thread
ws_thread = threading.Thread(target=start_websocket_thread)
ws_thread.start()

@app.route('/')
def index():
    return render_template('technical-signal.html')

@app.route('/get_signal')
def get_signal():
    return jsonify(signal_data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

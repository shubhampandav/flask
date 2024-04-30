from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta
from waitress import serve

app = Flask(__name__)
CORS(app)

# Define a dictionary to store authorized API keys
authorized_keys = {
    "12f5f96f-6b51-4b4a-9bf9-b23e6d728b39": "admin"
}

# Variable to store the latest updated price
latest_updated_price = None
last_updated_time = None

def calculate_resistance_support(latest_updated_price):
    resistance1 = (latest_updated_price ** 0.5 + 0.125) ** 2
    resistance2 = (latest_updated_price ** 0.5 + 0.25) ** 2
    resistance3 = (latest_updated_price ** 0.5 + 0.5) ** 2
    support1 = (latest_updated_price ** 0.5 - 0.125) ** 2
    support2 = (latest_updated_price ** 0.5 - 0.25) ** 2
    support3 = (latest_updated_price ** 0.5 - 0.5) ** 2
    return resistance1, resistance2, resistance3, support1, support2, support3

def update_latest_price(stock_name):
    global latest_updated_price, last_updated_time
    if datetime.now().weekday() < 5:  # Check if it's a weekday (Mon-Fri)
        now = datetime.now()
        if now.hour == 10 and now.minute >= 2:  # Check if it's 3:40 PM or later
            stock = yf.Ticker(stock_name)  # Example stock symbol, replace with the desired symbol
            latest_updated_price = stock.history(period='1d')['Close'].iloc[-1]
            last_updated_time = now

@app.route('/stock', methods=['GET'])
def get_stock_price():
    api_key = request.args.get('api_key')
    if api_key not in authorized_keys:
        return jsonify({'error': 'Unauthorized access'}), 401

    stock_name = request.args.get('name')
    if not stock_name:
        return jsonify({'error': 'Stock name not provided'}), 400

    try:
        global latest_updated_price, last_updated_time
        update_latest_price(stock_name)  # Pass stock_name to the function

        # Calculate resistance and support levels
        resistance1, resistance2, resistance3, support1, support2, support3 = calculate_resistance_support(latest_updated_price)

        return jsonify({
            'stock_name': stock_name,
            'latest_updated_price': latest_updated_price,  # Return the latest updated price
            'resistance1': resistance1,
            'resistance2': resistance2,
            'resistance3': resistance3,
            'support1': support1,
            'support2': support2,
            'support3': support3
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use Waitress as the production WSGI server
    serve(app, host='0.0.0.0', port=50100)

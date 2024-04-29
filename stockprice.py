from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta
from waitress import serve

app = Flask(__name__)
CORS(app)

@app.route('/stock', methods=['GET'])
def get_stock_price():
    stock_name = request.args.get('name')
    if not stock_name:
        return jsonify({'error': 'Stock name not provided'}), 400

    try:
        stock_data = yf.Ticker(stock_name)
        # Fetch data for the last two trading days
        historical_data = stock_data.history(period='2d')
        # Extract the closing price for the previous trading day
        previous_close = historical_data.iloc[-2]['Close']
        return jsonify({'stock_name': stock_name, 'previous_close': previous_close})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use Waitress as the production WSGI server
    serve(app, host='0.0.0.0', port=50100)

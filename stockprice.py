from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS from the flask_cors extension
import yfinance as yf
from waitress import serve

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in your Flask app

@app.route('/nse-stock-data')
def get_nse_stock_data():
    stock_name = request.args.get('stock_name')
    if not stock_name:
        return jsonify({'error': 'Stock name parameter is missing.'}), 400
    
    nse_stock = f"{stock_name.upper()}.NS"

    try:
        stock = yf.Ticker(nse_stock)
        price = stock.history(period='1d')['Close'].iloc[-1]
        return jsonify({'stock_name': stock_name, 'price': price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=50100)

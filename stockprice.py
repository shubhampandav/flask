from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

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


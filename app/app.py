from flask import Flask, render_template, request
import pandas as pd
from functions import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    df_filtered = None
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        if company_name:
            df_filtered = df_stock(company_name)
            df_filtered = df_filtered.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries for easy rendering

    return render_template('index.html', df_filtered=df_filtered)

@app.route('/ticker', methods=['GET', 'POST'])
def ticker():
    stock_info = None
    latest_news = None
    if request.method == 'POST':
        ticker_name = request.form.get('ticker_name')
        if ticker_name:
            stock_info = get_stock_info(ticker_name)
            long_name = stock_info['Name']
            latest_news = get_company_news(long_name,ticker_name)
            print("done")
    return render_template('ticker.html', 
                                stock_info=stock_info, 
                                latest_news=latest_news)

if __name__ == '__main__':
    app.run(debug=True)
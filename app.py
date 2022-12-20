import yfinance as yf
from flask import Flask, render_template, request
import matplotlib.pyplot as plt

from stocker import Stocker

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    code = request.form['code']
    price = yf.Ticker(code + '.TW').history(period='max').Close.tz_localize(None)
    tsmc = Stocker(price)
    model, model_data, fig = tsmc.create_prophet_model(days=90)
    # tsmc.evaluate_prediction()
    # tsmc.changepoint_prior_analysis(changepoint_priors=[0.001, 0.05, 0.1, 0.2])
    # tsmc.predict_future(days=100)
    return render_template('result.html', code=code)


if __name__ == '__main__':
    app.run()

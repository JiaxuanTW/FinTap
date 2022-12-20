import yfinance as yf
from flask import Flask, render_template, request

from stocker import Stocker
from utils import generate_fig_data

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    code = request.form['code']
    stock = yf.Ticker(code + '.TW').history(period='max')

    if stock.empty:
        # No stock with this code found
        return render_template('error.html', code=code)

    price = stock.Close.tz_localize(None)
    stocker = Stocker(price)
    model, model_data, model_fig = stocker.create_prophet_model(days=90)
    eval_predict_fig = stocker.evaluate_prediction()
    prior_analysis_fig = stocker.changepoint_prior_analysis(changepoint_priors=[0.001, 0.05, 0.1, 0.2])
    future_predict_fig = stocker.predict_future(days=100)

    model_fig = generate_fig_data(model_fig)
    eval_predict_fig = generate_fig_data(eval_predict_fig)
    prior_analysis_fig = generate_fig_data(prior_analysis_fig)
    future_predict_fig = generate_fig_data(future_predict_fig)

    return render_template('result.html', code=code, model_fig=model_fig, eval_predict_fig=eval_predict_fig,
                           prior_analysis_fig=prior_analysis_fig, future_predict_fig=future_predict_fig)


if __name__ == '__main__':
    app.run()

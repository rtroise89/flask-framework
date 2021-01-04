from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io, base64
from alpha_vantage.timeseries import TimeSeries
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

#Routing, tying URL to function. Needs a return value
@app.route('/')
def index():
    title = "Richard's App"
    return render_template("index.html", title=title)

@app.route('/graph', methods=["POST"])
def graph():
    api_key = 'MWDBRJVDC3PYQZEC'
    stock = request.form.get("stock")
    choice = request.form.get("features")
    title = "Richard's App"
    ts = TimeSeries(key=api_key, output_format='pandas')
    #Collect data depending on user's stock and price choices
    if choice=='close':
        data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
        df = pd.DataFrame(data['4. close'])
    elif choice=='adj_close':
        data, meta_data = ts.get_daily_adjusted(symbol=stock, outputsize='full')
        df = pd.DataFrame(data['5. adjusted close'])
    elif choice=='open':
        data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
        df = pd.DataFrame(data['1. open'])
    elif choice=='adj_open':
        data, meta_data = ts.get_daily_adjusted(symbol=stock, outputsize='full')
        df = pd.DataFrame(data['1. open'])

    #Plot the pandas dataframe
    img = io.BytesIO()
    plt.plot(df)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template("graph.html", url=plot_url, stock=stock, choice=choice)

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    return render_template("exception.html", e=e), 500


if __name__ == "__main__":
    app.run(debug=True)

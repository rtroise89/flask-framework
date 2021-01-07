from flask import Flask, render_template, request
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from werkzeug.exceptions import HTTPException
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas_bokeh

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

    p = figure(width=600, height=400, x_axis_type='datetime')
    #Collect data depending on user's stock and price choices
    if choice=='close':
        data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
        data['date_time'] = data.index
        p.line(data['date_time'], data['4. close'], line_width=2)
    elif choice=='adj_close':
        data, meta_data = ts.get_daily_adjusted(symbol=stock, outputsize='full')
        data['date_time'] = data.index
        p.line(data['date_time'], data['5. adjusted close'], line_width=2)
    elif choice=='open':
        data, meta_data = ts.get_daily(symbol=stock, outputsize='full')
        data['date_time'] = data.index
        p.line(data['date_time'], data['1. open'], line_width=2)


    script, div = components(p)

    return render_template("graph.html", div=div, script=script, stock=stock, choice=choice)

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    return render_template("exception.html", e=e), 500


if __name__ == "__main__":
    app.run(debug=True)

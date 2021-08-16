from flask import Flask, render_template
from flask_socketio import SocketIO

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.layouts import gridplot
from plots import covid

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/daily_total")
def daily_total():
    return 23

@app.route('/')
def index():
    global dataset
    fig1 = dataset.cases_graph()
    fig2 = dataset.vaccines_graph()
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components({"fig1":fig1, "fig2":fig2})
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html

if __name__ == "__main__":
    metrics = ["newCasesBySpecimenDate", "newPeopleVaccinatedCompleteByVaccinationDate"]
    endpoint = "https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric={metrics}&format=json".format(metrics="&metric=".join(metrics))
    dataset = covid(endpoint)
    socketio.run(app)

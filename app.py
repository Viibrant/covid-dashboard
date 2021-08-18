from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.layouts import row
from plots import covid

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on("loaded")
def loaded():
    global dataset
    national_new_cases = dataset.get_newcases_nationally()["cases"][-1]
    print(national_new_cases)
    emit(national_new_cases)

@app.route('/')
def index():
    global dataset
    cases = dataset.cases_graph()
    vaccines = dataset.vaccines_graph()
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components({"cases": cases, "vaccines": vaccines})
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
    socketio.run(app, debug=True)

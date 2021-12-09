from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import pandas as pd
import json
import plotly
import plotly.express as px
from plots import covid

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on("loaded")
def loaded():
    global dataset
    national_new_cases = dataset.get_newcases_nationally()["cases"][-1]
    print(national_new_cases)
    emit(national_new_cases)


@app.route("/")
def index():
    fig = dataset.cases_graph()
    plotly_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", plotly_json=plotly_json)


if __name__ == "__main__":
    metrics = ["newCasesBySpecimenDate", "newPeopleVaccinatedCompleteByVaccinationDate"]
    endpoint = "https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric={metrics}&format=json".format(
        metrics="&metric=".join(metrics)
    )
    dataset = covid(endpoint)
    socketio.run(app, debug=True)

from flask import Flask, render_template
from plots import plot_obj
import json
import plotly

app = Flask(__name__)

metrics = "&metric=".join(["newCasesBySpecimenDate", "newPeopleVaccinatedCompleteByVaccinationDate"])
endpoint = f"https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric={metrics}&format=json"


dataset = plot_obj(endpoint)

@app.route("/")
def index():
    case_fig = dataset.cases_graph()
    cases = json.dumps(case_fig, cls=plotly.utils.PlotlyJSONEncoder)

    vaccine_fig = dataset.full_vaccines_graph()
    vaccines = json.dumps(vaccine_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", cases=cases, vaccines=vaccines)


if __name__ == "__main__":
    app.run(app, use_reloader=False, passthrough_errors=True)

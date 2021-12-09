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
    fig = dataset.cases_graph()
    plotly_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", plotly_json=plotly_json)


if __name__ == "__main__":
    app.run(app, use_reloader=False, passthrough_errors=True)

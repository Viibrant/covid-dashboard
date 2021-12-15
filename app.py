from flask import Flask
from .plots import plot_obj
from dash import html, dcc
import plotly.express as px
import dash

server = Flask(__name__)
app = dash.Dash(name=__name__, server=server, requests_pathname_prefix="/covid/")

metrics = "&metric=".join(
    ["newCasesBySpecimenDate", "newPeopleVaccinatedCompleteByVaccinationDate"]
)
endpoint = f"https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric={metrics}&format=json"


stats = plot_obj(endpoint)

app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("NHS COVID-19 API"),
                        html.P("Visualising COVID-19 statistics with Plotly - Dash"),
                        html.P("(WORK IN PROGRESS)"),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[stats.cgraph(), stats.vgraph()],
                ),
            ],
        )
    ]
)


if __name__ == "__main__":
    app.run_server()
else:  # file is being imported
    from website import app

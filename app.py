from plots import plot_obj
from dash import html
import dash
import json
import plotly

app = dash.Dash(__name__)

metrics = "&metric=".join(
    ["newCasesBySpecimenDate", "newPeopleVaccinatedCompleteByVaccinationDate"]
)
endpoint = f"https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric={metrics}&format=json"


dataset = plot_obj(endpoint)

app.layout = html.Div(
    children=[
        html.Div(
            className="row",  # Define the row element
            children=[
                html.Div(
                    className="four columns div-user-controls"
                ),  # Define the left element
                html.Div(
                    className="eight columns div-for-charts bg-grey"
                ),  # Define the right element
            ],
        )
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)

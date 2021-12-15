from .check_file import get_dataset
from dash import dcc
import plotly.express as px
import pandas as pd


class plot_obj:
    # TODO! sort out *args for aggregate
    # TODO! vaccinations graph: 1st, 2nd ---> subplot
    def __init__(self, endpoint):
        raw_data = get_dataset(endpoint)

        self.statistics = raw_data
        self.statistics["date"] = pd.to_datetime(self.statistics["date"])

        self.latest_date = self.statistics.iloc[0]["date"].strftime("%Y-%m-%d")

    def aggregate(self, df: pd.DataFrame, x: str, y: str, *args) -> "dict[list]":
        args = list(args)
        # group all records with same dates together
        # then create a new dataframe and apply sum to all other columns
        grouped_dates = df.groupby(x)[y]
        aggregated = pd.concat(
            [grouped_dates.apply(sum), grouped_dates.count()], axis=1, keys=[x]
        )
        if len(args) == 2:
            x, y = args[0], args[1]

        # The dates column changed to row names so take all names and cast to list
        return {x: list(aggregated.index), y: aggregated[x].to_list()}

    def cgraph(self):
        df = self.aggregate(
            self.statistics, "date", "newCasesBySpecimenDate", "date", "cases"
        )
        fig = px.scatter(
            df,
            x="date",
            y="cases",
            title=f"New Cases per day as of {self.latest_date}",
            color="cases",
            trendline="lowess",
            trendline_options=dict(frac=0.1),
            template="plotly_dark",
        )

        return dcc.Graph(id="cases", figure=fig)

    def vgraph(self):
        df = self.aggregate(
            self.statistics,
            "date",
            "newPeopleVaccinatedCompleteByVaccinationDate",
            "date",
            "vaccines",
        )
        fig = px.ecdf(
            df,
            x="date",
            y="vaccines",
            ecdfnorm=None,
            title=f"People fully vaccinated as of {self.latest_date}",
            template="plotly_dark",
        )

        return dcc.Graph(id="vaccines", figure=fig)

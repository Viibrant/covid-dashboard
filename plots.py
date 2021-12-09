from check_file import get_dataset
import plotly.express as px
import pandas as pd


class plot_obj:
    def __init__(self, endpoint):
        raw_data = get_dataset(endpoint)

        self.statistics = raw_data
        self.statistics["date"] = pd.to_datetime(self.statistics["date"])

        self.latest_date = self.statistics.iloc[0]["date"].strftime("%Y-%m-%d")

    def get_newcases_nationally(self):
        # group all records with same dates together, then create a new dataframe and apply sum to all other columns
        grouped_dates = self.statistics.groupby("date").newCasesBySpecimenDate
        aggregated = pd.concat(
            [grouped_dates.apply(sum), grouped_dates.count()], axis=1, keys=["date"]
        )
        # The dates column changed to row names so take all names and cast to list
        return {"dates": list(aggregated.index), "cases": aggregated["date"].to_list()}

    def get_newvaccinations_nationally(self):
        grouped_dates = self.statistics.groupby(
            "date"
        ).newPeopleVaccinatedCompleteByVaccinationDate
        aggregated = pd.concat(
            [grouped_dates.apply(sum), grouped_dates.count()], axis=1, keys=["date"]
        )
        # The dates column changed to row names so take all names and cast to list
        return {"dates": list(aggregated.index), "cases": aggregated["date"].to_list()}

    def aggregate(self, df: pd.DataFrame, x: str, y: str, alt=(None, None)):
        # group all records with same dates together, then create a new dataframe and apply sum to all other columns
        grouped_dates = df.groupby(x)[y]
        aggregated = pd.concat(
            [grouped_dates.apply(sum), grouped_dates.count()], axis=1, keys=[x]
        )
        x = alt[0] if alt[0] != None else x
        y = alt[1] if alt[1] != None else y
        # The dates column changed to row names so take all names and cast to list
        return {x: list(aggregated.index), y: aggregated[x].to_list()}

    def cases_graph(self):
        df = self.aggregate(
            self.statistics, "date", "newCasesBySpecimenDate", alt=(None, "cases")
        )
        fig = px.line(
            df,
            x="date",
            y="cases",
            title="New Cases per day as of %s" % (self.latest_date),
        )
        return fig

    def full_vaccines_graph(self):
        df = self.aggregate(
            self.statistics,
            "date",
            "newPeopleVaccinatedCompleteByVaccinationDate",
            alt=(None, "vaccines"),
        )
        fig = px.line(
            df,
            x="date",
            y="vaccines",
            title="People fully vaccinated as of %s" % (self.latest_date),
        )
        fig.show()

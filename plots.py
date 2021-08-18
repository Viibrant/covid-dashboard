from bokeh.plotting import figure
from bokeh.models import DataRange1d, WheelZoomTool, HoverTool, DatetimeTickFormatter, NumeralTickFormatter, ColumnDataSource
from check_file import get_dataset
import pandas as pd
class covid:

    def __init__(self, endpoint):
        self.statistics = get_dataset(endpoint)
        self.statistics['date'] = pd.to_datetime(self.statistics['date'])
        # convert all dates to standard format
        self.latest_date = self.statistics.iloc[0]['date'].strftime("%d %b %Y")

    def get_newcases_nationally(self):
        # group all records with same dates together, then create a new dataframe and apply sum to all other columns
        grouped_dates = self.statistics.groupby("date").newCasesBySpecimenDate
        aggregated = pd.concat([grouped_dates.apply(
            sum), grouped_dates.count()], axis=1, keys=["date"])
        # The dates column changed to row names so take all names and cast to list
        return {"dates": list(aggregated.index), "cases": aggregated["date"].to_list()}

    def get_newvaccinations_nationally(self):
        grouped_dates = self.statistics.groupby("date").newPeopleVaccinatedCompleteByVaccinationDate
        aggregated = pd.concat([grouped_dates.apply(
            sum), grouped_dates.count()], axis=1, keys=["date"])
        # The dates column changed to row names so take all names and cast to list
        return {"dates": list(aggregated.index), "cases": aggregated["date"].to_list()}

    def cases_graph(self):
        # Generate graph for New Cases vs Date
        source = ColumnDataSource(data=self.get_newcases_nationally())
        p = figure(
            title="New Covid Cases as of %s" % self.latest_date,
            tools="pan, reset",
            toolbar_location=None,
            sizing_mode="stretch_both",
            plot_height=500,
            x_axis_type="datetime",
            x_range=DataRange1d(bounds="auto"),
            y_range=DataRange1d(bounds="auto")
        )

        zoom_tool = WheelZoomTool()
        zoom_tool.maintain_focus = False

        hover_tool = HoverTool()
        hover_tool.mode = "vline"
        hover_tool.tooltips = [
            ("Selected Date", "@dates{%d %b %Y}"), ("New Cases", "@cases{0,0}")]
        hover_tool.formatters = {"@dates": "datetime", "@cases": "numeral"}

        p.add_tools(zoom_tool, hover_tool)
        p.toolbar.active_scroll = p.select_one(WheelZoomTool)

        date_format = "%d %b %Y"
        p.xaxis.formatter = DatetimeTickFormatter(
            hours=date_format,
            days=date_format,
            months=date_format,
            years=date_format
        )
        p.xaxis.axis_label = "Date"

        p.yaxis.formatter = NumeralTickFormatter(format="0,0")
        p.yaxis.axis_label = "New Cases"
        p.line(x="dates", y="cases", source=source, color='red')

        return p

    def vaccines_graph(self):
        source = ColumnDataSource(data=self.get_newvaccinations_nationally())
        p = figure(
            title="People fully vaccinated as of %s" % self.latest_date,
            tools="pan, reset",
            toolbar_location=None,
            sizing_mode="stretch_both",
            plot_height=500,
            x_axis_type="datetime",
            x_range=DataRange1d(bounds="auto"),
            y_axis_location="right",
            y_range=DataRange1d(bounds="auto")
        )

        zoom_tool = WheelZoomTool()
        zoom_tool.maintain_focus = False

        hover_tool = HoverTool()
        hover_tool.mode = "vline"
        hover_tool.tooltips = [
            ("Selected Date", "@dates{%d %b %Y}"), ("Newly Vaccinated", "@cases{0,0}")]
        hover_tool.formatters = {"@dates": "datetime", "@cases": "numeral"}

        p.add_tools(zoom_tool, hover_tool)
        p.toolbar.active_scroll = p.select_one(WheelZoomTool)

        date_format = "%d %b %Y"
        p.xaxis.formatter = DatetimeTickFormatter(
            hours=date_format,
            days=date_format,
            months=date_format,
            years=date_format
        )
        p.xaxis.axis_label = "Date"

        p.yaxis.formatter = NumeralTickFormatter(format="0,0")
        p.yaxis.axis_label = "People Vaccinated"
        p.line(x="dates", y="cases", source=source, color='blue')

        return p
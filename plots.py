import time
import json
import pandas as pd
from datetime import date, datetime, timedelta
from requests import get
from bokeh.plotting import figure, show
from bokeh.models import DataRange1d, WheelZoomTool, HoverTool, DatetimeTickFormatter, NumeralTickFormatter, ColumnDataSource
from os.path import isfile, getctime
class covid:

    def __init__(self, endpoint):
        # Check if file doesn't exist
        file_exists = isfile("statistics.json")
        retries = 0
        latest = True

        if file_exists:
            with open("statistics.json") as json_file:
                data = json.load(json_file)

                # Read latest date from statistics.json and convert to Date object
                latest_date = datetime.strptime(
                    data[0]['date'], "%Y-%m-%d").date()

                # Get exact creation time then parse only date
                creation_date = getctime("statistics.json")
                creation_date = datetime.fromtimestamp(creation_date).date()
                # Data is always retrieved a day behind
                #   therefore if statistics.json is up to date then
                #       current_date == latest_date + 1 day
                if date.today() == latest_date + timedelta(days=1):
                    print("**** Dataset is up to date")
                    latest = True
                    # Convert dictionary to a Pandas DataFrame, far more efficient
                    self.statistics = pd.DataFrame(data)
                # Otherwise dataset itself may be outdated but retrieved today
                elif date.today() == creation_date:
                    print("**** Created today but outdated data")
                    latest = True
                    self.statistics = pd.DataFrame(data)
                else:
                    print("**** Dataset is outdated, downloading...")
                    latest = False

        while not latest or not file_exists:
            print("File exists:%s\nLatest version:%s" % (file_exists, latest))
            # Attempt to retrieve COVID Statistics from NHS, waiting time grows incrementally
            try:
                response = get(endpoint, allow_redirects=True, timeout=10)
                data = json.loads(response.text)['body']
                with open("statistics.json", "w") as json_file:
                    json.dump(data, json_file)

                self.statistics = pd.DataFrame(data)
                file_exists = True
                latest = True

            except Exception as e:
                wait = retries * 2
                print('Error! Waiting %s secs and re-trying...' % wait)
                time.sleep(wait)
                retries += 1
                if retries == 5:
                    raise e 

        # Convert all data in date column to datetimes for easier usage
        self.statistics['date'] = pd.to_datetime(self.statistics['date'])
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
            toolbar_location="left",
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
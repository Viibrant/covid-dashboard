from datetime import date, datetime, timedelta
from requests import get
from bokeh.plotting import figure, show
from bokeh.models import DataRange1d, WheelZoomTool, HoverTool, DatetimeTickFormatter, NumeralTickFormatter, ColumnDataSource
from bokeh.io import curdoc
from os.path import isfile
import time
import json

class covid:

    def __init__(self, endpoint):
        # Check if file doesn't exist
        file_exists = isfile("statistics.json")
        retries = 0

        if file_exists:
            with open("statistics.json") as json_file:
                data = json.load(json_file)

                # Read latest date from statistics.json and convert to Date object
                latest_date = datetime.strptime(data[0]['date'], "%Y-%m-%d").date()
                current_date = date.today()
                print(latest_date + timedelta(days=1))

                # Data is always retrieved a day behind
                #   therefore if statistics.json is up to date then
                #       latest_date + 1 day == current_date
                if current_date == latest_date + timedelta(days=1):
                    latest = True
                    self.statistics = data
                else:
                    latest = False

        while not latest or not file_exists:
            # Attempt to retrieve COVID Statistics from NHS, waiting time grows incrementally
            try:
                response = get(endpoint, timeout=10)
                api_response = response.json()["data"]

                with open("statistics.json", 'w') as json_file:
                    json.dump(api_response, json_file)
                self.statistics = api_response
                file_exists = True

            except Exception as e:
                wait = retries * 2;
                print('Error! Waiting %s secs and re-trying...'%wait)
                time.sleep(wait)
                retries += 1
                if retries == 5:
                    raise e

    def get_cases_nationally(self):
        # Parse JSON to get dates vs cases dictionary
        dates = []
        new_cases = []
        for record in self.statistics:
            record_cases = record["newCases"]
            record_date = datetime.strptime(record["date"], "%Y-%m-%d")
            if record_date in dates:
                new_cases[dates.index(record_date)] += record_cases
            else:
                dates.append(record_date)
                new_cases.append(record_cases)

        return {"dates": dates, "cases": new_cases}

    def cases_graph(self):
        # Generate graph for New Cases vs Date
        source = ColumnDataSource(data=self.get_cases_nationally())
        p = figure(
            title="New Covid Cases as of %s" % (date.today()),
            tools="pan, reset",
            sizing_mode="stretch_width",
            plot_height=500,
            x_axis_type="datetime",
            x_range=DataRange1d(bounds="auto",),
            y_range=DataRange1d(bounds="auto")
        )

        zoom_tool = WheelZoomTool()
        zoom_tool.maintain_focus = False

        hover_tool = HoverTool()
        hover_tool.mode = "vline"
        hover_tool.tooltips = [("Selected Date", "$x{%d %b %Y}"), ("New Cases", "@cases{0,0}")]
        hover_tool.formatters = {"$x": "datetime", "@cases": "numeral"}

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

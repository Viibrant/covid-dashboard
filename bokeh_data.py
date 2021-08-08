from datetime import date, datetime
from requests import get
from bokeh.plotting import figure, show
from bokeh.models import DataRange1d, WheelZoomTool, HoverTool, DatetimeTickFormatter, NumeralTickFormatter, ColumnDataSource
from bokeh.io import curdoc
import time

class covid:
    
    def __init__(self, endpoint):
        success = False
        retries = 0
        # Attempt to retrieve COVID Statistics from NHS, waiting time grows incrementally
        while not success:
            try:
                response = get(endpoint, timeout=10)
                self.api_response = response.json()
                success = True
            except Exception as e:
                wait = retries * 2;
                print('Error! Waiting %s secs and re-trying...'%wait)
                time.sleep(wait)
                retries += 1
                if retries == 5:
                    raise e


    def get_cases(self):
        # Parse JSON to get dates vs cases dictionary
        dates = []
        new_cases = []
        for dictionary in self.api_response['data']:
            values = list(dictionary.values())
            dates.append(datetime.strptime(values[0], "%Y-%m-%d"))
            new_cases.append(values[1])

        return {"dates": dates, "cases": new_cases}

    def cases_graph(self):
        source = ColumnDataSource(data=self.get_cases())
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



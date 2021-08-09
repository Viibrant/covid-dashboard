from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.layouts import gridplot
from bokeh_data import covid

app = Flask(__name__)

@app.route('/')
def bokeh():
    global dataset
    fig1 = dataset.cases_graph()
    fig2 = dataset.cases_graph()
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components({"fig1":fig1, "fig2":fig2})
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html

if __name__ == "__main__":
    endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        'filters=areaType=nation;areaName=england&'
        'structure={"date":"date","newCases":"newCasesByPublishDate"}'
    )
    dataset = covid(endpoint)
    app.run(debug=True)

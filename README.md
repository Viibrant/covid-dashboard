
<h1 align="center"><a href="http">COVID-19 Web App </a></h1>

<p align="center"> A simple COVID-19 Dashboard
</p>

## 🧐 About <a name = "about"></a>

This web app is a dashboard that presents NHS COVID-19 data in an easy to understand form. The data is retrieved from the NHS Coronavirus API.

## 🏁 Getting Started <a name = "getting_started"></a>

A simple
```
export FLASK_APP=app.py && flask run
```
is all you need to get this project running, follow the URL outputted in the terminal to access the local web server.

### Prerequisites

All dependencies are stored in `requirements.txt`
```console
pip install -r requirements.txt
```


## ⛏️ Built Using <a name = "built_using"></a>

- [Dash](https://dash.plotly.com) - Framework to build web-based analytic applications entirely in Python

- [Plotly](https://plotly.com/python/getting-started/) - Graphing Library
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Micro Web Framework
- [Requests](https://docs.python-requests.org/en/master/) - Python HTTP library
- [Coronavirus API](https://coronavirus.data.gov.uk/details/developers-guide) - NHS Coronavirus API
- [Pandas](https://pandas.pydata.org) - Python Data Analysis Library
- [GeoPandas](https://geopandas.org) - Pandas with Geospatial data
- [tqdm](https://github.com/tqdm/tqdm) - Progress bars in Python!
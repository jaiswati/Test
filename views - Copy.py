"""
Routes and views for the flask application.
"""

from datetime import datetime
import flask
import flask
from flask import render_template
from AMLWebProject import app

from datetime import datetime
from flask import render_template
from azureml import Workspace
from flask_jsonpify import jsonpify

@app.route('/')
@app.route('/home')
def home():
    ws = Workspace(
    workspace_id='30eac3f075f146d9a8b618a2fea395a2',
    authorization_token='tWbiP3cuChlkyh1jiFhB9dn/66/ai7MuB2+dASGf0Uxtt+UOLs8dEw6AWkrHIbo2C8byLJ3ankDwwPO1VK+QZg==',
    endpoint='https://studioapi.azureml.net')
    experiment = ws.experiments['30eac3f075f146d9a8b618a2fea395a2.f-id.735ce0c7a45a4ca0ba419e1ad25e4e72']
    ds = experiment.get_intermediate_dataset(
    node_id='e9de8fc3-107c-4853-9363-ce3353412951-16372',
    port_name='Results dataset',
    data_type_id='GenericCSV')
    frame = ds.to_dataframe()
    df=frame[frame['CustomerID']==17850.0]
    json_data = df.to_json(orient='values') 
    return jsonpify(json_data)

@app.route('/home1')
def home1():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

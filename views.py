"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from AMLWebProject import app
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
    data=frame    	
    data.drop_duplicates
    import pandas as pd
    data = data[pd.notnull(data['CustomerID'])]
    data = data[data.Quantity >= 0]
    import datetime as dt
    print('Most recent invoice is from:')
    print(data['InvoiceDate'].max())
    lastDate = dt.datetime(2011,12,10)
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data['TotalPrice'] = data.UnitPrice * data.Quantity
    rfmTable = data.groupby('CustomerID',as_index=False).agg({'InvoiceDate': lambda x: (lastDate - x.max()).days, 
											   'InvoiceNo': lambda x: len(x), 
											   'TotalPrice': lambda x: x.sum()})
    rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)
    rfmTable.rename(columns={ 'CustomerID':'customer_id',
							 'InvoiceDate': 'recency', 
							 'InvoiceNo': 'frequency', 
							 'TotalPrice': 'monetary'}, inplace=True)

    thr = rfmTable.drop('customer_id', axis=1).quantile(q=[0.25, 0.75])
    thr = thr.to_dict()

    def rank_r(x, p, t):
        if x <= t[p][0.25]:
            return str(1)
        elif x <= t[p][0.75]: 
            return str(2)
        else:
            return str(3)

    def rank_f(x, p, t):
        if x <= t[p][0.25]:
            return str(3)
        else:
            return str(1)

    def rank_m(x, p, t):
        if x <= t[p][0.25]:
            return str(3)
        elif x <= t[p][0.75]: 
            return str(2)
        else:
            return str(1)

    rfmTable['rank_r'] = rfmTable['recency'].apply(rank_r, args=('recency', thr))
    rfmTable['rank_f'] = rfmTable['frequency'].apply(rank_f, args=('frequency', thr))
    rfmTable['rank_m'] = rfmTable['monetary'].apply(rank_m, args=('monetary', thr))
    rfmTable['cluster'] = rfmTable['rank_r'] + rfmTable['rank_f'] + rfmTable['rank_m']
    rfmTable.head()

    def segment(rows):
    		if rows['cluster'] == '111':
    			return 'Best Customer'
    		elif rows['cluster'] == '211':
    			return 'Almost Lost'
    		elif rows['cluster'] == '311':
    			return 'Lost Customer'
    		elif rows['rank_r'] == '3':
    			return 'Cheap Lost'
    		elif rows['rank_f'] == '1':
    			return 'Loyal Customer'
    		elif rows['rank_m'] == '1':
    			return 'Big Spenders'
    		elif rows['rank_f'] == '3':
    			return 'New Customer'
    		else:
    			return rows['cluster']

    rfmTable['segment'] = rfmTable.apply(segment, axis=1)
    rfmTable.head()
    df=rfmTable[rfmTable['customer_id']==17850.0]
    df1= df['segment']
    df1.reset_index(drop=True, inplace=True)
    df2= df1[0]
    df=data[data['CustomerID']==17850.0]
    #json_data = df2.to_json(orient='values') 
    return df2 #jsonpify(json_data)

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

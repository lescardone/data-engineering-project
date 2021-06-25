import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
import streamlit as st

def stream_streamlit(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    init = firebase_admin.initialize_app
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    
    if not firebase_admin._apps:
        print("in the if")

        defaultApp = init(cred, 
                          {'projectId': PROJ_ID})
    else:
        print("in the else")
        defaultApp = firebase_admin.get_app()
        
    db = firestore.client()
    # Authenticate to Firestore with the JSON account key.
    
    # Create a reference to the Weather Collection
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)
    doc_ref = db.collection("shanghai-weather")
    results = doc_ref.where("time", ">", yesterday)

    data = []
    for doc in results.stream():
        data.append(doc.to_dict())
    df = pd.DataFrame(data = data, columns=['time', 'status','current_temp', 'rain', 'humidity'])
    df = format_data(df)
    run_streamlit(df)
    
def format_data(df):
    df['max_temp_C'] = df['current_temp'].map(lambda x: (x['temp_max']-32)*(5/9))
    df['min_temp_C'] = df['current_temp'].map(lambda x: (x['temp_min']-32)*(5/9))
    df['feels_like_C'] = df['current_temp'].map(lambda x: (x['feels_like']-32)*(5/9))
    df['max_temp_F'] = df['current_temp'].map(lambda x: x['temp_max'])
    df['min_temp_F'] = df['current_temp'].map(lambda x: x['temp_min'])
    df['feels_like_F'] = df['current_temp'].map(lambda x: x['feels_like'])                                         
    df.drop(columns=['current_temp'],axis=1,inplace=True)

    df['rain_volume_mm'] = df['rain'].map(lambda x: list(x.values()))
    df['rain_volume_mm'] = df['rain_volume_mm'].map(lambda x: x[0] if len(x)==1 else 0)
    df.drop(columns=['rain'],axis=1,inplace=True)

    df['time'] = df['time'].map(lambda x:x.astimezone(pytz.timezone('Asia/Shanghai')))
    df.sort_values(by='time',inplace=True)
    return(df)

def run_streamlit(df):
    st.set_page_config(layout="wide")
    st.subheader('Raw data')
    st.dataframe(df)

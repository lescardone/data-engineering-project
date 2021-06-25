import pyowm
from datetime import datetime
import collections
import pytz 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def call_shanghai_future(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    owm = pyowm.OWM(PERSONAL_API_KEY)
    manager = owm.weather_manager()
    shanghai_forecast_ = manager.one_call(lat=31.222219, lon=121.458061).forecast_daily

    shanghai_forecast = collections.defaultdict(list)
    for forecast in shanghai_forecast_:
      shanghai_forecast['time'].append(forecast.reference_time(timeformat='date'))
      shanghai_forecast['humidity'].append(forecast.humidity)
      shanghai_forecast['precipitation_proba'].append(forecast.precipitation_probability)
      shanghai_forecast['rain'].append(forecast.rain)
      shanghai_forecast['temperature'].append(forecast.temperature(unit='fahrenheit').get('min'))
    
    push_data(shanghai_forecast)
    return f'Got it!'

def push_data(shanghai_forecast):
    timenow = datetime.now().astimezone(pytz.timezone('Asia/Shanghai'))
    docName = f'Forecast--{timenow:%Y-%m-%d}'
    print(f'Document Name:{docName}')
    data = shanghai_forecast

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
    db.collection('shanghai-forecast').document(docName).set(data)

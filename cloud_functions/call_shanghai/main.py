import pyowm
from datetime import datetime
import collections
import pytz 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def call_shanghai_current(request):
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
    shanghai_current_ = manager.weather_at_coords(31.222219, 121.458061).weather

    shanghai_current = {}
    shanghai_current['time'] = shanghai_current_.reference_time(timeformat='date')
    shanghai_current['status'] = shanghai_current_.status
    shanghai_current['humidity'] = shanghai_current_.humidity
    shanghai_current['rain'] = shanghai_current_.rain
    shanghai_current['current_temp'] = shanghai_current_.temperature(unit='fahrenheit')
    
    push_data(shanghai_current)
    return f'Got it!'

def push_data(shanghai_current):
    timenow = datetime.now().astimezone(pytz.timezone('Asia/Shanghai'))
    docName = f'{timenow:%Y-%m-%d---%H-%M-%S}'
    print(f'Document Name:{docName}')
    data = shanghai_current

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
    db.collection('shanghai-weather').document(docName).set(data)
    return 'Data pushed!'
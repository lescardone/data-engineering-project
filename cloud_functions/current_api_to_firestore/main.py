import pyowm
from datetime import datetime
import pytz
import collections
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import secretmanager


def call_shanghai_current(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    owm = pyowm.OWM(owm_api_key())
    manager = owm.weather_manager()
    shanghai_current_ = manager.weather_at_coords(31.222219, 121.458061).weather

    shanghai_current = {}
    shanghai_current['reference_timestamp'] = shanghai_current_.reference_time()
    shanghai_current['status'] = shanghai_current_.status
    shanghai_current['humidity'] = shanghai_current_.humidity
    shanghai_current['rain'] = shanghai_current_.rain
    shanghai_current['current_temp'] = shanghai_current_.temperature(unit='fahrenheit')
    
    push_data(shanghai_current)
    return f'Got it!'

def owm_api_key():
    """Retrieves OpenWeatherMap API key from Google Cloud Secrets
    Args:
        None
    Returns:
        payload: API key as a string
    """
    secretClient = secretmanager.SecretManagerServiceClient()
    version = "versions/latest"
    name = f"projects/engineer-project-metis/secrets/weather-api/{version}"
    response = secretClient.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8").strip()
    return payload

def push_data(shanghai_current):
    """Pushes the data dictionary to the Firestore DB collection shanghai-weather
    Args:
        shanghai_current: dictionary of current weather in Shanghai
    Returns:
        'Data pushed!'
    """
    timenow = datetime.now().astimezone(pytz.timezone('Asia/Shanghai'))
    docName = f'{timenow:%Y-%m-%d---%H-%M-%S}'
    data = shanghai_current

    init = firebase_admin.initialize_app
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    
    if not firebase_admin._apps:
        defaultApp = init(cred, 
                          {'projectId': 'engineer-project-metis'})
    else:
        defaultApp = firebase_admin.get_app()
        
    db = firestore.client()
    db.collection('shanghai-weather').document(docName).set(data)
    db.collection('shanghai-current').document(docName).set(data)
    return 'Data pushed!'
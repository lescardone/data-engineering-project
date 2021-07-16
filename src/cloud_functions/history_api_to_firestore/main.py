import pyowm
from datetime import datetime, timedelta, timezone
from pyowm.utils import timestamps, formatting
import pytz
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import secretmanager

def call_shanghai_past(request):
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

    yesterday_epoch = formatting.to_UNIXtime(timestamps.yesterday())
    two_days_ago_epoch = int((datetime.now() - timedelta(days=2)).replace(tzinfo=timezone.utc).timestamp())
    three_days_ago_epoch = int((datetime.now() - timedelta(days=3)).replace(tzinfo=timezone.utc).timestamp())

    one_call_yest = manager.one_call_history(lat=31.222219, lon=121.458061,dt=yesterday_epoch)
    one_call_two = manager.one_call_history(lat=31.222219, lon=121.458061,dt=two_days_ago_epoch)
    one_call_three = manager.one_call_history(lat=31.222219, lon=121.458061,dt=three_days_ago_epoch)

    observed_weather_yest_ = one_call_yest.current
    observed_weather_two_ = one_call_two.current
    observed_weather_three_ = one_call_three.current

    shanghai_history = make_dict(observed_weather_yest_,observed_weather_two_,observed_weather_three_)
    push_data(shanghai_history)
    return "Got it!"


def make_dict(observed_weather_yest_,observed_weather_two_,observed_weather_three_):
    shanghai_history = {}
    shanghai_history['reference_timestamp'] = [observed_weather_yest_.reference_time()]
    shanghai_history['status'] = [observed_weather_yest_.status]
    shanghai_history['humidity'] = [observed_weather_yest_.humidity]
    shanghai_history['rain'] = [observed_weather_yest_.rain]
    shanghai_history['temperature'] = [observed_weather_yest_.temperature(unit='fahrenheit')]

    for weather in [observed_weather_two_, observed_weather_three_]:
        shanghai_history['reference_timestamp'].append(weather.reference_time())
        shanghai_history['status'].append(weather.status)
        shanghai_history['humidity'].append(weather.humidity)
        shanghai_history['rain'].append(weather.rain)
        shanghai_history['temperature'].append(weather.temperature(unit='fahrenheit'))
    return shanghai_history

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

def push_data(shanghai_history):
    """Pushes the data dictionary to the Firestore DB collection shanghai-weather
    Args:
        shanghai_current: dictionary of current weather in Shanghai
    Returns:
        'Data pushed!'
    """
    timenow = datetime.now().astimezone(pytz.timezone('Asia/Shanghai'))
    docName = f'History--{timenow:%Y-%m-%d--%H-%M}'
    data = shanghai_history

    init = firebase_admin.initialize_app
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    
    if not firebase_admin._apps:
        defaultApp = init(cred, 
                          {'projectId': 'engineer-project-metis'})
    else:
        defaultApp = firebase_admin.get_app()
        
    db = firestore.client()
    db.collection('shanghai-history').document(docName).set(data)
    db.collection('shanghai-historic').document(docName).set(data)
    return 'Data pushed!'
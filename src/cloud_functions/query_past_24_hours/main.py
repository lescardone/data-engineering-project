import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from datetime import datetime, timedelta
import pytz
import json

def most_recent_24(request):
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
        defaultApp = init(cred, 
                          {'projectId': 'engineer-project-metis'})
    else:
        defaultApp = firebase_admin.get_app() 
    db = firestore.client()
    
    # Create a reference to the Weather Collection
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)
    doc_ref = db.collection("shanghai-current")
    results = doc_ref.where("reference_timestamp", ">", yesterday.timestamp())

    data = []
    for doc in results.stream():
        data.append(doc.to_dict())
    
    r = json.dumps(data)
    return r
    
def save_data(data_list):
   with open("most_recent_24.json", "w") as f:
      json.dump(data_list, f)

def load_data(fname):
   with open(fname) as f:
       return json.load(f)

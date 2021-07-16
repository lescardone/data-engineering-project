import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from datetime import datetime, timedelta
import pytz
import json

def most_recent(request):
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
    
    doc_ref = db.collection("shanghai-current")
    query = doc_ref.order_by("reference_timestamp",direction=firestore.Query.DESCENDING).limit(1)
    results = query.stream()


    for doc in results:
        data = doc.to_dict()
    
    r = json.dumps(data)
    return r

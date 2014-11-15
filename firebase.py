import json

import requests

from FindFood import FindFood

FIREBASE_URL = 'https://foodsdb.firebaseio.com'

def put(url,data):
	return requests.put(FIREBASE_URL + url, data=json.dumps(data)).json()

def get(url):
	return requests.get(FIREBASE_URL + url).json()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("fastapi-study-dd2e4-firebase-adminsdk-fbsvc-52e24e5ef2.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
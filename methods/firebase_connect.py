from firebase_admin import credentials, firestore, initialize_app
import pyrebase

#Credenciais firebase Admin
cred = credentials.Certificate('firebase.json')
firebase_admin = initialize_app(cred, {'xxxxxxxxx': 'xxxxxxxxx'})
db = firestore.client()

#Credenciais firebase PYREBASE
firebaseConfig = {
    "apiKey": "xxxxxxxxx",
    "authDomain": "xxxxxxxxx",
    "projectId": "xxxxxxxxx",
    "storageBucket": "xxxxxxxxx",
    "messagingSenderId": "xxxxxxxxx",
    "databaseURL": "xxxxxx",
    "appId": "xxxxxxxxx",
    "measurementId": "xxxxxxxxx"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth_pyrebase = firebase.auth()
db = firestore.client()
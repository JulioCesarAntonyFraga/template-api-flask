from firebase_admin import credentials, firestore, initialize_app
import pyrebase


#Credenciais firebase Admin
cred = credentials.Certificate('checklist_firebase.json')
firebase_admin = initialize_app(cred, {'storageBucket': 'gererador-qr-code.appspot.com'})
db = firestore.client()

#Credenciais firebase PYREBASE
firebaseConfig = {
    "apiKey": "AIzaSyCRGRXzPU1yXgLFLkT3vLU_L0QJtT9oDzw",
    "authDomain": "gererador-qr-code.firebaseapp.com",
    "projectId": "gererador-qr-code",
    "storageBucket": "gererador-qr-code.appspot.com",
    "messagingSenderId": "734208597165",
    "databaseURL": "xxxxxx",
    "appId": "1:734208597165:web:1d76cdf4c4fef8de113a24",
    "measurementId": "G-9MDTLJF7PW"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth_pyrebase = firebase.auth()
db = firestore.client()
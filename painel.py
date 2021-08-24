from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

secret_key = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'

####METODO PARA LOGAR UM USUARIO DO FIREBASE############
def Login():
    json_data = request.json
    try:
        user= auth_pyrebase.sign_in_with_email_and_password(json_data['Email'], json_data['Senha'])
        userToken = auth_pyrebase.get_account_info(user['idToken'])
        userId = userToken['users'][0]['localId']
        account = db.collection('accounts').document(userId).get()
        token = jwt.encode({'user': {'Id': userId, 'UserName': account.get('name'), 'Email': json_data['Email']},'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},secret_key)
        return jsonify({'user': {'Id': userId, 'UserName': account.get('name'), 'Email': json_data['Email']}, 'token': token})
    except Exception as e:
        response = jsonify({'message': 'Usuário ou senha incorretos' + str(e)})
        return response, 401



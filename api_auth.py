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
        token = jwt.encode({'Id': userId, 'UserName': account.get('name'), 'Email': json_data['Email'],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},secret_key)
        return jsonify({'user': {'Id': userId, 'UserName': account.get('name'), 'Email': json_data['Email']}, 'token': token})
    except Exception as e:
        response = jsonify({'message': 'Usuário ou senha incorretos' + str(e)})
        return response, 401

####METODO PARA OS DETALHES DE UM USUARIO DO FIREBASE############
def get_user(user):
    User_id = user['Id']
    user = db.collection('accounts').document(User_id).get()

    try:
        dict_pergunta = {'user_id': user.id,'cargo': user.get('cargo'),
                'UserName': user.get('name'),'email': user.get('email'),
                'equipes_salvas': user.get('equipes_salvas'),
            }
        response = jsonify(dict_pergunta)
        return response, 200
    except:
        response = jsonify({'message':'Erro ao buscar o Usuário'})
        return response, 500

####METODO PARA EDITAR A CONTA DO USUÁRIO############
def edit_user(user):
    try:
        json_data_edit_user = request.json
        User_id = user['Id']
        db.collection('accounts').document(User_id).update(json_data_edit_user)
        response = jsonify({'message':'Editado com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível editar.' + str(e)})
        return response, 500

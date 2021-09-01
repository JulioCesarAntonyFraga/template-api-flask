from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from methods.firebase_connect import *

secret_key = 'MYSECRETKEY'

####METODO PARA LOGAR UM USUARIO DO FIREBASE############
def login():
    json_data = request.json

    try:
        token = jwt.encode({'Id': 'userId from database', 'UserName': json_data['UserName'], 'Email': json_data['Email'],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},secret_key)
        return jsonify({'user': {'Id': 'userId from database', 'UserName': json_data['UserName'], 'Email': json_data['Email']}, 'token': token})
    except Exception as e:
        response = jsonify({'message': 'Usuário ou senha incorretos' + str(e)})
        return response, 401

    #################### USE O MÉTODO ABAIXO CASO ESTEJA USANDO O FIREBASE ####################
    # try:
    #     user= auth_pyrebase.sign_in_with_email_and_password(json_data['Email'], json_data['Senha'])
    #     userToken = auth_pyrebase.get_account_info(user['idToken'])
    #     userId = userToken['users'][0]['localId']
    #     account = db.collection('accounts').document(userId).get()
    #     token = jwt.encode({'Id': userId, 'UserName': account.get('name'), 'Email': json_data['Email'],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},secret_key)
    #     return jsonify({'user': {'Id': userId, 'UserName': account.get('name'), 'Email': json_data['Email']}, 'token': token})
    # except Exception as e:
    #     response = jsonify({'message': 'Usuário ou senha incorretos' + str(e)})
    #     return response, 401

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

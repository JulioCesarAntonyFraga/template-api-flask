from flask.json import jsonify
from firebase_admin import auth
from flask import request

def reset_password(user):
    json_data_reset_user = request.json
    email = json_data_reset_user['Email']
    newPassword = json_data_reset_user['NovaSenha']
    uid = user['Id']

    if user['Id'] != uid:
        response = jsonify({'message': 'Erro. Não foi possível acessar essa conta.'})
        return response, 500
  
    try:
        user = auth.get_user_by_email(email)
        if(user.uid != ''):
            user = auth.update_user(
            uid,
            email=email,
            password= newPassword,)
            response = jsonify({'message':'Senha alterada com sucesso.'})
            return response, 200
        else:
            response = jsonify({'message':'Usuário não encontrado.'})
            return response, 404
    except Exception as e:
        response = jsonify({'message':'Erro Usuário não encontrado ou não existe. Mais detalhes' + str(e)})
        return response, 500

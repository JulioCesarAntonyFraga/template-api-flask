from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import Flask, request
import datetime
import jwt
from reset_password import reset_password
from api_auth import *
from perguntas import *
from verificacoes import *
from api_firebase import *
from checklists import *
from painel import *

app = Flask(__name__)
#credenciais aplicação
secret_key = app.config['SECRET_KEY'] = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'

##################AUTH FIREBASE E TOKEN###################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Bearer' in request.headers['authorization']:
            token = request.headers['authorization'].replace('Bearer ', '')

        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Nenhum token recebido !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            user = data['user']
        except:
            return jsonify({
                'message': 'Token inválido !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(user, *args, **kwargs)
    return decorated

####METODO EDITAR CHECKLIST############
@app.route('/api/checklists/edit_data/checklist/', methods=['PUT'])
@token_required
def Route_edit_checklist(user):
   return edit_checklist(user)

####METODO DELETAR CHECKLIST############
@app.route('/api/checklists/delete_data/checklist/', methods=['DELETE'])
@token_required
def Route_detele_checklist(user):
    return detele_checklist(user)

####METODO DELETAR CONFORMES############
@app.route('/api/painel/delete_data/conformes/', methods=['DELETE'])
@token_required
def Route_detele_conformes(user):
   return detele_conformes(user)

####METODO DELETAR NAO CONFORMES############
@app.route('/api/painel/delete_data/nao_conformes/', methods=['DELETE'])
@token_required
def Route_detele_nao_conformes(user):
   return detele_nao_conformes(user)

####METODO DELETAR NAO APLICAVEL############
@app.route('/api/painel/delete_data/nao_aplicavel/', methods=['DELETE'])
@token_required
def Route_detele_nao_aplicavel(user):
    return detele_nao_aplicavel(user)

####METODO DELETAR VERIFICACAO############
@app.route('/api/verificacoes/delete_data/verificacao/', methods=['GET'])
@token_required
def Route_detele_verificacao(user):
    return detele_verificacao

####METODO CRIAR CHECKLIST############
@app.route('/api/checklists/create_data/checklist/', methods=['POST'])
@token_required
def Route_create_checklist(user):
    return create_checklist(user)

####METODO EDITAR PERGUNTAS############
@app.route('/api/perguntas/edit_data/pergunta/', methods=['PUT'])
@token_required
def Route_edit_pergunta(user):
    return edit_pergunta(user)

####METODO CRIAR PERGUNTAS############
@app.route('/api/perguntas/create_data/pergunta/', methods=['POST'])
@token_required
def Route_create_pergunta(user):
    return create_pergunta(user)

#####METODO PARA PEGAR TODAS AS INFO DO PAINEL############
@app.route('/api/painel/get_data/', methods=['GET'])
@token_required
def Route_get_dashbord(user):
    return get_dashbord(user)

#####METODO PARA PEGAR TODAS AS VERIFICACOES############
@app.route('/api/verificacoes/get_data/', methods=['GET'])
@token_required
def Route_get_all_verificacoes(user):
    return get_all_verificacoes(user)

####METODO PARA PEGAR UMA VERIFICACAO############
@app.route('/api/verificacoes/get_data/verificacao/', methods=['GET'])
@token_required
def Route_get_verificacao(user):
   return get_verificacao(user)

####METODO PARA PEGAR TODAS AS CHECKLISTS############
@app.route('/api/checklists/get_data/', methods=['GET'])
@token_required
def Route_get_all_checklists(user):
    return get_all_checklists(user)

####METODO PARA PEGAR UMA CHECKLIST############
@app.route('/api/checklists/get_data/checklist/', methods=['GET'])
@token_required
def Route_get_checklist(user):
    return get_checklist(user)

####METODO PARA PEGAR UMA PERGUNTA DE UMA CHECKLIST############
@app.route('/api/checklists/get_data/perguntas/get/', methods=['GET'])
@token_required
def Route_get_pergunta(user):
   return get_pergunta(user)

####METODO PARA PEGAR TODAS PERGUNTAS DE UMA CHECKLIST############
@app.route('/api/checklists/get_data/perguntas/', methods=['GET'])
@token_required
def Route_get_all_perguntas(user):
    return get_all_perguntas(user)

####METODO PARA LOGAR UM USUARIO DO FIREBASE############
@app.route('/api/accounts/get_data/',  methods=['POST'])
def Route_Login():
    return Login()

####METODO PARA OS DETALHES DE UM USUARIO DO FIREBASE############
@app.route('/api/accounts/get_data/account/get/', methods=['GET'])
@token_required
def Route_Get_Accout_Details(user):
    return get_user(user)

####METODO PARA EDITAR A CONTA DO USUÁRIO############
@app.route('/api/accounts/edit_data/account/', methods=['PUT'])
@token_required
def Route_Edit_Details(user):
    return edit_user(user)
        
####METODOS DE LOGIN AUTH FIREBASE############
@app.route('/api/accounts/reset_pass/account/', methods=['POST'])
@token_required
def reset_pass(user):
    return reset_password(user)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.run(debug=True)

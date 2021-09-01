from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
from flask import Flask, request
import jwt
from methods.reset_password import reset_password
from methods.auth import *
from methods.firebase_connect import *
from methods.examples import *

app = Flask(__name__)
#credenciais aplicação
app.config['SECRET_KEY'] = 'MYSECRETKEY'
app.config['BASE_URL'] = '/api_base'

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
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = {
                "Email": data['Email'],
                "Id": data['Id'],
                "UserName": data['UserName'],
            }
        except:
            return jsonify({
                'message': 'Token inválido !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(user, *args, **kwargs)
    return decorated

@app.route(f"{app.config['BASE_URL']}/protected", methods=['GET'])
@token_required
def api_protected(user):
    return get_protected(user)

    # return get_protected(user) 

@app.route(f"{app.config['BASE_URL']}/unprotected", methods=['GET'])
def api_unprotected():
    return get_unprotected()

@app.route(f"{app.config['BASE_URL']}/login",  methods=['POST'])
def api_login():
    ############ QUALQUER LOGIN VAI FUNCIONAR AQUI ENQUANTO VOCÊ NÃO USAR O FIREBASE PARA FAZER LOGIN ############
    return login()

if __name__ == '__main__':
    # app.config['ENV'] = 'development'
    app.config['DEBUG'] = False
    app.run(debug=False)

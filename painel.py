from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

secret_key = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'

#####METODO PARA PEGAR TODAS AS INFO DO PAINEL############
def get_dashbord(user):
    Account_Verificacoes = user['Id']
    try:
        verificacoes = db.collection('accounts').document(Account_Verificacoes).collection('verificacoes').get()
        for v in verificacoes:
            itens = v.get('total_c') + v.get('total_nc') + v.get('total_na')
        conformes = db.collection('accounts').document(Account_Verificacoes).collection('conformes').get()
        nao_conformes = db.collection('accounts').document(Account_Verificacoes).collection('nao_conformes').get()
        nao_aplicavel = db.collection('accounts').document(Account_Verificacoes).collection('nao_aplicavel').get()
        planos_de_acao = db.collection('accounts').document(Account_Verificacoes).collection('planos_de_acao').get()
        
        dict_painel = {'conformes': len(conformes) / itens* 100, 'nao_conformes': len(nao_conformes) / itens * 100, 'planos_de_acao': len(planos_de_acao) / itens * 100, 'nao_aplicavel': len(nao_aplicavel) / itens * 100}
        response = jsonify(dict_painel)
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Erro. Não foi possível acessar o painel dessa conta.'})
        return response, 500

####METODO DELETAR CONFORMES############
def detele_conformes(user):
    try:
        User_id = user['Id']
     
        try:
            db.collection('accounts').document(User_id).collection('conformes').delete()
        except:
            pass
        response = jsonify({'message':'Todos os Conformes foram deletados com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível deletar todos os Conformes. Mais detalhes: ' + str(e)})
        return response, 500

####METODO DELETAR NAO CONFORMES############
def detele_nao_conformes(user):
    try:
        User_id = user['Id']
     
        try:
            db.collection('accounts').document(User_id).collection('nao_cpnformes').delete()
        except:
            pass
        response = jsonify({'message':'Todos os Não Conformes foram deletados com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível deletar todos os Não Conformes. Mais detalhes: ' + str(e)})
        return response, 500

####METODO DELETAR NAO APLICAVEL############
def detele_nao_aplicavel(user):
    try:
        User_id = user['Id']
     
        try:
            db.collection('accounts').document(User_id).collection('nao_aplicavel').delete()
        except:
            pass
        response = jsonify({'message':'Todos os os itens Não Aplicáveis foram deletados com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível deletar todos os itens Não Aplicáveis. Mais detalhes: ' + str(e)})
        return response, 500





from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

secret_key = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'


####METODO PARA PEGAR UMA PERGUNTA DE UMA CHECKLIST############
def get_pergunta(user):
    Account_Checklist = str(request.args['Account'])
    Account_Checklist = Account_Checklist.split('/')
    User_id = user['Id']
    checklist = Account_Checklist[0]
    pergunta = Account_Checklist[1]
    dict_pergunta = {}

    pergunta = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').document(pergunta).get()
    try:
        dict_pergunta = {'uid_pergunta': pergunta.id,'pergunta': pergunta.get('pergunta'),
                'observacao': pergunta.get('observacao'),'images': pergunta.get('images'),
            }

        response = jsonify(dict_pergunta)
        return response, 200
    except Exception as e:
        response = jsonify({'message': 'Erro. Não foi possível acessar esse Item dessa conta.'})
        return response, 500

####METODO PARA PEGAR TODAS PERGUNTAS DE UMA CHECKLIST############
def get_all_perguntas(user):

    Account_Checklist = str(request.args['Account'])
    Account_Checklist = Account_Checklist.split('/')
    User_id = Account_Checklist[0]
    checklist = Account_Checklist[1]
    list_perguntas = []

    if user['Id'] != User_id:
        response = jsonify({'message': 'Erro. Não foi possível acessar os Itens dessa conta.'})
        return response, 500

    perguntas_Checklists = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').get()
    try:
        for p in perguntas_Checklists:
            details_perguntas = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').document(p.id).get()
            list_perguntas.append({'uid_pergunta': p.id,'pergunta': details_perguntas.get('pergunta'),
                'observacao': details_perguntas.get('observacao'),'images': details_perguntas.get('images'),
            })
        response = jsonify(list_perguntas)
        return response, 200
    except Exception as e:
        response = jsonify({'message': 'Erro. Não foi possível acessar os Itens dessa conta.'})
        return response, 500


####METODO EDITAR PERGUNTAS############
def edit_pergunta(user):
    try:
        json_data_edit_pergunta = request.json
        User_id = user['Id']
        pergunta = json_data_edit_pergunta['uid_pergunta']
        checklist = json_data_edit_pergunta['uid_checklist']

        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').document(pergunta).update(json_data_edit_pergunta)
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('categorias').document(cat.id).collection('checklists').document(checklist).collection('perguntas').document(pergunta).update(json_data_edit_pergunta)
        except:
            pass
        response = jsonify({'message':'Editado com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível editar o item.' + str(e)})
        return response, 500

####METODO CRIAR PERGUNTAS############
def create_pergunta(user):
    try:
        json_data_edit_checklist = request.json
        User_id = user['Id']
        checklist = json_data_edit_checklist['uid_checklist']
        images = json_data_edit_checklist['images']
        observacao = json_data_edit_checklist['observacao']
        pergunta = json_data_edit_checklist['pergunta']

        dict_pergunta = {'images': images, 'observacao': observacao, 'pergunta': pergunta,
        }

        db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').add(dict_pergunta)
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').add(dict_pergunta)
        except:
            pass
        response = jsonify({'message':'Item criado com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível criar um novo Item. Mais detalhes: ' + str(e)})
        return response, 500
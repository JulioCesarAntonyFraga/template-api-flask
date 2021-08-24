from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

####METODO PARA PEGAR TODAS AS CHECKLISTS############
def get_all_checklists(user):
    Account_Checklists = user['Id']
    dict_checklists = {}
    list_checklists = []
    list_perguntas = []
    #####ESTRUTURANDO OS DADOS DA CHECKLIST####################
    Checklists = db.collection('accounts').document(Account_Checklists).collection('checklists').get()
    try:
        for c in Checklists:
            perguntas_Checklists = db.collection('accounts').document(Account_Checklists).collection('checklists').document(c.id).collection('perguntas').get()
            for p in perguntas_Checklists:
                details_perguntas = db.collection('accounts').document(Account_Checklists).collection('checklists').document(c.id).collection('perguntas').document(p.id).get()
                list_perguntas.append({'uid_pergunta': p.id,'pergunta': details_perguntas.get('pergunta'),
                    'observacao': details_perguntas.get('observacao'),'images': details_perguntas.get('images'),
                })
            dict_checklists = {'uid_checklist': c.id, 'CategoriasID': c.get('CategoriasID'), 
            'deleted_categoria': c.get('deleted_categoria'), 'descricao': c.get('descricao'), 
            'observacao': c.get('observacao'), 'title': c.get('title'), 'itens': len(perguntas_Checklists),'perguntas': list_perguntas,}
            list_checklists.append(dict_checklists)
            list_perguntas = []

        response = jsonify(list_checklists)
        return response, 200
    except Exception as e:
        response = jsonify({'message': 'Erro. Não foi possível acessar as checklists dessa conta.'})
        return response, 500

####METODO PARA PEGAR UMA CHECKLIST############
def get_checklist(user):
    Account_Checklist = str(request.args['Account'])
    User_id = user['Id']
    checklist = Account_Checklist
    list_perguntas = []
    list_verificacoes = []
    list_nao_aplicavel_details = []
    list_conformes_details = []
    list_nao_conformes_details = []
    list_verificacoes = []
    
    
    #####ESTRUTURANDO OS DADOS DA CHECKLIST####################
    Checklist_Firebase = db.collection('accounts').document(User_id).collection('checklists').document(checklist).get()
    perguntas_Checklists = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').get()
    try:
        for p in perguntas_Checklists:
            details_perguntas = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').document(p.id).get()
            list_perguntas.append({'uid_pergunta': p.id,'pergunta': details_perguntas.get('pergunta'),
                'observacao': details_perguntas.get('observacao'),'images': details_perguntas.get('images'),
            })

        verificacoes_total = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('verificacoes').get()
        for v in verificacoes_total:
            conformes_verificacao = db.collection('accounts').document(User_id).collection(
                'verificacoes').document(v.id).collection('conformes').get()
            for c in conformes_verificacao:
                list_conformes_details.append(
                    {'uid_conforme': c.id, 'pergunta': c.get('pergunta'), 'images': c.get('images'),
                        'situacao': c.get('situacao'), 'comentario': c.get('comentario')})

            nao_conformes_verificacao = db.collection('accounts').document(User_id).collection(
                'verificacoes').document(v.id).collection('nao_conformes').get()
            for nc in nao_conformes_verificacao:
                list_nao_conformes_details.append(
                    {'uid_conforme': nc.id, 'pergunta': nc.get('pergunta'), 'images': nc.get('images'),
                        'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

            nao_aplicavel_verificacao = db.collection('accounts').document(User_id).collection(
                'verificacoes').document(v.id).collection('nao_aplicavel').get()
            for na in nao_aplicavel_verificacao:
                list_nao_aplicavel_details.append(
                    {'uid_conforme': na.id, 'pergunta': na.get('pergunta'), 'images': na.get('images'),
                        'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

            list_verificacoes.append({'aplicado_por': v.get('aplicado_por'), 'cargo': v.get('cargo'),
                                        'data_checklist': v.get('data_checklist'),
                                        'name_checklist': v.get('name_checklist'), 'total_c': v.get('total_c'),
                                        'total_nc': v.get('total_nc'), 'total_na': v.get('total_na'),
                                        'uid_checklist': v.get('uid_checklist'),
                                        'uid_verfication': v.get('uid_verfication'),
                                        'nao_aplicavel': list_nao_aplicavel_details,
                                        'pdf': v.get('pdf'),
                                        'nao_conformes': list_nao_conformes_details, 'conformes': list_conformes_details,
                                        })

        dict_checklists = {'uid_checklist': Checklist_Firebase.id, 'CategoriasID': Checklist_Firebase.get('CategoriasID'), 
        'deleted_categoria': Checklist_Firebase.get('deleted_categoria'), 'descricao': Checklist_Firebase.get('descricao'), 
        'observacao': Checklist_Firebase.get('observacao'), 'title': Checklist_Firebase.get('title'), 'itens': len(perguntas_Checklists),'verificacoes': list_verificacoes, 'perguntas': list_perguntas,}
        
        response = jsonify(dict_checklists)
        return response, 200
    except Exception as e:
        response = jsonify({'message': 'Erro. Não foi possível acessar a checklist dessa conta.'})
        return response, 500
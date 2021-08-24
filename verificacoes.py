from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

secret_key = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'

#####METODO PARA PEGAR TODAS AS VERIFICACOES############
def get_all_verificacoes(user):
    Account_Verificacoes = user['Id']
    list_verificacoes = []
    list_nao_aplicavel_details = []
    list_conformes_details = []
    list_nao_conformes_details = []
    list_verificacoes = []
    #####ESTRUTURANDO TODAS AS VERIFICACOES DOS OS USUARIOS####################
    try:
        verificacoes_total = db.collection('accounts').document(Account_Verificacoes).collection('verificacoes').get()
        for v in verificacoes_total:
            conformes_verificacao = db.collection('accounts').document(Account_Verificacoes).collection(
                'verificacoes').document(v.id).collection('conformes').get()
            for c in conformes_verificacao:
                list_conformes_details.append(
                    {'uid_conforme': c.id, 'pergunta': c.get('pergunta'), 'images': c.get('images'),
                        'situacao': c.get('situacao'), 'comentario': c.get('comentario')})

            nao_conformes_verificacao = db.collection('accounts').document(Account_Verificacoes).collection(
                'verificacoes').document(v.id).collection('nao_conformes').get()
            for nc in nao_conformes_verificacao:
                list_nao_conformes_details.append(
                    {'uid_conforme': nc.id, 'pergunta': nc.get('pergunta'), 'images': nc.get('images'),
                        'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

            nao_aplicavel_verificacao = db.collection('accounts').document(Account_Verificacoes).collection(
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

        response = jsonify(list_verificacoes)
        return response, 200
    except Exception as e:
        response = jsonify({'message': 'Erro. Não foi possível acessar as verificações dessa conta.' + str(e)})
        return response, 500

####METODO PARA PEGAR UMA VERIFICACAO############
def get_verificacao(user):
    Account_Verificacoe = str(request.args['Account'])
    User_id = user['Id']
    verificacao = Account_Verificacoe
    dict_verificacao = {}
    list_nao_aplicavel_details = []
    list_conformes_details = []
    list_nao_conformes_details = []
    list_verificacoes = []
    #####ESTRUTURANDO TODAS AS VERIFICACOES DOS OS USUARIOS####################
    try:
        verificacoe_details = db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).get()
 
        conformes_verificacao = db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).collection('conformes').get()
        for c in conformes_verificacao:
            list_conformes_details.append(
                {'uid_conforme': c.id, 'pergunta': c.get('pergunta'), 'images': c.get('images'),
                    'situacao': c.get('situacao'), 'comentario': c.get('comentario')})

        nao_conformes_verificacao = db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).collection('nao_conformes').get()
        for nc in nao_conformes_verificacao:
            list_nao_conformes_details.append(
                {'uid_conforme': nc.id, 'pergunta': nc.get('pergunta'), 'images': nc.get('images'),
                    'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

        nao_aplicavel_verificacao = db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).collection('nao_aplicavel').get()
        for na in nao_aplicavel_verificacao:
            list_nao_aplicavel_details.append(
                {'uid_conforme': na.id, 'pergunta': na.get('pergunta'), 'images': na.get('images'),
                    'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

        dict_verificacao = {'aplicado_por': verificacoe_details.get('aplicado_por'), 'cargo': verificacoe_details.get('cargo'),
                                    'data_checklist': verificacoe_details.get('data_checklist'),
                                    'name_checklist': verificacoe_details.get('name_checklist'), 
                                    'total_c': verificacoe_details.get('total_c'),
                                    'total_nc': verificacoe_details.get('total_nc'), 
                                    'total_na': verificacoe_details.get('total_na'),
                                    'uid_checklist': verificacoe_details.get('uid_checklist'),
                                    'uid_verfication': verificacoe_details.get('uid_verfication'),
                                    'pdf': verificacoe_details.get('pdf'),
                                    'nao_aplicavel': list_nao_aplicavel_details,
                                    'nao_conformes': list_nao_conformes_details, 
                                    'conformes': list_conformes_details,
                                    }

        response = jsonify(dict_verificacao)
        return response, 200
    except Exception as e:
        response = jsonify({'message': 'Erro. Não foi possível acessar as checklists dessa conta.'})
        return response, 500

####METODO DELETAR VERIFICACAO############
def detele_verificacao(user):
    try:
        json_data_delete_verificacao = str(request.args['Account'])
        User_id = user['Id']
        verificacao = json_data_delete_verificacao
    
        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).delete()
        try:
            checklits_data = db.collection('accounts').document(User_id).collection('checklists').get()
            for c in checklits_data:
                db.collection('accounts').document(User_id).collection('checklists').document(c.id).collection('verificacoes').document(verificacao).delete()
        except:
            pass
        response = jsonify({'message':'Verificação deletada com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível deletar a Verificação. Mais detalhes: ' + str(e)})
        return response, 500
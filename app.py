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
from api_firebase import *
from checklists import *

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

#################CRUD API#################################

####METODO EDITAR CHECKLIST############
@app.route('/api/checklists/edit_data/checklist/', methods=['PUT'])
@token_required
def edit_checklist(user):
    try:
        json_data_edit_checklist = request.json
        User_id = user['Id']
        checklist = json_data_edit_checklist['uid_checklist']
    

        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('checklists').document(checklist).update(json_data_edit_checklist)
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('categorias').document(cat.id).collection('checklists').document(checklist).update(json_data_edit_checklist)
        except:
            pass
        response = jsonify({'message':'Editado com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível editar a checklist.' + str(e)})
        return response, 500

####METODO DELETAR CHECKLIST############
@app.route('/api/checklists/delete_data/checklist/', methods=['DELETE'])
@token_required
def detele_checklist(user):
    try:
        json_data_delete_checklist = str(request.args['Account'])
        User_id = user['Id']
        checklist = json_data_delete_checklist
    
        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('checklists').document(checklist).delete()
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('categorias').document(cat.id).collection('checklists').document(checklist).delete()
        except:
            pass
        response = jsonify({'message':'Checklist deletada com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível deletar a checklist. Mais detalhes: ' + str(e)})
        return response, 500

####METODO DELETAR CONFORMES############
@app.route('/api/painel/delete_data/conformes/', methods=['DELETE'])
@token_required
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
@app.route('/api/painel/delete_data/nao_conformes/', methods=['DELETE'])
@token_required
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
@app.route('/api/painel/delete_data/nao_aplicavel/', methods=['DELETE'])
@token_required
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

####METODO DELETAR VERIFICACAO############
@app.route('/api/verificacoes/delete_data/verificacao/', methods=['GET'])
@token_required
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

####METODO CRIAR CHECKLIST############
@app.route('/api/checklists/create_data/checklist/', methods=['POST'])
@token_required
def create_checklist(user):
    try:
        json_data_edit_checklist = request.json
        User_id = user['Id']
        descricao = json_data_edit_checklist['descricao']
        observacao = json_data_edit_checklist['observacao']
        title = json_data_edit_checklist['title']

        dict_checklist = {'descricao': descricao, 'observacao': observacao, 'title': title,
        'CategoriasID': 'NaN', 'deleted_categoria': True, 'icon': 'https://firebasestorage.googleapis.com/v0/b/connect-my-health-24512.appspot.com/o/edit_viagem.png?alt=media&token=d4c2ecde-9e3c-446b-89f0-d8d5d605e1f6'
        }

        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('checklists').add(dict_checklist)
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('checklists').add(dict_checklist)
        except:
            pass
        response = jsonify({'message':'Checklist criada com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível criar uma checklist. Mais detalhes: ' + str(e)})
        return response, 500
############################################################

####METODO EDITAR PERGUNTAS############
@app.route('/api/perguntas/edit_data/pergunta/', methods=['PUT'])
@token_required
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
@app.route('/api/perguntas/create_data/pergunta/', methods=['POST'])
@token_required
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
################ACESSAR DADOS DO FIREBASE####################

#####METODO PARA PEGAR TODAS AS INFO DO PAINEL############
@app.route('/api/painel/get_data/', methods=['GET'])
@token_required
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

#####METODO PARA PEGAR TODAS AS VERIFICACOES############
@app.route('/api/verificacoes/get_data/', methods=['GET'])
@token_required
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
@app.route('/api/verificacoes/get_data/verificacao/', methods=['GET'])
@token_required
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
def get_pergunta(user):
   return get_pergunta(user)

####METODO PARA PEGAR TODAS PERGUNTAS DE UMA CHECKLIST############
@app.route('/api/checklists/get_data/perguntas/', methods=['GET'])
@token_required
def get_all_perguntas(user):
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

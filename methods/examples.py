from flask.json import jsonify
from flask import  request
from methods.firebase_connect import *


def get_protected(user):
    return jsonify({'message' : 'This is a protected method!', 'user' : user})

def get_unprotected():
    return jsonify({'message' : 'This is a unprotected method! Everyone can see it!'})
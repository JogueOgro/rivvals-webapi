from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import coin_blueprint
from database import Session
from model.models import *
import json

@coin_blueprint.route('/coin', methods=['GET'])
@jwt_required()
def get_coin():
    return "COINS"


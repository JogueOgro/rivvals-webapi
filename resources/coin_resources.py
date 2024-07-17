from flask import request, jsonify
from . import coin_blueprint
from database import Session
from model.models import *
import json

@coin_blueprint.route('/coin', methods=['GET'])
def get_coin():
    return "COINS"


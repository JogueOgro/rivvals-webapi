from flask import request, jsonify, Blueprint
from database import Session
from model.models import *
import json

coin_blueprint = Blueprint('coin', __name__)

@coin_blueprint.route('/coin', methods=['GET'])
def get_coin():
    return "COINS"


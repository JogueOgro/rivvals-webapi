from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import user_blueprint

from model.models import *
from database import Session
from datetime import datetime
import bcrypt
import json

@user_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    session = Session()
    users = session.query(User).all()
    users_dicts = [user.to_dict() for user in users]
    return users_dicts

@user_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    session = Session()
    user = session.query(User).filter_by(iduser=user_id).first()
    session.close()
    if not user:
      return jsonify({'message': 'Usuário não encontrado'}), 404
    return user.to_dict()

@user_blueprint.route('/user', methods=['POST'])
def create_user():

    data = request.json

    password = data.get('password').encode("utf-8")
    salt = bcrypt.gensalt(rounds=15)
    hashed_password = bcrypt.hashpw(password, salt)

    new_user = User(
        name=data.get('name'),
        email=data.get('email'),
        password=hashed_password,
        creation_date=datetime.now(),
    )

    session = Session()
    session.add(new_user)
    session.commit()
    return new_user.to_dict()

@user_blueprint.route('/checkpassword', methods=['POST'])
def check_password():

    data = request.json
    session = Session()
    email=data.get('email')
    user = session.query(User).filter_by(email=email).first()

    if not user:
        session.close()
        return jsonify({'message': 'Usuário não encontrado'}), 404

    hashed_password = user.password.encode("utf-8")
    password=data.get('password').encode("utf-8")

    if bcrypt.checkpw(password, hashed_password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200

    return jsonify({'message': 'Senha incorreta'}), 401

@user_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    session = Session()
    user = session.query(User).filter_by(iduser=user_id).first()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    data = request.json
    if user:
        user.name = data.get('name'),
        user.email = data.get('email'),
        user.password = data.get('password'),
        user.creation_date = data.get('creation_date'),
        session.commit()
    return user.to_dict()

@user_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    user = session.query(User).filter_by(iduser=user_id).first()
    if not user:
      return jsonify({'message': 'Usuário não encontrado'}), 404
    else:
        session.delete(user)
        session.commit()
    return user.to_dict()
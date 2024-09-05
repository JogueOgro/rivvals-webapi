from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import util_blueprint
from database import Session
from model.models import *
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import os

@util_blueprint.route('/generate_sas_token', methods=['POST'])
def generate_sas_token():
    try:
        container_name = request.json.get('container_name')
        blob_name = request.json.get('blob_name')
        load_dotenv()

        sas_token = generate_blob_sas(
            account_name=os.getenv('AZURE_STORAGE_ACCOUNT_NAME'),
            container_name=container_name,
            blob_name=blob_name,
            account_key=os.getenv('AZURE_STORAGE_ACCOUNT_KEY'),
            permission=BlobSasPermissions(read=True, write=True, delete=True),
            expiry=datetime.utcnow() + timedelta(hours=4)  # Token válido por 4 horas
        )

        blob_url_with_sas = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

        return jsonify({"sas_token": sas_token, "url": blob_url_with_sas}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


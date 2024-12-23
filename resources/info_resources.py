from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import info_blueprint
from database import Session
from model.models import *

@info_blueprint.route('/notifications/<int:idplayer>', methods=['GET'])
@jwt_required()
def get_notifications(idplayer):
    session = Session()
    notifications = (
        session.query(Notification)
        .filter_by(player_idplayer=idplayer)
        .order_by(Notification.created.desc())
        .all()
    )
    return jsonify([notification.to_dict() for notification in notifications])


@info_blueprint.route('/api/notifications/<int:idnotification>/read', methods=['PUT'])
@jwt_required()
def mark_notification_as_read(idnotification):
    try:
        session = Session()
        notification = session.query(Notification).get(idnotification)
        if not notification:
            return jsonify({"error": "Notification not found"}), 404
        notification.isRead = True
        session.commit()
        return jsonify({"message": "Notification marked as read"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


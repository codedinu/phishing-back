import secrets
import string
from random import randint

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app import app, db
from app.models.scam_model import Scam
from app.schemas import ScamSchema
from flask import jsonify


@app.route('/addScam', methods=['POST'])
def add_scam():
    try:
        url = request.json.get('url')
        scam = Scam.query.get(url)

        if not scam:
            new_scam = Scam(url=url, count=1)
            db.session.add(new_scam)
            db.session.commit()
            return jsonify({'message': 'success'}), 201
        else:
            scam.count = scam.count + 1
            db.session.commit()
            return jsonify({'message': 'success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/checkScam', methods=['POST'])
def checkScam():
    try:
        url = request.json.get('url')
        scam = Scam.query.filter(Scam.url == url and Scam.count >= 10).all()

        if not scam:
            return jsonify({'message': 'Not Reported Scam'}), 201
        else:
            return jsonify({'message': 'Reported Scam'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/scams', methods=['GET'])
@jwt_required()
def getAllScams():
    try:
        all_scams = Scam.query.all()
        result = ScamSchema(many=True).dump(all_scams)
        response_data = {
            'scams': result,
            'message': 'Scams Reserved successfully',
            'code': 200
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500


@app.route('/recognizedScams', methods=['GET'])
@jwt_required()
def get_scams():
    try:
        all_scams = Scam.query.filter(Scam.count >= 10).all()
        result = ScamSchema(many=True).dump(all_scams)
        response_data = {
            'scams': result,
            'message': 'Recognized Scams Reserved successfully',
            'code': 200
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500

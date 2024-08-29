from random import randint
from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app import app, db
from app.models.history_model import History
from app.schemas import HistorySchema
from flask import jsonify


@app.route('/addHistory', methods=['POST'])
def add_history():
    try:
        url = request.json.get('url')
        user_id = request.json.get('user_id')
        status=request.json.get('status')

        new_history = History(url=url, user_id=user_id,status=status)
        db.session.add(new_history)
        db.session.commit()

        return jsonify({'message': 'History Added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/getUserHistory/<int:user_id>', methods=['GET'])
def get_userHistory(user_id):
    try:
        all_history = History.query.filter(History.user_id == user_id).all()
        history_list = []
        for history in all_history:
            print(history)
            history_data = {
                'id': history.history_id,
                'user_id': history.user_id,
                'url': history.url,
                'status': history.status,
                'datetime': history.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            }
            history_list.append(history_data)

        response_data = {
            'history': history_list,
            'code': 200
        }
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500


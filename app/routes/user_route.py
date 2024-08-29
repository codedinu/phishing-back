import secrets
import string
from random import randint

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from flask_mail import Mail, Message

from app import app, db
from app.models.user_model import User
from app.schemas import UserSchema

mail = Mail(app)
otp_storage = {}


def send_email_otp(recipient, otp):
    subject = "Your One-Time Password (OTP)"
    body = f"Your OTP is: {otp}"
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)



@app.route('/register', methods=['POST'])
def create_user():
    try:
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        otp = str(randint(100000, 999999))
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(name=name, email=email,  password=hashed_password, otp=otp)
        db.session.add(new_user)
        db.session.commit()

        otp_storage[email] = otp

        return jsonify({'message': 'success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/verify_user', methods=['POST'])
def verify_user():
    try:
        email = request.json.get('email')
        otp_entered = request.json.get('otp')

        if email in otp_storage and otp_storage[email] == otp_entered:
            user = User.query.filter_by(email=email).first()

            if user:
                user.is_verified = True
                db.session.commit()

                return jsonify({'message': 'User verified successfully.', 'user_id': user.user_id}), 200
            else:
                return jsonify({'error': 'User not found.'}), 404
        else:
            return jsonify({'error': 'Invalid OTP'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

            access_token = create_access_token(identity=user.user_id)
            user_details = {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'access_token': access_token
            }
            return jsonify(
                {'user': user_details, 'message': 'Login successful', 'code': 200}), 200
        else:
            return jsonify({'message': 'Invalid email or password', 'code': 400}), 400
    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500


@app.route('/changePassword', methods=['PUT'])
def changePassword():
    try:
        email = request.json.get('email')
        new_password = request.json.get('newPassword')

        if not email or not new_password:
            return jsonify({'error': 'Email and newPassword are required'}), 400

        user = User.query.filter_by(email=email).first()

        if user:
            new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            user.password = new_hashed_password

            db.session.commit()

            user_details = {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email
            }

            return jsonify({'user': user_details, 'message': 'Password updated', 'code': 200}), 200
        else:
            return jsonify({'message': 'Invalid email', 'code': 400}), 400

    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500



from flask import jsonify

@app.route('/updateUser/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found', 'code': 404}), 404
        
        name = request.json.get('name')
        email = request.json.get('email')

        if name:
            user.name = name
        if email:
            user.email = email

        
        db.session.commit()

        user_details = {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email
        }

        return jsonify({'user': user_details, 'message': 'User updated successfully', 'code': 200}), 200

    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500



@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        all_users = User.query.all()
        result = UserSchema(many=True).dump(all_users)
        response_data = {
            'users': result,
            'message': 'Users Reserved successfully',
            'code': 200
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e), 'code': 500}), 500

from marshmallow import ValidationError
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required
from app.models import Mechanic, db
from app.extensions import limiter, cache


@mechanic_bp.route('/login', methods=['POST'])
@limiter.limit("20 per day")
def login():
    try:
        data = login_schema.load(request.json) # Send email and password
    except ValidationError as e:
        return jsonify(e.messages), 400 #Returning the error as a response so my client can see whats wrong.
    
    mechanic = db.session.query(Mechanic).where(Mechanic.email==data['email']).first() #Search my db for a user with the passed in email

    if mechanic and check_password_hash(mechanic.password, data['password']): #Check the user stored password hash against the password that was sent
        token = encode_token(mechanic.id)
        return jsonify({
            "message": f'Welcome {mechanic.first_name}',
            "token": token
        }), 200
    
    return jsonify("Invalid email or password!"), 403


@mechanic_bp.route('', methods=['POST'])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    data['password'] = generate_password_hash(data['password'])

    new_mechanic = Mechanic(**data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


@mechanic_bp.route('', methods=['GET'])
@cache.cached(timeout=30)
def read_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanic_bp.route('/profile', methods=['GET'])
@limiter.limit("15 per hour")
@token_required
def read_mechanic(mechanic_id):
    mechanic_id = request.mechanic_id
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mechanic), 200


@mechanic_bp.route('', methods=['PUT'])
@token_required
def update_mechanic():
    mechanic_id = request.mechanic_id
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanic_bp.route('', methods=['DELETE'])
@token_required
def delete_mechanic():
    mechanic_id = request.mechanic_id
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted mechanic {mechanic_id}"}), 200


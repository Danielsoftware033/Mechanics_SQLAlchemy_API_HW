from marshmallow import ValidationError
from . import customers_bp
from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required, customer_token_required
from app.models import Customer, db
from app.extensions import limiter, cache
from sqlalchemy import select



#CREATE Customer ROUTE
@customers_bp.route('', methods=['POST']) 
@limiter.limit("20 per day")
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 

    new_customer = Customer(**data) 
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#Read Customers
@customers_bp.route('', methods=['GET']) 
def read_customers():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers), 200


@customers_bp.route('/paginated', methods=['GET'])
@cache.cached(timeout=30) 
def read_customers_paginated():
    try:
        page = int(request.args.get('page')) 
        per_page = int(request.args.get('per_page')) 
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page) 
        return customers_schema.jsonify(customers), 200
    except:
        customers = db.session.query(Customer).all()
        return customers_schema.jsonify(customers), 200


#Read Individual Customer 
@customers_bp.route('/<int:customer_id>', methods=['GET'])
@limiter.limit("25 per hour")
def read_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    return customer_schema.jsonify(customer), 200


#Update a User
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@limiter.limit("20 per month")
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id) 

    if not customer: 
        return jsonify({"message": "user not found"}), 404  
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in customer_data.items(): 
        setattr(customer, key, value) 

    db.session.commit()
    return customer_schema.jsonify(customer), 200


#Delete a customer
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@limiter.limit("15 per day")
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id) 
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted customer {customer_id}"}), 200
from app.blueprints.inventory import inventories_bp
from .schemas import ticket_inventory_schema, ticket_inventories_schema, inventory_schema, inventories_schema
from flask import request, jsonify, render_template
from marshmallow import ValidationError
from app.models import Inventory, ticket_inventories, db
from app.extensions import limiter
from app.util.auth import encode_token, token_required


@inventories_bp.route('', methods=['POST']) 
@limiter.limit("5 per day")
def create_inventory():
    try:
        data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    new_inventory = Inventory(**data) 
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201


@inventories_bp.route('', methods=['GET']) 
def read_inventories():
    inventories = db.session.query(Inventory).all()
    return inventory_schema.jsonify(inventories), 200


@inventories_bp.route('/<int:inventory_id>', methods=['PUT'])
@limiter.limit("8 per hour")
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify("Invalid inventory_id"), 404
    
    try:
        data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in data.items():
        setattr(inventory, key, value) 

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200


@inventories_bp.route('/<int:inventory_id', methods=['DELETE'])
@limiter.limit("8 per day")
def delete_inventory(inventory_id):
    inventory = db.session.get(Inventory,inventory_id)
    db.session.delete(inventory)
    db.session.commit()
    return jsonify(f"Successfully deleted part {inventory_id}")



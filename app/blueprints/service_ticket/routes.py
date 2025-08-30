from marshmallow import ValidationError
from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from app.models import Mechanic, ServiceTicket, Inventory, db
from app.util.auth import token_required, customer_token_required
from app.extensions import limiter
         

@service_ticket_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ServiceTicket(**data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201


@service_ticket_bp.route("/", methods=["GET"])
def read_service_tickets():
    tickets = db.session.query(ServiceTicket).all()
    return service_tickets_schema.jsonify(tickets), 200


@service_ticket_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_mechanic_tickets():
    mechanic_id = request.mechanic_id

    tickets = db.session.query(ServiceTicket).where(ServiceTicket.mechanics.any(Mechanic.id == mechanic_id)).all()

    return service_tickets_schema.jsonify(tickets), 200


@service_ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    ticket.mechanics.append(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message": "Service ticket not found"}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    ticket.mechanics.remove(mechanic)  
    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['PUT'])
@limiter.limit("600 per day", override_defaults=True)
def add_part_ticket(ticket_id, inventory_id):
     ticket = db.session.get(ServiceTicket, ticket_id)
     part = db.session.get(Inventory, inventory_id)

     if part not in ticket.inventories:
         ticket.inventories.append(part)
         db.session.commit()
         return jsonify({
            'message': f'successfully added {part.name} to Inventory'
        }), 200
     
     return jsonify("This part is already on the service ticket"), 400
 






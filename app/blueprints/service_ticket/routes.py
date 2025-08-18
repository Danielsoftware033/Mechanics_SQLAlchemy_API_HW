from marshmallow import ValidationError
from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify

from app.models import ServiceTicket, db



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


@service_ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def read_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route("/<int:ticket_id>", methods=["PUT"])
def update_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    try:
        ticket_data = service_ticket_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400

    for key, value in ticket_data.items():
        setattr(ticket, key, value)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted service ticket {ticket_id}"}), 200

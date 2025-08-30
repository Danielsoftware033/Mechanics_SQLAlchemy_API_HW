from app.extensions import ma
from app.models import ServiceTicket
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
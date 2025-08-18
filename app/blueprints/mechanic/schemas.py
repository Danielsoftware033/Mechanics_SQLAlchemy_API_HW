from app.extensions import ma
from app.models import Mechanic, ServiceTicket
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Mechanic #Creates a schema that validates the data as defined by our Users Model

mechanic_schema = MechanicSchema() #Creating an instance of my schema that I can actually use to validate, deserialize, and serialize JSON
mechanics_schema = MechanicSchema(many=True) #Allows this schema to translate a list of User objects all at once



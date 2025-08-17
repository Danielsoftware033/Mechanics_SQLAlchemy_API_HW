from datetime import date
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, Integer, Float, ForeignKey, Table
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError

app = Flask(__name__) #Instatiating our Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' #Connecting a sqlite db to our flask app

#Create a base class for our models
class Base(DeclarativeBase):
    pass
    #could add your own config

#Instatiate your SQLAlchemy database:
db = SQLAlchemy(model_class = Base)
#Initialize my extension onto my Flask app
db.init_app(app) #adding the db to the app.
ma = Marshmallow(app)


ticket_mechanics = Table(
    'ticket_mechanics',
    Base.metadata,
    mapped_column('ticket_id', Integer, ForeignKey('service_tickets.id'), primary_key=True),
    mapped_column('mechanic_id', Integer, ForeignKey('mechanics.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)

    service_tickets: Mapped[list["ServiceTicket"]] = relationship('ServiceTicket', back_populates='customer')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)

    service_tickets: Mapped[list["ServiceTicket"]] = relationship('ServiceTicket', secondary=ticket_mechanics, back_populates='mechanics')

class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(200), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    VIN: Mapped[str] = mapped_column(String(50), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    customer: Mapped["Customer"] = relationship('Customer', back_populates='service_tickets')
    mechanics: Mapped[list["Mechanic"]] = relationship('Mechanic', secondary=ticket_mechanics, back_populates='service_tickets')





class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic #Creates a schema that validates the data as defined by our Users Model

mechanic_schema = MechanicSchema() #Creating an instance of my schema that I can actually use to validate, deserialize, and serialize JSON
mechanics_schema = MechanicSchema(many=True) #Allows this schema to translate a list of User objects all at once


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)


@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanic(**data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanic_bp.route('/', methods=['GET'])
def read_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanic_bp.route('/<int:mechanic_id>', methods=['GET'])
def read_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mechanic), 200

@mechanic_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
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

@mechanic_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted mechanic {mechanic_id}"}), 200




with app.app_context():
    db.create_all() #Creating our database tables


app.run(debug=True)
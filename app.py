from datetime import date
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, Integer, Float, ForeignKey, Table

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



ticket_mechanics = Table(
    'ticket_mechanics',
    Base.metadata,
    mapped_column('ticket_id', Integer, ForeignKey('service_ticket.id'), primary_key=True),
    mapped_column('mechanic_id', Integer, ForeignKey('mechanic.id'), primary_key=True)
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
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customer.id'), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(200), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    VIN: Mapped[str] = mapped_column(String(50), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    customer: Mapped["Customer"] = relationship('Customer', back_populates='service_tickets')
    mechanics: Mapped[list["Mechanic"]] = relationship('Mechanic', secondary=ticket_mechanics, back_populates='service_tickets')



with app.app_context():
    db.create_all() #Creating our database tables


app.run()
from datetime import date
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, Integer, Float, ForeignKey, Table, Column, select
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

ticket_mechanics = Table(
    'ticket_mechanics',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id'), primary_key=True),
    Column('mechanic_id', Integer, ForeignKey('mechanics.id'), primary_key=True)
)

ticket_inventories = Table(
    'service_ticket_inventories',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id'), primary_key=True),
    Column('inventory_id', Integer, ForeignKey('inventories.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    service_tickets: Mapped[list["ServiceTicket"]] = relationship('ServiceTicket', back_populates='customer')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)

    service_tickets: Mapped[list["ServiceTicket"]] = relationship('ServiceTicket', secondary=ticket_mechanics, back_populates='mechanics')

class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    VIN: Mapped[str] = mapped_column(String(50), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    customer: Mapped["Customer"] = relationship('Customer', back_populates='service_tickets')
    mechanics: Mapped[list["Mechanic"]] = relationship('Mechanic', secondary=ticket_mechanics, back_populates='service_tickets')
    inventories: Mapped[list["Inventory"]] = relationship('Inventory', secondary=ticket_inventories, back_populates='service_tickets')

class Inventory(Base):
    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    service_tickets: Mapped[list["ServiceTicket"]] = relationship('ServiceTicket', secondary=ticket_inventories, back_populates='inventories')
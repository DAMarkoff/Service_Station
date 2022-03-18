from datetime import datetime
from time import time

import bcrypt
import jwt
from flask import current_app

from flask_login import UserMixin
from sqlalchemy import text
from sqlalchemy.orm import relationship

from project import db


class UsersGroup(db.Model):
	__tablename__ = 'users_groups'
	
	group_id = db.Column('group_id', db.Integer, primary_key=True, autoincrement=True, server_default=text("nextval('users_groups_group_id_seq'::regclass)"))
	group_name = db.Column('group_name', db.String, nullable=False)
	
	user = relationship('User', back_populates='group')
	
	
class User(db.Model, UserMixin):
	__tablename__ = 'users'
	
	user_id = db.Column('user_id', db.BigInteger, primary_key=True, autoincrement=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
	first_name = db.Column('first_name', db.String(50), nullable=False)
	last_name = db.Column('last_name', db.String(50), nullable=False)
	email = db.Column('email', db.String(350), nullable=False)
	phone = db.Column('phone', db.String(30), nullable=False)
	password_1 = db.Column('pass', db.String(32))
	active = db.Column('active', db.Boolean, nullable=False, server_default=text("true"))
	password = db.Column('password', db.String, nullable=False)
	salt = db.Column('salt', db.String, nullable=False)
	created = db.Column('created', db.DateTime)
	
	group_id = db.Column('group_id', db.ForeignKey('users_groups.group_id'), nullable=False)
	
	group = relationship('UsersGroup', back_populates='user')
	storage_order = relationship('StorageOrder', back_populates='user')
	
	def __init__(self, first_name: str, last_name: str, email: str, phone: str, password: str):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.phone = phone
		self.created = datetime.now()
		self.active = True
		self.group_id = 2
		self.set_password(password=password)
		
	def __repr__(self):
		return f'<User {self.email}, id {self.user_id}>'
		
	def get_id(self):
		return self.user_id
	
	def set_password(self, password: str) -> None:
		self.salt = bcrypt.gensalt(5)
		hashed_password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
		self.password = hashed_password.decode('utf-8')
	
	def check_password(self, password: str) -> bool:
		return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
	
	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.user_id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256') # .decode('utf-8')
	
	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)
	
	
class StorageOrder(db.Model):
	__tablename__ = 'storage_orders'

	storage_order_id = db.Column('storage_order_id', db.Integer, primary_key=True, autoincrement=True)
	start_date = db.Column('start_date', db.Date, nullable=False)
	stop_date = db.Column('stop_date', db.Date, nullable=False)
	storage_order_cost = db.Column('storage_order_cost', db.Integer, nullable=False)
	created = db.Column('created', db.DateTime)

	user_id = db.Column(db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
	shelf_id = db.Column(db.ForeignKey('warehouse.shelf_id'), nullable=False)

	shelf = relationship('Warehouse', back_populates='storage_order')
	user = relationship('User', back_populates='storage_order')


class Warehouse(db.Model):
	__tablename__ = 'warehouse'

	shelf_id = db.Column('shelf_id', db.Integer, primary_key=True, autoincrement=True)
	active = db.Column('active', db.Boolean, nullable=False)

	size_id = db.Column('size_id', db.ForeignKey('sizes.size_id'), nullable=False)

	size = relationship('Size', back_populates='warehouse')
	storage_order = relationship('StorageOrder', back_populates='shelf')


class Size(db.Model):
	__tablename__ = 'sizes'

	size_id = db.Column('size_id', db.Integer, primary_key=True, autoincrement=True)
	size_name = db.Column('size_name', db.Integer)

	warehouse = relationship('Warehouse', back_populates='size')
	
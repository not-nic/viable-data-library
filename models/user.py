from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from app import database


class User(UserMixin, database.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email_address = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

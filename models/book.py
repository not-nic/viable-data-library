from sqlalchemy import Column, Integer, String, Text, Boolean, DATE, ForeignKey
from app import database


class Book(database.Model):
    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    is_borrowed = Column(Boolean(), default=False)
    borrower = Column(String(255), ForeignKey('user.email_address'), nullable=True, default=None)
    return_date = Column(DATE, nullable=True)
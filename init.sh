#!/bin/bash

sleep 60

flask shell <<EOF
from app import database
database.create_all()
database.session.add(User(first_name='ned', last_name='flanders', email_address='nflanders1@email.com', password='password'))
database.session.add(User(first_name='Waylon', last_name='Smithers', email_address='waylonS@example.com', password='password2'))
database.session.add(User(first_name='Krusty', last_name='The Clown', email_address='Krusty@example.com', password='password3'))
database.session.commit()
database.session.add(Book(image_url='example.com/book1.jpg', title='I, Robot', description='By Isaac Asimov.', is_borrowed=True, borrower='nflanders1@email.com', return_date='2023-09-11'))
database.session.add(Book(image_url='example.com/book2.jpg', title='Esio Trot', description='By R Dahl.'))
database.session.add(Book(image_url='example.com/book3.jpg', title='Fantastic Mr. Fox', description='By R Dahl.'))
database.session.commit()
exit()
EOF

flask run --host=0.0.0.0
# Viable Data Library Service

![image](https://github.com/not-nic/viable-data-library/assets/67616855/07708ffa-cbd5-4830-9d5b-2ee807c7fe6f)
## Description
For this task I decided to use Flask and a MySQL database, as it is what I am most familiar with. I also chose to use a few extra libraries, like Flask-Login, Flask-Bcrypt and Flask-SQLAlchemy, as these are mature libraries with well documented solutions, which allowed me to stay close to the time limit.

Also, to better understand how I tackled this task, I have attached a screenshot of my notes where I have broken down the problem.
![image](https://github.com/not-nic/viable-data-library/assets/67616855/1cc8f43e-bbc1-466e-8e52-11c321877d06)
## How to Use
The application works within the browser and a tool like postman, if you would like to test it through postman the available endpoints are:
**Auth:**
- register : GET/POST – register a new user to the service.
- login : GET/POST – login to the service.

**Library:**
- Library/all – return all books in the database.
- Library/available – return all available books
- Library/borrowed – return all borrowed books
- Library/due – return a user’s books that are due today or are overdue.
- Library/borrow – allows a user to borrow a book
## Run with Docker
1. Clone this repository or download the files.
```bash
git clone https://github.com/not-nic/viable-data-library.git
cd viable-data-library
```
2. Run docker compose build.
```bash
docker compose up --build
```
Note: I have hardcoded the MySQL container IP address in docker-compose.yml to match the app.py python file. so it runs 'out of the box'.
## Install Guide
1. Clone this repository or download the files.
```bash
git clone https://github.com/not-nic/viable-data-library.git
cd viable-data-library
```
2. Install the required python packages:
```bash
$ pip install -r requirements.txt
```
3. Navigate to [app.py](app.py) and replace `SQLALCHEMY_DATABASE_URI` with your own MySQL database URI, I chose to run mine through docker.
```bash
$ docker run --name mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:latest
$ docker start mysql
$ sudo nano app.py
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://mysql:password@172.19.0.2:3306/viable-data"
```
4. Start a flask shell and seed the database with random users and books.
```bash
flask shell
>>> from app import database
>>> database.create_all()
>>> database.session.add(User(first_name='ned', last_name='flanders', email_address='nflanders1@email.com', password='password')) 
>>> database.session.add(User(first_name='Waylon', last_name='Smithers', email_address='waylonS@example.com', password='password2')) 
>>> database.session.add(User(first_name='Krusty', last_name='The Clown', email_address='Krusty@example.com', password='password3'))
>>> database.session.commit()
>>> database.session.add(Book(image_url='example.com/book1.jpg', title='I, Robot', description='By Isaac Asimov.', is_borrowed=True, borrower='nflanders1@email.com', return_date='2023-11-09'))
>>> database.session.add(Book(image_url='example.com/book2.jpg', title='Esio Trot', description='By R Dahl.'))
>>> database.session.add(Book(image_url='example.com/book3.jpg', title='Fantastic Mr. Fox', description='By R Dahl.'))
>>> database.session.commit()
>>> exit()
```
5. Start the flask application and test the application.
```bash
flask run --debug --host 0.0.0.0
```

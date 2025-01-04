from flask import Flask
from extension import db
#from flask_sqlalchemy import SQLAlchemy
from models import Patient, Doctor, MedicalRecord, Appointment, User

app = Flask(__name__)

#how to initialize and configure a simple mysql database. 'mysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://MedEase_user:medease@localhost/MedEase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db object instantiated from the class SQLAlchemy
db.init_app(app)


# testing the apri service
@app.route('/')
def index():
    return "Hello world !!!!"

@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello, {}!</h1>'.format(name)
    return f'<h1> Hello, {name}</h1>.'

if __name__ == "__main__":
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        
        #Create_all tables
        print("Creating new tables...")
        db.create_all()
        
        print("Database tables created successfully!")
        app.run(debug=True)

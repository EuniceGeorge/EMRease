from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#how to initialize and configure a simple mysql database. 'mysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://MedEase_user:medease@localhost/MedEase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db object instantiated from the class SQLAlchemy
db = SQLAlchemy(app)


# testing the api service
@app.route('/')
def index():
    return "Hello world !!!!"

@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello, {}!</h1>'.format(name)
    return f'<h1> Hello, {name}</h1>.'

if __name__ == "__main__":
    with app.app_context():
        # Drop all existing tables 
        print("Dropping existing tables...")
        db.drop_all()

        # #creating tables
        # print("Creating new tables...")
        # db.create_all()

    app.run(debug=True)

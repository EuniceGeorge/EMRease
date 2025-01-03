from flask import Flask
# from models import db, Patient, Doctor, MedicalRecord, Appointment

app = Flask(__name__)

# testing the apri service
@app.route('/')
def index():
    return "Hello world !!!!"

@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello, {}!</h1>'.format(name)
    return f'<h1> Hello, {name}</h1>.'

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from extension import db
from models import Patient, Doctor, MedicalRecord, Appointment, User

app = Flask(__name__)

#how to initialize and configure a simple mysql database. 'mysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://MedEase_user:medease@localhost/MedEase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize the db with the Flask app, it must be called before accessing the database
db.init_app(app)


# testing the apri service
@app.route('/')
def index():
    return "Hello world !!!!"

@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello, {}!</h1>'.format(name)
    return f'<h1> Hello, {name}</h1>.'

# Create resources for the EMR API
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#patients routes
@app.route('/api/patients', methods=['GET'])
def get_patient():
    patients = Patient.query.all()
    return jsonify([{
        'id': p.id,
        'first_name': p.first_name,
        'last_name': p.last_name,
        'date_of_birth': p.date_of_birth.strftime('%Y-%m-%d'),
        'gender': p.gender,
        'contact_number': p.contact_number,
        'email': p.email,
        'address': p.address
    } for p in patients])

# doctors routes
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#retrieve all doctors
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
        doctors = Doctor.query.all()
        return jsonify([{
            'id': d.id,
            'first_name': d.first_name,
            'last_name': d.last_name,
            'specialization': d.specialization,
            'contact_number': d.contact_number,
            'email': d.email
        } for d in doctors])

# Appointment Routes
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# retrieves all appointments
@app.route('/api/appointments', methods=['GET'])
def get_appointments():
        appointments = Appointment.query.all()
        return jsonify([{
            'id': a.id,
            'patient_id': a.patient_id,
            'doctor_id': a.doctor_id,
            'appointment_date': a.appointment_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': a.status,
            'reason': a.reason
        } for a in appointments])

# Medical Record Routes
# Retrieves all medical records for a specific patient
@app.route('/api/medical-records/patient/<int:patient_id>', methods=['GET'])
def get_patient_records(patient_id):
        records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
        return jsonify([{
            'id': r.id,
            'patient_id': r.patient_id,
            'doctor_id': r.doctor_id,
            'diagnosis': r.diagnosis,
            'treatment': r.treatment,
            'prescription': r.prescription,
            'visit_date': r.visit_date.strftime('%Y-%m-%d %H:%M:%S')
        } for r in records])

if __name__ == "__main__":
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        
        #Create_all tables
        print("Creating new tables...")
        db.create_all()
        
        print("Database tables created successfully!")
        app.run(debug=True)

from flask import Flask, request, jsonify, session, redirect, url_for, flash
from extension import db
from models import Patient, Doctor, MedicalRecord, Appointment, User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

#how to initialize and configure a simple mysql database. 'mysql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://MedEase_user:medease@localhost/MedEase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'password'

#Initialize the db with the Flask app, it must be called before accessing the database
db.init_app(app)


# # testing the apri service
# @app.route('/') 
# def index():
#     return "Hello world !!!!"

# @app.route('/user/<name>')
# def user(name):
#     # return '<h1>Hello, {}!</h1>'.format(name)
#     return f'<h1> Hello, {name}</h1>.'

# Create resources for the EMR API
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Login required'}), 401
            user = User.query.get(session['user_id'])
            if user.role not in roles:
                return jsonify({'error': 'Unauthorized access'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


#patients routes
@app.route('/api/patients', methods=['GET'])
@login_required  # Only logged-in users can access
@role_required(['admin', 'doctor'])  # Only these roles can access
def get_all_patient():
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

@app.route('/api/patients/<int:id>', methods=['GET'])
@login_required  # Only logged-in users can access
@role_required(['admin', 'doctor'])  # Only these roles can access
def get_patient_id(id):
        patient = Patient.query.get_or_404(id)
        return jsonify({
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),
            'gender': patient.gender,
            'contact_number': patient.contact_number,
            'email': patient.email,
            'address': patient.address
        })

@app.route('/api/patients', methods=['POST'])
@login_required  # Only logged-in users can access
@role_required(['admin'])  # Only these roles can access
def create_patient():
        data = request.get_json()
        new_patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'], 
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d'),
            gender=data['gender'],
            contact_number=data.get('contact_number'),
            email=data.get('email'),
            address=data.get('address')
        )
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({'message': 'Patient created successfully', 'id': new_patient.id}), 201

# doctors routes
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#retrieve all doctors
@app.route('/api/doctors', methods=['GET'])
@login_required  # Only logged-in users can access
@role_required(['admin'])  # Only these roles can access
def get_all_doctors():
        doctors = Doctor.query.all()
        return jsonify([{
            'id': d.id,
            'first_name': d.first_name,
            'last_name': d.last_name,
            'specialization': d.specialization,
            'contact_number': d.contact_number,
            'email': d.email
        } for d in doctors])

#Retrieve doctor by id
@app.route('/api/doctors/<int:id>', methods=['GET'])
@login_required  # Only logged-in users can access
@role_required(['admin'])  # Only these roles can access
def get_doctor_id(id):
        doctor = Doctor.query.get_or_404(id)
        return jsonify({
            'id': doctor.id,
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
            'specialization': doctor.specialization,
            'contact_number': doctor.contact_number,
            'email': doctor.email
        })

# create new doctor
@app.route('/api/doctors', methods=['POST'])
@login_required  # Only logged-in users can access
@role_required(['admin'])  # Only these roles can access
def create_doctor():
    data = request.get_json()
    new_doctor = Doctor(
        first_name=data['first_name'],
        last_name=data['last_name'],
        specialization=data['specialization'],
        contact_number=data.get('contact_number'),
        email=data.get('email')
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message': 'doctor created successfully', 'id': new_doctor.id}), 201

# Appointment Routes
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# retrieves all appointments
@app.route('/api/appointments', methods=['GET'])
@login_required  # Only logged-in users can access
@role_required(['admin', 'doctor'])  # Only these roles can access
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

#create a new appointments
@app.route('/api/appointments', methods=['POST'])
@login_required  # Only logged-in users can access
@role_required(['admin', 'doctor'])  # Only these roles can access
def create_appointment():
        data = request.get_json()
        new_appointment = Appointment(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=datetime.strptime(data['appointment_date'], '%Y-%m-%d %H:%M:%S'),
            status=data.get('status', 'scheduled'),
            reason=data.get('reason')
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment created successfully', 'id': new_appointment.id}), 201

# Medical Record Routes
# Retrieves all medical records for a specific patient
@app.route('/api/medical-records/patient/<int:patient_id>', methods=['GET'])
@login_required  # Only logged-in users can access
@role_required(['admin', 'doctor'])  # Only these roles can access
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

# create a new medical record
@app.route('/api/medical-records', methods=['POST'])
@login_required  # Only logged-in users can access
@role_required(['doctor'])  # Only these roles can access
def create_medical_record():
        data = request.get_json()
        new_record = MedicalRecord(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            diagnosis=data['diagnosis'],
            treatment=data['treatment'],
            prescription=data.get('prescription'),
            visit_date=datetime.now()
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Medical record created successfully', 'id': new_record.id}), 201

# Authentication routes for the roles(doctor, admin, staff)
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'staff'), # the default role is staff, if the role is not provided
        is_active=True
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
        
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    session['user_id'] = user.id
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    })

@app.route('/auth/logout')
@login_required
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})



if __name__ == "__main__":
    with app.app_context():
        # print("Dropping existing tables...")
        # db.drop_all()
        
        # #Create_all tables
        # print("Creating new tables...")
        #db.create_all()
        
        print("Database tables created successfully!")
        app.run(debug=True)

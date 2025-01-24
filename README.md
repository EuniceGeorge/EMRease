**Overview:**

The **MedEase API** is a robust and secure platform designed to facilitate the seamless management of healthcare data. It provides endpoints for managing key healthcare-related resources, including patients, doctors, appointments, medical records, and user authentication. The API is built with role-based access control to ensure that only authorized users can access or modify sensitive information, making it ideal for hospitals, clinics, and other healthcare providers.

---

**Key Features:**

1. **User Authentication & Authorization:**
    
    - Role-based access control for `admin`, `doctor`, and `staff`.
        
    - Secure login and registration functionality.
        
2. **Patient Management:**
    
    - Add, view, and manage patient records, including contact details, medical history, and more.
        
3. **Doctor Management:**
    
    - View and manage doctor profiles, specializations, and contact information.
        
4. **Appointment Scheduling:**
    
    - Create, view, and manage appointments between patients and doctors.
        
    - Track appointment statuses and reasons.
        
5. **Medical Records:**
    
    - View and create detailed medical records for patients, including diagnosis, treatments, and prescriptions.
        

---

**Authentication:**  
The API requires authentication for all endpoints, with access restricted based on the user role (`admin`, `doctor`, or `staff`). Sessions or tokens must be provided in the request headers for all protected routes.

**How to Use:**

- Set up an account or log in to obtain a session/token for authentication.
    
- Use the provided endpoints to manage patients, doctors, appointments, and medical records.
    
- Ensure proper role-based permissions when accessing each endpoint.
    

**Target Users:**

- **Administrators:** Manage doctors, patients, and overall system operations.
    
- **Doctors:** Access and update patient medical records and manage appointments.
    
- **Staff:** Limited access for assisting with basic operations like appointment scheduling.
    

**Technologies Used:**

- **Backend Framework:** Flask (Python)
    
- **Database:** SQLAlchemy for database interactions
    
- **Authentication:** Role-based access with custom decorators
    
- **Security:** Password hashing, session management, and input validation
    

**How to Use:**

- Set up an account or log in to obtain a session/token for authentication.
    
- Use the provided endpoints to manage patients, doctors, appointments, and medical records.
    
- Ensure proper role-based permissions when accessing each endpoint.

**PATIENT** 
**Description:**  
This folder contains routes for managing patient-related operations. These endpoints allow you to view, create, and manage patient information.

Endpoints:

`GET /api/patients:` Retrieve a list of all patients (admin/doctor access only).  
`GET /api/patients/:` Retrieve details of a specific patient by their ID.  
`POST /api/patients:` Create a new patient record (admin access only).

**DOCTOR**
**Description:**  
This folder contains routes for managing doctor-related operations. These endpoints allow you to view doctor profiles and create new doctor records.

**Endpoints:**

- `GET /api/doctors`: Retrieve a list of all doctors (admin access only).
    
- `GET /api/doctors/`: Retrieve details of a specific doctor by their ID.
    
- `POST /api/doctors`: Create a new doctor record (admin access only).

**APPOINTMENT**
**Description:**  
This folder contains routes for managing patient appointments. These endpoints allow viewing and scheduling appointments between patients and doctors.

**Endpoints:**

- `GET /api/appointments`: Retrieve a list of all appointments (admin/doctor access only).
    
- `POST /api/appointments`: Create a new appointment for a patient and doctor.

**MEDICAL RECORD**
**Description:**  
This folder contains routes for managing patient appointments. These endpoints allow viewing and scheduling appointments between patients and doctors.

**Endpoints:**

- `GET /api/appointments`: Retrieve a list of all appointments (admin/doctor access only).
    
- `POST /api/appointments`: Create a new appointment for a patient and doctor.

**AUTHENTICATION** 
**Description:**  
This folder contains routes for managing user authentication and authorization. Use these endpoints to log in, register, and manage access to the API.

**Endpoints:**

- `POST /auth/login`: Authenticate users and create a session or return a token.
    
- `POST /auth/register`: Register a new user with a username, email, and password.